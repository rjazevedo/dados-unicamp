import pandas as pd

import dac.clr_historico_escolar.__main__ as clr_historico_escolar
import dac.clr_resumo_por_periodo.__main__ as clr_resumo_por_periodo
import dac.clr_vida_academica.__main__ as clr_vida_academica
import dac.clr_vida_academica_habilitacao.__main__ as clr_vida_academica_habilitacao
import dac.uniao_dac_comvest.__main__ as uniao_dac_comvest
import dac.create_ids.__main__ as create_ids

from dac.clr_dados_cadastrais import school_codes
from dac.clr_dados_cadastrais import uf_codes
import dac.clr_dados_cadastrais.limpeza_dados as limpeza_dados_dac
import dac.clr_dados_cadastrais.setup_dados as setup_dados
import dac.create_ufs_codes.__main__ as create_ufs_codes
import dac.create_names_ids.__main__ as create_names_ids
from dac.create_ids import identificadores

import comvest.clear_dados.limpeza_dados as limpeza_dados_comvest
from comvest.clear_dados import cod_ibge, cod_inep, ids_nomes
from comvest.clear_perfil import limpeza_perfil
import comvest.escolas.__main__ as escolas
from comvest.clear_notas import limpeza_notas, presenca

import comvest.extract_cities.__main__ as extrair_cidades
import comvest.extract_courses.__main__ as extrair_cursos
import comvest.extract_enrolled.__main__ as extrair_enrolled

from comvest.utilities.io import read_output
from comvest.utilities.dtypes import (
    DTYPES_DADOS,
    DTYPES_PERFIL,
    DTYPES_MATRICULADOS,
    DTYPES_NOTAS
)
from comvest.assign_ids import comvest_ids
import comvest.extract.__main__ as comvest_database

import rais.pre_processing.__main__ as pre_process_rais
import rais.id_generation.__main__ as id_generation
import rais.extract.__main__ as rais_database

import socio.cleaning.__main__ as clear_socio
import socio.extract.__main__ as extract_socio

def exportar_comvest():
    comvest = read_output(
        "comvest_amostra.csv",
        dtype={**DTYPES_DADOS, **DTYPES_PERFIL, **DTYPES_MATRICULADOS, **DTYPES_NOTAS},
    )

    comvest.to_csv('/home/processados/pedido_0/comvest_amostra.csv', index=False)

def exportar_dac():
    pass

def exportar_rais():
    pass

def exportar_socios():
    pass

def exportar_pedido_0():
    exportar_comvest()

def main():
    #comvest_database.extract()

    #''' Insert other database extractions here '''

    #exportar_pedido_0()
    rodar_base_inteira()
    
def rodar_base_inteira():
    extrair_cidades.main()
    extrair_cursos.main()
    extrair_enrolled.main()
    limpeza_dados_comvest.extraction()
    setup_dados.load_dados_cadastais()
    create_ufs_codes.main()
    create_names_ids.main()
    limpeza_dados_dac.generate_clean_data()
    uf_codes.generate_uf_code()
    cod_ibge.merge() 
    escolas.main()
    school_codes.generate_school_codes()
    cod_inep.merge()
    ids_nomes.merge()
    limpeza_perfil.extraction()
    limpeza_notas.extraction()
    presenca.get()
    clr_historico_escolar.main()
    clr_resumo_por_periodo.main()
    clr_vida_academica.main()
    clr_vida_academica_habilitacao.main()
    uniao_dac_comvest.main()


if __name__ == '__main__':
    main()