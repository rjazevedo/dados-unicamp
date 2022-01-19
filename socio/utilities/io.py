import pandas as pd
import yaml

from cleaning_module.database_information import get_columns_info_socio
from cleaning_module.database_information import get_columns_info_empresa
from cleaning_module.database_information import get_dtype

stream = open('configuration.yaml')
config = yaml.safe_load(stream)

def read_socio():
    file = config['databasesocio']
    columns_info = get_columns_info_socio()
    return read_database(file, columns_info)

def read_empresa():
    file = config['databasecompany']
    columns_info = get_columns_info_empresa()
    df = read_database(file, columns_info)
    return df

def read_cnae():
    file = config['databasecnae']
    dtype = {
        0: 'object',
        1: 'object'
    }
    df = pd.read_csv(file, dtype=dtype, header=None)
    df = rename_columns_cnae(df)
    return df

#------------------------------------------------------------------------------------------------
def write_socio(df):
    file = config['results'] + 'socio.csv'
    write_database(df, file)

def write_empresa(df):
    file = config['results'] + 'empresa.csv'
    write_database(df, file)

def write_cnae(df):
    file = config['results'] + 'cnae_secundaria.csv'
    write_database(df, file)

#------------------------------------------------------------------------------------------------
def read_database(file, columns_info):
    dtype = get_dtype(columns_info, is_original=True)
    df = pd.read_csv(file, dtype=dtype)
    return df

def rename_columns_cnae(df):
    df['cnpj'] = df[0]
    df['cnae'] = df[1]
    df = df.loc[:,['cnpj', 'cnae']]
    return df

def write_database(df, file):
    df.to_csv(file, index=False)
