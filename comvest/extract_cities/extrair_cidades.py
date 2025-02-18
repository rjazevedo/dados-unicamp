"""
Módulo para extração de dados das cidades Comvest.

Este módulo contém funções para extrair e processar dados das cidades onde os exames Comvest foram aplicados.

Funções:
- cleandata(cities, date): Realiza a limpeza dos dados das cidades.
- extraction(): Executa a extração e processamento dos dados das cidades Comvest.

Como usar:
Implemente e execute as funções para realizar a extração e processamento dos dados das cidades Comvest.
"""


import pandas as pd
from comvest.utilities.io import files, read_from_db, write_result
from comvest.utilities.logging import progresslog, resultlog
from unidecode import unidecode


def cleandata(cities, date):
  """
  Realiza a limpeza dos dados das cidades.

  Parâmetros:
  ----------
  cities : DataFrame
      O DataFrame contendo os dados das cidades.
  date : int
      O ano do exame Comvest.

  Retorna:
  -------
  DataFrame
      O DataFrame contendo os dados das cidades limpos.
  """
  cities.insert(loc=0,column='ano_vest',value=date)

  cities = cities.iloc[:,0:2]
  cities.columns = ['ano_vest','cidades_vest']

  cities['cidades_vest'] = cities['cidades_vest'].map(lambda cid: unidecode(str(cid)).upper().strip())
  
  cities.drop_duplicates(inplace=True)

  return cities


def extraction():
  """
  Executa a extração e processamento dos dados das cidades Comvest.

  Esta função lê os dados das cidades de diferentes anos, realiza a limpeza dos dados e os concatena em um único DataFrame.

  Retorna:
  -------
  None
  """
  cities_frames = []

  for path, date in files.items():
    if "Profis" in path:
      continue
    
    print(f"Extraindo cidades do ano {date}...")
    cities = read_from_db(path, sheet_name='cidades')
    progresslog('cidades', date)

    # Cidades do Vestibular Indígena (aplicado a partir de 2019)
    if date >= 2019:
      cities_vi = read_from_db(path, sheet_name='vi_cidades')
      cities = pd.concat([cities, cities_vi])

    cities = cleandata(cities, date)
    cities_frames.append(cities)

  # Export CSV
  all_cities = pd.concat(cities_frames)
  all_cities.sort_values(by='ano_vest', ascending=False, inplace=True)

  FILE_NAME = 'cidades_comvest.csv'
  write_result(all_cities, FILE_NAME)
  resultlog(FILE_NAME)
