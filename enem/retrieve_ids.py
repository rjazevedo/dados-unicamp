import pandas as pd
import os
from tqdm import tqdm

COMVEST_IDS_PATH = '/home/gsiqueira/dados-unicamp/input/ids/dac_comvest_ids.csv'
COMVEST_ENEM_PATH = '/home/gsiqueira/dados-unicamp/output/insc_comvest_enem/'
RESULT_PATH = '/home/gsiqueira/dados-unicamp/output/ids_comvest_enem/'

def merge_ids_per_year(comvest_enem, comvest_ids, year):
    comvest_enem_ids_year = comvest_ids.merge(comvest_enem, left_on='insc_vest_comvest', right_on=f'comvest_{year}')
    comvest_enem_ids_year = comvest_enem_ids_year.drop(columns=[f'comvest_{year}', 'insc_vest_comvest', 'ano_ingresso_curso'])
    comvest_enem_ids_year = comvest_enem_ids_year.rename(columns={"id" : f'id_comvest_{year}'})
    return comvest_enem_ids_year


def retrieve_ids(comvest_ids_year, year):
    COMVEST_PATHS = [f"{COMVEST_ENEM_PATH}INSC{y}_COMV{year}.csv" for y in range(year - 2, year)]
    RESULT_PATHS = [f'{RESULT_PATH}insc{y}_comv{year}_ids.csv' for y in range(year - 2, year)]
   
    comvest_enem_dfs = [pd.read_csv(FILE) for FILE in COMVEST_PATHS if os.path.isfile(FILE)]
    
    comvest_enem_ids = list(map(lambda comvest_enem : merge_ids_per_year(comvest_enem, comvest_ids_year, year), comvest_enem_dfs))

    for i, ids in enumerate(comvest_enem_ids): ids.to_csv(RESULT_PATHS[i], index=False)

def main():
    comvest_ids = pd.read_csv(COMVEST_IDS_PATH)
    comvest_ids = comvest_ids.loc[:, ['id', 'insc_vest_comvest', 'ano_ingresso_curso']]

    for year in tqdm(range(2012, 2023)):
        print(f"retrieving ids from year {year} from DAC_COMVEST_IDS to COMVEST_ENEM_{year}")
        comvest_ids_year = comvest_ids[comvest_ids['ano_ingresso_curso'] == year]
        retrieve_ids(comvest_ids_year, year)



if __name__ == '__main__':
    main()