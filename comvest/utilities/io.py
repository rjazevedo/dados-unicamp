import pandas as pd
import glob
import re
import yaml

stream = open('comvest/configuration.yaml')
config = yaml.safe_load(stream)

DATABASE_PATH = config['database']
RESULT_PATH = config['results']
EXTERNAL_OUTPUT = config['external']

# Gets all the file names and makes a dictionary with
# file path as key and the respective date of the file as its value
files_path = glob.glob(DATABASE_PATH + '*')
files = { path: int(re.sub('[^0-9]','',path)) for path in files_path }

def read_from_db(PATH, sheet_name):
    return pd.read_excel(PATH, sheet_name=sheet_name)

def read_result(FILE_NAME):
    return pd.read_csv(RESULT_PATH + FILE_NAME)

def read_output(FILE_NAME, dtype=None, sep=','):
    return pd.read_csv(EXTERNAL_OUTPUT + FILE_NAME, dtype=dtype, sep=sep)

def write_result(df, FILE_NAME):
    df.to_csv(RESULT_PATH + FILE_NAME, index=False)

def write_output(df, FILE_NAME):
    df.to_csv(EXTERNAL_OUTPUT + FILE_NAME, index=False)