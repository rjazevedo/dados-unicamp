import pandas as pd

from socio.database_information.socio import get_columns_info_socio
from socio.database_information.empresa import get_columns_info_empresa

from socio.utilities.io import read_socio_original
from socio.utilities.io import read_empresa_original
from socio.utilities.io import read_cnae_original

from socio.utilities.io import write_socio
from socio.utilities.io import write_empresa
from socio.utilities.io import write_cnae

pd.set_option('display.max_columns', None)

# Clear socio database
# Input:
#   file: csv file with socio data
#   path_output: path where the output will be stored
def clear_socio():
    df = read_socio_original()
    columns_info = get_columns_info_socio()
    df = clear_columns(df, columns_info)
    write_socio(df)

# Clear empresa database
# Input:
#   file: csv file with empresa data
#   path_output: path where the output will be stored
def clear_empresa():
    df = read_empresa_original()
    columns_info = get_columns_info_empresa()
    df = clear_columns(df, columns_info)
    write_empresa(df)

# Clear cnae_secundaria database
# Input:
#   file: csv file with empresa data
#   path_output: path where the output will be stored
def clear_cnae_secundaria():
    df = read_cnae_original()
    write_cnae(df)

#------------------------------------------------------------------------------------------------
def clear_columns(df, columns_info):
    df = filter_columns(df, columns_info)
    change_column_types(df, columns_info)
    for column in columns_info:
        print('Cleaning:', column)
        clear_column(df, column, columns_info)
    return df

def filter_columns(df, columns_info):
    columns = list(columns_info.keys())
    df = df.loc[:, columns]
    return df

def change_column_types(df, columns_info):
    for column in columns_info:
        if 'has_null_value' in columns_info[column]:
            df[column] = df[column].fillna(-1)
            type_column = columns_info[column]['type']
            df[column] = df[column].astype(type_column)

def clear_column(df, column, columns_info):
    function = columns_info[column]['cleaning_function']
    if function != None:
        df[column] = df[column].map(function)
