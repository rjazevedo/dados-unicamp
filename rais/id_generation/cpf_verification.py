import pandas as pd
from difflib import SequenceMatcher

from rais.utilities.read import read_dac_comvest
from rais.utilities.read import read_rais_identification
from rais.utilities.write import write_dac_comvest_valid
from rais.utilities.file import create_folder_inside_year
from rais.utilities.file import get_all_tmp_files

from rais.utilities.logging import log_remove_invalid_cpf

def remove_invalid_cpf():
    log_remove_invalid_cpf()
    df_dac_comvest = read_dac_comvest()
    df_dac_comvest_merge = prepare_dac_comvest(df_dac_comvest)
    df_result = merge_by_cpf(df_dac_comvest_merge)
    df_result = get_invalid_cpf(df_result)
    df_result = change_invalid_cpf(df_dac_comvest, df_result)
    write_dac_comvest_valid(df_result)

def prepare_dac_comvest(df):
    df = df[df['cpf'] != '-']
    df.drop_duplicates(subset=['cpf'], inplace=True)
    df.rename(columns={'cpf': 'cpf_r'}, inplace=True)
    return df

def merge_by_cpf(df_dac_comvest):
    dfs = []
    for year in range(2002, 2019):
        df = merge_year(df_dac_comvest, year)
        dfs.append(df)
    df_result = pd.concat(dfs, sort=False)
    return df_result

# Merge rais from year with df_dac_comvest
def merge_year(df_dac_comvest, year):
    files = get_all_tmp_files(year, 'identification_data', 'pkl')
    dfs = []
    for file_rais in files:
        df_rais = read_rais_identification(file_rais)
        df = merge_dfs(df_rais, df_dac_comvest)
        dfs.append(df)

    df_result = pd.concat(dfs, sort=False)
    return df_result

# Merge rais df with dac/comvest df and remove invalid cpfs
def merge_dfs(df_rais, df_dac_comvest):
    result = df_rais.merge(df_dac_comvest)
    return result

def get_invalid_cpf(df):
    df['is_same_person'] = df.apply(lambda x: is_same_person(x['nome_r'], x['nome']), axis=1)
    df_same_person = df[df['is_same_person'] == True]
    df_not_same_person = df[df['is_same_person'] == False]
    df_total = pd.concat([df_same_person, df_not_same_person], sort=True)
    df_total.drop_duplicates(subset=['cpf_r'], keep='first', inplace=True)
    df_cpf_invalid = df_total[df_total['is_same_person'] == False]
    df_cpf_invalid = df_cpf_invalid.loc[:,['cpf_r']]
    df_cpf_invalid.rename(columns={'cpf_r': 'cpf'}, inplace=True)
    return df_cpf_invalid

# Says if person_a is person_b based on the probabilistic match between the two first names
def is_same_person(name_a, name_b):
    first_name_a = name_a.split()[0].split('.')[0].split('-')[0]
    first_name_b = name_b.split()[0].split('.')[0].split('-')[0]
    similar_rate = SequenceMatcher(None, first_name_a, first_name_b).ratio()
    return similar_rate > 0.7

def change_invalid_cpf(df_dac_comvest, df_cpf_invalid):
    df_cpf_invalid['invalid'] = True
    result = df_dac_comvest.merge(df_cpf_invalid, how='left')
    result = result.fillna({'invalid': False})
    result['cpf'] = result.apply(lambda x: get_cpf(x['cpf'], x['invalid']), axis=1)
    del result['invalid']
    return result

def get_cpf(cpf, is_invalid):
    if is_invalid:
        return '-'
    return cpf
