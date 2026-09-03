"""
Ferramenta de DEBUG para reexecutar etapas do pipeline (__main__.py) isoladamente,
reaproveitando os arquivos intermediarios ja existentes em /home/output/intermediario/.

NAO substitui __main__.py nem representa a arquitetura final do pipeline -- e um
atalho temporario para acelerar o ciclo "roda -> quebra -> corrige -> roda de novo"
enquanto varios bugs de import/dtype/coluna estao sendo corrigidos em sequencia.

Uso:
  # lista todas as etapas, agrupadas na mesma ordem/dependencia do __main__.py
  uv run debug_stages.py --list

  # roda so uma etapa (usa os intermediarios em disco como estao)
  uv run debug_stages.py --stage limpeza_perfil

  # roda varias etapas em sequencia, na ordem dada
  uv run debug_stages.py --stage limpeza_perfil limpeza_notas presenca

  # roda um grupo inteiro (mesma ordem que __main__.py chamaria)
  uv run debug_stages.py --stage-group comvest_base

  # roda VARIAS etapas em paralelo (processos separados). VOCE escolhe quais --
  # este script NAO valida automaticamente que as etapas escolhidas sao
  # independentes entre si (ver "IMPORTANTE" abaixo e as notas em --list).
  uv run debug_stages.py --parallel diplomas_scrapper unesp fuvest capes_clean

Depois de achar e corrigir todos os erros, faca a execucao limpa e sequencial de
verdade com `uv run __main__.py`.

IMPORTANTE sobre --parallel: cada etapa aqui e uma chamada de funcao que le e
escreve arquivos CSV em /home/output/intermediario/ (read_result/write_result).
Rodar duas etapas em paralelo so e seguro se nenhuma delas escreve um arquivo
que a outra le ou escreve. Isso NAO e verificado automaticamente -- antes de
usar --parallel, confira com grep (read_result/write_result/FILE_NAME) nos
modulos envolvidos, ou use so as combinacoes ja conferidas listadas abaixo em
--list. Etapas dentro do mesmo grupo em --stage-group NAO sao necessariamente
seguras em paralelo entre si (ex.: comvest_preproc e dac_preproc tem uma cadeia
real de dependencia por arquivo, apesar de parecerem passos separados).
"""
import argparse
import importlib
import subprocess
import sys
import time
from pathlib import Path

# Mesmos imports do __main__.py raiz, na mesma ordem -- se o __main__.py real
# importa sem erro hoje, isso aqui tambem importa sem erro.
from comvest.extract_cities import extrair_cidades
from comvest.extract_courses import extrair_cursos, dict_cursos
from comvest.extract_enrolled import extrair_matriculados, extrair_convocados
import comvest.clear_dados.limpeza_dados as limpeza_dados_comvest
from comvest.clear_dados import cod_ibge, cod_inep, ids_nomes
from comvest.escolas import validacao_esc
from comvest.clear_perfil import limpeza_perfil
from comvest.clear_notas import limpeza_notas, presenca
import comvest.extract.merge_sheets as merge_sheets
import comvest.assign_ids.comvest_ids as comvest_ids

import dac.clr_dados_cadastrais.setup_dados as setup_dados
from dac.create_ufs_codes import ufs_codes
from dac.create_names_ids import create_ids
import dac.clr_dados_cadastrais.limpeza_dados as limpeza_dados_dac
from dac.clr_dados_cadastrais import uf_codes, school_codes
from dac.clr_historico_escolar import historico_escolar
from dac.clr_resumo_por_periodo import resumo_por_periodo, resumo_periodo_cr
from dac.clr_vida_academica import vida_academica, dados_ingressantes
from dac.clr_vida_academica_habilitacao import habilitacao
from dac.uniao_dac_comvest import uniao_dac_comvest
import dac.create_ids.identificadores as identificadores

