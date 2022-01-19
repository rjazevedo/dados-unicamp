import pandas as pd
import numpy as np

def clear_nome(value):
    if value == 'Cpf Nao Consta Na Base-Cpf' or value == '!':
        return np.nan
    return value

def clear_cnpj_cpf(value):
    if value == '99999999999999':
        return np.nan
    return value

def clear_codigo_qualificacao(value):
    if value == 0:
        return -1
    return value

def clear_data(value):
    if pd.isnull(value):
        return np.nan
    
    year = value[:4]
    month = value[5:7]
    day = value[8:]
    return day + month + year

def clear_cpf(value):
    if value == '00000000000':
        return np.nan
    return value

def clear_motivo_situacao_cadastral(value):
    if value == 0:
        return -1
    return value

def clear_codigo_natureza_juridica(value):
    if value == '8885':
        return np.nan
    return value

def clear_cnae_fiscal(value):
    if value == '8888888':
        return np.nan
    return value.zfill(7)

def clear_cep(value):
    if value == '0':
        return np.nan

def clear_id_municipio_rf(value):
    return value.zfill(4)
