import pandas as pd
import yaml

stream = open('configuration.yaml')
config = yaml.safe_load(stream)

DATABASE_PATH = config['database']
RESULT_PATH = config['results']
EXTERNAL_OUTPUT = config['external']

def read_from_database(FILE_NAME, converters=None):
    return pd.read_excel(DATABASE_PATH + FILE_NAME, converters=converters)

def read_from_external(FILE_NAME, converters=None):
    return pd.read_excel(EXTERNAL_OUTPUT + FILE_NAME, converters=converters)

def read_multiple_from_database(FILE_NAMES, converters=None):
    return pd.concat([read_from_database(f, converters) for f in FILE_NAMES])

def read_result(FILE_NAME, dtype=None, sep=','):
    return pd.read_csv(RESULT_PATH + FILE_NAME, dtype=dtype, sep=sep)

def read_from(FILENAME, dtype=None, sep=','):
    return pd.read_csv(FILENAME, dtype=dtype, sep=sep)

def write_result(df, FILE_NAME):
    df.to_csv(RESULT_PATH + FILE_NAME, index=False)