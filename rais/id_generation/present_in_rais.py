import pandas as pd
import clean_module.file
import clean_module.dtypes

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