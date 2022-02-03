import pandas as pd


def assign_ids():
    comvest = pd.read_csv('output/comvest_amostra.csv', dtype=str)

    ids = pd.read_csv('dac_comvest_ids.csv', dtype=str, sep=';').loc[:, ['id','insc_vest','ano_ingresso_curso']]
    ids.columns = ['id', 'insc_vest', 'ano_vest']


    comvest_with_ids = pd.merge(comvest, ids, on=['insc_vest','ano_vest'], how='left')

    comvest_with_ids.to_csv('output/comvest_amostra.csv', index=False)