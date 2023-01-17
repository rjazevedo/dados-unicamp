import pandas as pd
from enum import Enum
import os

class Bases(Enum):
    DAC = "/home/input/DAC/"
    MUNICIPIOS = "/home/input/municipios/"
    COMVEST = "/home/input/COMVEST/"

    RESULT = "/home/output/tmp/"
    OUTPUT = "/home/output/dac/"

    TESTE = "/home/fernando/dados-unicamp/dac/results/"

class DfType(Enum):
    XLS = ".xls"
    CSV = ".csv"

def read_input(FILE_NAME, base=Bases.DAC, dftype=DfType.XLS, converters=None, sheet_name=0, names=None, dtype=None,  sep=','):
    if dftype == DfType.XLS:
        return pd.read_excel(base.value + FILE_NAME, converters=converters, sheet_name=sheet_name, names= names, dtype=dtype)
    else:
        return pd.read_csv(base.value + FILE_NAME, dtype=dtype, sep=sep)

def read_multiple_from_input(FILE_NAMES, base=Bases.DAC, dftype=DfType.XLS, converters=None):
    return pd.concat([read_input(f, base=base, dftype=dftype, converters=converters) for f in FILE_NAMES])

def write_output(df, FILE_NAME):
    df.to_csv(Bases.OUTPUT.value + FILE_NAME, index=False)

def read_result(FILE_NAME, dtype=None, sep=','):
    return pd.read_csv(Bases.RESULT.value + FILE_NAME, dtype=dtype, sep=sep)

def write_result(df, FILE_NAME,):
    df.to_csv(Bases.RESULT.value + FILE_NAME, index=False)

def check_if_need_result_file(df):
    if os.path.exists(Bases.RESULT.value + df):    
        return False
    else: 
        return True