import pandas as pd

def filter_by_year(df, years):
    return df[df['ano_vest'].isin(years)]['id']

def filter_by_course(df, courses, db):
    if db == 'comvest':
        return df.loc[
            (df['opc1'].isin(courses)) |
            (df['opc2'].isin(courses)) | 
            (df['opc3'].isin(courses)) | 
            (df['curso_matric'].isin(courses)) |
            (df['curso_aprovado'].isin(courses))
            ]['id']
    elif db == 'dac':
        return df[df['curso'].isin(courses)]['id']