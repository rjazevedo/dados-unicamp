import pandas as pd
import yaml

from socio.utilities.dtype import get_dtype

from socio.database_information.socio import get_columns_info_socio
from socio.database_information.empresa import get_columns_info_empresa
from socio.database_information.cnae_secundaria import get_columns_info_cnae_secundaria

stream = open('socio/configuration.yaml')
config = yaml.safe_load(stream)

def read_ids():
    file = config['database_ids']
    dtype = {
        'nome': 'object',
        'cpf': 'object',
        'id': 'int64'
    }
    df = pd.read_csv(file, dtype=dtype, sep=';', low_memory=False)
    return df

#------------------------------------------------------------------------------------------------
def read_socio_original():
    file = config['database_socio']
    columns_info = get_columns_info_socio()
    return read_database(file, columns_info)

def read_empresa_original():
    file = config['database_company']
    columns_info = get_columns_info_empresa()
    df = read_database(file, columns_info, low_memory=False)
    return df

def read_cnae_original():
    file = config['database_cnae']
    dtype = {
        0: 'object',
        1: 'object'
    }
    df = pd.read_csv(file, dtype=dtype, header=None)
    df = rename_columns_cnae(df)
    return df

#------------------------------------------------------------------------------------------------
def read_socio_clean():
    file = config['path_output'] + 'socio.csv'
    columns_info = get_columns_info_socio()
    return read_database(file, columns_info, is_original=False)

def read_empresa_clean():
    file = config['path_output'] + 'empresa.csv'
    columns_info = get_columns_info_empresa()
    df = read_database(file, columns_info, is_original=False)
    return df

def read_cnae_clean():
    file = config['path_output'] + 'cnae_secundaria.csv'
    columns_info = get_columns_info_cnae_secundaria()
    df = read_database(file, columns_info, is_original=False)
    return df

#------------------------------------------------------------------------------------------------
def write_socio(df):
    file = config['path_output'] + 'socio.csv'
    write_database(df, file)

def write_empresa(df):
    file = config['path_output'] + 'empresa.csv'
    write_database(df, file)

def write_cnae(df):
    file = config['path_output'] + 'cnae_secundaria.csv'
    write_database(df, file)

def write_socio_sample(df):
    file = config['path_output'] + 'socio_amostra.csv'
    write_database(df, file)

#------------------------------------------------------------------------------------------------
def read_database(file, columns_info, is_original=True, low_memory=True):
    dtype = get_dtype(columns_info, is_original=is_original)
    df = pd.read_csv(file, dtype=dtype, low_memory=low_memory)
    return df

def rename_columns_cnae(df):
    df['cnpj'] = df[0]
    df['cnae'] = df[1]
    df = df.loc[:,['cnpj', 'cnae']]
    return df

def write_database(df, file):
    df.to_csv(file, index=False)
