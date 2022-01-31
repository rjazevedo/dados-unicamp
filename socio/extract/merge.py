import pandas as pd

from socio.utilities.io import read_socio_clean
from socio.utilities.io import read_ids
from socio.utilities.io import write_socio_sample

from socio.extract.standardization_functions import get_upper
from socio.extract.standardization_functions import get_first_name
from socio.extract.standardization_functions import get_reduced_cpf
from socio.extract.standardization_functions import get_similarity

from socio.utilities.logging import log_extracting_ids

def merge_socio_dac_comvest():
    log_extracting_ids()
    df_socio = read_socio_clean()
    prepare_socio(df_socio)
    df_dac_comvest = read_ids()
    df_dac_comvest = prepare_dac_comvest(df_dac_comvest)
    df_merged = merge(df_socio, df_dac_comvest)
    write_socio_sample(df_merged)

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
