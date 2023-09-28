import pandas as pd

DIPLOMAS_FILE = '/home/output/intermediario/usp-diplomados.csv'
COMVEST_FILE = '/home/output/intermediario/dados_comvest.csv'

FINAL = '/home/processados/diplomados/diplomados_extraction.csv'
diplomas = pd.read_csv(DIPLOMAS_FILE)
comvest = pd.read_csv(COMVEST_FILE)

comvest_nomes = comvest.loc[:, ['id_nome_c', 'nome_c', 'ano_vest']]
comvest_nomes = comvest_nomes.rename(columns={'nome_c' : 'nome', 'ano_vest' : 'ano_realizacao_comvest'})
diplomas_ids = diplomas.merge(comvest_nomes, how='left')

diplomas_ids.drop_duplicates(inplace=True)

diplomas_ids.to_csv(FINAL, index=False)