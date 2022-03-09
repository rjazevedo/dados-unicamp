import logging
import pandas as pd
from comvest.utilities.io import files, read_from_db, read_result, write_result
from comvest.utilities.logging import progresslog, resultlog


def cleandata(df, date):
  df.insert(loc=0, column='ano_vest', value=date)
  df.drop('nome', axis=1, errors='ignore', inplace=True)
  df = df.iloc[:,0:3]
  df.columns = ['ano_vest','insc_vest','curso_matric']
  df['insc_vest'] = pd.to_numeric(df['insc_vest'], errors='coerce', downcast='integer').astype('Int64')
  df.dropna(inplace=True)

  return df


def validacao_curso(df, date):
  cursos = df_cursos.loc[df_cursos['ano_vest'] == date]['cod_curso'].tolist()
  
  # Codigos que nao constam na lista de cursos serao remapeados para missing
  df['curso_matric'].fillna(-1, inplace=True)
  df['curso_matric'] = df['curso_matric'].map(lambda cod: int(cod) if int(cod) in cursos else '')
  df['curso_matric'] = pd.to_numeric(df['curso_matric'], errors='coerce').astype('Int64')
  df.dropna(subset=['curso_matric'], inplace=True)
  
  return df


# Leitura dos cursos p posterior validação
try:
  df_cursos = read_result('cursos.csv')
except:
  logging.warning('Couldn\'t find "cursos.csv"')


def extraction():
  matriculados_frames = []

  for path, date in files.items():
    matriculados = read_from_db(path, sheet_name='matriculados')
    progresslog('matriculados', date)

    matriculados = cleandata(matriculados, date)
    matriculados = validacao_curso(matriculados, date)

    matriculados_frames.append(matriculados)

  # Exportar CSV
  all_matriculados = pd.concat(matriculados_frames)
  all_matriculados.sort_values(by='ano_vest', ascending=False, inplace=True)

  FILE_NAME = 'matriculados_comvest.csv'
  write_result(all_matriculados, FILE_NAME)
  resultlog(FILE_NAME)