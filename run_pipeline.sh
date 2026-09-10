#!/bin/bash
# Orquestrador COMPLETO do pipeline (cidades -> identificadores), com
# paralelismo aplicado em toda etapa que e um laco "por ano"/"por pasta"
# independente. Roda tudo via tsp, sem precisar de ninguem acompanhando:
# enfileira, espera, confere falha, encadeia a proxima etapa sozinho.
#
# Uso:
#   bash run_pipeline.sh [--from-phase FASE] [--workers N] [--rais-clear-workers N]
#
#   --from-phase FASE   comeca a partir desta fase, pulando as anteriores
#                        (default: preproc, ou seja roda tudo do zero).
#                        Fases, na ordem: preproc, pivot, fanout, empresa,
#                        finalizacao
#   --workers N          concorrencia global do tsp pros workers por
#                        ano/pasta (default: 8)
#   --rais-clear-workers N  concorrencia da fila SEPARADA do rais_clear
#                        (default: 4) -- cada worker pode chegar a ~26GB de
#                        RSS (SP sozinho e grande), fila isolada pra nao
#                        competir com a concorrencia alta do resto.
#
# Rode como 1 job do tsp, nao direto no terminal:
#   tsp bash run_pipeline.sh --from-phase fanout
# (assim sobrevive a sessao que o lancou -- ver run_parallel_recover.sh,
# mesmo principio.)
#
# Desenho (por que cada fase e o que ela faz):
#
# [preproc] Os grupos comvest_preproc/dac_preproc/enem_preproc/comvest_base/
#   enem_merge/dac_base sao rapidos (~2,3h somados na ultima medicao real,
#   job tsp 22) e nao tem laco por ano/pasta que valha a pena paralelizar --
#   rodam sequencial via debug_stages.py --from/--to, na ordem ja definida
#   la (GROUP_ORDER).
#
# [pivot] pre_process_parquet e identification sao lacos por ano
#   independentes entre si (rodam em paralelo um do outro) E internamente
#   (1 worker por ano cada). cpf_verification e sequencial e rapido.
#   recover_cpf_dac_comvest reusa o script paralelo que ja existe
#   (rais/id_generation/run_parallel_recover.sh). random_index e sequencial
#   e rapido.
#
# [fanout] Cadeias independentes entre si (nenhuma le a saida da outra,
#   todas so leem o pivo dac_comvest_ids.csv + seus proprios inputs
#   upstream), cada uma rodando como 1 job tsp que por sua vez pode
#   enfileirar+esperar seus proprios sub-workers:
#     - RAIS:     rais_merge (por ano) -> rais_recover_cpf (lookup
#                 sequencial + por ano) -> rais_clear (por ano +
#                 finalizacao sequencial)
#     - SOCIO:    socio_clear (por pasta/data) -> socio_merge (sequencial)
#     - CAPES:    capes_clean (por pasta/ano) -> capes_merge (sequencial)
#     - ENEM:     enem_vest_ids -> enem_ids_merge (sequencial, rapido)
#     - UNESP, FUVEST: sequencial, rapido, sem dependencia entre si
#     - DIPLOMAS: nao depende do pivo, roda em paralelo com o resto
#   Todas essas cadeias competem pela MESMA fila do tsp (-S N_WORKERS
#   setado 1x no topo) -- o tsp balanceia dinamicamente entre TODOS os
#   jobs de TODAS as cadeias, nao precisa dividir workers por cadeia na
#   mao.
#
# [empresa] empresa/estabelecimento/simples dependem de socio_merge
#   (socio_amostra.csv) ter terminado. Independentes entre si.
#
# [finalizacao] merge_sheets -> comvest_ids -> identificadores, sequencial,
#   por ultimo (mesma ordem de __main__.py).

set -e

