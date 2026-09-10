"""Tasks do Prefect para o pre-processamento e base da COMVEST.

Mapeamento ~1:1 com as funcoes ja existentes (mesmas chamadas que
debug_stages.py usa no grupo comvest_preproc/comvest_base/finalizacao) --
nenhuma logica de negocio foi reescrita aqui, so decorada com @task.
"""

from prefect import task

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

from config.settings import get_config
from flows.cache import file_exists_cache_key


def _result_file(name):
    return lambda: get_config("comvest")["result"] + name


@task(cache_key_fn=file_exists_cache_key(_result_file("cidades_comvest.csv")))
def extrair_cidades_task():
    extrair_cidades.extraction()


@task(cache_key_fn=file_exists_cache_key(_result_file("cursos_comvest.csv")))
def extrair_cursos_task():
    extrair_cursos.extraction()


@task
def dict_cursos_task():
    dict_cursos.get()


@task(cache_key_fn=file_exists_cache_key(_result_file("matriculados_comvest.csv")))
def extrair_matriculados_task():
    extrair_matriculados.extraction()


@task
def extrair_convocados_task():
    extrair_convocados.extraction()


@task(cache_key_fn=file_exists_cache_key(_result_file("dados_comvest.csv")))
def limpeza_dados_comvest_task():
    limpeza_dados_comvest.extraction()


@task(cache_key_fn=file_exists_cache_key(_result_file("dados_comvest_com_uf.csv")))
def cod_ibge_task():
    cod_ibge.merge()


@task
def validacao_esc_task():
    validacao_esc.validation()


@task
def cod_inep_task():
    cod_inep.merge()


@task
def ids_nomes_task():
    ids_nomes.merge()


@task
def limpeza_perfil_task():
    limpeza_perfil.extraction()


@task
def limpeza_notas_task():
    limpeza_notas.extraction()


@task
def presenca_task():
    presenca.get()


@task
def merge_sheets_task():
    merge_sheets.merge()


@task
def comvest_ids_task():
    comvest_ids.assign_ids()
