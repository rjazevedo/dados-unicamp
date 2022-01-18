import pandas as pd
import numpy as np
import re
import clean_module.file
import clean_module.dtypes

def generate_index(path):
    file = path + 'dac_comvest_recovered.csv'
    dtype = clean_module.dtypes.get_dtype_dac_comvest()
    df = clean_module.file.read_csv(file, dtype)

    df['doc'] = df.apply(lambda x: clear_document(x['doc']), axis=1)
    df_cpf_present = get_index_by_cpf(df)
    offset(df_cpf_present, 1)
    
    df2 = df.copy()
    df_cpf_missing = get_index_by_doc(df2)
    offset(df_cpf_missing, df_cpf_present['id'].max() + 1)
    result = pd.concat([df_cpf_present, df_cpf_missing])

    print(result.head(100))

    file_out = path + 'dac_comvest_ids.csv'
    clean_module.file.to_csv(result, file_out)

def get_index_by_cpf(df):
    df_cpf_present = df[df['cpf'] != '-']
    df_cpf_present = df_cpf_present.sample(frac=1).reset_index(drop=True)
    codes, uniques = pd.factorize(df_cpf_present['cpf'])
    df_cpf_present.insert(0, 'id', codes, True)
    return df_cpf_present

def get_index_by_doc(df):
    df_cpf_missing = df[df['cpf'] == '-']
    df_cpf_missing['join'] = df_cpf_missing.apply(lambda x: str(x['doc']) + str(x['dta_nasc']), axis=1)
    df_cpf_missing = df_cpf_missing.sample(frac=1).reset_index(drop=True)
    codes, uniques = pd.factorize(df_cpf_missing['join'])
    df_cpf_missing.insert(0, 'id', codes, True)
    del df_cpf_missing['join']
    return df_cpf_missing

def offset(df, value):
    df['id'] = df.apply(lambda x: x['id'] + value, axis=1)

def clear_document(value):
    if type(value) != str:
        return value
    new_string = re.sub(r"[x]", "X", value)
    new_string = re.sub(r"[^X0-9]", "", new_string)
    new_string = new_string.zfill(15)
    return new_string
