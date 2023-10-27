from tqdm import tqdm
from enem.utilities.io import write_result

import pandas as pd

def main():
    clean_all()

def clean_all():
    for y in tqdm(range(2012, 2023)):
        if y == 2021: continue
        print(f"Cleaning {y}...")
        clean_year(y)

def clean_year(YEAR):
    COMVEST_PATH = f'/home/input/Enem_Unicamp/Enem{YEAR}.xlsx'

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


    comvest = pd.read_excel(COMVEST_PATH)
    
    for cols in DROP_PAD: comvest.drop(columns=cols, inplace=True, errors='ignore')

    comvest = comvest.drop(comvest.iloc[:, 25:], axis=1)
    comvest.columns = COMVEST_COLUMNS

    for cols in DROP_COLUMNS: comvest.drop(columns=cols, inplace=True)

    write_result(comvest, f'Enem_Comvest/EnemComvest{YEAR}.csv')

if __name__ == '__main__':
    main()