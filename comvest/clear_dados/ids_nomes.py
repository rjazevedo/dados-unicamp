"""
Módulo para atribuição de IDs baseados em nomes nos dados Comvest.

Este módulo contém a função para atribuir IDs baseados em nomes aos dados lidos de arquivos CSV.

Funções:
- merge(): Atribui IDs baseados em nomes aos dados e salva o resultado em um arquivo CSV.

Como usar:
Implemente e execute a função `merge` para atribuir IDs baseados em nomes aos dados.
"""


import pandas as pd
from comvest.utilities.io import read_result, read_output, write_result
from comvest.utilities.dtypes import DTYPES_DADOS


def merge():
    """
    Atribui IDs baseados em nomes aos dados e salva o resultado em um arquivo CSV.

    Lê os dados de arquivos CSV, atribui IDs baseados em nomes aos registros e salva o resultado em um novo arquivo CSV.

    Retorna
    -------
    None
    """
    dados = read_result("dados_comvest.csv", DTYPES_DADOS)
    tabela_nomes = read_result("ids_of_names.csv")

    tabela_nomes.columns = [
        'nome_c',
        'id_nome_c'
    ]
    dados = pd.merge(dados, tabela_nomes, how="left")

    tabela_nomes.columns = [
        'nome_pai_c',
        'id_nome_pai_c'
    ]
    dados = pd.merge(dados, tabela_nomes, how="left")

    tabela_nomes.columns = [
        'nome_mae_c',
        'id_nome_mae_c'
    ]
    dados = pd.merge(dados, tabela_nomes, how="left")

    dados["id_nome_c"] = pd.to_numeric(
        dados["id_nome_c"], errors="coerce", downcast="integer"
    ).astype("Int64")
    dados["id_nome_pai_c"] = pd.to_numeric(
        dados["id_nome_pai_c"], errors="coerce", downcast="integer"
    ).astype("Int64")
    dados["id_nome_mae_c"] = pd.to_numeric(
        dados["id_nome_mae_c"], errors="coerce", downcast="integer"
    ).astype("Int64")

    write_result(dados, "dados_comvest.csv")
