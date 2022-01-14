from utilities.io import read_result
from utilities.io import write_result
from utilities.io import get_identificadores

def get_ids():
    ids = get_identificadores()
    ids = ids.loc[:, ['id', 'insc_vest', 'ano_ingresso_curso']]
    amostra = read_result('amostra.csv', dtype=str, sep=';')
    amostra = amostra.rename(columns={'ano_ingresso' : 'ano_ingresso_curso'})
    amostra_ids = amostra.merge(ids, how='left')
    amostra_ids = amostra_ids[~amostra_ids.id.isna()]
    write_result(amostra_ids, 'amostra_ids.csv')
    