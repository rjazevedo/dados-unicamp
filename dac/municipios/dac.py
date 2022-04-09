from dac.utilities.columns import dados_cadastrais_cols
from dac.utilities.io import read_from_database
from dac.utilities.io import write_output
from dac.municipios.comvest import concat_and_drop_duplicates
import pandas as pd

def generate_mun_dac():
    dados_cadastrais = read_from_database('DadosCadastraisAluno.xlsx')
    
    dados_cadastrais.columns = dados_cadastrais_cols
    mun_nasc = extract_mun_and_uf(dados_cadastrais, ['mun_nasc_d', 'uf_nasc_d', 'cod_pais_nascimento'])
    mun_esc_form_em = extract_mun_and_uf(dados_cadastrais, ['mun_esc_form_em', 'uf_esc_form_em', 'sigla_pais_esc_form_em'])

    #TODO: Tratar essas colunas sem uf, atrávez do cpf
    #no_uf = dados_cadastrais[['mun_atual', 'mun_resid_d']]
    
    result = concat_and_drop_duplicates([mun_nasc, mun_esc_form_em])
    return result

def extract_mun_and_uf(df, columns):
    mun_and_uf = df[columns]
    mun_and_uf.columns = ['municipio', 'uf', 'pais']
    mun_and_uf = mun_and_uf[mun_and_uf['pais'] == 'BR']
    mun_and_uf.pop('pais')
    return mun_and_uf