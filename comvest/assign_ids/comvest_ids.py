import pandas as pd
from comvest.utilities.io import read_output, write_output


def assign_ids():
    comvest = read_output('comvest_amostra.csv')

    ids = read_output('dac_comvest_ids.csv', sep=';').loc[:, ['id','insc_vest','ano_ingresso_curso']]
    ids.columns = ['id', 'insc_vest', 'ano_vest']


    comvest_with_ids = pd.merge(comvest, ids, on=['insc_vest','ano_vest'], how='left')

    write_output(comvest_with_ids, 'comvest_amostra.csv')