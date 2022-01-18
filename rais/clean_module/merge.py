import pandas as pd
import clean_module.file
import clean_module.dtypes
import clean_module.recover_cpf_rais
from difflib import SequenceMatcher

#------------------------------------------------------------------------------------------------
# Merge dac/comvest union with all rais files to create a database in rais only with people of interest
def merge_rais_dac_comvest(path):
    merge_all_years(path)
    clean_module.recover_cpf_rais.recover_cpf_all_years(path)
    check_is_in_rais(path)

#------------------------------------------------------------------------------------------------
# Merge all the years from rais with uniao_dac_comvest and save in file rais.csv
def merge_all_years(path):
    file_dac_comvest = path + 'dac_comvest_ids.csv'
    df_dac_comvest = read_file_dac_comvest(file_dac_comvest)

    for year in range(2002, 2019):
        path_year = clean_module.file.get_year_path(year, path)
        clean_module.file.create_folder(path_year, 'rais_dac_comvest')
        merge_year(df_dac_comvest, path_year)

# Merge rais from year with df_dac_comvest and save in files in rais_dac_comvest directory
def merge_year(df_dac_comvest, path):
    path_folder = path + 'identification_data/'
    files = clean_module.file.get_all_files(path_folder, 'pkl')

    for file_rais in files:
        df_rais = read_file_rais(file_rais)
        df = merge_dfs(df_rais, df_dac_comvest)

        file_out = clean_module.file.change_folder_name(file_rais, 'rais_dac_comvest')
        file_out = clean_module.file.change_file_format(file_out, 'csv')
        clean_module.file.to_csv(df, file_out, index=True)

# Merge rais df with dac/comvest df and remove invalid cpfs
def merge_dfs(df_rais, df_dac_comvest):
    result = df_rais.reset_index().merge(df_dac_comvest)
    result = check_is_same_person(result)
    result = filter_columns_rais_dac_comvest(result)
    result = result.drop_duplicates().set_index('index')
    return result

#------------------------------------------------------------------------------------------------
# Read file with dac/comvest union and return dataframe
def read_file_dac_comvest(file):
    dtype = clean_module.dtypes.get_dtype_dac_comvest()
    df = clean_module.file.read_csv(file, dtype)

    df = df[df['cpf'] != '-']
    df.drop_duplicates(subset=['cpf'], inplace=True)
    df.rename(columns={'cpf': 'cpf_r'}, inplace=True)
    return df

# Read file with rais information and return dataframe
def read_file_rais(file):
    df = pd.read_pickle(file)
    return df

# Rename columns after merge
def filter_columns_rais_dac_comvest(df):
    columns = ['ano_base', 'nome_r', 'cpf_r', 'dta_nasc_r', 'pispasep', 'index', 'id']
    df = df.loc[:, columns]
    return df

#------------------------------------------------------------------------------------------------
# Remove cases of people with different names and return resultant dataframe
def check_is_same_person(df):
    same_person = df.apply(lambda x: is_same_person(x['nome_r'], x['nome']), axis=1)
    return df[same_person]

# Says if person_a is person_b based on the probabilistic match between the two first names
def is_same_person(name_a, name_b):
    first_name_a = name_a.split()[0]
    first_name_b = name_b.split()[0]
    similar_rate = SequenceMatcher(None, first_name_a, first_name_b).ratio()
    return similar_rate > 0.7

#------------------------------------------------------------------------------------------------
# Create a column in dac/comvest union saying if the person is in rais or not, and save it in uniao_dac_comvest_is_in_rais.csv
def check_is_in_rais(path):
    file_dac_comvest = path + 'dac_comvest_recovered.csv'
    dtype_dac_comvest = clean_module.dtypes.get_dtype_dac_comvest()
    df_dac_comvest = clean_module.file.read_csv(file_dac_comvest, dtype_dac_comvest)

    df_rais = join_merged_files(path)
    df_final = check_intersection_dfs(df_dac_comvest, df_rais)

    file_out = path + 'dac_comvest_is_in_rais.csv'
    clean_module.file.to_csv(df_final, file_out)

# Concat files in rais_dac_comvest in all years
def join_merged_files(path):
    dfs = []
    for year in range(2002, 2019):
        df = join_merged_files_year(year, path)
        dfs.append(df)

    df_result = pd.concat(dfs, sort=False)
    return df_result

# Concat files in rais_dac_comvest in a specific year
def join_merged_files_year(year, path):
    path_year = clean_module.file.get_year_path(year, path)
    path_files = path_year + 'rais_dac_comvest/'
    files = clean_module.file.get_all_files(path_files, 'csv')

    dfs = []
    for file in files:
        dtype = clean_module.dtypes.get_dtype_rais_clean()
        df = clean_module.file.read_csv(file, dtype, index='index')
        dfs.append(df)

    df_result = pd.concat(dfs, sort=False)
    return df_result

# Create a column in dac/comvest dataframe saying if the person is in rais or not
def check_intersection_dfs(df_dac_comvest, df_rais):
    df_rais = df_rais.loc[:,['cpf_r', 'ano_base']]
    df_rais.rename(columns={'cpf_r': 'cpf'}, inplace=True)
    in_rais = df_dac_comvest.merge(df_rais, on='cpf', how='left')
    in_rais['presente_na_rais'] = in_rais['ano_base'].notnull()
    del in_rais['ano_base']
    in_rais = in_rais.drop_duplicates()
    return in_rais
