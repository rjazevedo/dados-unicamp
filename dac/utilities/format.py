import pandas as pd
import numpy as np
import unicodedata
import re

def str_to_upper_ascii(df, unicode_columns):
    clear_unicode = lambda s : str(unicodedata.normalize(u'NFKD', s).encode('ascii', 'ignore').decode('utf8')).strip().upper() if s != 'nan' else ''
    normalizar = np.vectorize(clear_unicode)
    for c in unicode_columns:
        df[c] = normalizar(df[c].values.astype(str))

def padronize_sex(df, name_column):
    df[name_column] = df[name_column].map ({
        'MASCULINO' : 1, 
        'FEMININO' : 2
        }).fillna(0).astype(int)

def padronize_race(df, name_column):
    df[name_column] = df[name_column].map({
        0 : 0, # NAO DECLARADO
        1 : 4, # AMARELA 
        2 : 1, # BRANCA
        3 : 5, # INDIGENA
        4 : 2, # PRETA
        5 : 3  # PARDA
        }).fillna(0).astype(int)

def padronize_marstat(df, name_column):
    df[name_column] = df[name_column].map({
        "SOLTEIRO" : 1,
        "CASADO" : 2,
        "VIUVO" : 3,
        "DIVORCIADO" : 4,
        "SEPARADO_JUDICIALMENTE" : 4,
        "UNIAO_ESTAVEL" : 5
    }).fillna(0).astype(int)

def format_doc(doc, len):
    endsx = doc[-1].lower() == 'x' 
    doc = re.sub("[^0-9]","", doc)
    doc = doc + 'X' if endsx else doc
    doc = doc.zfill(len)
    return doc

def fill_doc(docs, len):
    empty_doc = lambda doc : doc == '' or doc == 'nan' or doc == '0' or doc == '0.0'
    normalizar = np.vectorize(lambda s : '-' if empty_doc(s) else format_doc(s, len))
    return normalizar(docs.values.astype(str))

def padronize_dates(df, date_columns):
    reset_dates = np.vectorize(lambda s : ('' if s =='NaT' else s).zfill(8))
    for c in date_columns:
        df[c] = reset_dates(pd.to_datetime(df[c]).dt.strftime("%d%m%Y"))

def calc_cr_periodo(df, column):
    df['nota_credito'] =  df['nota'] * df['creditos']
    desempenho = df.groupby(['identif', 'ano', 'periodo'])
    nota_credito_per = desempenho.nota_credito.sum()
    creditos_per = desempenho.creditos.sum()
    cr_periodo = 0.1 * nota_credito_per / creditos_per
    cr_periodo = (np.round(cr_periodo, 4)).to_frame(name=column)
    cr_periodo.reset_index(level=['identif', 'ano', 'periodo'], inplace=True)
    
    return cr_periodo

def dates_to_year(df, column):
    reset_dates = np.vectorize(lambda s : (s if str(s).isdigit() else '').zfill(4))
    df[column] = reset_dates(pd.to_datetime(df[column]).dt.strftime("%Y"))