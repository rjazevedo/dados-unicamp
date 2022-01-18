import pandas as pd
import numpy as np
from difflib import SequenceMatcher

import clean_module.df_operations
import clean_module.dtypes
import clean_module.file

#------------------------------------------------------------------------------------------------

UNICO = 3
HOMONIMO = 4
HIGH_SIMILARITY = 5
MEDIUM_SIMILARITY = 6

MIN_MEDIUM_SIMILARITY = 0.7
MIN_HIGH_SIMILARITY = 0.8

#------------------------------------------------------------------------------------------------
# Uses initial union dac/comvest to recover missing cpfs in rais and generate a new file with cpfs recovered
def recover_cpf_dac_comvest(path):
    file = path + 'dac_comvest_valid.csv'
    dtype = clean_module.dtypes.get_dtype_dac_comvest()
    df_dac_comvest = clean_module.file.read_csv(file, dtype)

    df_cpf_missing = get_cpf_missing_dac_comvest(df_dac_comvest)
    df_cpf_recovered_exact_match = recover_cpf_exact_match(df_cpf_missing, path)
    df_cpf_missing = update_cpf_missing(df_cpf_missing, df_cpf_recovered_exact_match)
    df_cpf_recovered_probabilistic_match = recover_cpf_probabilistic_match(df_cpf_missing, path)
    df_final = join_cpf_recovered(df_dac_comvest, df_cpf_recovered_exact_match, df_cpf_recovered_probabilistic_match)

    file_out = path + 'dac_comvest_recovered.csv'
    clean_module.file.to_csv(df_final, file_out)

#------------------------------------------------------------------------------------------------
# Return df with only the lines with cpf missing or cpf from parents
def get_cpf_missing_dac_comvest(df):
    cpf_missing = df[df.apply(lambda x: x['cpf'] == '-', axis=1)]
    cpf_missing = cpf_missing.drop_duplicates()
    return cpf_missing

# Return df with matches made with name and birthdate equal
def recover_cpf_exact_match(df, path):
    prepare_df_dac_comvest_exact_match(df)
    df_recovered = merge_with_rais(df, path, False)
    df_recovered = remove_invalid_cpf(df_recovered)
    df_recovered = fix_duplicated_rows_exact_match(df_recovered)
    return df_recovered

# Return df with missing cpfs after first recover
def update_cpf_missing(df_cpf_missing, df_cpf_recovered):
    columns = ['insc_vest', 'ano_ingresso_curso']
    updated_cpf_missing = clean_module.df_operations.subtract(df_cpf_missing, df_cpf_recovered, columns)
    return updated_cpf_missing

# Return df with matches made with first name, birthdate equal and high similarity between names
def recover_cpf_probabilistic_match(df, path):
    prepare_df_dac_comvest_probabilistic_match(df)
    df_merged = merge_with_rais(df, path, True)
    df_recovered = remove_invalid_cpf(df_merged)
    df_recovered = fix_duplicated_rows_probabilistic_match(df_recovered)
    return df_recovered

# Return df with initial dataframe replaced with all cpfs recovered
def join_cpf_recovered(df_dac_comvest, df_cpf_recovered_exact_match, df_cpf_recovered_probabilistic_match):
    dfs = [df_cpf_recovered_exact_match, df_cpf_recovered_probabilistic_match]
    df_cpf_recovered = pd.concat(dfs)
    result = update_cpf_dac_comvest(df_cpf_recovered, df_dac_comvest)
    return result

#------------------------------------------------------------------------------------------------
# Rename columns to use in merge
def prepare_df_dac_comvest_exact_match(df):
    del df['cpf']

# Rename columns to use in merge
def prepare_df_rais_exact_match(df):
    df.rename(columns={'cpf_r': 'cpf'}, inplace=True)
    df.rename(columns={'dta_nasc_r': 'dta_nasc'}, inplace=True)
    df.rename(columns={'nome_r': 'nome'}, inplace=True)

# Rename columns and get first name to use in merge
def prepare_df_dac_comvest_probabilistic_match(df):
    df['primeiro_nome'] = df.apply(lambda x: get_first_name(x['nome']), axis=1)

# Rename columns and get first name to use in merge
def prepare_df_rais_probabilistic_match(df):
    df.rename(columns={'cpf_r': 'cpf'}, inplace=True)
    df.rename(columns={'dta_nasc_r': 'dta_nasc'}, inplace=True)
    df['primeiro_nome'] = df.apply(lambda x: get_first_name(x['nome_r']), axis=1)

