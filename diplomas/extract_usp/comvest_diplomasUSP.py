import pandas as pd
from diplomas.utilities.io import read_result

def merge():
    DIPLOMAS_FILE = 'usp-diplomados.csv'
    COMVEST_FILE = 'dados_comvest.csv'

    FINAL = 'diplomados_extraction.csv'
    diplomas = read_result(DIPLOMAS_FILE)
    comvest = read_result(COMVEST_FILE)

    comvest_nomes = comvest.loc[:, ['id_nome_c', 'nome_c', 'ano_vest']]
    comvest_nomes = comvest_nomes.rename(columns={'nome_c' : 'nome', 'ano_vest' : 'ano_realizacao_comvest'})
    diplomas_ids = diplomas.merge(comvest_nomes, how='left')

    diplomas_ids.drop_duplicates(inplace=True)

    diplomas_ids.to_csv(FINAL, index=False)