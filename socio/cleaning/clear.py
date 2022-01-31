import pandas as pd

from socio.database_information.socio import get_columns_info_socio
from socio.database_information.empresa import get_columns_info_empresa

from socio.utilities.io import read_socio_original
from socio.utilities.io import read_empresa_original
from socio.utilities.io import read_cnae_original

from socio.utilities.io import write_socio
from socio.utilities.io import write_empresa
from socio.utilities.io import write_cnae

from socio.utilities.logging import log_cleaning_database
from socio.utilities.logging import log_cleaning_column

def clear_socio():
    log_cleaning_database('Socio')
    df = read_socio_original()
    columns_info = get_columns_info_socio()
    df = clear_columns(df, columns_info)
    write_socio(df)

def clear_empresa():
    log_cleaning_database('Empresa')
    df = read_empresa_original()
    columns_info = get_columns_info_empresa()
    df = clear_columns(df, columns_info)
    write_empresa(df)

def clear_cnae_secundaria():
    log_cleaning_database('CNAE')
    df = read_cnae_original()
    write_cnae(df)

#------------------------------------------------------------------------------------------------
def clear_columns(df, columns_info):
    df = filter_columns(df, columns_info)
    change_column_types(df, columns_info)
    for column in columns_info:
        log_cleaning_column(column)
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
