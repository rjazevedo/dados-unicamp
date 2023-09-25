import pandas as pd
import numpy as np
from tqdm import tqdm 

def separate_enem_comvest(YEAR):
    COMVEST_PATH = f'../input/enem/Enem_Unicamp/Enem{YEAR}.xlsx'

    COMVEST_COLUMNS = [f'comvest_{YEAR}', f'enem{YEAR - 1}', f'enem{YEAR - 2}', 'NOME', 'CPF', 
                    f'ncnt{YEAR - 2}', f'ncht{YEAR - 2}', f'nlct{YEAR - 2}', 
                    f'nmt{YEAR - 2}', f'nred{YEAR - 2}', 
                    f'pcnt{YEAR - 2}', f'pcht{YEAR - 2}', f'plct{YEAR - 2}', 
                    f'pmt{YEAR - 2}', f'pred{YEAR - 2}', 
                    f'ncnt{YEAR - 1}', f'ncht{YEAR - 1}', f'nlct{YEAR - 1}', 
                    f'nmt{YEAR - 1}', f'nred{YEAR - 1}', 
                    f'pcnt{YEAR - 1}', f'pcht{YEAR - 1}', f'plct{YEAR - 1}', 
                    f'pmt{YEAR - 1}', f'pred{YEAR - 1}']
    
    
    DROP_PAD = [[f'nredPad{y}'] for y in range(YEAR - 2002, YEAR - 2000)]
    DROP_COLUMNS = [[f'pcnt{y}', f'pcht{y}', f'plct{y}', f'pmt{y}', f'pred{y}'] for y in range(YEAR - 2, YEAR)]

    ENEM_YEARS = [[f'comvest_{YEAR}', f'enem{y}', f'ncnt{y}', f'ncht{y}', 
                f'nlct{y}', f'nmt{y}', f'nred{y}'] for y in range(YEAR - 2, YEAR)]


    comvest = pd.read_excel(COMVEST_PATH)
    
    for cols in DROP_PAD: comvest.drop(columns=cols, inplace=True, errors='ignore')

    comvest = comvest.drop(comvest.iloc[:, 25:], axis=1)
    comvest.columns = COMVEST_COLUMNS

    for cols in DROP_COLUMNS: comvest.drop(columns=cols, inplace=True)

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

    enem_before.to_csv(f'../output/insc_comvest_enem/INSC{YEAR - 2}_COMV{YEAR}.csv', index=False)
    enem_last.to_csv(f'../output/insc_comvest_enem/INSC{YEAR - 1}_COMV{YEAR}.csv', index=False)


for y in tqdm(range(2012, 2023)):
    if y == 2021: continue
    print(f"Separating {y}...")
    separate_enem_comvest(y)