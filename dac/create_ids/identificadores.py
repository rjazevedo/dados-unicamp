from utilities.io import read_result
from utilities.io import write_result
from utilities.io import get_identificadores

def generate_ids():
    ids = get_identificadores()
    vida_academica = read_result('vida_academica.csv', dtype=str).loc[:, ['identif', 'insc_vest', 'curso', 'ano_ingresso_curso', 'cod_tipo_ingresso']]
    identifs = vida_academica.merge(ids, on=['insc_vest', 'ano_ingresso_curso'], how='left')
    identifs = identifs[~identifs.id.isna()]
    write_result(identifs, 'identifs.csv')