import clean_module.file
import clean_module.dtypes
import pandas as pd
from difflib import SequenceMatcher

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

def remove_invalid_cpf(path, file):
    dtype = clean_module.dtypes.get_dtype_dac_comvest()
    df = pd.read_csv(file, sep=',', encoding='latin', dtype=dtype)
    df_dac_comvest = read_file_dac_comvest(df)

    df_result = merge_all_years(df_dac_comvest, path)
    df_result = get_invalid_cpf(df_result)
    df_result = change_invalid_cpf(df, df_result)

    file_out = path + 'dac_comvest_valid.csv'
    clean_module.file.to_csv(df_result, file_out)

def read_file_dac_comvest(df):
    df = df[df['cpf'] != '-']
    df.drop_duplicates(subset=['cpf'], inplace=True)
    df.rename(columns={'cpf': 'cpf_r'}, inplace=True)
    return df

def merge_all_years(df_dac_comvest, path):
    dfs = []
    for year in range(2002, 2019):
        path_year = clean_module.file.get_year_path(year, path)
        clean_module.file.create_folder(path_year, 'rais_dac_comvest')
        df = merge_year(df_dac_comvest, path_year)
        dfs.append(df)
    df_result = pd.concat(dfs, sort=False)
    return df_result

# Merge rais from year with df_dac_comvest and save in files in rais_dac_comvest directory
def merge_year(df_dac_comvest, path):
    path_folder = path + 'identification_data/'
    files = clean_module.file.get_all_files(path_folder, 'pkl')

    dfs = []
    for file_rais in files:
        print(file_rais)
        df_rais = clean_module.merge.read_file_rais(file_rais)
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
