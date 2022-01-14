import pandas as pd
from utilities.io import read_result, read_from, write_result

def rescue():
    COMVEST_2019_PATH = '/home/gproenca/DadosProjetoFernandaFGV/auxiliares/dados/ingresso2019.csv'
    non_identif = read_result('nonidentif.csv', dtype=str)
    comvest2019 = read_from(COMVEST_2019_PATH, dtype=str)
    comvest2019.rename({'ano_vest' : 'ano_ingresso_curso'}, inplace=True, axis=1)
    
    rescued2019 = non_identif.merge(comvest2019.loc[:, ['ano_ingresso_curso', 'insc_vest']], on=['ano_ingresso_curso', 'insc_vest'])
    rescued2019['rescued'] = 1
    non_identif['rescued'] = 0

    non_identif = pd.concat([rescued2019, non_identif])
    non_identif.drop_duplicates(subset=['ano_ingresso_curso', 'insc_vest'], inplace=True, keep='first')
    
    rescued2019 = non_identif[non_identif.rescued == 1].drop(['rescued'], axis=1)
    non_identif = non_identif[non_identif.rescued == 0].drop(['rescued'], axis=1)

    write_result(rescued2019, 'explore/rescued2019.csv')
    write_result(non_identif, 'explore/non_rescued.csv')