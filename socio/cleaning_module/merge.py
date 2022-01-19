import cleaning_module.database_information
import pandas as pd
from difflib import SequenceMatcher

def merge_socio_dac_comvest(file_dac_comvest, path_socio):
    df_socio = read_file_socio(path_socio)
    df_dac_comvest = read_file_dac_comvest(file_dac_comvest)
    df_merged = merge(df_socio, df_dac_comvest)
    file_out = path_socio + 'socio_amostra.csv'
    df_merged.to_csv(file_out, index=False)

#------------------------------------------------------------------------------------------------
def read_file_socio(path):
    file = path + 'socio.csv'
    columns_info = cleaning_module.database_information.get_columns_info_socio()
    dtype = cleaning_module.database_information.get_dtype(columns_info)
    df = pd.read_csv(file, dtype=dtype)
    prepare_socio(df)
    return df

def read_file_dac_comvest(file):
    dtype = get_dtype_dac_comvest()
    df = pd.read_csv(file, dtype=dtype, sep=';')
    df = prepare_dac_comvest(df)
    return df

#------------------------------------------------------------------------------------------------
def get_dtype_dac_comvest():
    return {
        'nome': 'object',
        'cpf': 'object',
        'id': 'int64'
    }

#------------------------------------------------------------------------------------------------
def prepare_socio(df):
    df.dropna(subset=['nome_socio'], inplace=True)
    df['nome_socio'] = df['nome_socio'].map(get_upper)
    df['primeiro_nome'] = df['nome_socio'].map(get_first_name)

def prepare_dac_comvest(df):
    df = df.loc[:,['cpf', 'nome', 'id']]
    df['cnpj_cpf_do_socio'] = df['cpf'].map(get_reduced_cpf)
    df['primeiro_nome'] = df['nome'].map(get_first_name)
    return df

#------------------------------------------------------------------------------------------------
def merge(df_socio, df_dac_comvest):
    df = df_dac_comvest.merge(df_socio, on=['cnpj_cpf_do_socio', 'primeiro_nome'])
    df['similaridade'] = df.apply(lambda x: get_similarity(x['nome'], x['nome_socio']), axis=1)
    same_person_df = df[df['similaridade'] > 0.5]
    filter_columns(same_person_df)
    return same_person_df

def filter_columns(df):
    del df['cpf']
    del df['nome']
    del df['nome_socio']
    del df['cnpj_cpf_do_socio']
    del df['primeiro_nome']
    del df['similaridade']

#------------------------------------------------------------------------------------------------
def get_upper(name):
    return name.upper()

def get_first_name(name):
    names = name.split()
    return names[0]

def get_reduced_cpf(cpf):
    if cpf == '-':
        return '-'
    reduced_cpf = '***' + cpf[3:-2] + '**'
    return reduced_cpf

def get_similarity(name_a, name_b):
    last_name_a = name_a.split()[1:]
    last_name_b = name_b.split()[1:]
    similar_rate = SequenceMatcher(None, last_name_a, last_name_b).ratio()
    return similar_rate