# Returns only the first name of the person
def get_first_name(name):
    if type(name) != str:
        return np.nan
    list_names = name.split()
    return list_names[0]

#------------------------------------------------------------------------------------------------
# Merge dataframe with all files from rais to recover missing cpfs
def merge_with_rais(df_dac_comvest, path, is_probabilistic):
    dfs = []
    for year in range(2002, 2019):
        path_year = clean_module.file.get_year_path(year, path)
        df_recovered = merge_with_rais_year(df_dac_comvest, path_year, is_probabilistic)
        dfs.append(df_recovered)

    df = pd.concat(dfs)
    df = df.drop_duplicates()
    return df

# Merge dataframe with all files from some year to recover missing cpfs
def merge_with_rais_year(df_dac_comvest, path, is_probabilistic):
    path_files = path + 'identification_data/'
    files_rais = clean_module.file.get_all_files(path_files, 'pkl')

    dfs = []
    for file in files_rais:
        df_rais = pd.read_pickle(file)
        del df_rais['pispasep']
        if is_probabilistic:
            df_recovered = find_cpf_probabilistic_match(df_dac_comvest, df_rais)
        else:
            df_recovered = find_cpf_exact_match(df_dac_comvest, df_rais)
        dfs.append(df_recovered)

    df = pd.concat(dfs)
    df = df.drop_duplicates()
    return df

#------------------------------------------------------------------------------------------------
# Merge dataframes in name and birthdate, and return all matches
def find_cpf_exact_match(df_dac_comvest, df_rais):
    prepare_df_rais_exact_match(df_rais)
    result = pd.merge(df_dac_comvest, df_rais, on=['nome', 'dta_nasc'])
    if result.empty:
        return result

    result = result[result.apply(lambda x: type(x['cpf']) == str, axis=1)]
    return result

# Merge dataframes in first name and birthdate, and return matches with high similarity
def find_cpf_probabilistic_match(df_dac_comvest, df_rais):
    prepare_df_rais_probabilistic_match(df_rais)
    result = pd.merge(df_dac_comvest, df_rais, on=['primeiro_nome', 'dta_nasc'])
    if result.empty:
        return result

    result['similaridade'] = result.apply(lambda x: get_similarity(x['nome_r'], x['nome']), axis=1)
    result = result[result.apply(lambda x: (type(x['cpf']) == str) and (x['similaridade'] >= MIN_MEDIUM_SIMILARITY), axis=1)]
    return result

# Calculate similarity of names a and b
def get_similarity(a, b):
    if (type(a) != str) or (type(b) != str):
        return 0.0
    nomes_a = a.split()
    nomes_b = b.split()
    sobrenome_a = ' '.join(nomes_a[1:])
    sobrenome_b = ' '.join(nomes_b[1:])
    
    similar_rate = SequenceMatcher(None, sobrenome_a, sobrenome_b).ratio()
    return similar_rate

def remove_invalid_cpf(df):
    df = df[df.apply(lambda x: is_valid_cpf(x['cpf']), axis=1)]
    return df

def is_valid_cpf(value):
    filled_cpf = value.zfill(11)
    cpf = [int(char) for char in filled_cpf if char.isdigit()]

    if len(cpf) != 11:
        return False
    if cpf == cpf[::-1]:
        return False

    #  Valida os dois dígitos verificadores
    for i in range(9, 11):
        valor = sum((cpf[num] * ((i+1) - num) for num in range(0, i)))
        digito = ((valor * 10) % 11) % 10
        if digito != cpf[i]:
            return False
    return True

#------------------------------------------------------------------------------------------------
# Remove duplicated lines according to priority
def fix_duplicated_rows_exact_match(df):
    df = order_by_priority(df)
    get_origem_cpf_column_exact_match(df)
    df = get_dac_information_exact_match(df)
    columns = ['insc_vest', 'ano_ingresso_curso']
    df = clean_module.df_operations.remove_duplicated_rows(df, columns)
    return df

# Remove duplicated lines according to priority
def fix_duplicated_rows_probabilistic_match(df):
    get_origem_cpf_column_probabilistic_match(df)
    df = order_by_similarity(df)
    df = get_dac_information_probabilistic_match(df)
    columns = ['insc_vest', 'ano_ingresso_curso']
    df = clean_module.df_operations.remove_duplicated_rows(df, columns)
    return df

