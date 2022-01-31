import pandas as pd
import numpy as np

from rais.extract import cleaning_functions

from rais.utilities.rais_information import get_all_columns_rais
from rais.utilities.rais_information import get_column
from rais.utilities.rais_information import get_columns_info_rais
from rais.utilities.rais_information import get_info_period

from rais.utilities.dtypes import get_dtype_rais_clean

from rais.utilities.file import create_folder_inside_year
from rais.utilities.file import get_all_tmp_files

from rais.utilities.read import read_rais_merge
from rais.utilities.read import read_rais_original_by_merge
from rais.utilities.read import read_rais_clean

from rais.utilities.write import write_rais_clean
from rais.utilities.write import write_rais_sample

from rais.utilities.logging import log_cleaning_year
from rais.utilities.logging import log_cleaning_file

def clear_all_years():
    for year in range(2002, 2019):
        log_cleaning_year(year)
        clear_year(year)
    join_all_years()

def clear_year(year):
    create_folder_inside_year(year, 'clean_data')
    files = get_all_tmp_files(year, 'rais_dac_comvest', 'csv')
    for file in files:
        clear_file(file, year)

def clear_file(file, year):
    log_cleaning_file(file)
    df_clean = read_rais_merge(file)
    df_original = read_rais_original_by_merge(file, year)
    df_final = get_columns(df_clean, df_original, year, file)
    write_rais_clean(df_final, year, file)

def join_all_years():
    dfs = []
    for year in range(2002, 2019):
        files = get_all_tmp_files(year, 'clean_data', 'csv')
        for file in files:
            df = read_rais_clean(file)
            dfs.append(df)
    result = pd.concat(dfs)
    anonymize_data(result)
    write_rais_sample(result)

#------------------------------------------------------------------------------------------------
def get_columns(df_clean, df_original, year, file):
    df_merged = pd.merge(df_clean, df_original, left_index=True, right_index=True)
    df_merged = rename_all_columns(df_merged, year)
    df_clean = clean_columns(df_merged, year)
    columns = get_all_columns_rais()
    df_clean = df_clean.loc[:, columns]
    return df_clean

#------------------------------------------------------------------------------------------------
def rename_all_columns(df, year):
    columns = get_all_columns_rais()
    columns.remove('id')
    columns.remove('nome_r')
    columns.remove('dta_nasc_r')
    columns.remove('cpf_r')
    columns.remove('pispasep')
    columns.remove('ano_base')
    df = rename_columns(df, year, columns)
    return df

def rename_columns(df, year, columns):
    dtypes = get_dtype_rais_clean()
    column_names = df.columns
 
    for column in columns:
        column_name = get_column(column, year)
        if column_name != None and column_name in column_names:
            df.rename(columns={column_name: column}, inplace=True)
        else:
            dtype = dtypes[column]
            if dtype == 'object':
                df[column] = np.nan
                df = df.astype({column: 'object'})
            elif dtype == 'int64':
                df[column] = -1
            elif dtype == 'float64':
                df[column] = -1.0
    return df

#------------------------------------------------------------------------------------------------
def clean_columns(df, year):
    columns_info = get_columns_info_rais()
    for column in columns_info:
        periods = columns_info[column]['clean_function']
        function = get_info_period(year, periods)
        if function != None:
            df[column] = df.apply(lambda x: function(x[column]), axis=1)
    recover_cnpj_raiz(df)
    get_ano_nasc(df)
    fix_deslig_info(df, year)
    return df

def get_ano_nasc(df):
    df['ano_nasc_r'] = df.apply(lambda x: cleaning_functions.get_ano_nasc(x['dta_nasc_r']), axis=1)

def recover_cnpj_raiz(df):
    df['cnpj_raiz'] = df.apply(lambda x: cleaning_functions.recover_cnpj_raiz(x['cnpj'], x['cnpj_raiz']), axis=1)

def fix_deslig_info(df, year):
    if year == 2010:
        df['deslig_dia'] = df.apply(lambda x: cleaning_functions.fix_deslig(x['deslig_motivo'], x['deslig_dia']), axis=1)
    elif year >= 2014:
        df['deslig_dia'] = df.apply(lambda x: cleaning_functions.fix_deslig(x['deslig_motivo'], x['deslig_dia']), axis=1)
    if year >= 2010 and year <= 2011:
        df['deslig_mes'] = df.apply(lambda x: cleaning_functions.fix_deslig(x['deslig_motivo'], x['deslig_mes']), axis=1)
    elif year >= 2013 and year <= 2018:
        df['deslig_mes'] = df.apply(lambda x: cleaning_functions.fix_deslig(x['deslig_motivo'], x['deslig_mes']), axis=1)

#------------------------------------------------------------------------------------------------
def anonymize_data(df):
    del df['nome_r']
    del df['dta_nasc_r']
    del df['cpf_r']
    del df['pispasep']
    del df['ctps']
