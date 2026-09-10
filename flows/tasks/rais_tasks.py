"""Tasks do Prefect para RAIS: pre-processamento, geracao do pivo
(dac_comvest_ids.csv) e extract/clear final.

Decomposicao por ano: reaproveita as funcoes "worker de 1 ano so" ja
existentes e validadas em producao via tsp (run_pipeline.sh,
run_parallel_recover.sh) -- nenhuma logica nova escrita aqui, so troca o
orquestrador de concorrencia (tsp -> Prefect .map()/wait_for). Dois padroes
diferentes, reaproveitados como estao:

1. Workers "simples" (pre_process_parquet, identification, rais_merge,
   rais_recover_cpf, rais_clear): cada ano e uma unidade de trabalho
   completa e independente -- .map() direto, sem finalize (exceto
   rais_clear, que tem um passo de uniao final).

2. recover_cpf_dac_comvest (fuzzy matching CPF x nome+data nascimento):
   NAO e "1 ano = 1 resultado independente" -- e "Passo 1 paralelizavel por
   ano" (cada ano so escaneia o RAIS daquele ano em busca de candidatos,
   grava match bruto particionado por ano/lote) + "Passo 2 sequencial,
   tudo-ou-nada" (dedup final entre TODOS os anos, so depois que Passo 1
   terminou em todos). Ver rais/id_generation/rais_recover_worker.py e
   rais_recover_finalize.py (codigo ja existente, so reaproveitado aqui).

random_index.generate_index() continua monolitico -- pd.factorize sobre a
populacao embaralhada inteira, nao tem passo parcial por ano equivalente.
"""

from flows.memory_log import task_with_memory_log as task

from config.settings import get_config
from rais.id_generation import cpf_verification
from rais.id_generation import random_index
from rais.pre_processing import identification
from rais.pre_processing import parquet_parsing
from rais.extract import merge
from rais.extract import recover_cpf_rais
from rais.extract import clear
from rais.utilities.file import create_folder, create_folder_tmp, create_folder_year, create_folder_inside_year
from rais.utilities.read import read_ids, read_dac_comvest_valid
from rais.id_generation import recover_cpf_dac_comvest as recover_dac_comvest_mod
from rais.id_generation.recover_cpf_dac_comvest import (
    get_cpf_missing_dac_comvest,
    prepare_candidate_batches,
    stream_raw_matches,
    finalize_batch,
    finalize_and_write,
    _reset_scratch_files,
    _cleanup_raw_matches_dir,
)
from rais.utilities.logging import log_recover_batch


def rais_years() -> list[int]:
    intervalo = get_config("rais")["intervalo_rais"]
    return list(range(intervalo[0], intervalo[1] + 1))


# --- pre-processamento parquet (Camada 2 de cache do plan.md) ---

@task
def pre_process_parquet_setup_task():
    create_folder(
        path=get_config("rais")["path_output_data"],
        folder_name=parquet_parsing.pre_processed_folder,
    )


@task
def pre_process_parquet_year_task(year: int):
    parquet_parsing.parse_rais_year(year)


# --- identification (cache pkl -- ver nota em rais_ids_flow.py sobre
# nenhum consumidor mais ler esse cache hoje; mantido por paridade) ---

@task
def identification_setup_task():
    create_folder_tmp()


@task
def identification_year_task(year: int):
    create_folder_year(year)
    identification.get_identification_from_year(year)


@task
def cpf_verification_task():
    cpf_verification.remove_invalid_cpf()


# --- recover_cpf_dac_comvest: Passo 1 (por ano) + Passo 2 (finalize) ---

@task
def recover_cpf_reset_task():
    _reset_scratch_files()


@task
def recover_cpf_worker_year_task(year: int):
    df_dac_comvest = read_dac_comvest_valid()
    df_cpf_missing = get_cpf_missing_dac_comvest(df_dac_comvest)
    exact_batches, prob_batches, batch_min_year, _ = prepare_candidate_batches(
        df_cpf_missing
    )
    stream_raw_matches(
        exact_batches, prob_batches, batch_min_year, year_start=year, year_end=year
    )


@task
def recover_cpf_finalize_task():
    df_dac_comvest = read_dac_comvest_valid()
    df_cpf_missing = get_cpf_missing_dac_comvest(df_dac_comvest)
    _, _, _, all_batch_ids = prepare_candidate_batches(df_cpf_missing)
    n_batches = len(all_batch_ids)

    for i, batch_id in enumerate(all_batch_ids, start=1):
        log_recover_batch(i, n_batches, recover_dac_comvest_mod.BATCH_SIZE)
        finalize_batch(batch_id)

    _cleanup_raw_matches_dir()
    finalize_and_write(df_dac_comvest)


@task
def random_index_task():
    random_index.generate_index()


# --- fanout: rais_merge, rais_recover_cpf (RAIS <-> lookup PIS/CPF), rais_clear ---

@task
def rais_merge_year_task(year: int):
    df_dac_comvest = read_ids()
    df_dac_comvest = merge.prepare_dac_comvest(df_dac_comvest)
    create_folder_inside_year(year, "rais_dac_comvest")
    merge.merge_year(df_dac_comvest, year)


@task
def rais_recover_cpf_build_lookup_task():
    recover_cpf_rais.build_and_save_pis_cpf_lookup()


@task
def rais_recover_cpf_year_task(year: int):
    df_pis_cpf = recover_cpf_rais.load_pis_cpf_lookup()
    recover_cpf_rais.recover_cpf_year(df_pis_cpf, year)


@task
def rais_clear_year_task(year: int):
    clear.clear_year(year)


@task
def rais_clear_finalize_task():
    clear.join_all_years()
