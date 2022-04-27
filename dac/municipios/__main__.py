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
from dac.municipios.utility_mun import key_merge
from dac.municipios.utility_mun import create_key_for_merge
from dac.municipios.utility_mun import create_concat_key_for_merge
from dac.municipios.utility_mun import CODE_UF_EQUIV
import re
import pandas as pd
import numpy as np
pd.options.mode.chained_assignment = None

def main():
    concat_mun = generate_mun_dac_comvest()
    ibge_data = get_ibge_data()
    create_key_for_merge(ibge_data)
    
    all_counties_comvest = read_result('comvest_counties_df.csv')

    right_merge_df = null_filter(all_counties_comvest, 'alta')
    wrong_merge_df = null_filter(all_counties_comvest, '', False)
    wrong_merge_df = clear_wrong_merge_df(wrong_merge_df)
    
    ufs = list(CODE_UF_EQUIV.values())
    uf_filter = wrong_merge_df['uf'].isin(ufs)

    valid_uf = wrong_merge_df[uf_filter]
    merged_valid_df = key_merge(valid_uf, ibge_data, 0.85)
    valid_match = null_filter(merged_valid_df, 'media')
    no_valid_match = null_filter(merged_valid_df, '', False)
    
    invalid_uf = wrong_merge_df[~uf_filter]
    merged_invalid_df = key_merge(invalid_uf, ibge_data, 0.95)
    match_invalid_uf = null_filter(merged_invalid_df, 'baixa')
    no_match_invalid_uf = null_filter(merged_invalid_df, '', False)

    dac_counties_df = read_result('dac_counties_df.csv')
    match_results = concat_and_drop_duplicates([right_merge_df, valid_match, no_valid_match, match_invalid_uf ,no_match_invalid_uf, dac_counties_df])
    write_output(match_results, 'final_counties.csv')
    
def null_filter(df, trust='', complement=True):
    filtro = df['codigo_municipio'].isnull()
    if complement:
        df_correto = df[~filtro]
        df_correto['confianca'] = trust
        return df_correto
    else:
        df_correto = df[filtro]
        df_correto['confianca'] = ''
        return df_correto

def clear_typos_comvest_uf(df):
    df['uf'] = df['uf'].fillna('')
    df['uf'] = df['uf'].astype(str).replace(['0', 'NAN'], '', regex=True).astype("string")
    df['uf'].map(lambda x: "".join(re.findall("[a-zA-Z]+", x)))
    return df

def clear_wrong_merge_df(df):
    df = df[['municipio_x', 'uf_x']]
    df.columns = ['municipio', 'uf']
    df = clear_typos_comvest_uf(df)
    create_key_for_merge(df)
    return df

#TODO: Mudar o nome dos csvs dos municípios 
def generate_mun_dac_comvest():
    comvest_dict = generate_mun_comvest()
    dac_dict = generate_mun_dac()
    ibge_data = get_ibge_data()
    ibge_data_dict = get_ibge_data_dict()
    merged_dac_df = merge_by_uf(dac_dict, ibge_data, ibge_data_dict)
    write_result(merged_dac_df, 'dac_counties_df.csv')
    merged_comvest_df = merge_by_uf(comvest_dict, ibge_data, ibge_data_dict)
    write_result(merged_comvest_df, 'comvest_counties_df.csv')

if __name__ == '__main__':
    main()