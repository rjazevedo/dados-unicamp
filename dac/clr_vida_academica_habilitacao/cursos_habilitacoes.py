from dac.utilities.io import read_input
from dac.utilities.io import write_result
from dac.utilities.columns import cursos_habilitacoes_cols
from dac.utilities.format import padronize_int_miss
from dac.utilities.format import padronize_string_miss

# Todo: Checar se o que o rodolfo transferiu é o atualizado
#FILE_NAME = 'CursosHabilitacoesAtualizado.xlsx'
FILE_NAME = 'Cursos_Habilitacoes.xlsx'
RESULT_NAME = 'cursos_habilitacoes.csv'

drop_cols = ['NIVEL', 'NOME CURSO', 'NOME HABILITACAO']

def generate_clean_data():
    cursos_habilitacoes = read_input(FILE_NAME)
    cursos_habilitacoes.columns = cursos_habilitacoes_cols
    cursos_habilitacoes.drop(drop_cols, axis=1, inplace=True)
    
    padronize_string_miss(cursos_habilitacoes, ['codigo_habilitacao'], ' ')
    padronize_string_miss(cursos_habilitacoes, ['tp_integralizacao_sugerido'], '<null>')
    cursos_habilitacoes['tp_integralizacao_sugerido'] = cursos_habilitacoes['tp_integralizacao_sugerido'].replace('', '0', regex=True).astype('Int64')

    padronize_int_miss(cursos_habilitacoes, ['ano_ingresso', 'curso', 'total_creditos_curso_hab', 'total_horas_curso_hab','tp_integralizacao_sugerido',
            'tp_integralizacao_max'], 0)
    return cursos_habilitacoes