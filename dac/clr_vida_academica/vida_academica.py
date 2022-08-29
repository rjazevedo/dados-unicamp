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
    vida_academica = load_vida_academica()
    
    str_to_upper_ascii(vida_academica, ['curso_atual_nome', 'tipo_ingresso', 'motivo_saida', 'cota_d', 'cota_tipo', 'cota_descricao'])
    vida_academica.insc_vest = vida_academica.insc_vest.astype(str).str[:-2]
    padronize_int_miss(vida_academica, ['ano_saida', 'opcao_vest'], 0)

    vida_academica.drop_duplicates(subset=None, keep="first", inplace=True)
    tecnology_courses(vida_academica)
    adm_courses(vida_academica)
    agreements_courses(vida_academica)
    write_result(vida_academica, RESULT_NAME)
    
    indices = vida_academica.loc[:, ['insc_vest', 'ano_ingresso_curso', 'identif', 'curso']]
    write_result(indices, INDICES_NAME)
    return vida_academica, indices


def load_vida_academica():
    vida_academica_pre_99 = read_from_database(PRE_99_BASE_NAME, sheet_name=VIDA_ACADEMICA_SHEET_NAME, names=vida_academica_cols)
    vida_academica_pos_99 = read_from_database(POS_99_BASE_NAME, names=vida_academica_cols)

    vida_academica = pd.concat([vida_academica_pre_99, vida_academica_pos_99])
    clear_columns(vida_academica)
    filt = (vida_academica['ano_ingresso_curso'] >= 1999)

    # Isso é nescessário para remover a intersecção de bases, tem registros < 99 na base pós e vice-versa
    pre_99 = vida_academica[~filt].copy()
    pos_99 = vida_academica[filt].copy()

    pre_99["origem"] = 'pre'
    pos_99["origem"] = 'pos'

    vida_academica = pd.concat([pre_99, pos_99])
    return vida_academica


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


def tecnology_courses(df):
    tecnology_courses_list = [36, 33, 32, 31]
    course_filt = df['curso'].isin(tecnology_courses_list)
    no_insc_vest = (df['insc_vest'] == '')
    year_filt = (df['ano_ingresso_curso'] == 1987)
    filt = (no_insc_vest & course_filt & year_filt)

    df.loc[filt, 'tipo_ingresso'] = "OUTROS"
    df.loc[filt, 'cod_tipo_ingresso'] = 102


def adm_courses(df):
    adm_courses_list = [109, 110]
    course_filt = df['curso'].isin(adm_courses_list)
    no_insc_vest = (df['insc_vest'] == '')
    no_profis = (df['cod_tipo_ingresso'] == 1)
    filt = (no_insc_vest & course_filt & no_profis)
    
    df.loc[filt, 'tipo_ingresso'] = "RETORNO P/ NOVA HABILITACAO/CURSO"
    df.loc[filt, 'cod_tipo_ingresso'] = 103
    
    
def agreements_courses(df):    
    agreements_courses_list = [35, 59, 65, 66, 67]
    filt = df['curso'].isin(agreements_courses_list)
    df.loc[filt, 'tipo_ingresso'] = "CONVENIO"
    df.loc[filt, 'cod_tipo_ingresso'] = 101
    write_result(df[filt], "agreements.csv")