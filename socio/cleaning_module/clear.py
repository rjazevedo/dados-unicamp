import cleaning_module.database_information
import cleaning_module.cleaning_functions
import pandas as pd

pd.set_option('display.max_columns', None)

# Clear socio database
# Input:
#   file: csv file with socio data
#   path_output: path where the output will be stored
def clear_socio(file, path_output):
    columns_info = cleaning_module.database_information.get_columns_info_socio()
    df = read_file(file, columns_info)
    df = clear_columns(df, columns_info)
    write_file_socio(df, path_output)

# Clear empresa database
# Input:
#   file: csv file with empresa data
#   path_output: path where the output will be stored
def clear_empresa(file, path_output):
    columns_info = cleaning_module.database_information.get_columns_info_empresa()
    df = read_file(file, columns_info)
    df = clear_columns(df, columns_info)
    write_file_empresa(df, path_output)

# Clear cnae_secundaria database
# Input:
#   file: csv file with empresa data
#   path_output: path where the output will be stored
def clear_cnae_secundaria(file, path_output):
    df = read_file_cnae(file)
    df = fix_columns_cnae(df)
    write_file_cnae_secundaria(df, path_output)

#------------------------------------------------------------------------------------------------
def read_file(file, columns_info):
    dtype = cleaning_module.database_information.get_dtype(columns_info, is_original=True)
    df = pd.read_csv(file, dtype=dtype)
    return df

def read_file_cnae(file):
    dtype = {
        0: 'object',
        1: 'object'
    }
    df = pd.read_csv(file, dtype=dtype, header=None)
    return df

def fix_columns_cnae(df):
    df['cnpj'] = df[0]
    df['cnae'] = df[1]
    df = df.loc[:,['cnpj', 'cnae']]
    return df

def write_file_socio(df, path_output):
    file_out = path_output + 'socio.csv'
    df.to_csv(file_out, index=False)

def write_file_empresa(df, path_output):
    file_out = path_output + 'empresa.csv'
    df.to_csv(file_out, index=False)

def write_file_cnae_secundaria(df, path_output):
    file_out = path_output + 'cnae_secundaria.csv'
    df.to_csv(file_out, index=False)

#------------------------------------------------------------------------------------------------
def clear_columns(df, columns_info):
    df = filter_columns(df, columns_info)
    change_column_types(df, columns_info)
    for column in columns_info:
        print('Cleaning:', column)
        clear_column(df, column, columns_info)
    return df

def filter_columns(df, columns_info):
    columns = list(columns_info.keys())
    df = df.loc[:, columns]
    return df

def change_column_types(df, columns_info):
    for column in columns_info:
        if 'has_null_value' in columns_info[column]:
            df[column] = df[column].fillna(-1)
            type_column = columns_info[column]['type']
            df[column] = df[column].astype(type_column)

def clear_column(df, column, columns_info):
    function = columns_info[column]['cleaning_function']
    if function != None:
        df[column] = df[column].map(function)
