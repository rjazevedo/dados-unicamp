import pandas as pd
from pandas import DataFrame
# Importando cleaning_utils
from utilities.cleaning_utils import clean_string

def compare(df_1: DataFrame, df_2: DataFrame):
    """
    Compara dois DataFrames e retorna as diferenças entre eles.

    Parâmetros
    ----------
    df_1 : DataFrame
        O DataFrame que será comparado com o novo.
    df_2 : DataFrame
        O novo DataFrame que será usado para a comparação.

    Retorna
    -------
    """
    if df_1.equals(df_2):
        return df_1
    else:
        missing_columns, new_columns, commom_columns = compare_columns_name(df_1, df_2)


def compare_columns_name(df_1: DataFrame, df_2: DataFrame) -> set:
    """
    Compara as colunas de dois DataFrames e retorna as diferenças entre elas.

    Parâmetros
    ----------
    df_1 : DataFrame
        O DataFrame que será comparado com o novo.
    df_2 : DataFrame
        O novo DataFrame que será usado para a comparação.

    Retorna
    -------
    missing_columns : set
        As colunas que estão presentes no primeiro DataFrame, mas não estão no segundo.
    new_columns : set
        As colunas que estão presentes no segundo DataFrame, mas não estão no primeiro.
    commom_columns : set
        As colunas que estão presentes em ambos os DataFrames
    """
    df_1.columns.map(clean_string)
    df_2.columns.map(clean_string)
    columns_1 = set(df_1.columns)
    columns_2 = set(df_2.columns)
    
    missing_columns = columns_1 - columns_2
    new_columns = columns_2 - columns_1
    commom_columns = columns_1 & columns_2
    
    return missing_columns, new_columns, commom_columns
    

def compare_rows(df_1: DataFrame, df_2: DataFrame, identifier: str) -> set:
    """
    Compara as linhas de dois DataFrames e retorna as diferenças entre elas.

    Parâmetros
    ----------
    df_1 : DataFrame
        O DataFrame que será comparado com o novo.
    df_2 : DataFrame
        O novo DataFrame que será usado para a comparação.
    identifier : str
        O nome da coluna que será usada para identificar se há diferenças entre as linhas.

    Retorna
    -------
    missing_rows : set
        As linhas que estão presentes no primeiro DataFrame, mas não estão no segundo.
    new_rows : set
        As linhas que estão presentes no segundo DataFrame, mas não estão no primeiro.
    """
    # Se os identificadores forem iguais, então não foi adicionada ou removida nenhuma amostra
    # Ainda é possível que haja diferenças entre os valores das amostras para outras colunas que não o identificador
    if df_1[identifier].equals(df_2[identifier]):
        return None, None
   
    # Se os identificadores forem diferentes, então houve adição ou remoção de amostras
    missing_rows = df_1[~df_1[identifier].isin(df_2[identifier])]
    missing_rows = set(missing_rows[identifier])

    new_rows = df_2[~df_2[identifier].isin(df_1[identifier])]
    new_rows = set(new_rows[identifier])

    return missing_rows, new_rows


# def compare_values(df_1: DataFrame, df_2: DataFrame):

def get_categorical_or_numeric_columns(df: DataFrame) -> tuple:
    """
    Retorna as colunas categóricas e numéricas de um DataFrame.

    Parâmetros
    ----------
    df : DataFrame
        O DataFrame que será usado para a extração das colunas.

    Retorna
    -------
    categorical_columns : set
        As colunas categóricas do DataFrame.
    numeric_columns : set
        As colunas numéricas do DataFrame.
    """
    categorical_columns = []
    numeric_columns = []
    
    for column in df.columns:
        n_elements = column.unique()


    return categorical_columns, numeric_columns