from dac.utilities.io import read_from_database
from dac.utilities.io import write_result
from dac.utilities.columns import cursos_habilitacoes_cols
from dac.utilities.format import padronize_int_miss
from dac.utilities.format import padronize_string_miss

FILE_NAME = 'CursosHabilitacoes.xlsx'
RESULT_NAME = 'cursos_habilitacoes.csv'

drop_cols = ['NIVEL', 'NOME CURSO', 'NOME HABILITACAO']

def generate_clean_data():
    cursos_habilitacoes = read_from_database(FILE_NAME)
    cursos_habilitacoes.columns = cursos_habilitacoes_cols
    cursos_habilitacoes.drop(drop_cols, axis=1, inplace=True)

    padronize_string_miss(cursos_habilitacoes, ['codigo_habilitacao'], ' ')
    padronize_int_miss(cursos_habilitacoes, ['ano_ingresso', 'curso', 'total_creditos_curso_hab'], 0)


    return cursos_habilitacoes