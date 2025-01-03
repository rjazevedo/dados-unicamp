"""
Módulo para criação do dicionário de cursos Comvest.

Este módulo contém a função principal para criar um dicionário de cursos Comvest combinando dados de diferentes fontes.

Funções:
- get(): Cria o dicionário de cursos Comvest.

Como usar:
Implemente e execute a função para criar o dicionário de cursos Comvest.
"""


import pandas as pd
from comvest.utilities.io import read_auxiliary ,read_result, write_result

def get():
    """
    Cria o dicionário de cursos Comvest.

    Esta função lê os dados dos cursos de diferentes fontes, combina os dados, remove duplicatas e escreve o resultado em um arquivo CSV.

    Retorna
    -------
    None
    """
    cursos_dac = read_auxiliary('cursos_dac.xlsx', dtype={'ANO':'Int64','CURSO':'Int64'}).loc[:,['ANO','CURSO']]
    cursos_comvest = read_result('cursos_comvest.csv').loc[:, ['ano_vest','cod_curso']]

    cursos_dac.columns = cursos_comvest.columns

    cursos = pd.concat([cursos_dac, cursos_comvest])

    cursos.drop_duplicates(subset=['ano_vest','cod_curso'], inplace=True)
    cursos.sort_values(by='ano_vest', ascending=False, inplace=True)

    write_result(cursos, 'cursos.csv')
    