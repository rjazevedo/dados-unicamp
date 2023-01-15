import pandas as pd
import glob
import re
import yaml

stream = open('comvest/configuration.yaml')
config = yaml.safe_load(stream)

DATABASE_PATH = config['database']
RESULT_PATH = config['results']
EXTERNAL_OUTPUT = config['external']
AUXILIARY_PATH = config['auxiliary']
DAC_TMP = config['dac_tmp']
DAC = config['dac']

# Gets all the file names and makes a dictionary with
# file path as key and the respective date of the file as its value
files_path = glob.glob(DATABASE_PATH + '*.xlsx')
files = { path: int(re.sub('[^0-9]','',path)) for path in files_path }

def read_from_db(PATH, sheet_name=None, dtype=None):
    return pd.read_excel(PATH, sheet_name=sheet_name, dtype=dtype)

def read_auxiliary(FILE_NAME, dtype=None, sep=',', encoding=None):
    return pd.read_excel(AUXILIARY_PATH + FILE_NAME, dtype=dtype) if '.xls' in FILE_NAME else pd.read_csv(AUXILIARY_PATH + FILE_NAME, dtype=dtype, sep=sep, encoding=encoding)

def read_result(FILE_NAME, database='comvest', dtype=None):
    if database == 'dac':
        return pd.read_csv(DAC_TMP + FILE_NAME, dtype=dtype)
    return pd.read_csv(RESULT_PATH + FILE_NAME, dtype=dtype)

def read_output(FILE_NAME, database='comvest', dtype=None, sep=',', na_values=None):
    if database == 'dac':
        return pd.read_csv(DAC + FILE_NAME, dtype=dtype)
    return pd.read_csv(EXTERNAL_OUTPUT + FILE_NAME, dtype=dtype, sep=sep, na_values=na_values)

def write_result(df, FILE_NAME):
    df.to_csv(RESULT_PATH + FILE_NAME, index=False)

def write_output(df, FILE_NAME):
    df.to_csv(EXTERNAL_OUTPUT + FILE_NAME, index=False)