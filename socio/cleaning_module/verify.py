import cleaning_module.database_information
import pandas as pd

pd.set_option('display.max_columns', None)

# Verify columns in each clean database
# Input:
#   path: path to directory where it was put the clean files
def verify_cleaning(path):
    verify_socio(path)
    verify_empresa(path)
    verify_cnae_secundaria(path)

#------------------------------------------------------------------------------------------------
def verify_socio(path):
    file = path + 'socio.csv'
    columns_info = cleaning_module.database_information.get_columns_info_socio()
    dtype = cleaning_module.database_information.get_dtype(columns_info)
    df = pd.read_csv(file, dtype=dtype)

    verify_columns(df, columns_info)
    verify_nome_socio(df)
    verify_ano_entrada_sociedade(df)

def verify_empresa(path):
    file = path + 'empresa.csv'
    columns_info = cleaning_module.database_information.get_columns_info_empresa()
    dtype = cleaning_module.database_information.get_dtype(columns_info)
    df = pd.read_csv(file, dtype=dtype)
    
    verify_columns(df, columns_info)
    verify_codes_columns(df, columns_info)

def verify_cnae_secundaria(path):
    file = path + 'cnae_secundaria.csv'
    columns_info = cleaning_module.database_information.get_columns_info_cnae_secundaria()
    dtype = cleaning_module.database_information.get_dtype(columns_info)
    df = pd.read_csv(file, dtype=dtype)
    
    verify_columns(df, columns_info)
    verify_codes_columns(df, columns_info)

#------------------------------------------------------------------------------------------------
def verify_columns(df, columns_info):
    for column in columns_info:
        function = columns_info[column]['verification_function']
        if function != None:
            verify_column(df, column, function)

def verify_column(df, column, function):
    print('Verifying:', column)
    df = df.dropna(subset=[column])
    df = df[df[column] != -1]
    df_failed = df[df[column].map(function)]
    print_result(df_failed)

def print_result(df_failed):
    if df_failed.empty:
        print('OK')
    else:
        print('Failed in:')
        print(df_failed.head())

#------------------------------------------------------------------------------------------------
def verify_nome_socio(df):
    print('Verifying: nome_socio')
    df_aux = df.dropna(subset=['nome_socio'])
    df_failed = df_aux[df_aux.apply(lambda x: cleaning_module.verification_functions.check_nome_socio(x['nome_socio'], x['identificador_de_socio']), axis=1)]
    print_result(df_failed)

def verify_ano_entrada_sociedade(df):
    print('Verifying: ano_entrada_sociedade')
    df_failed = df[df.apply(lambda x: cleaning_module.verification_functions.check_ano(x['ano_entrada_sociedade'], x['data_entrada_sociedade']), axis=1)]
    print_result(df_failed)

#------------------------------------------------------------------------------------------------
def verify_codes_columns(df, columns_info):
    for column in columns_info:
        if 'codes_file' in columns_info[column]:
            file = columns_info[column]['codes_file']
            df_codes = read_df_codes(file, column)
            verify_codes(df, df_codes, column)

def read_df_codes(file, column):
    dtype = {column: 'object'}
    df_codes = pd.read_csv(file, dtype=dtype)
    return df_codes

def verify_codes(df, df_codes, column):
    print('Verifying:', column)
    df = df.dropna(subset=[column])
    df_codes['found'] = True
    df_merge = df.merge(df_codes, how='left', on=[column])
    df_failed = df_merge[df_merge['found'] != True]
    print_result(df_failed)