from enem.comvest_enem import clear_comvest
from enem.comvest_enem import divide_comvest
from enem.comvest_enem import comvest_enem
from enem.comvest_enem import comvest_vest_ids
from enem.comvest_enem import comvest_enem_ids

from diplomas.extract_usp import scrapper
from diplomas.extract_usp import comvest_diplomasUSP

from rais.id_generation import cpf_verification
from rais.id_generation import recover_cpf_dac_comvest
from rais.id_generation import random_index
from rais.pre_processing import identification
from rais.pre_processing import parquet_parsing
from rais.extract import merge
from rais.extract import recover_cpf_rais
from rais.extract import clear

from socio.cleaning import clear as clear_socio
from socio.extract import merge as merge_socio

from capes.cleaning import clean as clean_capes
from capes.extract import merge as merge_capes

from unesp.extract.extract import extract_unesp
from fuvest.extract.extract import extract_fuvest
from empresa.extract import extract_empresa_amostra
from estabelecimento.extract import extract_estabelecimento_amostra
from simples.extract import extract_simples_amostra


# Cada entrada: nome curto -> (grupo, callable sem args, ou callable que recebe `args`)
# Ordem e argumentos identicos ao main() de __main__.py.
STAGES = {
    # --- COMVEST pre-processamento ---
    "cidades": ("comvest_preproc", lambda a: extrair_cidades.extraction()),
    "cursos": ("comvest_preproc", lambda a: extrair_cursos.extraction()),
    "dict_cursos": ("comvest_preproc", lambda a: dict_cursos.get()),
    "matriculados": ("comvest_preproc", lambda a: extrair_matriculados.extraction()),
    "convocados": ("comvest_preproc", lambda a: extrair_convocados.extraction()),
    "limpeza_dados_comvest": ("comvest_preproc", lambda a: limpeza_dados_comvest.extraction()),

    # --- DAC pre-processamento ---
    "setup_dados": ("dac_preproc", lambda a: setup_dados.load_dados_cadastais()),
    "ufs_codes": ("dac_preproc", lambda a: ufs_codes.generate_clean_data()),
    "create_ids": ("dac_preproc", lambda a: create_ids.create_ids()),
    "limpeza_dados_dac": ("dac_preproc", lambda a: limpeza_dados_dac.generate_clean_data()),
    "uf_codes": ("dac_preproc", lambda a: uf_codes.generate_uf_code()),

    # --- ENEM pre-processamento ---
    "clear_comvest": ("enem_preproc", lambda a: clear_comvest.clean_all()),
    "divide_comvest": ("enem_preproc", lambda a: divide_comvest.split_all()),

    # --- Base da COMVEST ---
    "cod_ibge": ("comvest_base", lambda a: cod_ibge.merge()),
    "validacao_esc": ("comvest_base", lambda a: validacao_esc.validation()),
    "school_codes": ("comvest_base", lambda a: school_codes.generate_school_codes()),
    "cod_inep": ("comvest_base", lambda a: cod_inep.merge()),
    "ids_nomes": ("comvest_base", lambda a: ids_nomes.merge()),
    "limpeza_perfil": ("comvest_base", lambda a: limpeza_perfil.extraction()),
    "limpeza_notas": ("comvest_base", lambda a: limpeza_notas.extraction()),
    "presenca": ("comvest_base", lambda a: presenca.get()),

    # --- Merge ENEM ---
    "comvest_enem": ("enem_merge", lambda a: comvest_enem.merge()),

    # --- Base da DAC ---
    "historico_escolar": ("dac_base", lambda a: historico_escolar.generate_clean_data()),
    "resumo_por_periodo": ("dac_base", lambda a: resumo_por_periodo.generate_clean_data()),
    "resumo_periodo_cr": ("dac_base", lambda a: resumo_periodo_cr.generate_cr()),
    "vida_academica": ("dac_base", lambda a: vida_academica.generate_clean_data()),
    "dados_ingressantes": ("dac_base", lambda a: dados_ingressantes.generate()),
    "habilitacao": ("dac_base", lambda a: habilitacao.generate()),
    "uniao_dac_comvest": ("dac_base", lambda a: uniao_dac_comvest.generate()),

    # --- RAIS pre-processamento + geracao do pivo (dac_comvest_ids.csv) ---
    # pre_process_parquet: cache novo em parquet (rais/pre_processing/parquet_parsing.py),
    # consumido so por recover_cpf_dac_comvest.py via read_rais_identification_parquet().
    # Roda em paralelo/independente de "identification" (pkl) -- os dois cachês coexistem
    # ate a reconciliacao completa (merge.py/cpf_verification.py/recover_cpf_rais.py
    # continuam no pkl por ora, ver plan.md item 5).
    "pre_process_parquet": ("rais_ids_pivot", lambda a: parquet_parsing.parse_rais()),
    "identification": ("rais_ids_pivot", lambda a: identification.get_identification_from_all_years()),
    "cpf_verification": ("rais_ids_pivot", lambda a: cpf_verification.remove_invalid_cpf()),
    "recover_cpf_dac_comvest": ("rais_ids_pivot", lambda a: recover_cpf_dac_comvest.recover_cpf_dac_comvest()),
    "random_index": ("rais_ids_pivot", lambda a: random_index.generate_index()),

    # --- Fanout (tudo abaixo depende so do pivo dac_comvest_ids.csv, exceto diplomas*) ---
    "diplomas_scrapper": ("fanout", lambda a: scrapper.proccess_usp()),
    "diplomas_merge": ("fanout", lambda a: comvest_diplomasUSP.merge()),
    "enem_vest_ids": ("fanout", lambda a: comvest_vest_ids.retrieve()),
    "enem_ids_merge": ("fanout", lambda a: comvest_enem_ids.merge()),
    "rais_merge": ("fanout", lambda a: merge.merge_all_years()),
    "rais_recover_cpf": ("fanout", lambda a: recover_cpf_rais.recover_cpf_all_years()),
    "rais_clear": ("fanout", lambda a: clear.clear_all_years(a.tipo_extracao_rais)),
    "socio_clear": ("fanout", lambda a: clear_socio.clear_socio()),
    "socio_merge": ("fanout", lambda a: merge_socio.merge_socio_dac_comvest(a.tipo_extracao_socios)),
    "capes_clean": ("fanout", lambda a: clean_capes.clean_capes()),
    "capes_merge": ("fanout", lambda a: merge_capes.extract_ids()),
    "unesp": ("fanout", lambda a: extract_unesp()),
    "fuvest": ("fanout", lambda a: extract_fuvest()),

    # --- Depende de socio_merge (socio_amostra.csv) ---
    "empresa": ("empresa_estab_simples", lambda a: extract_empresa_amostra()),
    "estabelecimento": ("empresa_estab_simples", lambda a: extract_estabelecimento_amostra()),
    "simples": ("empresa_estab_simples", lambda a: extract_simples_amostra()),

    # --- Atribuicao final de ids ---
    "merge_sheets": ("finalizacao", lambda a: merge_sheets.merge()),
    "comvest_ids": ("finalizacao", lambda a: comvest_ids.assign_ids()),
    "identificadores": ("finalizacao", lambda a: identificadores.create_ids()),
}

