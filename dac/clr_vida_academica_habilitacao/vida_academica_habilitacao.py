import pandas as pd
import numpy as np
from dac.utilities.io import read_input
from dac.utilities.columns import vida_academica_habilitacao_cols
from dac.utilities.format import padronize_dates
from dac.utilities.format import dates_to_year
from dac.utilities.format import padronize_int_miss
from dac.utilities.format import padronize_string_miss

FILE_NAME = 'Rodolfo_VidaAcademicaCursoHabilitacao.xlsx'

def generate():
    vida_academica_habilitacao = read_input(FILE_NAME)
    vida_academica_habilitacao.columns = vida_academica_habilitacao_cols
    
    dates_to_year(vida_academica_habilitacao, 'data_conclusao')
    padronize_int_miss(vida_academica_habilitacao, ['ano_saida', 'periodo_limite_integralizacao'], 0)

    vida_academica_habilitacao['ano_limite_integralizacao'] = vida_academica_habilitacao['ano_limite_integralizacao'].replace(np.nan, 0).astype('Int64')
    vida_academica_habilitacao['ano_limite_integralizacao'] = vida_academica_habilitacao['ano_limite_integralizacao'].replace([0,13], pd.NA).astype('Int64')
    
    padronize_string_miss(vida_academica_habilitacao, ['nome_habilitacao', 'tipo_periodo_saida', 'codigo_habilitacao', 'data_conclusao'], [' ', '0000'])

    return vida_academica_habilitacao