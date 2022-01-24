import pandas as pd

from socio.verification.verification_functions import check_nome_socio
from socio.verification.verification_functions import check_ano

from socio.utilities.io import read_socio_clean
from socio.utilities.io import read_empresa_clean
from socio.utilities.io import read_cnae_clean

from socio.database_information.socio import get_columns_info_socio
from socio.database_information.empresa import get_columns_info_empresa
from socio.database_information.cnae_secundaria import get_columns_info_cnae_secundaria

pd.set_option('display.max_columns', None)

def verify_socio():
    df = read_socio_clean()
    columns_info = get_columns_info_socio()
    verify_columns(df, columns_info)
    verify_nome_socio(df)
    verify_ano_entrada_sociedade(df)

def verify_empresa():
    df = read_empresa_clean()
    columns_info = get_columns_info_empresa()
    verify_columns(df, columns_info)
    verify_codes_columns(df, columns_info)

def verify_cnae_secundaria():
    df = read_cnae_clean()
    columns_info = get_columns_info_cnae_secundaria()
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
    df_failed = df_aux[df_aux.apply(lambda x: check_nome_socio(x['nome_socio'], x['identificador_de_socio']), axis=1)]
    print_result(df_failed)

def verify_ano_entrada_sociedade(df):
    print('Verifying: ano_entrada_sociedade')
    df_failed = df[df.apply(lambda x: check_ano(x['ano_entrada_sociedade'], x['data_entrada_sociedade']), axis=1)]
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