# Ordem dos grupos == ordem real de execucao em __main__.py
GROUP_ORDER = [
    "comvest_preproc", "dac_preproc", "enem_preproc", "comvest_base",
    "enem_merge", "dac_base", "rais_ids_pivot", "fanout",
    "empresa_estab_simples", "finalizacao",
]

# Combinacoes conferidas manualmente (grep em read_result/write_result dos
# modulos envolvidos) como seguras para --parallel nesta sessao. Fora dessas,
# confira voce mesmo antes de rodar em paralelo -- ver aviso no topo do arquivo.
VERIFIED_PARALLEL_SAFE = [
    # Depois que 'dict_cursos' (cursos.csv) ja rodou, estes dois ramos sao
    # independentes entre si (nenhum le o output do outro):
    ["matriculados", "limpeza_dados_comvest"],  # convocados ainda depende de matriculados ter terminado
    # Segundo a investigacao registrada em plan.md (nao re-verificado nesta
    # sessao stage a stage): depois que dac_comvest_ids.csv (pivo) existir,
    # estes ramos do fanout leem so o pivo + seus proprios inputs upstream e
    # escrevem em arquivos de saida distintos:
    ["diplomas_scrapper", "unesp", "fuvest", "capes_clean"],
]


def stage_order():
    """Retorna as chaves de STAGES na mesma ordem de GROUP_ORDER / __main__.py."""
    ordered = []
    for g in GROUP_ORDER:
        ordered += [k for k, (grp, _) in STAGES.items() if grp == g]
    return ordered


