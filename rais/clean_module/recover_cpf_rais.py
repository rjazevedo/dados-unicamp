import pandas as pd
import clean_module.dtypes
import clean_module.file

def recover_cpf_all_years(path):
    df = join_all_years(path)
    df_pis_cpf = get_pis_cpf(df)

    for year in range(2002, 2019):
        path_year = path + str(year) + '/'
        recover_cpf_year(df_pis_cpf, path_year)

#------------------------------------------------------------------------------------------------
# Join rais people that is dac comvest union and save in file "rais.csv"
def join_all_years(path):
    dfs = []
    for year in range(2002, 2019):
        path_year = clean_module.file.get_year_path(year, path)
        df = join_year(path_year)
        dfs.append(df)

    df = pd.concat(dfs, sort=True)
    return df

# Join rais people from year that is dac comvest union and return dataframe
def join_year(path):
    path_folder = path + 'rais_dac_comvest/'
    files = clean_module.file.get_all_files(path_folder, 'csv')
    dtype = clean_module.dtypes.get_dtype_rais_clean()

    dfs = []
    for file_rais in files:
        df = clean_module.file.read_csv(file_rais, dtype)
        dfs.append(df)
    
    df = pd.concat(dfs, sort=True)
    return df

#------------------------------------------------------------------------------------------------
def get_pis_cpf(df):
    df_cpf_pis = df.loc[:, ['cpf_r', 'pispasep', 'id']]
    df_cpf_pis = df_cpf_pis.drop_duplicates()
    df_cpf_pis = df_cpf_pis[df_cpf_pis.apply(lambda x: pd.notna(x['pispasep']), axis=1)]
    df_cpf_pis = df_cpf_pis[df_cpf_pis.duplicated(subset=['pispasep'], keep=False).apply(lambda x: not x)]
    return df_cpf_pis

#------------------------------------------------------------------------------------------------
def recover_cpf_year(df_pis_cpf, path):
    path_data = path + 'identification_data/'
    files = clean_module.file.get_all_files(path_data, 'pkl')

    for file in files:
        print("Recovering:", file)
        recover_cpf_file(df_pis_cpf, file)

def recover_cpf_file(df_pis_cpf, file):
    df_rais = pd.read_pickle(file)
    df_cpf_recovered = recover_cpf(df_pis_cpf, df_rais)
    df_cpf_known = get_df_cpf_known(file)
    df_concat = pd.concat([df_cpf_known, df_cpf_recovered], sort=True)

    file_out = clean_module.file.change_folder_name(file, 'rais_dac_comvest')
    file_out = clean_module.file.change_file_format(file_out, 'csv')
    clean_module.file.to_csv(df_concat, file_out, index=True)

def recover_cpf(df_pis_cpf, df_rais):
    df_cpf_missing = df_rais[df_rais.apply(lambda x: pd.isna(x['cpf_r']), axis=1)]
    del df_cpf_missing['cpf_r']
    del df_cpf_missing['mun_estbl']
    df_cpf_missing = df_cpf_missing.reset_index()
    cpf_recovered = pd.merge(df_cpf_missing, df_pis_cpf, on="pispasep")
    cpf_recovered = cpf_recovered.set_index('index')
    return cpf_recovered

#------------------------------------------------------------------------------------------------
def get_df_cpf_known(file):
    file_cpf_known = clean_module.file.change_folder_name(file, 'rais_dac_comvest')
    file_cpf_known = clean_module.file.change_file_format(file_cpf_known, 'csv')
    dtype = clean_module.dtypes.get_dtype_rais_clean()
    df_cpf_known = clean_module.file.read_csv(file_cpf_known, dtype, index='index')
    return df_cpf_known
