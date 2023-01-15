import pandas as pd
from dac.utilities.io import write_result
import unidecode
from dac.create_ufs_codes.comvest import generate_comvest
from dac.create_ufs_codes.dac import generate_dac
from dac.create_ufs_codes.dados_ibge import generate_ibge_data
from dac.create_ufs_codes.utilities import concat_and_drop_duplicates
from dac.create_ufs_codes.merges import probabilist_merge_by_counties
from dac.create_ufs_codes.merges import probabilist_merge_by_concat_key
from dac.create_ufs_codes.merges import probabilist_merge
from dac.create_ufs_codes.merges import perfect_merge

def generate_clean_data():
    counties = setup_conties()
    ibge_data = generate_ibge_data()
    correct_list = []
    
    wrong = perfect_merge(counties, ibge_data, correct_list)
    wrong = probabilist_merge(wrong, ibge_data, correct_list)
    wrong = probabilist_merge_by_concat_key(wrong, ibge_data, correct_list)
    probabilist_merge_by_counties(wrong, ibge_data, correct_list)
    
    final_df = concat_and_drop_duplicates(correct_list)
    final_df = final_df.drop(['key'], axis=1)

    final_df = padronize_final_columns(final_df, "municipio_ibge")
    final_df = padronize_final_columns(final_df, "nome_uf")
    write_result(final_df, "final_counties.csv")


def setup_conties():
    comvest = generate_comvest()
    dac = generate_dac()
    result = concat_and_drop_duplicates([comvest, dac])
    return result


def padronize_final_columns(df, column):
    df[column] = df[column].fillna("")
    df[column] = df[column].astype("string")
    df[column] = df[column].apply(unidecode.unidecode)
    df[column] = df[column].str.upper()
    return df