#------------------------------------------------------------------------------------------------
# Order dataframe by priority of the year and state
def order_by_priority(df):
    df['prioridade'] = df.apply(lambda x: get_priority(x['mun_estbl'], x['ano_base']), axis=1)
    df = df.sort_values(by='prioridade', ascending=False)
    del df['prioridade']
    del df['mun_estbl']
    del df['ano_base']
    df = df.drop_duplicates()
    return df

# Order dataframe by similarity between names in rais and dac/comvest
def order_by_similarity(df):
    df = df.sort_values(by='similaridade', ascending=False)
    del df['similaridade']
    return df

# Get the value of priority based on state and year of the register
def get_priority(mun, year):
    if type(mun) == str:
        mun_priority = get_priority_mun(mun)
    else:
        mun_priority = 0
    return mun_priority * 10000 + year

# Get the priority of a city
def get_priority_mun(mun):
    state_code = mun[0:2]
    if state_code == '35':    # SP
        return 3
    elif state_code == '33':  # RJ
        return 2
    elif state_code == '31':  # MG
        return 2
    elif state_code == '32':  # ES
        return 2
    elif state_code == '53':  # DF
        return 1
    return 0

#------------------------------------------------------------------------------------------------
# Create origem_cpf column
def get_origem_cpf_column_exact_match(df):
    columns = ['insc_vest', 'ano_ingresso_curso']
    df['duplicado'] = df.duplicated(subset=columns, keep=False)
    df['origem_cpf'] = df.apply(lambda x: get_origem_cpf_exact_match(x['duplicado']), axis=1)
    del df['duplicado']

# Create origem_cpf column
def get_origem_cpf_column_probabilistic_match(df):
    df['origem_cpf'] = df.apply(lambda x: get_origem_cpf_probabilistic_match(x['similaridade']), axis=1)

# Get origem_cpf according to if the instance is duplicated
def get_origem_cpf_exact_match(is_duplicated):
    if is_duplicated:
        return HOMONIMO
    return UNICO

# Get origem_cpf according to similarity
def get_origem_cpf_probabilistic_match(similarity):
    if similarity >= MIN_HIGH_SIMILARITY:
        return HIGH_SIMILARITY
    return MEDIUM_SIMILARITY

#------------------------------------------------------------------------------------------------
# Filter and rename columns
def get_dac_information_exact_match(df):
    df.rename(columns={'dtanasc': 'dta_nasc'}, inplace=True)
    df = filter_columns_dac_comvest(df)
    return df

# Filter and rename columns
def get_dac_information_probabilistic_match(df):
    df.rename(columns={'dtanasc': 'dta_nasc'}, inplace=True)
    df.rename(columns={'nome_dac_comvest': 'nome'}, inplace=True)
    df = filter_columns_dac_comvest(df)
    return df

# Filter only columns that appear in dac/comvest
def filter_columns_dac_comvest(df):
    columns = ['insc_vest', 'nome', 'origem_cpf', 'dta_nasc', 'ano_ingresso_curso', 'cpf']
    df = df.loc[:, columns]
    df = df.drop_duplicates()
    return df

#------------------------------------------------------------------------------------------------
# Update initial dataframe with recovered cpfs and return resultant dataframe
def update_cpf_dac_comvest(df_cpf_recovered, df_uniao_dac_comvest):
    df_cpf_recovered = df_cpf_recovered.loc[:,['insc_vest', 'ano_ingresso_curso', 'cpf', 'origem_cpf']]
    df_cpf_recovered.rename(columns={'cpf': 'cpf_recovered'}, inplace=True)
    df_cpf_recovered.rename(columns={'origem_cpf': 'origem_cpf_recovered'}, inplace=True)
    df_cpf_recovered['recovered'] = True

    result = df_uniao_dac_comvest.merge(df_cpf_recovered, on=['insc_vest', 'ano_ingresso_curso'], how='left')
    result['cpf'] = result.apply(lambda x: get_cpf(x['recovered'], x['cpf'], x['cpf_recovered']), axis=1)
    result['origem_cpf'] = result.apply(lambda x: int(get_cpf(x['recovered'], x['origem_cpf'], x['origem_cpf_recovered'])), axis=1)

    del result['cpf_recovered']
    del result['origem_cpf_recovered']
    del result['recovered']

    return result

# Return either original cpf or recovered cpf
def get_cpf(was_recovered, value1, value2):
    if was_recovered == True:
        return value2
    return value1
