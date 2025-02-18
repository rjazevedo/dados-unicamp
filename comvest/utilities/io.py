"""
Módulo para operações de entrada e saída de dados.

Este módulo contém funções para ler dados de arquivos Excel e CSV, além de classes enumeradas para definir caminhos base e tipos de arquivos.

Classes:
- Bases: Enumeração que define os caminhos base para diferentes tipos de dados.
- DfType: Enumeração que define os tipos de arquivos suportados (XLS e CSV).

Funções:
- read_from_db(PATH, sheet_name=None, dtype=None): Lê dados de um arquivo Excel.
- read_auxiliary(FILE_NAME, dtype=None, sep=",", encoding=None): Lê dados de um arquivo auxiliar (Excel ou CSV).
- read_result(FILE_NAME, dtype=None, na_values=None): Lê dados de um arquivo CSV da pasta de resultados.
- read_output(FILE_NAME, database="comvest", dtype=None, sep=",", na_values=None): Lê dados de um arquivo CSV da pasta de saída.
- write_result(df, FILE_NAME): Escreve um DataFrame em um arquivo CSV na pasta de resultados.
- write_output(df, FILE_NAME): Escreve um DataFrame em um arquivo CSV na pasta de saída.
- check_if_need_result_file(df): Verifica se um arquivo de resultado já existe.

Como usar:
Importe as funções e classes deste módulo para ler dados de arquivos Excel e CSV.

Exemplo:
import pandas as pd
from io import read_from_db, read_auxiliary, Bases

df = read_from_db(Bases.COMVEST.value + 'file.xlsx')
aux_df = read_auxiliary('auxiliary_file.csv')
"""


import pandas as pd
from enum import Enum
import glob
import re
import os

class Bases(Enum):
    """
    Enumeração que define os caminhos base para diferentes tipos de dados.
    """
    COMVEST = "/home/input/COMVEST/"
    RESULT = "/home/output/intermediario/"
    OUTPUT = "/home/output/comvest/"
    DAC_OUTPUT = "/home/output/dac/"
    AUXILIARY = "/home/input/COMVEST/auxiliary/"
    TESTE = "/home/fernando/dados-unicamp/output/"


class DfType(Enum):
    """
    Enumeração que define os tipos de arquivos suportados.
    """
    XLS = ".xls"
    CSV = ".csv"


# Gets all the file names and makes a dictionary with
# file path as key and the respective date of the file as its value
files_path = glob.glob(Bases.COMVEST.value + "*.xlsx")
files = {path: int(re.sub("[^0-9]", "", path)) for path in files_path}


def read_from_db(PATH, sheet_name=None, dtype=None):
    """
    Lê dados de um arquivo Excel.

    Parâmetros
    ----------
    PATH : str
        O caminho do arquivo Excel.
    sheet_name : str, opcional
        O nome da planilha a ser lida. Se None, lê a primeira planilha.
    dtype : dict, opcional
        Um dicionário que mapeia os nomes das colunas para seus tipos de dados.

    Retorna
    -------
    DataFrame
        Um DataFrame contendo os dados lidos do arquivo Excel.
    """
    return pd.read_excel(PATH, sheet_name=sheet_name, dtype=dtype)


def read_auxiliary(FILE_NAME, dtype=None, sep=",", encoding=None):
    """
    Lê dados de um arquivo auxiliar (Excel ou CSV).

    Parâmetros
    ----------
    FILE_NAME : str
        O nome do arquivo auxiliar.
    dtype : dict, opcional
        Um dicionário que mapeia os nomes das colunas para seus tipos de dados.
    sep : str, opcional
        O delimitador a ser usado se o arquivo for CSV. O padrão é ','.
    encoding : str, opcional
        A codificação a ser usada se o arquivo for CSV.

    Retorna
    -------
    DataFrame
        Um DataFrame contendo os dados lidos do arquivo auxiliar.
    """
    auxiliary = Bases.AUXILIARY.value
    return (
        pd.read_excel(auxiliary + FILE_NAME, dtype=dtype)
        if ".xls" in FILE_NAME
        else pd.read_csv(auxiliary + FILE_NAME, dtype=dtype, sep=sep, encoding=encoding)
    )


def read_result(FILE_NAME, dtype=None, na_values=None):
    """
    Lê dados de um arquivo CSV da pasta de resultados.

    Parâmetros
    ----------
    FILE_NAME : str
        O nome do arquivo CSV.
    dtype : dict, opcional
        Um dicionário que mapeia os nomes das colunas para seus tipos de dados.
    na_values : scalar, str, list-like, or dict, opcional
        Valores adicionais a serem considerados como NA/NaN.

    Retorna
    -------
    DataFrame
        Um DataFrame contendo os dados lidos do arquivo CSV.
    """
    return pd.read_csv(Bases.RESULT.value + FILE_NAME, dtype=dtype, na_values=na_values, low_memory=False, on_bad_lines='skip')


def read_output(FILE_NAME, database="comvest", dtype=None, sep=",", na_values=None):
    """
    Lê dados de um arquivo CSV da pasta de saída.

    Parâmetros
    ----------
    FILE_NAME : str
        O nome do arquivo CSV.
    database : str, opcional
        O banco de dados de onde ler os dados. Pode ser 'comvest' ou 'dac'. O padrão é 'comvest'.
    dtype : dict, opcional
        Um dicionário que mapeia os nomes das colunas para seus tipos de dados.
    sep : str, opcional
        O delimitador a ser usado. O padrão é ','.
    na_values : scalar, str, list-like, or dict, opcional
        Valores adicionais a serem considerados como NA/NaN.

    Retorna
    -------
    DataFrame
        Um DataFrame contendo os dados lidos do arquivo CSV.
    """
    if database == "dac":
        return pd.read_csv(Bases.DAC_OUTPUT.value + FILE_NAME, dtype=dtype)
    return pd.read_csv(
        Bases.OUTPUT.value + FILE_NAME, dtype=dtype, sep=sep, na_values=na_values
    )


def write_result(df, FILE_NAME):
    """
    Escreve um DataFrame em um arquivo CSV na pasta de resultados.

    Parâmetros
    ----------
    df : DataFrame
        O DataFrame a ser escrito.
    FILE_NAME : str
        O nome do arquivo CSV.

    Retorna
    -------
    None
    """
    df.to_csv(Bases.RESULT.value + FILE_NAME, index=False)


def write_output(df, FILE_NAME):
    """
    Escreve um DataFrame em um arquivo CSV na pasta de saída.

    Parâmetros
    ----------
    df : DataFrame
        O DataFrame a ser escrito.
    FILE_NAME : str
        O nome do arquivo CSV.

    Retorna
    -------
    None
    """
    df.to_csv(Bases.OUTPUT.value + FILE_NAME, index=False)


def check_if_need_result_file(df):
    """
    Verifica se um arquivo de resultado já existe.

    Parâmetros
    ----------
    df : str
        O nome do arquivo CSV.

    Retorna
    -------
    bool
        True se o arquivo não existe, False caso contrário.
    """
    if os.path.exists(Bases.RESULT.value + df):
        return False
    else:
        return True