# 16 causou 2 OOMs reais no dia 2026-09-09 (rais_clear isolado numa fila
# separada resolveu o primeiro, mas o capes_merge -- ~12GB sozinho -- ainda
# estourou rodando concorrente com varios workers do rais_recover_cpf +
# socio_merge ativos ao mesmo tempo). 8 da mais margem quando varias etapas
# pesadas da fila principal coincidem, ao custo de mais tempo total.
N_WORKERS=8
FROM_PHASE="preproc"
# rais_clear roda numa fila tsp SEPARADA (TS_SOCKET dedicado) com bem menos
# concorrencia -- cada worker pode chegar a ~26GB de RSS (SP sozinho e
# 2,1GB comprimido em parquet, bem mais em memoria), e 16 workers concorrentes
# derrubou processos de OUTROS usuarios da maquina via OOM real (confirmado
# via journalctl -k, 2026-09-09). Isolar numa fila propria evita penalizar a
# concorrencia das outras cadeias (socio/capes/etc), que rodaram bem com 16.
RAIS_CLEAR_WORKERS=4

while [[ $# -gt 0 ]]; do
    case "$1" in
        --workers) N_WORKERS="$2"; shift 2 ;;
        --rais-clear-workers) RAIS_CLEAR_WORKERS="$2"; shift 2 ;;
        --from-phase) FROM_PHASE="$2"; shift 2 ;;
        *) echo "argumento desconhecido: $1"; exit 1 ;;
    esac
done

PHASES=(preproc pivot fanout empresa finalizacao)
phase_index() {
    for i in "${!PHASES[@]}"; do
        [ "${PHASES[$i]}" == "$1" ] && echo "$i" && return
    done
    echo "fase invalida: $1" >&2; exit 1
}
FROM_IDX=$(phase_index "$FROM_PHASE")
should_run_phase() {
    local idx; idx=$(phase_index "$1")
    [ "$idx" -ge "$FROM_IDX" ]
}

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

DEBUG="uv run python3 debug_stages.py"

echo "=== ajustando concorrencia global do tsp pra $N_WORKERS ==="
tsp -S "$N_WORKERS"

# ------------------------------------------------------------------------
# Utilitarios de fila/espera, reusados por toda fase paralela abaixo.
# ------------------------------------------------------------------------

# Enfileira 1 job no tsp e devolve o id (stdout). Uso: jid=$(enqueue cmd...)
enqueue() {
    tsp "$@"
}

# Espera todos os jobs (ids passados como args) terminarem.
wait_jobs() {
    local ids=("$@")
    while true; do
        local all_done=true
        for jid in "${ids[@]}"; do
            local state
            state=$(tsp | awk -v id="$jid" '$1==id {print $2}')
            if [ "$state" != "finished" ]; then all_done=false; break; fi
        done
        $all_done && break
        sleep 30
    done
}

# Confere E-Level de todos os jobs. Ecoa "OK" ou "FALHOU: <ids>".
check_jobs() {
    local ids=("$@")
    local failed=()
    for jid in "${ids[@]}"; do
        local elevel
        elevel=$(tsp | awk -v id="$jid" '$1==id {print $4}')
        [ "$elevel" != "0" ] && failed+=("$jid")
    done
    if [ "${#failed[@]}" -gt 0 ]; then
        echo "FALHOU: ${failed[*]}"
    else
        echo "OK"
    fi
}

# Enfileira 1 job por ano (ordem decrescente -- LPT, anos recentes do RAIS
# tem mais vinculos/linhas), espera todos, e sai com erro se algum falhar.
run_year_workers() {
    local label="$1"; shift
    local year_start="$1" year_end="$2"; shift 2
    local cmd=("$@")
    echo "=== [$label] enfileirando 1 job por ano ($year_start-$year_end, ordem decrescente) ==="
    local ids=()
    for year in $(seq "$year_end" -1 "$year_start"); do
        local jid
        jid=$(enqueue "${cmd[@]}" --year "$year")
        ids+=("$jid")
    done
    echo "=== [$label] aguardando ${#ids[@]} workers ==="
    wait_jobs "${ids[@]}"
    local result; result=$(check_jobs "${ids[@]}")
    if [ "$result" != "OK" ]; then
        echo "!!! [$label] $result -- confira os logs (tsp -c <id>) antes de tentar de novo"
        exit 1
    fi
    echo "=== [$label] todos os anos OK ==="
}

