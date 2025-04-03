import logging
import sys
import os


# Adiciona o diretório raiz do projeto ao PYTHONPATH
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


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

# ENEM -=-=-=-=-=-=-=-=-=-=-=-=-=-
from enem.comvest_enem import clear_comvest 
from enem.comvest_enem import divide_comvest
from enem.comvest_enem import comvest_enem
from enem.comvest_enem import comvest_vest_ids
from enem.comvest_enem import comvest_enem_ids

# DIPLOMADOS -=-=-=-=-=-=-=-=-=-=-=-=-=-
from diplomas.extract_usp import scrapper 
from diplomas.extract_usp import comvest_diplomasUSP


# RAIS -=-=-=-=-=-=-=-=-=-=-=-=-=-
from rais.id_generation import cpf_verification
from rais.id_generation import recover_cpf_dac_comvest
from rais.id_generation import random_index
from rais.pre_processing.__main__ import pre_process_data as pre_process_rais
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

# Configurando o logger com o nome "main"
logger = logging.getLogger("main")

# O nível de log padrão é INFO, então só serão exibidas mensagens de INFO ou superior
# Acima de INFO temos WARNING, ERROR e CRITICAL
logger.setLevel("INFO") 

# Configurando o logger para escrever em um arquivo
fh = logging.FileHandler("main2.log")

# Adicionando o handler ao logger
logger.addHandler(fh)

def main():
    d = {1: "limitada", 2: "completa"}
    while True:
        socios_in = int(
            input(
                "Digite 1 para realizar a extração limitada da base sócios ou 2 para a extração completa:"
            )
        )
        if socios_in != 1 and socios_in != 2:
            print("Entrada inválida, digite novamente.")
        else:
            tipo_extracao_socios = d[socios_in]
            break

    # # Pre-processamento COMVEST
    # logger.info("Iniciando o pré-processamento de dados da COMVEST")
    # extrair_cidades.extraction()
    # extrair_cursos.extraction()
    # dict_cursos.get()
    # extrair_matriculados.extraction()
    # extrair_convocados.extraction()
    # limpeza_dados_comvest.extraction()


    # # Pre-processamento DAC
    # logger.info("Iniciando o pré-processamento de dados da DAC")
    # setup_dados.load_dados_cadastais()
    # ufs_codes.generate_clean_data()
    # create_ids.create_ids()
    # limpeza_dados_dac.generate_clean_data()
    # uf_codes.generate_uf_code()

    # print("pre processamento enem")
    # # Pre processamento enem
    # logger.info("Iniciando o pré-processamento de dados do ENEM")
    # clear_comvest.clean_all()
    # divide_comvest.split_all()


    # # Base da COMVEST
    # logger.info("Iniciando a geração de bases da COMVEST")
    # cod_ibge.merge()
    # validacao_esc.validation()
    # # Gera códigos das escolas na DAC
    # school_codes.generate_school_codes()
    # logger.info("Iniciando o merge de códigos INEP")
    # cod_inep.merge()
    # ids_nomes.merge()
    # logger.info("Iniciando a limpeza de perfil e notas")
    # limpeza_perfil.extraction()
    # limpeza_notas.extraction()
    # presenca.get()

    # print("merge enem")
    # # Merge Enem Data
    # logger.info("Iniciando o merge de dados do ENEM")
    # comvest_enem.merge()

    # # Base da DAC
    # logger.info("Iniciando a geração de bases da DAC")
    # historico_escolar.generate_clean_data()
    # resumo_por_periodo.generate_clean_data()
    # resumo_periodo_cr.generate_cr()
    # vida_academica.generate_clean_data()
    # dados_ingressantes.generate()
    # habilitacao.generate()
    # uniao_dac_comvest.generate()

    
    # # Pre processamento rais
    # logger.info("Iniciando o pré-processamento de dados da RAIS")
    # pre_process_rais()

    # # Geracao ids
    # logger.info("Iniciando a geração de ids")
    logger.info("Remove CPFs inválidos")
    cpf_verification.remove_invalid_cpf()
    logger.info("Finalizado - Remove CPFs inválidos")
    logger.info("Recupera CPFs DAC e COMVEST")
    recover_cpf_dac_comvest.recover_cpf_dac_comvest()
    logger.info("Finalizado - Recupera CPFs DAC e COMVEST")
    logger.info("Gera índices aleatórios")
    random_index.generate_index()
    logger.info("Finalizado - Gera índices aleatórios")

    # Processamento Diplomados
    logger.info("Iniciando o pré-processamento de dados de Diplomados")
    scrapper.proccess_usp()
    comvest_diplomasUSP.merge()

    print("retrieve enem ids")
    # Merge ENEM com ids
    logger.info("Iniciando o merge de ids do ENEM")
    comvest_vest_ids.retrieve()
    comvest_enem_ids.merge()

    # Merge rais com ids
    logger.info("Iniciando o merge de ids da RAIS")
    merge.merge_all_years()
    recover_cpf_rais.recover_cpf_years()
    clear.clear_all_years()
    
    logger.info("Iniciando a limpeza de dados da base sócios")
    clear_socio.clear_socio()
    logger.info("Iniciando o merge de dados da base sócios com DAC_COMVEST")
    merge_socio.merge_socio_dac_comvest(tipo_extracao_socios)
    
    logger.info("Iniciando a limpeza de dados da base CAPES")
    clean_capes.clean_capes()
    logger.info("Iniciando o merge de dados da base CAPES com DAC_COMVEST")
    merge_capes.extract_ids()
    
    logger.info("Iniciando a extração de dados da base UNESP")
    extract_unesp()
    extract_fuvest()
    logger.info("Iniciando a extração de dados da base fuvest")

    logger.info("Iniciando a extração de dados da base empresa")
    extract_empresa_amostra()
    extract_estabelecimento_amostra()
    extract_simples_amostra()

    logger.info("Iniciando a atribuição de ids para DAC e COMVEST")
    # Atribuição de ids para DAC e COMVEST
    merge_sheets.merge()
    comvest_ids.assign_ids()
    identificadores.create_ids()

    logger.info("Extração de dados finalizada com sucesso!")


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    main()
