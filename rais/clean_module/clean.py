import pandas as pd
import numpy as np
import re
import clean_module.dtypes

#------------------------------------------------------------------------------------------------
def clean_cpf_column(df):
    df['cpf_r'] = df.apply(lambda x: get_cpf(x['cpf_r']), axis=1)

def clean_pispasep_column(df):
    df['pispasep'] = df.apply(lambda x: get_pispasep(x['pispasep']), axis=1)

def clean_name_column(df):
    df['nome_r'] = df.apply(lambda x: get_name(x['nome_r']), axis=1)

def clean_birthdate_column(df):
    df['dta_nasc_r'] = df.apply(lambda x: get_birthdate(x['dta_nasc_r']), axis=1)

#------------------------------------------------------------------------------------------------
def get_cpf(cpf):
    if (type(cpf) != str):
        return np.nan
        
    cpf = cpf.strip()
    if (cpf == '0') or (cpf == '99') or (cpf == '191') or (cpf == '00000000000') or (cpf == '11111111111') or (cpf == '33333333333'):
        return np.nan

    fixed_cpf = cpf.zfill(11)
    return fixed_cpf

# Invalid birthdates must be NaN
# Birthdates must have 8 digits
def get_birthdate(value):
    return value.zfill(8)

# Invalid names must be NaN
# Names mustn't have leading spaces
def get_name(name):
    if type(name) != str:
        return np.nan

    fixed_name = name.strip()
    return fixed_name

def get_ano_nasc(birthdate):
    if type(birthdate) != str:
        return -1
    year = birthdate[4:]
    return int(year)

def get_mun(value):
    if value == '000000':
        return np.nan
    return value

def get_vinculo_tipo(value):
    code = {
        'CLT U/PJ IND': 10,
        'CLT U/PF IND': 15,
        'CLT R/PJ IND': 20,
        'CLT R/PF IND': 25,
        'ESTATUTARIO': 30,
        'ESTAT RGPS': 31,
        'ESTAT N/EFET': 35,
        'AVULSO': 40,
        'TEMPORARIO': 50,
        'APREND CONTR': 55,
        'CLT U/PJ DET': 60,
        'CLT U/PF DET': 65,
        'CLT R/PJ DET': 70,
        'CLT R/PF DET': 75,
        'DIRETOR': 80,
        'CONT PRZ DET': 90,
        'CONT TMP DET': 95,
        'CONT LEI EST': 96,
        'CONT LEI MUN': 97,
        'IGNORADO': -1
    }
    return code[value]

def fix_deslig(motivo, period):
    if (motivo != 0) and (period == 0):
        return -1
    else:
        return period

def get_cbo(value):
    if value == '{ñ cl' or value == 'IGNORADO':
        return np.nan
    return value

def get_cbo_number(value):
    if value == 'IGNORADO':
        return np.nan
    return value[4:]

def get_cbo_valid(value):
    if value == '0000-1':
        return np.nan
    return value

def get_sexo(value):
    value = value.strip()
    return int(value)

def get_sexo_word(value):
    if value == 'MASCULINO':
        return 1
    elif value == 'FEMININO':
        return 2

def get_raca(value):
    code = {
        -1: 0,
        1: 5,
        2: 1,
        4: 2,
        6: 4,
        8: 3,
        9: 6,
        99: 0
    }
    return code[value]

def get_estbl_tamanho(value):
    return value + 1

def get_estbl_tipo(value):
    if type(value) != str:
        return -1
    return int(value)

def get_dta_admissao(value):
    value = value.zfill(8)
    return value

def get_dta_admissao_valid(value):
    year = int(value[4:])
    is_year_valid = year >= 1900 and year <= 2018
    if not is_year_valid:
        return np.nan
    return value
    
def get_float(value):
    if type(value) != str:
        return -1
    if not ',' in value:
        return -1
    number = value.replace(',', '.')
    return float(number)

def get_horas_contr(value):
    if type(value) != str:
        return -1
    return int(value)

def get_pispasep(value):
    if value == '0':
        return np.nan
    return value

def get_ctps(value):
    if value == '0' or value == '9999999' or value == '99999990000' or value == '00000000':
        return np.nan
    return value.zfill(8)

def get_ctps_valid(value):
    if value == '00000000':
        return np.nan
    return value

def get_cei_vinc(value):
    if value == '0':
        return np.nan
    return value.zfill(12)

def get_cei_vinc_longer(value):
    if int(value) == 0:
        return np.nan
    return value[2:]

def get_cei_vinc_valid(value):
    if value == '000000000000':
        return np.nan
    return value

def get_cnpj(value):
    value = value.zfill(14)
    return value

def get_cnpj_raiz(value):
    value = value.zfill(8)
    return value

def recover_cnpj_raiz(cnpj, cnpj_raiz):
    if int(cnpj_raiz) != 0:
        return cnpj_raiz
    return cnpj[:8]

def get_cnae_20_classe(value):
    if value[0] == 'C':
        return value[7:]
    return value

def get_cnae_20_subclasse(value):
    if value == '-1':
        return np.nan
    return value

def get_afast_causa(value):
    if (value == 99):
        return -1
    return value

def get_afast_causa_string(value):
    if type(value) != str:
        return -1
    return int(value)

def get_afast_dia(value):
    if (value == 'IGNORADO') or (value == '99'):
        return -1
    return int(value)

def get_afast_mes(value):
    if (value == 99):
        return -1
    return value

def get_afast_mes_string(value):
    if type(value) != str:
        return -1
    return int(value)

def get_afast_dias_total(value):
    if type(value) != str:
        return -1
    return int(value)

def get_afast_dias_total_valid(value):
    if value > 366:
        return -1
    return int(value)

def get_idade(value):
    if value == 0:
        return -1
    return value

def get_deslig_dia(value):
    if (value == '{ñ'):
        return 0
    if value == 'NAO DESL ANO':
        return 0
    return int(value)

def get_estbl_cep(value):
    if (value == '99999999'):
        return np.nan
    return value

def get_razao_social(value):
    if (type(value) != str):
        return np.nan
    new_string = re.sub(r"[^a-zA-Z0-9 ]", "", value)
    list_string = new_string.split()
    new_string = ' '.join(list_string)
    return new_string
