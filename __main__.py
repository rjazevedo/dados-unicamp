import logging

import dac.clr_historico_escolar.__main__ as clr_historico_escolar
import dac.clr_resumo_por_periodo.__main__ as clr_resumo_por_periodo
import dac.clr_vida_academica.__main__ as clr_vida_academica
import dac.clr_vida_academica_habilitacao.__main__ as clr_vida_academica_habilitacao
import dac.uniao_dac_comvest.__main__ as uniao_dac_comvest

from dac.clr_dados_cadastrais import school_codes
from dac.clr_dados_cadastrais import uf_codes
import dac.clr_dados_cadastrais.limpeza_dados as limpeza_dados_dac
import dac.clr_dados_cadastrais.setup_dados as setup_dados
import dac.create_ufs_codes.__main__ as create_ufs_codes
import dac.create_names_ids.__main__ as create_names_ids
import dac.create_ids.identificadores as identificadores

import comvest.clear_dados.limpeza_dados as limpeza_dados_comvest
from comvest.clear_dados import cod_ibge, cod_inep, ids_nomes
from comvest.clear_perfil import limpeza_perfil
import comvest.escolas.__main__ as escolas
from comvest.clear_notas import limpeza_notas, presenca

import comvest.extract.merge_sheets as merge_sheets
import comvest.assign_ids.comvest_ids as comvest_ids
import comvest.extract_cities.__main__ as extrair_cidades
import comvest.extract_courses.__main__ as extrair_cursos
import comvest.extract_enrolled.__main__ as extrair_enrolled

from rais.id_generation import cpf_verification
from rais.id_generation import recover_cpf_dac_comvest
from rais.id_generation import random_index
from rais.pre_processing import identification
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


def main():
    rodar_base_inteira()


def rodar_base_inteira():
    print(1)
    merge_sheets.merge()
    print(2)
    comvest_ids.assign_ids()
    print(3)
    identificadores.create_ids()
    print(4)


def dummy():
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

    # Pre processamento rais
    identification.get_identification_from_all_years()
    # Geracao ids
    cpf_verification.remove_invalid_cpf()
    recover_cpf_dac_comvest.recover_cpf_dac_comvest()
    random_index.generate_index()

    # Merge rais com ids
    merge.merge_all_years()
    recover_cpf_rais.recover_cpf_all_years()
    clear.clear_all_years()

    clear_socio.clear_socio()
    merge_socio.merge_socio_dac_comvest()

    clean_capes.clean_capes()
    merge_capes.extract_ids()

    extract_unesp()
    extract_fuvest()

    extract_empresa_amostra()
    extract_estabelecimento_amostra()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    main()
