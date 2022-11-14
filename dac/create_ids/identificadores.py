from dac.utilities.io import read_result
from dac.utilities.io import write_result
from dac.utilities.io import read_from_external
from dac.utilities.io import write_output
import pandas as pd

def replicate_ids_dac():
    ids = read_from_external('dac_comvest_ids.csv', dtype=str).loc[:, ["id", "identif"]]
    ids = ids.drop_duplicates(subset=["id", "identif"])

    dados_cadastrais = read_result('dados_cadastrais.csv')
    vida_academica = read_result('vida_academica.csv')
    vida_academica_habilitacao = read_result('vida_academica_habilitacao.csv', dtype=str)
    historico_escolar = read_result('historico_escolar_aluno.csv')
    resumo_por_periodo = read_result('resumo_periodo_cr.csv')

    dados_cadastrais["identif"] = dados_cadastrais["identif"].astype(str)
    dados_cadastrais = pd.merge(dados_cadastrais, ids, on=["identif"], how="left").drop(['insc_vest','identif', 'cpf', 'doc', 'nome','dta_nasc', 'origem', "ano_ingresso_curso"], axis=1, errors='ignore')
    
    vida_academica["identif"] = vida_academica["identif"].astype(str)
    vida_academica = pd.merge(vida_academica, ids, on=["identif"], how="left").drop(['insc_vest','identif', 'origem'], axis=1, errors='ignore')
    
    vida_academica_habilitacao["identif"] = vida_academica_habilitacao["identif"].astype(str)
    vida_academica_habilitacao = pd.merge(vida_academica_habilitacao, ids, on=["identif"], how="left").drop(['identif'], axis=1, errors='ignore')
    
    historico_escolar["identif"] = historico_escolar["identif"].astype(str)
    historico_escolar = pd.merge(historico_escolar, ids, on=["identif"], how="left").drop(['insc_vest','identif'], axis=1, errors='ignore')
    
    resumo_por_periodo["identif"] = resumo_por_periodo["identif"].astype(str)
    resumo_por_periodo = pd.merge(resumo_por_periodo, ids, on=["identif"], how="left").drop(['insc_vest','identif'], axis=1, errors='ignore')

    write_output(dados_cadastrais, 'dados_cadastrais.csv')
    write_output(vida_academica, 'vida_academica.csv')
    write_output(vida_academica_habilitacao, 'vida_academica_habilitacao.csv')
    write_output(historico_escolar, 'historico_escolar.csv')
    write_output(resumo_por_periodo, 'resumo_por_periodo.csv')