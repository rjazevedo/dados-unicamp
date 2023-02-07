import pandas as pd
from dac.utilities.io import read_result
from dac.utilities.io import write_result
from dac.utilities.columns import dados_cadastrais_final_cols

UF_CODE_NAME = 'final_counties.csv'
RESULT = "dados_cadastrais_com_uf.csv"
DADOS_CADASTRAIS = "dados_cadastrais.csv"

# Atribui os códigos das ufs presentes na tabela
def generate_uf_code():
    dados_cadastrais = read_result(DADOS_CADASTRAIS) 
    final_counties = read_result(UF_CODE_NAME)

    final_counties = final_counties[['municipio', 'uf', 'codigo_municipio', 'confianca', 'municipio_ibge', 'uf_ibge']]
    final_counties = final_counties.drop_duplicates(['municipio', 'uf'])

    final_counties.columns = ['mun_nasc_d', 'uf_nasc_d', 'cod_mun_nasc_d', 'origem_cod_mun_nasc_d', 'mun_nasc_ibge', 'uf_nasc_ibge']
    mun_nasc_d_merge = pd.merge(dados_cadastrais, final_counties, how='left')

    final_counties.columns = ['mun_esc_form_em', 'uf_esc_form_em', 'cod_mun_form_em', 'origem_cod_mun_form_em', 'mun_esc_form_em_ibge', 'uf_esc_form_em_ibge']
    mun_nasc_d_merge = pd.merge(mun_nasc_d_merge, final_counties, how='left')
    
    mun_nasc_d_merge = mun_nasc_d_merge.reindex(columns= dados_cadastrais_final_cols)
    write_result(mun_nasc_d_merge, RESULT)