# Idem, mas por pasta (recebe a lista de pastas via stdin, 1 por linha).
run_folder_workers() {
    local label="$1"; shift
    local cmd=("$@")
    local ids=()
    while IFS= read -r folder; do
        [ -z "$folder" ] && continue
        local jid
        jid=$(enqueue "${cmd[@]}" --folder "$folder")
        ids+=("$jid")
    done
    echo "=== [$label] enfileirados ${#ids[@]} jobs (1 por pasta) ==="
    wait_jobs "${ids[@]}"
    local result; result=$(check_jobs "${ids[@]}")
    if [ "$result" != "OK" ]; then
        echo "!!! [$label] $result -- confira os logs (tsp -c <id>) antes de tentar de novo"
        exit 1
    fi
    echo "=== [$label] todas as pastas OK ==="
}

RAIS_YEAR_START=$(uv run python3 -c "import yaml; print(yaml.safe_load(open('rais/configuration.yaml'))['intervalo_rais'][0])")
RAIS_YEAR_END=$(uv run python3 -c "import yaml; print(yaml.safe_load(open('rais/configuration.yaml'))['intervalo_rais'][1])")

# ------------------------------------------------------------------------
# [preproc]
# ------------------------------------------------------------------------
phase_preproc() {
    echo "############## FASE preproc ##############"
    jid=$(enqueue $DEBUG --from cidades --to uniao_dac_comvest)
    wait_jobs "$jid"
    result=$(check_jobs "$jid")
    if [ "$result" != "OK" ]; then
        echo "!!! [preproc] falhou -- confira 'tsp -c $jid'"
        exit 1
    fi
    echo "=== [preproc] OK ==="
}

# ------------------------------------------------------------------------
# [pivot]
# ------------------------------------------------------------------------
phase_pivot() {
    echo "############## FASE pivot ##############"

    # pre_process_parquet e identification sao independentes entre si --
    # enfileiram junto, competem pela mesma fila.
    echo "=== [pivot] pre_process_parquet + identification (em paralelo, por ano cada) ==="
    ids=()
    for year in $(seq "$RAIS_YEAR_END" -1 "$RAIS_YEAR_START"); do
        ids+=("$(enqueue uv run python3 -m rais.pre_processing.parquet_parsing --year "$year")")
        ids+=("$(enqueue uv run python3 -m rais.pre_processing.identification --year "$year")")
    done
    wait_jobs "${ids[@]}"
    result=$(check_jobs "${ids[@]}")
    if [ "$result" != "OK" ]; then
        echo "!!! [pivot] pre_process_parquet/identification: $result"
        exit 1
    fi
    echo "=== [pivot] pre_process_parquet + identification OK ==="

    echo "=== [pivot] cpf_verification (sequencial) ==="
    jid=$(enqueue $DEBUG --run-one cpf_verification)
    wait_jobs "$jid"
    result=$(check_jobs "$jid")
    if [ "$result" != "OK" ]; then
        echo "!!! [pivot] cpf_verification falhou -- confira 'tsp -c $jid'"
        exit 1
    fi

    echo "=== [pivot] recover_cpf_dac_comvest (script paralelo dedicado) ==="
    bash rais/id_generation/run_parallel_recover.sh "$N_WORKERS"
    tsp -S "$N_WORKERS"

    echo "=== [pivot] random_index (sequencial) ==="
    jid=$(enqueue $DEBUG --run-one random_index)
    wait_jobs "$jid"
    result=$(check_jobs "$jid")
    if [ "$result" != "OK" ]; then
        echo "!!! [pivot] random_index falhou -- confira 'tsp -c $jid'"
        exit 1
    fi
    echo "=== [pivot] OK -- dac_comvest_ids.csv atualizado ==="
}

