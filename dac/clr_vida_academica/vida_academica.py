from utilities.io import read_from_database
from utilities.io import write_result
from utilities.columns import vida_academica_cols
from utilities.format import str_to_upper_ascii

FILE_NAME = 'VidaAcademicaCurso.xlsx'
RESULT_NAME = 'vida_academica.csv'
INDICES_NAME = 'indices.csv'

def generate_clean_data():
    vida_academica = read_from_database(FILE_NAME)
    vida_academica.columns = vida_academica_cols


    str_to_upper_ascii(vida_academica, ['curso_nome', 'tipo_ingresso', 'motivo_saida', 'cota', 'cota_tipo', 'cota_descricao'])
    vida_academica.insc_vest = vida_academica.insc_vest.astype(str).str[:-2]
    write_result(vida_academica, RESULT_NAME)

    indices = vida_academica.loc[:, ['insc_vest', 'ano_ingresso_curso', 'identif', 'curso']]
    write_result(indices, INDICES_NAME)
    return vida_academica, indices