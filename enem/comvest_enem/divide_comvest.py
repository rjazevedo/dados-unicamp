import pandas as pd
import numpy as np
from tqdm import tqdm 
from enem.utilities.io import write_result, read_result

def separate_enem_comvest(YEAR):
    ENEM_COMVEST_PATH = f'Enem_Comvest/EnemComvest{YEAR}.csv'

    RESULT_1 = f'/Enem_Comvest/split/INSC{YEAR - 2}_COMV{YEAR}.csv'
    RESULT_2 = f'/Enem_Comvest/split/INSC{YEAR - 1}_COMV{YEAR}.csv'

    comvest = read_result(ENEM_COMVEST_PATH)

    ENEM_YEARS = [[f'comvest_{YEAR}', f'enem{y}', f'ncnt{y}', f'ncht{y}', 
                f'nlct{y}', f'nmt{y}', f'nred{y}'] for y in range(YEAR - 2, YEAR)]


    enem_before = comvest.loc[:, ENEM_YEARS[0]]
    enem_last = comvest.loc[:, ENEM_YEARS[1]]

    
    print(f'{comvest.shape[0]} entries in total\n')
    
    print(f"Droping INSC nulls {YEAR - 2}")
    
    enem_before.dropna(subset=[f'enem{YEAR - 2}'], inplace=True)
    print(f'{enem_before.shape[0]} entries in enem {YEAR - 2}\n')
    
    enem_before = enem_before.replace(0, np.nan)
    enem_before.dropna(subset=[f'ncnt{YEAR - 2}', f'ncht{YEAR - 2}', 
                            f'nlct{YEAR - 2}', f'nred{YEAR - 2}',
                            f'nmt{YEAR - 2}'], inplace=True, thresh=2) 
      
    enem_before.drop(columns=[f'enem{YEAR - 2}'], inplace=True) 
    enem_before = enem_before.fillna(0) 

    print(f'{enem_before.shape[0]} entries in enem {YEAR - 2} after null removal\n')
    
    
    
    print(f"Droping INSC nulls {YEAR - 1}")

    enem_last.dropna(subset=[f'enem{YEAR - 1}'], inplace=True)
    print(f'{enem_last.shape[0]} entries in enem {YEAR - 1}\n')
    
    enem_last = enem_last.replace(0, np.nan)
    enem_last.dropna(subset=[f'ncnt{YEAR - 1}', f'ncht{YEAR - 1}', 
                            f'nlct{YEAR - 1}', f'nred{YEAR - 1}',
                            f'nmt{YEAR - 1}'], inplace=True, thresh=2)

    enem_last.drop(columns=[f'enem{YEAR - 1}'], inplace=True)
    enem_last = enem_last.fillna(0)

    print(f'{enem_last.shape[0]} entries in enem {YEAR - 1} after null removal\n')

    write_result(enem_before, RESULT_1)
    write_result(enem_last, RESULT_2)

def main():
    split_all()

if __name__ == '__main__':
    main()

def split_all():
    for y in tqdm(range(2012, 2023)):
        if y == 2021: continue
        print(f"Separating {y}...")
        separate_enem_comvest(y)