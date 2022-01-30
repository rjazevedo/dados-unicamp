import pandas as pd


comvest_2000_2018 = pd.read_csv('resultados/comvest_2000-2018.csv', dtype=str)

ids = pd.read_csv('dac_comvest_ids.csv', dtype=str, sep=';').loc[:, ['id','insc_vest','ano_ingresso_curso']]
ids.columns = ['id', 'insc_vest', 'ano_vest']


new_db = pd.merge(comvest_2000_2018, ids, on=['insc_vest','ano_vest'])

new_db.to_csv('bases finais/base_comvest-2000_2018.csv', index=False)