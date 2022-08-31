from dac.clr_vida_academica_habilitacao import cursos_habilitacoes
from dac.clr_vida_academica_habilitacao import vida_academica_habilitacao
from dac.utilities.io import write_output
from dac.utilities.io import write_result
from dac.utilities.io import read_result
from dac.create_ufs_codes.dac import generate_mun_dac
from dac.create_ufs_codes.dados_ibge import get_ibge_data
from dac.create_ufs_codes.dados_ibge import get_ibge_data_dict
from dac.create_ufs_codes.comvest import generate_mun_comvest
from dac.create_ufs_codes.utility_mun import get_the_closest_matche
from dac.create_ufs_codes.utility_mun import merge_by_uf
from dac.create_ufs_codes.utility_mun import concat_and_drop_duplicates
from dac.create_ufs_codes.utility_mun import key_merge
from dac.create_ufs_codes.utility_mun import create_key_for_merge
from dac.create_ufs_codes.utility_mun import padronize_string
from dac.create_ufs_codes.utility_mun import create_concat_key_for_merge
from dac.create_ufs_codes.utility_mun import CODE_UF_EQUIV
from dac.create_ufs_codes.new_ufs_codes import inicio
import re
import pandas as pd
import numpy as np
pd.options.mode.chained_assignment = None


def main():
    #comvest_dict = generate_mun_comvest()
    inicio()

    return
    concat_mun = generate_mun_dac_comvest()
    ibge_data = get_ibge_data()
    create_key_for_merge(ibge_data)
    
    all_counties_comvest = read_result('comvest_counties_df.csv')

    right_merge_df = null_filter(all_counties_comvest, 2)
    atribute_exact_matches(right_merge_df)    
    wrong_merge_df = null_filter(all_counties_comvest, pd.NA, False)
    wrong_merge_df = clear_wrong_merge_df(wrong_merge_df)
    
    ufs = list(CODE_UF_EQUIV.values())
    uf_filter = wrong_merge_df['uf'].isin(ufs)

    valid_uf = wrong_merge_df[uf_filter]
    valid_uf_with_trust = atribute_trust(valid_uf, 3, 0.85, ibge_data)
    
    invalid_uf = wrong_merge_df[~uf_filter]
    invalid_uf_with_trust = atribute_trust(valid_uf, 4, 0.95, ibge_data)

    dac_counties_df = read_result('dac_counties_df.csv')
    match_results = concat_and_drop_duplicates([right_merge_df, valid_uf_with_trust, invalid_uf_with_trust, dac_counties_df])
    write_result(match_results, 'counties_code.csv')


def atribute_trust(df, trust, cutoff, ibge_data):
    merged_valid_df = key_merge(df, ibge_data, cutoff)
    valid_match = null_filter(merged_valid_df, trust)
    valid_match.drop_duplicates(subset=['municipio_y'], keep=False, inplace=True)
    no_valid_match = null_filter(merged_valid_df, pd.NA, False)
    no_valid_match.drop_duplicates(subset=['municipio_y'], keep=False, inplace=True)
    concat = pd.concat([valid_match, no_valid_match], ignore_index=True)
    return concat


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
 
def generate_mun_dac_comvest():
    comvest_dict = generate_mun_comvest()
    dac_dict = generate_mun_dac()
    ibge_data = get_ibge_data()
    ibge_data_dict = get_ibge_data_dict()

    merged_dac_df = merge_by_uf(dac_dict, ibge_data, ibge_data_dict)

    right_dac = null_filter(merged_dac_df, 2)
    atribute_exact_matches(right_dac)
    wrong_dac = null_filter(merged_dac_df, pd.NA, False)
    
    merged_dac_df = concat_and_drop_duplicates([right_dac, wrong_dac])

    write_result(merged_dac_df, 'dac_counties_df.csv')
    merged_comvest_df = merge_by_uf(comvest_dict, ibge_data, ibge_data_dict)
    write_result(merged_comvest_df, 'comvest_counties_df.csv')


def atribute_exact_matches(df):
    df['mun_a'] = df['municipio_x'].astype(str).map(lambda x: padronize_string(x))
    df['mun_b'] = df['municipio_y'].astype(str).map(lambda x: padronize_string(x))
    df['confianca'][df['mun_a'] == df['mun_b']] = 1
    df.drop(['mun_a', 'mun_b'], axis=1, inplace=True)


if __name__ == '__main__':
    main()