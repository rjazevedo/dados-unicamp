import pandas as pd

def filter_by_year(df):
    # FILTRO HARD CODED PARA TESTE
    years = [2004, 2012, 2018]

    return df[df['ano_vest'].isin(years)]

def filter_by_course(df):
    # FILTRO HARD CODED PARA TESTE
    courses = [3, 42]

    return df.loc[
        (df['opc1'].isin(courses)) |
        (df['opc2'].isin(courses)) | 
        (df['opc3'].isin(courses)) | 
        (df['curso_matric'].isin(courses)) |
        (df['curso_aprovado'].isin(courses))
        ]