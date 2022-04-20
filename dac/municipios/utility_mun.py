from unidecode import unidecode
import difflib as dff
import pandas as pd

CODE_UF_EQUIV = { 11: 'RO', 12: 'AC', 13: 'AM', 14: 'RR', 15: 'PA', 16: 'AP', 17: 'TO', 21: 'MA', 22: 'PI', 
                  23: 'CE', 24: 'RN', 25: 'PB', 26: 'PE', 27: 'AL', 28: 'SE', 29: 'BA', 31: 'MG', 32: 'ES',
                  33: 'RJ', 35: 'SP', 41: 'PR', 42: 'SC', 43: 'RS', 50: 'MS', 51: 'MT', 52: 'GO', 53: 'DF' }

def extract_mun_and_uf(df, columns):
    mun_and_uf = df[columns]
    mun_and_uf.columns = ['municipio', 'uf', 'pais']
    mun_and_uf = mun_and_uf[mun_and_uf['pais'] == 'BR']
    mun_and_uf.pop('pais')
    return mun_and_uf

def concat_and_drop_duplicates(dfs):
    concat = pd.concat(dfs, ignore_index = True)
    concat = concat.drop_duplicates(keep=False)
    return concat

def padronize_string(element):
    string_to_lower = element.lower()
    no_space_string = string_to_lower.replace(" ", "")
    no_accent_string = unidecode(no_space_string)
    return no_accent_string

def create_key_for_merge(df):
    df['key'] = df['municipio'].astype(str).map(lambda x: padronize_string(x))

def create_concat_key_for_merge(df):
    df['key'] = df['uf'].astype(str).map(lambda x: padronize_string(x)) + df['municipio'].astype(str).map(lambda x: padronize_string(x))
 
def create_dictonary_ufs(df):
    dict = {}
    for key,value in CODE_UF_EQUIV.items():
        filter_condition = (df['uf'] == value)
        df_uf = df[filter_condition]
        dict[value] = df_uf
        df = df[~filter_condition]
    
    dict[''] = df
    return dict

def merge_by_uf(dict_df, ibge_data, ibge_data_dict):
    dfs = []
    for key,value in dict_df.items():

        if key != '':
            ibge_data_filtered = ibge_data_dict[key]
            value['key'] = value['key'].map(lambda x: get_the_closest_matche(x, ibge_data_filtered['key']))
            merged_df = pd.merge(value, ibge_data_filtered, on=['key'], how='left')
            dfs.append(merged_df)

        else:
            create_concat_key_for_merge(value)
            value['key'] = value['key'].map(lambda x: get_the_closest_matche(x, ibge_data['key'], cutoff=0.85))
            merged_df = pd.merge(value, ibge_data, on=['key'], how='left')
            dfs.append(merged_df)
            
    return pd.concat(dfs, ignore_index = True)

def get_the_closest_matche(element, serie, cutoff=0.7):
    values = dff.get_close_matches(element, serie, cutoff=cutoff)
    if len(values) > 0:
        return values[0]
    else:
        return ''