"""
Script para ler e padronizar/limpar os dados do Profis.

Este script lê as planilhas do arquivo Profis11a22.xlsx, padroniza e limpa os dados,
e retorna um DataFrame consolidado com os dados processados.

Funções
-------
read_sheets() -> DataFrame
    Lê as planilhas do arquivo Profis11a22.xlsx e retorna um DataFrame consolidado.

clean_data(df: DataFrame) -> DataFrame
    Padroniza e limpa os dados do DataFrame fornecido.

main() -> None
    Função principal que executa o fluxo de leitura, limpeza e exibição dos dados.
"""


import pandas as pd
from pandas import DataFrame


def read_sheets() -> DataFrame:
    """
    Lê as plainhas do arquivo Profis11a22.xlsx
        
    Retorna
    -------
    dict
        Dicionário com os nomes das planilhas como chaves e os DataFrames como valores.
    """
    path = "/home/input/COMVEST/Profis11a22.xlsx"
    return pd.read_excel(path, sheet_name=None)


def clean_data():
    """
    Padroniza e limpa os dados do DataFrame fornecido.
    
    Parâmetros
    ----------
    df : DataFrame
        DataFrame com os dados a serem padronizados e limpos.
    
    Retorna
    -------
    DataFrame
        DataFrame com os dados padronizados e limpos.
    """
    sheets = read_sheets()
    
    for sheet_name, df in sheets.items():
        print(f"Processando planilha: {sheet_name}")
        cleaned_df = clean_data(df)
    
    

