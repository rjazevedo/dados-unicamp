import os
import pandas as pd
from pandas import DataFrame
import sys
from openpyxl import load_workbook
from enem.utilities.format import reading_parameters


def main():
    for year in range(2012, 2021):
        print(f"Comparando o ano {year}") 
        new_file_path = f'/home/output/enem/comvest_enem{year}.csv'
        old_file_path = f'/home/jonatas/testes-enem/enem/comvest_enem{year}.csv'
        
        new_df = pd.read_csv(new_file_path)
        old_df = pd.read_csv(old_file_path)

        # Imprimindo quantos valores não-nulos há nas colunas comvest_{year + 1} e comvest_{year + 2}
        print(f"Quantidade de valores não-nulos nas colunas comvest_{year + 1}:")
        print("Para o arquivo antigo:")
        print(old_df[f'comvest_{year + 1}'].count())
        print("Para o arquivo novo:")
        print(new_df[f'comvest_{year + 1}'].count())
        print()
        
        if year != 2019:
            print(f"Quantidade de valores não-nulos nas colunas comvest_{year + 2}:")
            print("Para o arquivo antigo:")
            print(old_df[f'comvest_{year + 2}'].count())
            print("Para o arquivo novo:")
            print(new_df[f'comvest_{year + 2}'].count())
            print()


if __name__ == "__main__":
    main()
