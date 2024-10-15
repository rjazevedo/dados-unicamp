import numpy as np
import pandas as pd
from unidecode import unidecode


def clean_name(name):
    """
    Limpa o nome fornecido, removendo acentos, convertendo para maiúsculas 
    e eliminando espaços em branco extras.

    Parâmetros:
        name (str): O nome a ser limpo.

    Retorna:
        str: O nome limpo, ou uma string vazia se o nome for nulo.
    """
    if pd.isnull(name):
        return ""
    else:
        s = unidecode(name).upper().strip()
        return " ".join(s.split())


def clean_emec(emec):
    """
    Limpa o valor do emec, retornando NaN para valores inválidos.

    Parâmetros:
        emec (str): O valor do emec a ser limpo.

    Retorna:
        str ou np.nan: O valor do emec limpo ou NaN se o valor for inválido.
    """
    if pd.isna(emec):
        return np.nan
    if emec == "NI":
        return np.nan
    else:
        return emec


def clean_ano(ano):
    """
    Limpa o valor do ano, retornando NaN para anos inválidos.

    Parâmetros:
        ano (int): O ano a ser limpo.

    Retorna:
        int ou np.nan: O ano limpo ou NaN se o ano for inválido.
    """
    if pd.isna(ano):
        return np.nan
    if ano < 1900 or ano > 2022:
        return np.nan
    else:
        return ano


def clean_ano_str(ano):
    """
    Limpa o valor do ano a partir de uma string, retornando NaN para anos inválidos.

    Parâmetros:
        ano (str): O ano em formato de string a ser limpo.

    Retorna:
        int ou np.nan: O ano limpo ou NaN se o ano for inválido.
    """
    ano = int(ano)
    if ano < 1900 or ano > 2022:
        return np.nan
    else:
        return ano


def clean_mes(mes):
    """
    Limpa o valor do mês, retornando NaN para meses inválidos.

    Parâmetros:
        mes (int): O mês a ser limpo.

    Retorna:
        int ou np.nan: O mês limpo ou NaN se o mês for inválido.
    """
    if pd.isna(mes):
        return np.nan
    if mes < 1 or mes > 12:
        return np.nan
    else:
        return mes


def clean_cd_area(cod):
    """
    Limpa o código da área, retornando NaN para códigos inválidos.

    Parâmetros:
        cod (int): O código da área a ser limpo.

    Retorna:
        int ou np.nan: O código da área limpo ou NaN se o código for inválido.
    """
    if cod < 1 or cod > 50:
        print(cod)
        return np.nan
    else:
        return cod


def clean_data(data):
    """
    Limpa a data fornecida no formato 'DDMMMYY' e a converte para o formato 'DDMMYYYY'.

    Parâmetros:
        data (str): A data a ser limpa no formato 'DDMMMYY'.

    Retorna:
        str: A data limpa no formato 'DDMMYYYY'.
    """
    meses = {
        "JAN": "01",
        "FEB": "02",
        "MAR": "03",
        "APR": "04",
        "MAY": "05",
        "JUN": "06",
        "JUL": "07",
        "AUG": "08",
        "SEP": "09",
        "OCT": "10",
        "NOV": "11",
        "DEC": "12",
    }
    dia = data[0:2]
    mes = data[2:5]
    mes = meses[mes]
    ano = data[5:7]

    if int(ano[0]) > 2:
        ano = "19" + ano
    else:
        ano = "20" + ano

    return dia + mes + ano
