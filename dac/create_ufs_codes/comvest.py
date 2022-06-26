from dac.utilities.columns import dados_cadastrais_cols
from dac.utilities.io import read_from_database
from dac.utilities.io import write_output
from unidecode import unidecode
from comvest.utilities.dtypes import DTYPES_DADOS
from dac.create_ufs_codes.utility_mun import concat_and_drop_duplicates
from dac.create_ufs_codes.utility_mun import create_key_for_merge
from dac.create_ufs_codes.utility_mun import create_dictonary_ufs
import pandas as pd
import glob

VEST_PATH = '/home/fernando/dados-unicamp/input/comvest/'

def generate_mun_comvest():
    dfs = []
    all_vests = glob.glob(VEST_PATH + '*')
    for year in all_vests:
        df = pd.read_excel(year, sheet_name='dados')
        df = rename_colums(df)
        dfs.append(df)
    
    result = concat_and_drop_duplicates(dfs)
    create_key_for_merge(result)
    comvest_dict = create_dictonary_ufs(result)
    return comvest_dict

def rename_colums(df):
    df = tratar_mun_nasc(df)
    df = tratar_uf_nasc(df)
    df = tratar_mun_resid(df)
    df = tratar_uf_resid(df)
    df = tratar_mun_escola(df)
    df = tratar_uf_escola(df)
        
    df1 = df[['MUN_NASC', 'UF_NASC']].rename(columns={'MUN_NASC': 'municipio', 'UF_NASC': 'uf'})
    df2 = df[['MUN_RESID', 'UF_RESID']].rename(columns={'MUN_RESID': 'municipio', 'UF_RESID': 'uf'})
    df3 = df[['MUN_ESC_EM', 'UF_ESCOLA_EM']].rename(columns={'MUN_ESC_EM': 'municipio', 'UF_ESCOLA_EM': 'uf'})

    df_concat = concat_and_drop_duplicates([df1, df2, df3])
    return df_concat

def tratar_mun_nasc(df):
    for col in df.columns:
        if col in {'MUNICIPIO_NASC','MU_NASC','MUNIC_NASC','CIDNASC','CIDNAS'}:
            df.rename({col: 'MUN_NASC'}, axis=1, inplace=True)
            df['MUN_NASC'] = df['MUN_NASC'].map(lambda mun: unidecode(str(mun)).upper() if str(mun) != '-' else '')
            return df
    return df

def tratar_uf_nasc(df):
    for col in df.columns:
        if col in {'UFNASC','EST_NASC','UFNAS'}:
            df.rename({col: 'UF_NASC'}, axis=1, inplace=True)
            df['UF_NASC'] = df['UF_NASC'].map(lambda uf: unidecode(str(uf)).upper() if str(uf) != '-' else '')
            return df
    return df

def tratar_mun_resid(df):
    for col in df.columns:
        if col in {'MUEND','MUNIC_END','MUNICIPIO','CID','CIDEND'}:
            df.rename({col: 'MUN_RESID'}, axis=1, inplace=True)
            df['MUN_RESID'] = df['MUN_RESID'].map(lambda mun: unidecode(str(mun)).upper())
            return df
    return df

def tratar_uf_resid(df):
  # Se a UF de Residência é dado por UFEND, UF_END ou ESTADO, entao renomeia a coluna para UF_RESID
    if 'UFEND' in df.columns:
        df.rename({'UFEND': 'UF_RESID'}, axis=1, inplace=True)
    elif 'UF_END' in df.columns:
        df.rename({'UF_END': 'UF_RESID'}, axis=1, inplace=True)
    elif 'ESTADO' in df.columns:
        df.rename({'ESTADO': 'UF_RESID'}, axis=1, inplace=True)
    elif 'EST' in df.columns:
        df.rename({'EST': 'UF_RESID'}, axis=1, inplace=True)
    return df

def tratar_mun_escola(df):
  # Checa coluna do município da escola do ensino médio do candidato
    for col in df.columns:
        if col in {'MUESC','MUN_ESC','MUN_ESCOLA','MUNESC','MUNICIPIO_ESCOLA','CIDESC'}:
            df.rename({col: 'MUN_ESC_EM'}, axis=1, inplace=True)
            df['MUN_ESC_EM'] = df['MUN_ESC_EM'].map(lambda mun: unidecode(str(mun)).upper() if str(mun) != '-' else '')
            return df
    return df

def tratar_uf_escola(df):
  # Checa coluna da UF onde se localiza a escola do ensino médio do candidato
    for col in df.columns:
        if col in {'UFESC','UF_ESC','ESTADO_ESC','ESTESC','UF_ESCOLA','ESTADO_ESCOLA','EST_ESCOLA'}:
            df.rename({col: 'UF_ESCOLA_EM'}, axis=1, inplace=True)
            return df
    return df