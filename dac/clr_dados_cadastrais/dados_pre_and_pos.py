from dac.utilities.columns import dados_cadastrais_cols
from dac.utilities.io import read_input
from dac.utilities.io import write_result
from dac.utilities.format import padronize_string_miss
from dac.utilities.io import Bases
import pandas as pd
import numpy as np

PRE_99_BASE_NAME = 'Rodolfo_Complementacao.xlsx'
POS_99_BASE_NAME = 'Rodolfo_DadosCadastraisAluno.xlsx'
DADOS_SHEET_NAME = 'Dados Cadastrais'

def load_dados_cadastais():
    dados_cadastrais_pre_99 = read_input(PRE_99_BASE_NAME, base=Bases.DAC, sheet_name=DADOS_SHEET_NAME, names=dados_cadastrais_cols)
    dados_cadastrais_pos_99 = read_input(POS_99_BASE_NAME, base=Bases.DAC, names=dados_cadastrais_cols)
    dados_cadastrais = pd.concat([dados_cadastrais_pre_99, dados_cadastrais_pos_99])
    dados_cadastrais = clear_dados_cadastrais_pre_99(dados_cadastrais)
    write_result(dados_cadastrais, "dados_cadastrais_intermediario.csv")


# Limpa erros na tabela pré 99 vistos empiricamente
def clear_dados_cadastrais_pre_99(df):
    ceps_colums = ['cep_nasc', 'cep_resid_d', 'cep_escola_em', 'cep_atual']
    null_colums = ['uf_nasc_d', 'escola_em_d', 'uf_esc_form_em', 'mun_esc_form_em', 'sigla_pais_esc_form_em', 'pais_esc_form_em', 'naturalizado', 'mun_atual', 'mun_resid_d','cep_nasc', 'cep_resid_d', 'cep_escola_em', 'cep_atual']
    padronize_string_miss(df, [null_colums], '<null>')
    df[ceps_colums] = df[ceps_colums].replace('',np.nan).astype(float)

    df['dta_nasc'] = df['dta_nasc'].astype(str)
    df['dta_nasc'] = pd.to_datetime(df['dta_nasc'], errors='coerce', format= '%Y-%m-%d')
    df['ano_conclu_em'] = df['ano_conclu_em'].astype(str)
    df['ano_conclu_em'] = pd.to_datetime(df['ano_conclu_em'], errors='coerce', format= '%Y-%m-%d')
    return df