def print_list():
    print("Todo grupo deve ser tratado como SEQUENCIAL internamente (mesma ordem")
    print("do __main__.py) a menos que uma combinacao especifica esteja na lista")
    print("'combinacoes conferidas para --parallel' abaixo.\n")
    for g in GROUP_ORDER:
        keys = [k for k, (grp, _) in STAGES.items() if grp == g]
        print(f"[{g}]")
        for k in keys:
            print(f"  {k}")

    print("\ncombinacoes conferidas para --parallel:")
    for combo in VERIFIED_PARALLEL_SAFE:
        print(f"  {' '.join(combo)}")


def run_stage(key, args):
    group, fn = STAGES[key]
    print(f"=== rodando '{key}' (grupo: {group}) ===", flush=True)
    t0 = time.time()
    fn(args)
    print(f"=== '{key}' OK em {time.time() - t0:.1f}s ===", flush=True)


def _launch_stage_subprocess(key, args, log_dir):
    """Roda uma etapa como subprocesso próprio (--run-one interno), com stdout+stderr
    (incluindo traceback completo de qualquer exceção) gravado em log_dir/{key}.log.
    Isolamento por processo: uma etapa que trava, vaza estado global, ou chama
    sys.exit() nao afeta as etapas seguintes."""
    log_path = log_dir / f"{key}.log"
    cmd = [
        sys.executable, str(Path(__file__).resolve()),
        "--run-one", key,
        "--tipo-extracao-rais", args.tipo_extracao_rais,
        "--tipo-extracao-socios", args.tipo_extracao_socios,
    ]
    log_f = open(log_path, "w")
    p = subprocess.Popen(cmd, stdout=log_f, stderr=subprocess.STDOUT)
    return p, log_f, log_path


def _print_failure_tail(key, log_path, n=30):
    print(f"\n--- últimas {n} linhas de {log_path} ---")
    with open(log_path) as f:
        lines = f.readlines()
    print("".join(lines[-n:]))


def run_sequential(keys, args, log_dir):
    """Roda etapas uma de cada vez, NA ORDEM dada. Se uma etapa falhar, o
    traceback completo fica salvo em log_dir/{nome}.log e a execução segue
    para a próxima etapa (não para tudo por causa de uma falha isolada) --
    assim dá pra rodar 'daqui até o fim' de uma vez e revisar todos os logs
    de falha depois, em vez de corrigir um erro por turno."""
    log_dir.mkdir(parents=True, exist_ok=True)
    failures = []
    for k in keys:
        log_path = log_dir / f"{k}.log"
        print(f"=== rodando '{k}' -> {log_path} ===", flush=True)
        t0 = time.time()
        p, log_f, _ = _launch_stage_subprocess(k, args, log_dir)
        rc = p.wait()
        log_f.close()
        dt = time.time() - t0
        if rc == 0:
            print(f"=== '{k}' OK em {dt:.1f}s ===", flush=True)
        else:
            print(f"!!! '{k}' FALHOU em {dt:.1f}s (rc={rc}) -- log completo em {log_path}", flush=True)
            failures.append(k)

    if failures:
        print(f"\n=== {len(failures)} etapa(s) falharam: {', '.join(failures)} ===")
        for k in failures:
            _print_failure_tail(k, log_dir / f"{k}.log")
    return failures