# ------------------------------------------------------------------------
# [fanout] -- cada cadeia roda como 1 job tsp que enfileira+espera seus
# proprios sub-workers. Lancadas todas de uma vez (ids coletados), depois
# esperamos TODAS as cadeias terminarem.
# ------------------------------------------------------------------------
chain_rais() {
    set -e
    run_year_workers "rais_merge" "$RAIS_YEAR_START" "$RAIS_YEAR_END" \
        uv run python3 -m rais.extract.merge

    echo "=== [rais_recover_cpf] construindo lookup pis->cpf (sequencial, le todos os anos) ==="
    jid=$(tsp uv run python3 -m rais.extract.recover_cpf_rais --build-lookup)
    while [ "$(tsp | awk -v id="$jid" '$1==id {print $2}')" != "finished" ]; do sleep 20; done
    elevel=$(tsp | awk -v id="$jid" '$1==id {print $4}')
    if [ "$elevel" != "0" ]; then
        echo "!!! [rais_recover_cpf] build-lookup falhou -- confira 'tsp -c $jid'"; exit 1
    fi

    run_year_workers "rais_recover_cpf" "$RAIS_YEAR_START" "$RAIS_YEAR_END" \
        uv run python3 -m rais.extract.recover_cpf_rais

    # rais_clear numa fila tsp SEPARADA (TS_SOCKET dedicado), concorrencia
    # bem menor -- ver comentario no topo do arquivo (RAIS_CLEAR_WORKERS).
    # Exportar/desfazer TS_SOCKET aqui so afeta este processo (chain_rais
    # roda em background, fork proprio) -- nao vaza pras outras cadeias.
    export TS_SOCKET="$SCRIPT_DIR/.run_pipeline_logs/ts_rais_clear.socket"
    tsp -S "$RAIS_CLEAR_WORKERS"
    run_year_workers "rais_clear" "$RAIS_YEAR_START" "$RAIS_YEAR_END" \
        uv run python3 -m rais.extract.clear

    echo "=== [rais_clear] finalizacao (concat + anonimizacao + amostra final, sequencial) ==="
    jid=$(tsp uv run python3 -m rais.extract.clear --finalize)
    while [ "$(tsp | awk -v id="$jid" '$1==id {print $2}')" != "finished" ]; do sleep 20; done
    elevel=$(tsp | awk -v id="$jid" '$1==id {print $4}')
    if [ "$elevel" != "0" ]; then
        unset TS_SOCKET
        echo "!!! [rais_clear] finalizacao falhou -- confira 'tsp -c $jid'"; exit 1
    fi
    unset TS_SOCKET
    echo "=== [cadeia RAIS] OK ==="
}

chain_socio() {
    set -e
    uv run python3 -c "
from socio.utilities.io import list_dirs_socio_input
for f in sorted(list_dirs_socio_input()): print(f)
" > /tmp/socio_folders.$$.txt
    run_folder_workers "socio_clear" uv run python3 -m socio.cleaning.clear < /tmp/socio_folders.$$.txt
    rm -f /tmp/socio_folders.$$.txt

    echo "=== [socio_merge] sequencial ==="
    jid=$(tsp $DEBUG --run-one socio_merge)
    while [ "$(tsp | awk -v id="$jid" '$1==id {print $2}')" != "finished" ]; do sleep 20; done
    elevel=$(tsp | awk -v id="$jid" '$1==id {print $4}')
    if [ "$elevel" != "0" ]; then
        echo "!!! [socio_merge] falhou -- confira 'tsp -c $jid'"; exit 1
    fi
    echo "=== [cadeia SOCIO] OK ==="
}

chain_capes() {
    set -e
    uv run python3 -c "
from capes.utilities.io import list_dirs_capes_input
for f in sorted(list_dirs_capes_input()): print(f)
" > /tmp/capes_folders.$$.txt
    run_folder_workers "capes_clean" uv run python3 -m capes.cleaning.clean < /tmp/capes_folders.$$.txt
    rm -f /tmp/capes_folders.$$.txt

    echo "=== [capes_merge] sequencial ==="
    jid=$(tsp $DEBUG --run-one capes_merge)
    while [ "$(tsp | awk -v id="$jid" '$1==id {print $2}')" != "finished" ]; do sleep 20; done
    elevel=$(tsp | awk -v id="$jid" '$1==id {print $4}')
    if [ "$elevel" != "0" ]; then
        echo "!!! [capes_merge] falhou -- confira 'tsp -c $jid'"; exit 1
    fi
    echo "=== [cadeia CAPES] OK ==="
}

chain_enem() {
    set -e
    jid=$(tsp $DEBUG --from enem_vest_ids --to enem_ids_merge)
    while [ "$(tsp | awk -v id="$jid" '$1==id {print $2}')" != "finished" ]; do sleep 20; done
    elevel=$(tsp | awk -v id="$jid" '$1==id {print $4}')
    if [ "$elevel" != "0" ]; then
        echo "!!! [cadeia ENEM] falhou -- confira 'tsp -c $jid'"; exit 1
    fi
    echo "=== [cadeia ENEM] OK ==="
}

