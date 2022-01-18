import pandas as pd
import numpy as np
import clean_module.file
import clean_module.dtypes
import clean_module.clean
import clean_module.rais_information

#------------------------------------------------------------------------------------------------
def clean_all_years(path):
    for year in range(2002, 2019):
        clean_year(year, path)
    join_all_years(path)

def clean_year(year, path):
    path_year = clean_module.file.get_year_path(year, path)
    clean_module.file.create_folder(path_year, 'clean_data')

    path_data = path_year + 'rais_dac_comvest/'
    files = clean_module.file.get_all_files(path_data, 'csv')
    for file in files:
        clean_file(file, year)

def clean_file(file, year):
    print('Cleaning', file)
    dtype_clean = clean_module.dtypes.get_dtype_rais_clean()
    df_clean = clean_module.file.read_csv(file, dtype_clean, index='index')

    file_original = clean_module.file.change_folder_name(file, 'original_data')
    file_original = clean_module.file.change_file_format(file_original, clean_module.rais_information.get_extension(year))
    dtype_original = clean_module.dtypes.get_dtype_rais_original(year)
    df_original = clean_module.file.read_csv(file_original, dtype_original)

    df_final = get_columns(df_clean, df_original, year, file)

    file_out = clean_module.file.change_folder_name(file, 'clean_data')
    clean_module.file.to_csv(df_final, file_out, index=True)

def join_all_years(path):
    dfs = []
    for year in range(2002, 2019):
        path_year = clean_module.file.get_year_path(year, path)
        path_data = path_year + 'clean_data/'
        files = clean_module.file.get_all_files(path_data, 'csv')
        for file in files:
            dtype = clean_module.dtypes.get_dtype_rais_clean()
            df = clean_module.file.read_csv(file, dtype, index=0)
            dfs.append(df)

    result = pd.concat(dfs)
    anonymize_data(result)

    file_out = path + 'rais.csv'
    clean_module.file.to_csv(result, file_out)

#------------------------------------------------------------------------------------------------
def get_columns(df_clean, df_original, year, file):
    df_merged = pd.merge(df_clean, df_original, left_index=True, right_index=True)
    df_merged = rename_all_columns(df_merged, year)

    df_clean = clean_columns(df_merged, year)
    columns = clean_module.rais_information.get_all_columns_rais()
    df_clean = df_clean.loc[:, columns]
    return df_clean

#------------------------------------------------------------------------------------------------
def rename_all_columns(df, year):
    columns = clean_module.rais_information.get_all_columns_rais()
    columns.remove('id')
    columns.remove('nome_r')
    columns.remove('dta_nasc_r')
    columns.remove('cpf_r')
    columns.remove('pispasep')
    columns.remove('ano_base')
    df = rename_columns(df, year, columns)
    return df

def rename_columns(df, year, columns):
    dtypes = clean_module.dtypes.get_dtype_rais_clean()
    column_names = df.columns
 
    for column in columns:
        column_name = clean_module.rais_information.get_column(column, year)
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
    columns_info = clean_module.rais_information.get_columns_info_rais()
    for column in columns_info:
        periods = columns_info[column]['clean_function']
        function = clean_module.rais_information.get_info_period(year, periods)
        if function != None:
            df[column] = df.apply(lambda x: function(x[column]), axis=1)
    recover_cnpj_raiz(df)
    get_ano_nasc(df)
    fix_deslig_info(df, year)
    return df

def get_ano_nasc(df):
    df['ano_nasc_r'] = df.apply(lambda x: clean_module.clean.get_ano_nasc(x['dta_nasc_r']), axis=1)

def recover_cnpj_raiz(df):
    df['cnpj_raiz'] = df.apply(lambda x: clean_module.clean.recover_cnpj_raiz(x['cnpj'], x['cnpj_raiz']), axis=1)

def fix_deslig_info(df, year):
    if year == 2010:
        df['deslig_dia'] = df.apply(lambda x: clean_module.clean.fix_deslig(x['deslig_motivo'], x['deslig_dia']), axis=1)
    elif year >= 2014:
        df['deslig_dia'] = df.apply(lambda x: clean_module.clean.fix_deslig(x['deslig_motivo'], x['deslig_dia']), axis=1)
    if year >= 2010 and year <= 2011:
        df['deslig_mes'] = df.apply(lambda x: clean_module.clean.fix_deslig(x['deslig_motivo'], x['deslig_mes']), axis=1)
    elif year >= 2013 and year <= 2018:
        df['deslig_mes'] = df.apply(lambda x: clean_module.clean.fix_deslig(x['deslig_motivo'], x['deslig_mes']), axis=1)

#------------------------------------------------------------------------------------------------
def anonymize_data(df):
    del df['nome_r']
    del df['dta_nasc_r']
    del df['cpf_r']
    del df['pispasep']
    del df['ctps']
