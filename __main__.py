import logging

# COMVEST -=-=-=-=-=-=-=-=-=-=-=-
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

# DAC -=-=-=-=-=-=-=-=-=-=-=-=-=-
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

# RAIS -=-=-=-=-=-=-=-=-=-=-=-=-=-
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

from simples.extract import extract_simples_amostra


def main():
    # Pre-processamento COMVEST
    extrair_cidades.extraction()
    extrair_cursos.extraction()
    dict_cursos.get()
    extrair_matriculados.extraction()
    extrair_convocados.extraction()
    limpeza_dados_comvest.extraction()

    # Pre-processamento DAC
    setup_dados.load_dados_cadastais()
    ufs_codes.generate_clean_data()
    create_ids.create_ids()
    limpeza_dados_dac.generate_clean_data()
    uf_codes.generate_uf_code()

    # Base da COMVEST
    cod_ibge.merge()
    validacao_esc.validation()
    # Gera códigos das escolas na DAC
    school_codes.generate_school_codes()
    cod_inep.merge()
    ids_nomes.merge()
    limpeza_perfil.extraction()
    limpeza_notas.extraction()
    presenca.get()

    # Base da DAC
    historico_escolar.generate_clean_data()
    resumo_por_periodo.generate_clean_data()
    resumo_periodo_cr.generate_cr()
    vida_academica.generate_clean_data()
    dados_ingressantes.generate()
    habilitacao.generate()
    uniao_dac_comvest.generate()

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
    extract_simples_amostra()

    # Atribuição de ids para DAC e COMVEST
    merge_sheets.merge()
    comvest_ids.assign_ids()
    identificadores.create_ids()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    main()
