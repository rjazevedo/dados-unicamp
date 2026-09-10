"""Tasks do Prefect para RAIS: pre-processamento, geracao do pivo
(dac_comvest_ids.csv) e extract/clear final.

random_index.generate_index() e recover_cpf_dac_comvest() dependem do
conjunto completo de dados (pd.factorize / fuzzy matching multi-estagio) --
NAO decompor em tasks parciais por ano (ver restricao de cache tudo-ou-nada
no plan.md).
"""

from flows.memory_log import task_with_memory_log as task

from rais.id_generation import cpf_verification
from rais.id_generation import recover_cpf_dac_comvest
from rais.id_generation import random_index
from rais.pre_processing import identification
from rais.pre_processing import parquet_parsing
from rais.extract import merge
from rais.extract import recover_cpf_rais
from rais.extract import clear


@task
def pre_process_parquet_task():
    parquet_parsing.parse_rais()


@task
def identification_task():
    identification.get_identification_from_all_years()


@task
def cpf_verification_task():
    cpf_verification.remove_invalid_cpf()


@task
def recover_cpf_dac_comvest_task():
    recover_cpf_dac_comvest.recover_cpf_dac_comvest()


@task
def random_index_task():
    random_index.generate_index()


@task
def rais_merge_task():
    merge.merge_all_years()


@task
def rais_recover_cpf_task():
    recover_cpf_rais.recover_cpf_all_years()


@task
def rais_clear_task(tipo_extracao_rais: str):
    clear.clear_all_years(tipo_extracao_rais)
