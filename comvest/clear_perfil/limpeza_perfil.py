import glob
import logging
import re
import pandas as pd
from unidecode import unidecode
import numpy as np
from comvest.clear_perfil import normalizar_respostas
from comvest.clear_perfil import limpeza_questoes


def validacao_cidade(df, date):
  cidades_ano = df_cidades[df_cidades['ano_vest'] == date]

  cidades = cidades_ano['cidades_vest'].tolist()
  cidades = [unidecode(cidade.lower().strip()) for cidade in cidades]
  cidades.append('especiais')

  validar_cidade = np.vectorize(lambda cid: cid if unidecode(str(cid).lower().strip()) in cidades else '')

  try:
    df['cid_inscricao'] = validar_cidade(df['cid_inscricao'])
  except:
    # logging.debug('Comvest {} file doesn\'t have a \'cid_inscricao\' column'.format(date))
    print('Comvest {} file doesn\'t have a \'cid_inscricao\' column'.format(date))
  
  return df

def validacao_curso(df, date):
  cursos = df_cursos.loc[df_cursos['ano_vest'] == date]['cod_curso'].tolist()

  validar_curso = np.vectorize(lambda cod: str(cod) if cod in cursos else '')
  df['curso_aprovado'] = validar_curso(df['curso_aprovado'])
  df['curso_aprovado'] = pd.to_numeric(df['curso_aprovado'], errors='coerce').astype('Int64')

  return df

def cleandata(df, questoes, date):
  # Renomeia colunas de acordo com o mapeamento das questões
  df = df.rename(questoes, axis=1)
  df = df.rename({'insc_cand':'insc_vest','curpas':'curso_aprovado','aprovf2':'aprov_f1','local_residencia':'local_resid'}, axis=1)

  df['ano_vest'] = date

  # 75 => Medicina Famerp; 81 => Enfermagem Famerp
  df['instituicao'] = df.apply(lambda row: 2 if row['opcao1'] in [75,81] else 1, axis=1)

  df['aprov_f1'] = df['aprov_f1'].map({'S':1, 'N':0, 1:1, 0:0})

  try:
    df.insert(loc=df.columns.get_loc('local_resid')+1, column='reg_campinas', value='')
  except:
      # logging.debug('File read from {} doesn\'t have a \'local_resid\' column'.format(path))
      print('Comvest {} file doesn\'t have a \'local_resid\' column'.format(date))

  df = validacao_cidade(df,date)
  df = validacao_curso(df,date)

  return df


# Gets all the file names and makes a dictionary with 
# file path as key and the respective date of the file as its value
files_path = glob.glob("input/comvest/*")
files = { path: int(re.sub('[^0-9]','',path)) for path in files_path }

# Leitura das cidades e cursos p posterior validação
df_cidades = pd.read_csv('output/cidades_comvest.csv')
df_cursos = pd.read_csv('output/cursos_comvest.csv')

def extraction():
  perfil_comvest = []

  cols = [
    'insc_cand','sexo','opcao1','aprovf2','est_civil','local_residencia',
    'isento','paais','curpas','cid_inscricao'
  ]

  for path, date in files.items():
    df = pd.read_excel(path, sheet_name='perfil')
    # Mudar print para logs
    print('File was read from {}'.format(path))

    # Obtém dicionário com as perguntas do questionario devidamente renomeadas
    df_questoes, _ = limpeza_questoes.get_questions(path)
    questoes = df_questoes.set_index(['questao']).to_dict()['descricao']

    for col in df.columns:
      # Adiciona todas as colunas das perguntas do questionário
      if 'q' in col.lower() and col not in cols:
        cols.append(col)

    final_cols = list(set(cols) & set(df.columns))
    df = df[final_cols]

    df = cleandata(df, questoes, date)
    df = normalizar_respostas.normalizar(df, date)

    # Rearranja colunas
    df = df.reindex(columns=[
      'ano_vest',
      'insc_vest',
      'cid_inscricao',
      'instituicao',
      'sexo',
      'est_civil',
      'local_resid',
      'isento',
      'paais',
      'raca',
      'tipo_esc_ef',
      'tipo_esc_ef_1',
      'tipo_esc_ef_2',
      'tipo_esc_em',
      'tipo_curso_em',
      'periodo_em',
      'cursinho',
      'cursinho_motivo',
      'cursinho_tempo',
      'cursinho_tipo',
      'cursinho_nao_motivo',
      'univ_outra',
      'unicamp_motivo',
      'opc1_motivo_a',
      'opc1_motivo_b',
      'renda_sm',
      'renda_sm_a',
      'renda_sm_b',
      'renda_sm_c',
      'renda_sm_d',
      'renda_qtas',
      'renda_contrib_qtas',
      'moradia_situacao',
      'ocup_pai',
      'ocup_mae',
      'trabalha_pai',
      'trabalha_mae',
      'educ_pai',
      'educ_mae',
      'trabalha',
      'contribui_renda_fam',
      'jornal_le',
      'livros_qtos',
      'lugar_calmo_casa',
      'jornal_assina',
      'revistas_assina',
      'enciclopedia',
      'atlas',
      'dicionario',
      'calculadora',
      'empr_domest_qtas',
      'idiomas',
      'internet',
      'internet_onde',
      'cozinha_qtas',
      'sala_qtas',
      'quarto_qts',
      'banheiro_qts',
      'radio_qts',
      'tv_qts',
      'dvd_vhs_qts',
      'computador_qtos',
      'carro_qtos',
      'geladeira',
      'maq_roupa',
      'aspirador',
      'freezer',
      'maq_louca',
      'aprov_f1',
      'curso_aprovado'
    ])

    # Mudar print para logs
    print('{} was transformed'.format(path.split('/')[2].split('.')[0]))

    perfil_comvest.append(df)

  # Exportar CSV
  perfil_comvest = pd.concat(perfil_comvest)
  perfil_comvest.sort_values(by='ano_vest', ascending=False, inplace=True)

  file_name = 'perfil_comvest'
  perfil_comvest.to_csv("output/{}.csv".format(file_name), index=False)