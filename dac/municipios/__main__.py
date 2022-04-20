from dac.clr_vida_academica_habilitacao import cursos_habilitacoes
from dac.clr_vida_academica_habilitacao import vida_academica_habilitacao

from dac.utilities.io import write_output
from dac.utilities.io import write_result
from dac.utilities.io import read_result

from dac.municipios.dac import generate_mun_dac
from dac.municipios.dados_ibge import get_ibge_data
from dac.municipios.dados_ibge import get_ibge_data_dict

from dac.municipios.comvest import generate_mun_comvest

from dac.municipios.utility_mun import get_the_closest_matche
from dac.municipios.utility_mun import merge_by_uf
from dac.municipios.utility_mun import concat_and_drop_duplicates

import pandas as pd

def main():
    #concat_mun = generate_mun_dac_comvest()
    
    #-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    clear_comvest = read_result('merged_comvest_municipios.csv')
    filtro = merged_comvest_df['codigo_municipio'].isnull()
    df_correto = merged_comvest_df[~filtro]
    df_errado = merged_comvest_df[filtro]

    write_output(df_correto, 'municipios_certos.csv')
    write_output(df_errado, 'municipios_errados.csv')

def generate_mun_dac_comvest():
    comvest_dict = generate_mun_comvest()
    dac_dict = generate_mun_dac()
    ibge_data = get_ibge_data()
    ibge_data_dict = get_ibge_data_dict()
    merged_dac_df = merge_by_uf(dac_dict, ibge_data, ibge_data_dict)
    merged_comvest_df = merge_by_uf(comvest_dict, ibge_data, ibge_data_dict)
    concat_data = concat_and_drop_duplicates([dac_data, comvest_data])
    #merged_dac_df.drop(['uf_codigo', 'municipio'], axis='columns', inplace=True)
    return concat_data


if __name__ == '__main__':
    main()