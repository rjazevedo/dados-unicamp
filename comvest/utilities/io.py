import pandas as pd
from enum import Enum
import glob
import re

class Bases(Enum):
    COMVEST = "/home/input/COMVEST/"
    RESULT = "/home/output/intermediario/"
    OUTPUT = "/home/output/comvest/"
    DAC_OUTPUT = "/home/output/comvest/"
    AUXILIARY = "/home/input/COMVEST/auxiliary/"
    TESTE = "/home/fernando/dados-unicamp/output/"

class DfType(Enum):
    XLS = ".xls"
    CSV = ".csv"

# Gets all the file names and makes a dictionary with
# file path as key and the respective date of the file as its value
files_path = glob.glob(Bases.COMVEST.value + '*.xlsx')
files = { path: int(re.sub('[^0-9]','',path)) for path in files_path }

def read_from_db(PATH, sheet_name=None, dtype=None):
    return pd.read_excel(PATH, sheet_name=sheet_name, dtype=dtype)

def read_auxiliary(FILE_NAME, dtype=None, sep=',', encoding=None):
    auxiliary = Bases.AUXILIARY.value
    return pd.read_excel(auxiliary + FILE_NAME, dtype=dtype) if '.xls' in FILE_NAME else pd.read_csv(auxiliary + FILE_NAME, dtype=dtype, sep=sep, encoding=encoding)

def read_result(FILE_NAME, dtype=None):
    return pd.read_csv(Bases.RESULT.value + FILE_NAME, dtype=dtype)

def read_output(FILE_NAME, database='comvest', dtype=None, sep=',', na_values=None):
    if database == 'dac':
        return pd.read_csv(DAC_OUTPUT.value + FILE_NAME, dtype=dtype)
    return pd.read_csv(Bases.OUTPUT.value + FILE_NAME, dtype=dtype, sep=sep, na_values=na_values)

def write_result(df, FILE_NAME):
    df.to_csv(Bases.RESULT.value + FILE_NAME, index=False)

def write_output(df, FILE_NAME):
    df.to_csv(Bases.OUTPUT.value + FILE_NAME, index=False)

def check_if_need_result_file(df):
    if os.path.exists(Bases.RESULT.value + df):    
        return False
    else: 
        return True
