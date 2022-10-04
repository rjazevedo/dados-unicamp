import pandas as pd
import difflib as dff
from unidecode import unidecode
from dac.utilities.io import write_result

CODE_UF_EQUIV = { 11: 'RO', 12: 'AC', 13: 'AM', 14: 'RR', 15: 'PA', 16: 'AP', 17: 'TO', 21: 'MA', 22: 'PI', 
                  23: 'CE', 24: 'RN', 25: 'PB', 26: 'PE', 27: 'AL', 28: 'SE', 29: 'BA', 31: 'MG', 32: 'ES',
                  33: 'RJ', 35: 'SP', 41: 'PR', 42: 'SC', 43: 'RS', 50: 'MS', 51: 'MT', 52: 'GO', 53: 'DF' }


def extract_mun_and_uf(df, columns):
    mun_and_uf = df[columns]
    mun_and_uf.columns = ['municipio', 'uf', 'pais']
    mun_and_uf = mun_and_uf[mun_and_uf['pais'] == 'BR']
    mun_and_uf.pop('pais')
    return mun_and_uf


def give_trust(df, trust_value):
    trust = df.copy()
    trust.loc[:,["confianca"]] = trust_value
    return trust


def get_wrong_and_right(df):
    filtro = df['codigo_municipio'].isnull()
    right = df[~filtro]
    wrong = df[filtro]
    wrong = remove_unused_columns(wrong)
    return (right, wrong)


def padronize_string(element):
    string_to_lower = element.lower()
    no_space_string = string_to_lower.replace(" ", "")
    no_accent_string = unidecode(no_space_string)
    return no_accent_string


def merge_by_uf(dict_df, ibge_data):
    correct_dfs = []
    wrong_dfs = []

    for key,value in dict_df.items():
        if key != '':
            ibge_data_filtered = ibge_data[ibge_data['uf'] == key]
            merged_df = key_merge(value, ibge_data_filtered, 0.8)
            correct_dfs.append(merged_df[0])
            wrong_dfs.append(merged_df[1])
        else:
            wrong_dfs.append(value)

    correct_df = concat_and_drop_duplicates(correct_dfs)
    wrong_df = concat_and_drop_duplicates(wrong_dfs)
    wrong_df = remove_unused_columns(wrong_df)
    return correct_df, wrong_df


def merge_by_counties(df, ibge_data):
    df.insert(0, 'ID', range(0, len(df)))
    right, wrong = key_merge(df, ibge_data, 0.88)

    no_duplicated_right = right.drop_duplicates(keep=False, subset=["ID"])
    no_duplicated_right = no_duplicated_right.drop(['ID'], axis=1)

    duplicated_right = right.duplicated(keep='last', subset=['ID'])
    duplicated_right = right[duplicated_right]
    duplicated_right = remove_unused_columns(duplicated_right)
    
    wrong = remove_unused_columns(wrong)
    wrong = concat_and_drop_duplicates([wrong, duplicated_right])

    right = no_duplicated_right
    return right, wrong


def merge_by_concat_key(df, ibge_data):
    right, wrong = key_merge(df, ibge_data, 0.85)
    wrong = remove_unused_columns(wrong)
    return right, wrong


def remove_unused_columns(df):
    new_df = df.copy()
    importante_columns = ['municipio', 'uf']
    for index in df.columns:
        if index not in importante_columns:
            new_df.drop(index, axis=1, inplace=True)
    return new_df


def concat_and_drop_duplicates(dfs):
    concat = pd.concat(dfs, ignore_index = True)
    concat = concat.drop_duplicates()
    return concat


def key_merge(value, ibge_data, cutoff):
    value['key'] = value['key'].map(lambda x: get_the_closest_matche(x, ibge_data['key'], cutoff=cutoff))
    merged_df = pd.merge(value, ibge_data, on=['key'], how='left', suffixes=('','_ibge'))
    right, wrong = get_wrong_and_right(merged_df)
    return (right, wrong)


def get_the_closest_matche(element, serie, cutoff):
    values = dff.get_close_matches(element, serie, cutoff=cutoff)
    if len(values) > 0:
        return values[0]
    else:
        return ''


def create_key_for_merge(df):
    df['key'] = df['municipio'].astype(str).map(lambda x: padronize_string(x))
    return df


def create_concat_key_for_merge(df):
    df['key'] = df['uf'].astype(str).map(lambda x: padronize_string(x)) + df['municipio'].astype(str).map(lambda x: padronize_string(x))
    return df


def create_dictonary_ufs(df):
    dict = {}
    for key,value in CODE_UF_EQUIV.items():
        filter_condition = (df['uf'] == value)
        df_uf = df[filter_condition]
        dict[value] = df_uf
        df = df[~filter_condition]
    dict[''] = df
    return dict


def copy_columns_for_perfect_merge(df):
    new_df = df.copy()
    new_df['municipio_ibge'] = new_df['municipio']
    new_df['uf_ibge'] = new_df['uf']
    return new_df
