from dac.utilities.columns import dados_cadastrais_cols
from dac.utilities.io import read_result
from dac.create_ufs_codes.utilities import extract_mun_and_uf
from dac.create_ufs_codes.utilities import concat_and_drop_duplicates
import pandas as pd
import re

DADOS_CADASTRAIS = "dados_cadastrais_intermediario.csv"

def generate_dac():
    dados_cadastrais = read_result(DADOS_CADASTRAIS)
    mun_nasc = extract_mun_and_uf(dados_cadastrais, ['mun_nasc_d', 'uf_nasc_d', 'cod_pais_nascimento'])
    mun_esc_form_em = extract_mun_and_uf(dados_cadastrais, ['mun_esc_form_em', 'uf_esc_form_em', 'sigla_pais_esc_form_em'])
    result = concat_and_drop_duplicates([mun_nasc, mun_esc_form_em])
    return result