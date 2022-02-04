import pandas as pd
from comvest.utilities.io import files, read_from_db, write_result
from unidecode import unidecode


def cleandata(cities, date):
  '''
    Desc: Data wrangling for cities' sheets
    Args: Cities df, date
    Returns: Clean cities dataframe with two columns: ano_vest, cidades_vest
      where ano_vest is the column correspondent to the year of Comvest exam, 
      cidades_vest is the column correspondent to the cities where the exam was applied 
  '''

  cities.insert(loc=0,column='ano_vest',value=date)

  cities = cities.iloc[:,0:2]
  cities.columns = ['ano_vest','cidades_vest']

  cities['cidades_vest'] = cities['cidades_vest'].map(lambda cid: unidecode(str(cid)).upper().strip())
  
  cities.drop_duplicates(inplace=True)

  return cities


def extraction():
  cities_frames = []

  for path, date in files.items():
    cities = read_from_db(path, sheet_name='cidades')

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