import pandas as pd
from comvest.utilities.io import read_result, read_output, write_result
from comvest.utilities.dtypes import DTYPES_DADOS


def validation():
    dados = read_result('dados_comvest.csv', DTYPES_DADOS)
    tabela_mun = read_output('final_counties.csv')

    tabela_mun = tabela_mun[['municipio_x', 'uf_y', 'codigo_municipio']]
    tabela_mun = tabela_mun.drop_duplicates(['municipio_x', 'uf_y'])

    tabela_mun.columns = ['mun_nasc_c', 'uf_nasc_c', 'cod_mun_nasc_c']
    dados = pd.merge(dados, tabela_mun, how='left')

    tabela_mun.columns = ['mun_resid_c', 'uf_resid', 'cod_mun_resid_c']
    dados = pd.merge(dados, tabela_mun, how='left')

    tabela_mun.columns = ['mun_esc_em_c', 'uf_esc_em', 'cod_mun_esc_em_c']
    dados = pd.merge(dados, tabela_mun, how='left')

    write_result(dados, 'dados_comvest.csv')