import pandas as pd
from dac.extract_database import dac_database
import dac.clr_dados_cadastrais.dados_pre_and_pos as dados_pre_and_pos
import dac.create_ufs_codes.__main__ as create_ufs_codes
import dac.create_names_ids.__main__ as create_names_ids
from dac.create_ids import identificadores
from comvest.clear_dados import limpeza_dados, cod_ibge, cod_inep, ids_nomes
from comvest.clear_perfil import limpeza_perfil
from comvest.clear_notas import limpeza_notas, presenca
import comvest.extract_enrolled.__main__ as extrair_enrolled
import comvest.extract_cities.__main__ as extrair_cidades
import comvest.extract_courses.__main__ as extrair_cursos
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
    limpeza_dados.extraction()
    # OK
    dados_pre_and_pos.load_dados_cadastais()
    create_ufs_codes.main()
    create_names_ids.main()
    return 
    escolas.main()
    dados_cadastrais.main()
    cod_ibge.merge()
    cod_inep.merge()
    ids_nomes.merge()
    limpeza_perfil.extraction()
    limpeza_notas.extraction()
    presenca.get()


if __name__ == '__main__':
    main()