def run_parallel(keys, args, log_dir):
    log_dir.mkdir(parents=True, exist_ok=True)
    procs = {}
    for k in keys:
        print(f"lançando '{k}' em background -> {log_dir / f'{k}.log'}")
        procs[k] = _launch_stage_subprocess(k, args, log_dir)

    print(f"\naguardando {len(procs)} processos...\n")
    results = {}
    for k, (p, log_f, log_path) in procs.items():
        rc = p.wait()
        log_f.close()
        results[k] = rc

    print("\n=== resumo ===")
    failures = []
    for k, rc in results.items():
        status = "OK" if rc == 0 else f"FALHOU (rc={rc})"
        print(f"  {k}: {status}")
        if rc != 0:
            failures.append(k)

    for k in failures:
        _print_failure_tail(k, log_dir / f"{k}.log")

    return failures


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--list", action="store_true", help="lista etapas e grupos")
    parser.add_argument("--stage", nargs="+", metavar="NOME", help="roda etapas em sequência, na ordem dada")
    parser.add_argument("--stage-group", metavar="GRUPO", help="roda um grupo inteiro, em sequência")
    parser.add_argument("--from", dest="from_stage", metavar="NOME",
                         help="roda em sequência a partir desta etapa (ordem real do pipeline)")
    parser.add_argument("--to", dest="to_stage", metavar="NOME",
                         help="roda em sequência até esta etapa (inclusive); combine com --from")
    parser.add_argument("--parallel", nargs="+", metavar="NOME", help="roda etapas em paralelo (processos separados)")
    parser.add_argument("--run-one", metavar="NOME",
                         help=argparse.SUPPRESS)  # uso interno: subprocesso de uma única etapa
    parser.add_argument("--tipo-extracao-rais", choices=["limitada", "completa"], default="completa")
    parser.add_argument("--tipo-extracao-socios", choices=["limitada", "completa"], default="completa")
    parser.add_argument("--log-dir", default=None,
                         help="onde salvar os logs (default: ./.debug_stage_logs)")
    args = parser.parse_args()

    if args.run_one:
        # Subprocesso interno: roda 1 etapa, deixa exceção propagar (traceback
        # completo vai pro stdout/stderr, que o processo pai já está
        # redirecionando pro arquivo de log) e sai com código != 0 se falhar.
        run_stage(args.run_one, args)
        return

    if args.list or not any([args.stage, args.stage_group, args.parallel, args.from_stage, args.to_stage]):
        print_list()
        return

    log_dir = Path(args.log_dir) if args.log_dir else Path(__file__).resolve().parent / ".debug_stage_logs"

    if args.stage:
        failures = run_sequential(args.stage, args, log_dir)
    elif args.stage_group:
        keys = [k for k in stage_order() if STAGES[k][0] == args.stage_group]
        failures = run_sequential(keys, args, log_dir)
    elif args.from_stage or args.to_stage:
        order = stage_order()
        start = order.index(args.from_stage) if args.from_stage else 0
        end = order.index(args.to_stage) + 1 if args.to_stage else len(order)
        keys = order[start:end]
        print(f"rodando {len(keys)} etapa(s), de '{keys[0]}' até '{keys[-1]}': {', '.join(keys)}\n")
        failures = run_sequential(keys, args, log_dir)
    elif args.parallel:
        if sorted(args.parallel) not in [sorted(c) for c in VERIFIED_PARALLEL_SAFE]:
            print("aviso: esta combinacao de etapas NAO esta na lista de combinacoes "
                  "conferidas (--list) -- confira voce mesmo se alguma etapa escreve um "
                  "arquivo que outra le/escreve antes de confiar no resultado. Rodando mesmo assim.\n")
        failures = run_parallel(args.parallel, args, log_dir)

    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
