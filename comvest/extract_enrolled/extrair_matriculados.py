import glob
import re
import pandas as pd


def cleandata(df, date):
  df.insert(loc=0, column='ano_vest', value=date)
  df.drop('nome', axis=1, errors='ignore', inplace=True)
  df = df.iloc[:,0:3]
  df.columns = ['ano_vest','insc_vest','curso_matric']

  return df


def validacao_curso(df, date):
  cursos = df_cursos.loc[df_cursos['ano_vest'] == date]['cod_curso'].tolist()
  
  # Codigos que nao constam na lista de cursos serao remapeados para missing
  df['curso_matric'] = df['curso_matric'].map(lambda cod: str(cod) if cod in cursos else '')
  df['curso_matric'] = pd.to_numeric(df['curso_matric'], errors='coerce').astype('Int64')

  return df


# Gets all the file names and makes a dictionary with
# file path as key and the respective date of the file as its value
files_path = glob.glob("input/comvest/*")
files = { path: int(re.sub('[^0-9]','',path)) for path in files_path }

# Leitura dos cursos p posterior validação
df_cursos = pd.read_csv('output/cursos_comvest.csv')

def extraction():
  matriculados_frames = []

  for path, date in files.items():
    matriculados = pd.read_excel(path, sheet_name='matriculados')

    matriculados = cleandata(matriculados, date)
    matriculados = validacao_curso(matriculados, date)

    matriculados_frames.append(matriculados)

  # Exportar CSV
  all_matriculados = pd.concat(matriculados_frames)
  all_matriculados.sort_values(by='ano_vest', ascending=False, inplace=True)
  all_matriculados.dropna(inplace=True)

  file_name = 'matriculados_comvest'
  all_matriculados.to_csv("output/{}.csv".format(file_name), index=False)