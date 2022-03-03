import pandas as pd
from comvest.utilities.io import read_output, write_output
from comvest.utilities.dtypes import DTYPES_DADOS, DTYPES_PERFIL, DTYPES_MATRICULADOS, DTYPES_NOTAS


def assign_ids():
    comvest = read_output('comvest_amostra.csv', dtype={**DTYPES_DADOS, **DTYPES_PERFIL, **DTYPES_MATRICULADOS, **DTYPES_NOTAS})

    ids = read_output('dac_comvest_ids.csv', dtype={'id':'int64', 'insc_vest':'Int64', 'ano_ingresso_curso':'int64'}, sep=';', na_values={'insc_vest': 'n'}).loc[:, ['id','insc_vest','ano_ingresso_curso']]
    ids.columns = ['id', 'insc_vest', 'ano_vest']
    ids['insc_vest'] = ids['insc_vest'].fillna(0)


    comvest_with_ids = pd.merge(ids, comvest, on=['insc_vest','ano_vest'])
    comvest_with_ids.drop_duplicates(subset=['insc_vest','ano_vest'], inplace=True)
    comvest_with_ids.drop(columns=['insc_vest'], inplace=True)

    write_output(comvest_with_ids, 'comvest_amostra.csv')