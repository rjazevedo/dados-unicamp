"""
Este script fornece funções utilitárias para leitura e escrita de dados relacionados ao Enem e à Comvest para a Unicamp.

Módulos necessários:
- pandas: Para manipulação de dados em DataFrames.
- enum: Para definição de enumerações.
- glob: Para manipulação de caminhos de arquivos.
- re: Para operações com expressões regulares.
- os: Para manipulação de arquivos e diretórios.

Classes:
- Bases: Enumeração que define os caminhos base para os arquivos de resultados e dados combinados do Enem e Comvest.

Funções:
- read_result(FILENAME): Lê um arquivo CSV de resultados.
- write_result(df, FILENAME): Escreve um DataFrame em um arquivo CSV de resultados.
- read_comvest_grades(): Lê os arquivos de notas da Comvest e retorna um dicionário com os DataFrames das notas.

Como usar:
Importe as funções `read_result`, `write_result` e `read_comvest_grades` para manipular os dados do Enem e da Comvest.
"""


import pandas as pd
from pandas import DataFrame
from enum import Enum
import glob
import re
import os

class Bases(Enum):
    """
    Enumeração que define os caminhos base para os arquivos de resultados e dados combinados do Enem e Comvest.
    """
    RESULT = "/home/output/intermediario/"
    ENEM_COMVEST = "/home/output/intermediario/Enem_Comvest/"


def read_result(FILENAME: str) -> DataFrame:
    """
    Lê um arquivo CSV de resultados.

    Parâmetros
    ----------
    FILENAME : str
        O nome do arquivo a ser lido.

    Retorna
    -------
    DataFrame
        O DataFrame contendo os dados lidos do arquivo CSV.
    """
    return pd.read_csv(Bases.RESULT.value + FILENAME, low_memory=False)


def write_result(df: DataFrame, FILENAME: str) -> None:
    """
    Escreve um DataFrame em um arquivo CSV de resultados.

    Parâmetros
    ----------
    df : DataFrame
        O DataFrame a ser escrito no arquivo.
    FILENAME : str
        O nome do arquivo onde os dados serão escritos.

    Retorna
    -------
    None
    """
    df.to_csv(Bases.RESULT.value + FILENAME, index=False)


def read_comvest_grades() -> dict[int, DataFrame]:
    """
    Lê os arquivos de notas da Comvest e retorna um dicionário com os DataFrames das notas.

    Retorna
    -------
    dict
        Um dicionário onde as chaves são os anos e os valores são os DataFrames contendo as notas da Comvest.
    """
    grades = {}

    for file in os.listdir(Bases.ENEM_COMVEST.value):
        if 'Enem' in file[0:5]:
            grade = pd.read_csv(Bases.ENEM_COMVEST.value + file, low_memory=False)
            year = int(file[11:15])
            grades.update({year : grade})

    return grades
