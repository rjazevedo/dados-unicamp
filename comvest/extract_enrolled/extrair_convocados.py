import pandas as pd
from comvest.utilities.io import read_auxiliary, read_result, write_result


def extraction():
    convocados = read_auxiliary(
        'ConvocadosMatriculadosLista87a21.xlsx',
        dtype={'ano':'Int64','insc':str,'curso':'Int64','lista':'Int64'}
    )
    matriculados = read_result('matriculados_comvest.csv', dtype={'curso_matric':'Int64'})

    convocados.rename(columns={'ano':'ano_vest','insc':'insc_vest','curso':'curso_convocado','convocado':'convoc','matrfim':'matric','lista':'chamada_vest'}, inplace=True)
    convocados['insc_vest'] = convocados.apply(lambda row: str(row['ano_vest'])[-2:] + row['insc_vest'] if row['ano_vest'] in [2002,2003] else row['insc_vest'], axis=1)
    convocados['insc_vest'] = pd.to_numeric(convocados['insc_vest'], errors='coerce', downcast='integer').astype('Int64')
    convocados = convocados.merge(matriculados, on=['ano_vest','insc_vest'], how='outer')
    convocados.sort_values(by='ano_vest', ascending=False, inplace=True)

    FILE_NAME = 'matriculados_comvest.csv'
    write_result(convocados, FILE_NAME)