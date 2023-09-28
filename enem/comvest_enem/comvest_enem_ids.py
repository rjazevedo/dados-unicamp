import os 
import pandas as pd
import numpy as np
from enem.utilities.format import reading_parameters

def retrieve_enem(YEAR, parameters):
    COMVEST_PATH_1 = f'/home/gsiqueira/dados-unicamp/output/ids_comvest_enem/insc{YEAR}_comv{YEAR + 1}_ids.csv'
    COMVEST_PATH_2 = f'/home/gsiqueira/dados-unicamp/output/ids_comvest_enem/insc{YEAR}_comv{YEAR + 2}_ids.csv'

    ENEM_PATH = f'/home/gsiqueira/dados-unicamp/input/enem/enem/MICRODADOS_ENEM_{YEAR}.csv'
    OUTPUT_FILE = f'/home/output/enem/comvest_enem{YEAR}.csv'

    COLUMNS_ENEM = parameters["columns"]
    NEW_COLUMNS = ['insc_enem', f'ncnt{YEAR}', f'ncht{YEAR}', f'nlct{YEAR}', f'nmt{YEAR}', f'nred{YEAR}']
    GRADES = NEW_COLUMNS[1:]

    
    print(f'RETRIEVING YEAR {YEAR}')
    print('reading enem')
    enem = pd.read_csv(ENEM_PATH, encoding='latin-1', sep=parameters['separator'])
    enem = enem.loc[:, COLUMNS_ENEM]

    print('reassigning enem names')
    enem.columns = NEW_COLUMNS

    print('transforming grades to numeric')
    for grade in GRADES:
        enem[grade] = pd.to_numeric(enem[grade], errors='coerce')


    print('dropping null or zero grades\n')
    enem = enem.fillna(value={subject : 0 for subject in GRADES})
    enem = enem.dropna(subset=GRADES, thresh=2)
    enem = enem.replace(np.nan, 0)
    enem_comvest = enem

    if os.path.isfile(COMVEST_PATH_1):
        print(f'reading comvest {YEAR + 1}')
        
        comvest_1 = pd.read_csv(COMVEST_PATH_1)
        print(f'{comvest_1.shape[0]} entries in comvest {YEAR + 1}\n')  
        print(f'merging Enem {YEAR} with comvest {YEAR + 1}')
        comvest_1 = comvest_1.rename(columns={f'id_comvest_{YEAR + 1}' : f'comvest_{YEAR + 1}'})
        enem_comvest = enem.merge(comvest_1, how='left')

        entries = (enem_comvest[enem_comvest[f'comvest_{YEAR + 1}'].notna()]).shape[0]    
        print(f'{entries} entries found in merge between ENEM {YEAR} and comvest {YEAR + 1}\n')


    if os.path.isfile(COMVEST_PATH_2):
        print(f'reading comvest {YEAR + 2}')
        comvest_2 = pd.read_csv(COMVEST_PATH_2)
        print(f'{comvest_2.shape[0]} entries in comvest {YEAR + 1}\n')    
        print(f'merging Enem {YEAR} with comvest {YEAR + 2}')
        comvest_2 = comvest_2.rename(columns={f'id_comvest_{YEAR + 2}' : f'comvest_{YEAR + 2}'})
        enem_comvest = enem_comvest.merge(comvest_2, how='left')
        
        entries = (enem_comvest[enem_comvest[f'comvest_{YEAR + 2}'].notna()]).shape[0]
        print(f'{entries} entries found in merge between ENEM {YEAR} and comvest {YEAR + 2}\n')

    
    print(f'Saving database into {OUTPUT_FILE}\n')
    enem_comvest.to_csv(OUTPUT_FILE, index=False)

def retrieve():
    for year in range(2020, 2021): 
        retrieve_enem(year, reading_parameters[year])
    

def main():
    retrieve()
    
if __name__ == '__main__':
    main()