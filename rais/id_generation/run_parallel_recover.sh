#!/bin/bash
# Roda recover_cpf_dac_comvest em paralelo, um worker por ano do RAIS,
# via tsp (task spooler) -- sem precisar de ninguem acompanhando: o script
# enfileira tudo, espera terminar, confere falha, e roda a finalizacao
# sozinho. Pode rodar em background (nohup/tsp) e conferir o resultado
# depois.
#
# Uso:
#   bash rais/id_generation/run_parallel_recover.sh [N_WORKERS]
#   (N_WORKERS default: 16)
#
# Desenho:
# - Cada ano (2002-2022, 21 no total) vira 1 job na fila do tsp -- nao
#   agrupa anos por worker de antemao. O tsp (-S N_WORKERS) puxa o proximo
#   ano da fila assim que um slot libera, balanceando a carga sozinho --
#   nao precisa adivinhar de antemao quais anos sao mais pesados.
# - Enfileirado em ordem DECRESCENTE (2022 primeiro, 2002 por ultimo) --
#   escalonamento LPT (longest job first): anos recentes do RAIS tem mais
#   vinculos formais registrados (mais pesados), comecar por eles evita
#   sobrar um ano pesado sozinho no fim da fila com poucos workers ainda
#   ocupados nele.
# - So roda a finalizacao (rais_recover_finalize.py) depois que TODOS os
#   21 workers terminarem com sucesso -- se qualquer um falhar, aborta sem
#   rodar a finalizacao (evita gerar resultado incompleto silenciosamente).

set -e

N_WORKERS="${1:-16}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
cd "$REPO_ROOT"

echo "=== ajustando concorrencia do tsp pra $N_WORKERS ==="
tsp -S "$N_WORKERS"

echo "=== limpando estado anterior (raw batches + resultado parcial) ==="
uv run python3 -c "
import sys; sys.path.insert(0, '.')
from rais.id_generation.recover_cpf_dac_comvest import RAW_MATCHES_DIR, CPF_RECOVERED_BATCHES_FILE
import os, shutil
if os.path.exists(CPF_RECOVERED_BATCHES_FILE):
    os.remove(CPF_RECOVERED_BATCHES_FILE)
shutil.rmtree(RAW_MATCHES_DIR, ignore_errors=True)
os.makedirs(RAW_MATCHES_DIR, exist_ok=True)
"

echo "=== enfileirando 21 workers (1 por ano, ordem decrescente 2022->2002) ==="
JOB_IDS=()
for year in $(seq 2022 -1 2002); do
    jid=$(tsp uv run python3 -m rais.id_generation.rais_recover_worker --year-start "$year" --year-end "$year")
    JOB_IDS+=("$jid")
    echo "  ano $year -> job tsp $jid"
done

echo "=== aguardando os ${#JOB_IDS[@]} workers terminarem (checagem a cada 60s) ==="
while true; do
    all_done=true
    for jid in "${JOB_IDS[@]}"; do
        state=$(tsp | awk -v id="$jid" '$1==id {print $2}')
        if [ "$state" != "finished" ]; then
            all_done=false
            break
        fi
    done
    if $all_done; then break; fi
    sleep 60
done

echo "=== todos os workers terminaram -- conferindo falhas ==="
FAILED=0
for jid in "${JOB_IDS[@]}"; do
    elevel=$(tsp | awk -v id="$jid" '$1==id {print $4}')
    if [ "$elevel" != "0" ]; then
        echo "  !!! job $jid terminou com E-Level=$elevel (falhou)"
        FAILED=1
    fi
done

if [ "$FAILED" -eq 1 ]; then
    echo "=== ABORTADO: pelo menos 1 worker falhou, finalizacao NAO foi rodada ==="
    echo "Rode 'tsp' pra ver quais jobs falharam e inspecione o log de cada um antes de tentar de novo."
    exit 1
fi

echo "=== todos os workers OK -- rodando finalizacao (dedup final + escrita do resultado) ==="
tsp -S 1
finalize_jid=$(tsp uv run python3 -m rais.id_generation.rais_recover_finalize)
echo "finalizacao enfileirada como job tsp $finalize_jid, aguardando..."

while true; do
    state=$(tsp | awk -v id="$finalize_jid" '$1==id {print $2}')
    if [ "$state" == "finished" ]; then break; fi
    sleep 30
done

elevel=$(tsp | awk -v id="$finalize_jid" '$1==id {print $4}')
if [ "$elevel" != "0" ]; then
    echo "=== finalizacao FALHOU (E-Level=$elevel) -- confira o log do job $finalize_jid ==="
    exit 1
fi

echo "=== CONCLUIDO COM SUCESSO -- uniao_dac_comvest_recovered.csv atualizado ==="
