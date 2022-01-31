import rais.clean_module.rais_information
import pandas as pd

from rais.utilities.read import read_rais_sample
from rais.utilities.read import read_database

from rais.verification.verification_functions import check_deslig
from rais.verification.verification_functions import check_cnpj_raiz

# Verify all columns in rais.csv
def verify_output():
    df = read_rais_sample()
    verify_columns(df)

# Verify all columns in df and print if any has an invalid value
def verify_columns(df):
    set_global_variables()
    columns_info = rais.clean_module.rais_information.get_columns_info_rais()
    for column in columns_info:
        verify_column(column, df)
    verify_cnpj_raiz(df)
    verify_deslig_info(df)

# Verify column in df and print if it has an invalid value
def verify_column(column, df):
    print('Verifying', column)
    columns_info = rais.clean_module.rais_information.get_columns_info_rais()
    function = columns_info[column]['check_function']
    missed = df[df.apply(lambda x: not function(x[column]), axis=1)]
    if not missed.empty:
        values = missed.loc[:,[column]]
        print(values.head())

#------------------------------------------------------------------------------------------------
# Verify cnpj_raiz in df and print if it has an invalid value
def verify_cnpj_raiz(df):
    missed = df[df.apply(lambda x: not check_cnpj_raiz(x['cnpj'], x['cnpj_raiz']), axis=1)]
    if not missed.empty:
        values = missed.loc[:,['cnpj_raiz', 'cnpj']]
        print(values.head())

# Verify deslig_info in df and print if it has an invalid value
def verify_deslig_info(df):
    missed = df[df.apply(lambda x: not check_deslig(x['deslig_motivo'], x['deslig_mes'], x['deslig_dia']), axis=1)]
    if not missed.empty:
        values = missed.loc[:,['deslig_motivo', 'deslig_mes', 'deslig_dia']]
        print(values.head())

#------------------------------------------------------------------------------------------------
# Set global variables with all available codes to columns mun, cnae, cbo and nat_juridica
def set_global_variables():
    file = '/home/larissa/dados-unicamp/rais/clean_module/codes/municipios.csv'
    dtype = {'municipio': 'object'}
    global municipios
    municipios = read_database(file, dtype, squeeze=True)

    file = '/home/larissa/dados-unicamp/rais/clean_module/codes/cnae95.csv'
    dtype = {'cnae95': 'object'}
    global cnae95
    cnae95 = read_database(file, dtype, squeeze=True)

    file = '/home/larissa/dados-unicamp/rais/clean_module/codes/cbo94.csv'
    dtype = {'cbo94': 'object'}
    global cbo94
    cbo94 = read_database(file, dtype, squeeze=True)

    file = '/home/larissa/dados-unicamp/rais/clean_module/codes/nat_juridica.csv'
    dtype = {'nat_juridica': 'object'}
    global nat_juridica
    nat_juridica = read_database(file, dtype, squeeze=True)

    file = '/home/larissa/dados-unicamp/rais/clean_module/codes/cbo02.csv'
    dtype = {'cbo02': 'object'}
    global cbo02
    cbo02 = read_database(file, dtype, squeeze=True)

    file = '/home/larissa/dados-unicamp/rais/clean_module/codes/cnae20classe.csv'
    dtype = {'cnae20classe': 'object'}
    global cnae20classe
    cnae20classe = read_database(file, dtype, squeeze=True)

    file = '/home/larissa/dados-unicamp/rais/clean_module/codes/cnae20subclasse.csv'
    dtype = {'cnae20subclasse': 'object'}
    global cnae20subclasse
    cnae20subclasse = read_database(file, dtype, squeeze=True)
