import pandas as pd

from rais.utilities.file import get_all_tmp_files
from rais.utilities.read import read_rais_merge
from rais.utilities.read import read_rais_merge_by_identification
from rais.utilities.read import read_rais_identification
from rais.utilities.write import write_rais_merge
from rais.utilities.logging import log_recover_cpf_rais

def recover_cpf_all_years():
    df = join_all_years()
    df_pis_cpf = get_pis_cpf(df)

    for year in range(2002, 2019):
        log_recover_cpf_rais(year)
        recover_cpf_year(df_pis_cpf, year)

#------------------------------------------------------------------------------------------------
# Join rais people that is dac comvest union and save in file "rais.csv"
def join_all_years():
    dfs = []
    for year in range(2002, 2019):
        df = join_year(year)
        dfs.append(df)
    df = pd.concat(dfs, sort=True)
    return df

# Join rais people from year that is dac comvest union and return dataframe
def join_year(year):
    files = get_all_tmp_files(year, 'rais_dac_comvest', 'csv')
    dfs = []
    for file_rais in files:
        df = read_rais_merge(file_rais)
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
def recover_cpf_year(df_pis_cpf, year):
    files = get_all_tmp_files(year, 'identification_data', 'pkl')
    for file in files:
        recover_cpf_file(df_pis_cpf, file, year)

def recover_cpf_file(df_pis_cpf, file, year):
    df_rais = read_rais_identification(file)
    df_cpf_recovered = recover_cpf(df_pis_cpf, df_rais)
    df_cpf_known = read_rais_merge_by_identification(file, year)
    df_concat = pd.concat([df_cpf_known, df_cpf_recovered], sort=True)
    write_rais_merge(df_concat, year, file)

def recover_cpf(df_pis_cpf, df_rais):
    df_cpf_missing = df_rais[df_rais.apply(lambda x: pd.isna(x['cpf_r']), axis=1)]
    del df_cpf_missing['cpf_r']
    del df_cpf_missing['mun_estbl']
    df_cpf_missing = df_cpf_missing.reset_index()
    cpf_recovered = pd.merge(df_cpf_missing, df_pis_cpf, on="pispasep")
    cpf_recovered = cpf_recovered.set_index('index')
    return cpf_recovered