chain_unesp_fuvest() {
    set -e
    jid=$(tsp $DEBUG --stage unesp fuvest)
    while [ "$(tsp | awk -v id="$jid" '$1==id {print $2}')" != "finished" ]; do sleep 20; done
    elevel=$(tsp | awk -v id="$jid" '$1==id {print $4}')
    if [ "$elevel" != "0" ]; then
        echo "!!! [unesp/fuvest] falhou -- confira 'tsp -c $jid'"; exit 1
    fi
    echo "=== [cadeia UNESP/FUVEST] OK ==="
}

chain_diplomas() {
    set -e
    jid=$(tsp $DEBUG --from diplomas_scrapper --to diplomas_merge)
    while [ "$(tsp | awk -v id="$jid" '$1==id {print $2}')" != "finished" ]; do sleep 20; done
    elevel=$(tsp | awk -v id="$jid" '$1==id {print $4}')
    if [ "$elevel" != "0" ]; then
        echo "!!! [cadeia DIPLOMAS] falhou -- confira 'tsp -c $jid'"; exit 1
    fi
    echo "=== [cadeia DIPLOMAS] OK ==="
}

phase_fanout() {
    echo "############## FASE fanout ##############"
    echo "=== lancando as 6 cadeias independentes em paralelo (bash background) ==="

    LOG_DIR="$SCRIPT_DIR/.run_pipeline_logs"
    mkdir -p "$LOG_DIR"

    chain_rais         > "$LOG_DIR/chain_rais.log"         2>&1 &
    PID_RAIS=$!
    chain_socio        > "$LOG_DIR/chain_socio.log"        2>&1 &
    PID_SOCIO=$!
    chain_capes        > "$LOG_DIR/chain_capes.log"        2>&1 &
    PID_CAPES=$!
    chain_enem         > "$LOG_DIR/chain_enem.log"         2>&1 &
    PID_ENEM=$!
    chain_unesp_fuvest > "$LOG_DIR/chain_unesp_fuvest.log" 2>&1 &
    PID_UF=$!
    chain_diplomas     > "$LOG_DIR/chain_diplomas.log"     2>&1 &
    PID_DIPLOMAS=$!

    FAILED=0
    for pid_var in PID_RAIS PID_SOCIO PID_CAPES PID_ENEM PID_UF PID_DIPLOMAS; do
        pid="${!pid_var}"
        if ! wait "$pid"; then
            echo "!!! cadeia $pid_var (pid $pid) falhou -- veja $LOG_DIR/"
            FAILED=1
        fi
    done

    if [ "$FAILED" -eq 1 ]; then
        echo "=== [fanout] ABORTADO: pelo menos 1 cadeia falhou. Logs em $LOG_DIR/ ==="
        exit 1
    fi
    echo "=== [fanout] todas as cadeias OK ==="
}

# ------------------------------------------------------------------------
# [empresa]
# ------------------------------------------------------------------------
phase_empresa() {
    echo "############## FASE empresa ##############"
    jid=$(enqueue $DEBUG --stage empresa estabelecimento simples)
    wait_jobs "$jid"
    result=$(check_jobs "$jid")
    if [ "$result" != "OK" ]; then
        echo "!!! [empresa] falhou -- confira 'tsp -c $jid'"
        exit 1
    fi
    echo "=== [empresa] OK ==="
}

# ------------------------------------------------------------------------
# [finalizacao]
# ------------------------------------------------------------------------
phase_finalizacao() {
    echo "############## FASE finalizacao ##############"
    jid=$(enqueue $DEBUG --from merge_sheets --to identificadores)
    wait_jobs "$jid"
    result=$(check_jobs "$jid")
    if [ "$result" != "OK" ]; then
        echo "!!! [finalizacao] falhou -- confira 'tsp -c $jid'"
        exit 1
    fi
    echo "=== [finalizacao] OK ==="
}

# ------------------------------------------------------------------------
# Execucao
# ------------------------------------------------------------------------
should_run_phase preproc      && phase_preproc
should_run_phase pivot        && phase_pivot
should_run_phase fanout       && phase_fanout
should_run_phase empresa      && phase_empresa
should_run_phase finalizacao  && phase_finalizacao

echo "############## PIPELINE COMPLETO ##############"
