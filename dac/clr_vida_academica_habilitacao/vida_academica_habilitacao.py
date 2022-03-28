import pandas as pd
import numpy as np
from dac.utilities.io import read_from_database
from dac.utilities.io import write_result
from dac.utilities.columns import vida_academica_habilitacao_cols
from dac.utilities.format import padronize_dates
from dac.utilities.format import dates_to_year
from dac.utilities.format import padronize_int_miss
from dac.utilities.format import padronize_string_miss

FILE_NAME = 'VidaAcademicaCursoHabilitacao.xlsx'
RESULT_NAME = 'vida_academica_habilitacao.csv'

def generate():
    vida_academica_habilitacao = read_from_database(FILE_NAME)
    vida_academica_habilitacao.columns = vida_academica_habilitacao_cols

    dates_to_year(vida_academica_habilitacao, 'data_conclusao')
    vida_academica_habilitacao['periodo_limite_integralizacao'] = vida_academica_habilitacao['periodo_limite_integralizacao'].fillna(0)

    padronize_int_miss(vida_academica_habilitacao, ['ano_saida', 'periodo_limite_integralizacao'], 0)

    # TODO: como padronizar isso aqui ?
    vida_academica_habilitacao['ano_limite_integralizacao'] = vida_academica_habilitacao['ano_limite_integralizacao'].replace(np.nan, 0).astype('Int64')
    vida_academica_habilitacao['ano_limite_integralizacao'] = vida_academica_habilitacao['ano_limite_integralizacao'].replace([0,13], pd.NA).astype('Int64')
    
    # TODO: como padronizar isso aqui ?      
    vida_academica_habilitacao['nome_habilitacao'] = vida_academica_habilitacao['nome_habilitacao'].fillna('')
    padronize_string_miss(vida_academica_habilitacao, ['tipo_periodo_saida', 'codigo_habilitacao', 'data_conclusao'], [' ', '0000'])

    return vida_academica_habilitacao