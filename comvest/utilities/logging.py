"""
Módulo para operações de logging.

Este módulo contém funções para registrar logs de progresso e resultados.

Funções:
- progresslog(sheet_name, year): Registra uma mensagem de log indicando a leitura de uma planilha específica de um arquivo de um determinado ano.
- resultlog(FILE_NAME): Registra uma mensagem de log indicando a escrita de um arquivo de resultado.

Como usar:
Importe as funções deste módulo para registrar logs de progresso e resultados.
"""


import logging


def progresslog(sheet_name, year):
    """
    Registra uma mensagem de log indicando a leitura de uma planilha específica de um arquivo de um determinado ano.

    Parâmetros:
    ----------
    sheet_name : str
        O nome da planilha sendo lida.
    year : int
        O ano do arquivo sendo lido.

    Retorna:
    -------
    None
    """
    logging.info(f'Reading in sheet {sheet_name} of Comvest\'s {year} file')


def resultlog(FILE_NAME):
    """
    Registra uma mensagem de log indicando a escrita de um arquivo de resultado.

    Parâmetros:
    ----------
    FILE_NAME : str
        O nome do arquivo de resultado sendo escrito.

    Retorna:
    -------
    None
    """
    logging.info(f'Writing {FILE_NAME} result')
