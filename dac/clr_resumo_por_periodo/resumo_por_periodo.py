#TODO: merge com vida academica leva em conta o ano de ingresso e identificação /s curso
from dac.utilities.io import read_from_database
from dac.utilities.io import write_result
from dac.utilities.io import write_output
from dac.utilities.columns import resumo_por_periodo_cols
from dac.utilities.format import padronize_dates
from dac.utilities.format import str_to_upper_ascii
from dac.utilities.format import padronize_string_miss
from dac.utilities.format import padronize_int_miss
import pandas as pd

DATABASE_FILE = 'ResumoPorPeriodo.xlsx'
RESULT_FILE = 'resumo_por_periodo.csv'

drop = ['cod_espec_hab', 'aproveitamentos', 'motivo']
def generate_clean_data():
    resumo_por_periodo = read_from_database(DATABASE_FILE)
    resumo_por_periodo.columns = resumo_por_periodo_cols
    
    for col in drop:
        resumo_por_periodo.drop(col, axis=1, inplace=True)

    padronize_int_miss(resumo_por_periodo, ['ano_saida', 'periodo_saida'], 0)
    padronize_dates(resumo_por_periodo, ['data_inicio', 'data_fim'])
    padronize_string_miss(resumo_por_periodo, ['tipo_periodo_ingresso'], '=')

    str_to_upper_ascii(resumo_por_periodo, ['situacao'])
    write_result(resumo_por_periodo, RESULT_FILE)
    return resumo_por_periodo