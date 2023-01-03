from dac.utilities.columns import dados_cadastrais_cols
from dac.utilities.io import read_from_database
from dac.clr_dados_cadastrais.dados_cadastrais import clear_dados_cadastrais_pre_99
from dac.create_ufs_codes.utilities import extract_mun_and_uf
from dac.create_ufs_codes.utilities import concat_and_drop_duplicates
from dac.create_ufs_codes.utilities import CODE_UF_EQUIV
import pandas as pd
import re

PRE_99_BASE_NAME = 'Rodolfo_Complementacao.xlsx'
POS_99_BASE_NAME = 'DadosCadastraisAluno.xlsx'
DADOS_SHEET_NAME = 'Dados Cadastrais'

def generate_dac():
    dados_cadastrais_pre_99 = read_from_database(PRE_99_BASE_NAME, sheet_name=DADOS_SHEET_NAME, names=dados_cadastrais_cols)
    dados_cadastrais_pos_99 = read_from_database(POS_99_BASE_NAME, names=dados_cadastrais_cols)
   
    dados_cadastrais = pd.concat([dados_cadastrais_pre_99, dados_cadastrais_pos_99])
    dados_cadastrais = clear_dados_cadastrais_pre_99(dados_cadastrais)
    
    mun_nasc = extract_mun_and_uf(dados_cadastrais, ['mun_nasc_d', 'uf_nasc_d', 'cod_pais_nascimento'])
    mun_esc_form_em = extract_mun_and_uf(dados_cadastrais, ['mun_esc_form_em', 'uf_esc_form_em', 'sigla_pais_esc_form_em'])
    result = concat_and_drop_duplicates([mun_nasc, mun_esc_form_em])
    return result