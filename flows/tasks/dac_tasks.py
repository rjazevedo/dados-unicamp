"""Tasks do Prefect para o pre-processamento e base da DAC.

Mapeamento ~1:1 com as funcoes existentes (mesmo grupo dac_preproc/dac_base/
finalizacao de debug_stages.py) -- sem reescrever logica de negocio.
"""

from prefect import task

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


@task
def setup_dados_task():
    setup_dados.load_dados_cadastais()


@task
def ufs_codes_task():
    ufs_codes.generate_clean_data()


@task
def create_ids_task():
    create_ids.create_ids()


@task
def limpeza_dados_dac_task():
    limpeza_dados_dac.generate_clean_data()


@task
def uf_codes_task():
    uf_codes.generate_uf_code()


@task
def school_codes_task():
    school_codes.generate_school_codes()


@task
def historico_escolar_task():
    historico_escolar.generate_clean_data()


@task
def resumo_por_periodo_task():
    resumo_por_periodo.generate_clean_data()


@task
def resumo_periodo_cr_task():
    resumo_periodo_cr.generate_cr()


@task
def vida_academica_task():
    vida_academica.generate_clean_data()


@task
def dados_ingressantes_task():
    dados_ingressantes.generate()


@task
def habilitacao_task():
    habilitacao.generate()


# uniao_dac_comvest.generate() faz o fuzzy matching multi-estagio entre
# DAC e COMVEST sobre o conjunto completo de dados -- NAO decompor em
# tasks parciais (ver restricao de cache tudo-ou-nada no plan.md).
@task
def uniao_dac_comvest_task():
    uniao_dac_comvest.generate()


@task
def identificadores_task():
    identificadores.create_ids()
