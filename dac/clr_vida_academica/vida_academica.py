from dac.utilities.io import read_from_database
from dac.utilities.io import write_result
from dac.utilities.io import write_output
from dac.utilities.dtypes import dtypes_vida_academica
from dac.utilities.columns import vida_academica_cols
from dac.utilities.format import str_to_upper_ascii
from dac.utilities.format import padronize_int_miss
from dac.utilities.format import padronize_string_miss
from dac.utilities.dtypes import dtypes_vida_academica
import numpy as np
import pandas as pd

PRE_99_BASE_NAME = 'Rodolfo_Complementacao.xlsx'
POS_99_BASE_NAME = 'VidaAcademicaCurso.xlsx'
VIDA_ACADEMICA_SHEET_NAME = 'Vida Academica Curso'

RESULT_NAME = 'vida_academica.csv'
INDICES_NAME = 'indices.csv'

def generate_clean_data():
    vida_academica_pre_99 = read_from_database(PRE_99_BASE_NAME, sheet_name=VIDA_ACADEMICA_SHEET_NAME, names=vida_academica_cols)
    vida_academica_pos_99 = read_from_database(POS_99_BASE_NAME, names=vida_academica_cols)

    vida_academica = pd.concat([vida_academica_pre_99, vida_academica_pos_99])
    clear_columns(vida_academica)
    
    str_to_upper_ascii(vida_academica, ['curso_atual_nome', 'tipo_ingresso', 'motivo_saida', 'cota_d', 'cota_tipo', 'cota_descricao'])
    vida_academica.insc_vest = vida_academica.insc_vest.astype(str).str[:-2]
    padronize_int_miss(vida_academica, ['ano_saida', 'opcao_vest'], 0)

    vida_academica.drop_duplicates(subset=None, keep="first", inplace=True)
    write_result(vida_academica, RESULT_NAME)
    
    indices = vida_academica.loc[:, ['insc_vest', 'ano_ingresso_curso', 'identif', 'curso']]
    write_result(indices, INDICES_NAME)
    return vida_academica, indices

# Limpa erros na tabela pré 99 vistos empiricamente
def clear_columns(df):
    df['insc_vest'] = df['insc_vest'].fillna(0)
    df['insc_vest'].replace(0, '<null>', inplace=True)
    df['insc_vest'] = df['insc_vest'].astype(str)
    padronize_string_miss(df, ['chamada_vest'], '<null>')
    padronize_string_miss(df, ['insc_vest'], '<null>')
    
    df['insc_vest'].replace("", np.nan, inplace=True)
    df['insc_vest'] = df['insc_vest'].astype('float64')
    df['insc_vest'].replace(np.nan, "", inplace=True)