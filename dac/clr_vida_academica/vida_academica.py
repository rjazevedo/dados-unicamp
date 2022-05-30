from dac.utilities.io import read_from_database
from dac.utilities.io import write_result
from dac.utilities.io import write_output
from dac.utilities.columns import vida_academica_cols
from dac.utilities.format import str_to_upper_ascii
from dac.utilities.format import padronize_int_miss

FILE_NAME = 'VidaAcademicaCurso.xlsx'
RESULT_NAME = 'vida_academica.csv'
INDICES_NAME = 'indices.csv'

def generate_clean_data():
    vida_academica = read_from_database(FILE_NAME)
    vida_academica.columns = vida_academica_cols

    str_to_upper_ascii(vida_academica, ['curso_atual_nome', 'tipo_ingresso', 'motivo_saida', 'cota_d', 'cota_tipo', 'cota_descricao'])
    vida_academica.insc_vest = vida_academica.insc_vest.astype(str).str[:-2]
    padronize_int_miss(vida_academica, ['ano_saida', 'opcao_vest'], 0)
    write_result(vida_academica, RESULT_NAME)

    indices = vida_academica.loc[:, ['insc_vest', 'ano_ingresso_curso', 'identif', 'curso']]
    write_result(indices, INDICES_NAME)
    return vida_academica, indices