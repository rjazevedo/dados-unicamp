from dac.utilities.io import read_result
from dac.utilities.io import write_result
from dac.utilities.io import write_output
from dac.utilities.io import Bases
import pandas as pd

DADOS_CADASTRAIS = 'dados_cadastrais.csv'
VIDA_ACADEMICA = 'vida_academica.csv'
VIDA_ACADEMICA_HABILITACAO = 'vida_academica_habilitacao.csv'
HISTORICO_ESCOLAR = 'historico_escolar_aluno.csv'
RESUMO_POR_PERIODO = 'resumo_periodo_cr.csv'
DAC_COMVEST_IDS = 'dac_comvest_ids.csv'


def create_ids():
    ids = read_result(DAC_COMVEST_IDS, base=Bases.RESULT_RAIS, dtype=str).loc[:, ["id", "identif"]]    
    ids = ids.drop_duplicates(subset=["id", "identif"])

    dados_cadastrais = read_result(DADOS_CADASTRAIS)
    vida_academica = read_result(VIDA_ACADEMICA)
    #vida_academica_habilitacao = read_result(VIDA_ACADEMICA_HABILITACAO, dtype=str)
    historico_escolar = read_result(HISTORICO_ESCOLAR)
    resumo_por_periodo = read_result(RESUMO_POR_PERIODO)

    dados_cadastrais["identif"] = dados_cadastrais["identif"].astype(str)
    dados_cadastrais = pd.merge(dados_cadastrais, ids, on=["identif"], how="left").drop(['insc_vest','identif', 'cpf', 'doc', 'nome','dta_nasc', 'origem', "ano_ingresso_curso"], axis=1, errors='ignore')
    
    vida_academica["identif"] = vida_academica["identif"].astype(str)
    vida_academica = pd.merge(vida_academica, ids, on=["identif"], how="left").drop(['insc_vest','identif', 'origem'], axis=1, errors='ignore')
    
    #vida_academica_habilitacao["identif"] = vida_academica_habilitacao["identif"].astype(str)
    #vida_academica_habilitacao = pd.merge(vida_academica_habilitacao, ids, on=["identif"], how="left").drop(['identif'], axis=1, errors='ignore')
    
    historico_escolar["identif"] = historico_escolar["identif"].astype(str)
    historico_escolar = pd.merge(historico_escolar, ids, on=["identif"], how="left").drop(['insc_vest','identif'], axis=1, errors='ignore')
    
    resumo_por_periodo["identif"] = resumo_por_periodo["identif"].astype(str)
    resumo_por_periodo = pd.merge(resumo_por_periodo, ids, on=["identif"], how="left").drop(['insc_vest','identif'], axis=1, errors='ignore')

    write_output(dados_cadastrais, DADOS_CADASTRAIS)
    write_output(vida_academica, VIDA_ACADEMICA)
    #write_output(vida_academica_habilitacao, VIDA_ACADEMICA_HABILITACAO)
    write_output(historico_escolar, HISTORICO_ESCOLAR)
    write_output(resumo_por_periodo, RESUMO_POR_PERIODO)