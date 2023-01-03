import numpy as np
import pandas as pd
from unidecode import unidecode


def clean_name(name):
    if pd.isnull(name):
        return ""
    else:
        s = unidecode(name).upper().strip()
        return " ".join(s.split())


def clean_emec(emec):
    if emec == "NI":
        return np.nan
    else:
        return emec


def clean_ano(ano):
    if ano < 1900 or ano > 2020:
        return np.nan
    else:
        return ano


def clean_mes(mes):
    if mes < 1 or mes > 12:
        return np.nan
    else:
        return mes


def clean_cd_area(cod):
    if cod < 1 or cod > 50:
        print(cod)
        return np.nan
    else:
        return cod


def clean_data(data):
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
