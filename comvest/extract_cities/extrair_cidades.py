import glob
import re
import pandas as pd
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


# Gets all the file names and makes a dictionary with 
# file path as key and the respective date of the file as its value
files_path = glob.glob("input/comvest/*")
files = { path: int(re.sub('[^0-9]','',path)) for path in files_path }

cities_frames = []

def extraction():
  for path, date in files.items():
    cities = pd.read_excel(path, sheet_name='cidades')

    # Cidades do Vestibular Indígena (aplicado a partir de 2019)
    if date >= 2019:
      cities_vi = pd.read_excel(path, sheet_name='vi_cidades')
      cities = pd.concat([cities, cities_vi])

    cities = cleandata(cities, date)
    cities_frames.append(cities)

  # Export CSV
  all_cities = pd.concat(cities_frames)
  all_cities.sort_values(by='ano_vest', ascending=False, inplace=True)

  file_name = 'cidades_comvest'
  all_cities.to_csv("output/{}.csv".format(file_name), index=False)