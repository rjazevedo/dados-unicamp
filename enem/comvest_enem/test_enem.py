import os
import pandas as pd
from pandas import DataFrame
import sys
from openpyxl import load_workbook
from enem.utilities.format import reading_parameters


def main():
    for year in range(2012, 2021):
        print(f"Comparando o ano {year}") 
        comvest_1 = pd.read_csv(f'/home/output/intermediario/Enem-Comvest/ids_comvest_enem/insc{year}_comv{year + 1}_ids.csv')
        comvest_2 = pd.read_csv(f'/home/output/intermediario/Enem-Comvest/ids_comvest_enem/insc{year}_comv{year + 2}_ids.csv')
        ENEM_PATH = f'/home/input/Enem/enem/MICRODADOS_ENEM_{year}.csv'

        comvest_1[f'enem{year}'] = pd.to_numeric(comvest_1[f'enem{year}'], errors='coerce').dropna().astype(int)
        comvest_2[f'enem{year}'] = pd.to_numeric(comvest_2[f'enem{year}'], errors='coerce').dropna().astype(int)
        
        NEW_COLUMNS = [f'enem{year}', f'ncnt{year}', f'ncht{year}', f'nlct{year}', f'nmt{year}', f'nred{year}']
        GRADES = NEW_COLUMNS[1:]
        parameters = reading_parameters[year]
        COLUMNS_ENEM = parameters["columns"]
        enem = pd.read_csv(ENEM_PATH, encoding='latin-1', sep=parameters['separator'])
        enem = enem.loc[:, COLUMNS_ENEM]
        enem.columns = NEW_COLUMNS

        # Merge comvest_1 and enem DataFrames on 'inscricao' column
        merged_1 = pd.merge(comvest_1, enem, on=f'enem{year}', suffixes=('_comvest', '_enem'))
        
        # Merge comvest_2 and enem DataFrames on 'inscricao' column
        merged_2 = pd.merge(comvest_2, enem, on=f'enem{year}', suffixes=('_comvest', '_enem'))

        # Check if the corresponding scores are the same
        for col in GRADES:  # Replace with actual score column names
            if not (merged_1[f'{col}_comvest'] == merged_1[f'{col}_enem']).all():
                print(f'Differences found in {col} for year {year} in comvest_1')
            if not (merged_2[f'{col}_comvest'] == merged_2[f'{col}_enem']).all():
                print(f'Differences found in {col} for year {year} in comvest_2')


if __name__ == "__main__":
    main()
