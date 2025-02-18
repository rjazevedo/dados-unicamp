import os
import pandas as pd
from pandas import DataFrame
import sys
from openpyxl import load_workbook


def compare_enems(df_enem_pre: DataFrame, df_enem_pos: DataFrame, year: int):
    """
    Verifica se as pessoas que estão no DataFrame do enem também estão no DataFrame da Comvest.
    
    O resultado é salvo em um arquivo excel, indicando quais pessoas estão só em um dos arquivos e quais estão em ambos.
    
    Parâmetros
    ----------
    df_enem_pre : DataFrame
        DataFrame do enem pré-processado.
    df_enem_pos : DataFrame
        DataFrame do enem pós-processado.
    year : int
        Ano do DataFrame.
        
    Retorna
    -------
    None
    """
    if year == 2018:
        comvest2019_enem_pre = df_enem_pre["comvest_2019"].dropna()
        comvest2020_enem_pre = df_enem_pre["comvest_2020"].dropna()
        comvest2019_enem_pos = df_enem_pos["comvest_2019"].dropna()
        comvest2020_enem_pos = df_enem_pos["comvest_2020"].dropna()
        
        print(f"Entradas não nulas em comvest_2019 (pré-processado) para 2018: {len(comvest2019_enem_pre)}")
        print(f"Entradas não nulas em comvest_2019 (pós-processado) para 2018: {len(comvest2019_enem_pos)}")
        print(f"Entradas não nulas em comvest_2020 (pré-processado) para 2018: {len(comvest2020_enem_pre)}")
        print(f"Entradas não nulas em comvest_2020 (pós-processado) para 2018: {len(comvest2020_enem_pos)}")
        
    elif year == 2019:
        comvest2020_enem_pre = df_enem_pre["comvest_2020"].dropna()
        comvest2020_enem_pos = df_enem_pos["comvest_2020"].dropna()
        
        print(f"Entradas não nulas em comvest_2020 (pré-processado) para 2019: {len(comvest2020_enem_pre)}")
        print(f"Entradas não nulas em comvest_2020 (pós-processado) para 2019: {len(comvest2020_enem_pos)}")
        
    elif year == 2020:
        comvest2022_enem_pre = df_enem_pre["comvest_2022"].dropna()
        comvest2022_enem_pos = df_enem_pos["comvest_2022"].dropna()
        
        print(f"Entradas não nulas em comvest_2022 (pré-processado) para 2020: {len(comvest2022_enem_pre)}")
        print(f"Entradas não nulas em comvest_2022 (pós-processado) para 2020: {len(comvest2022_enem_pos)}")
                

def main():
    print("Lendo as informações dos outputs novos do Enem...")
    enem2018_pos = pd.read_csv("/home/output/enem/comvest_enem2018.csv")
    enem2019_pos = pd.read_csv("/home/output/enem/comvest_enem2019.csv")
    enem2020_pos = pd.read_csv("/home/output/enem/comvest_enem2020.csv")

    print("Lendo as informações dos outputs antigos do Enem...")
    enem2018_pre = pd.read_csv("/home/gsiqueira/dados-unicamp/output/comvest_enem2018.csv")
    enem2019_pre = pd.read_csv("/home/gsiqueira/dados-unicamp/output/comvest_enem2019.csv")
    enem2020_pre = pd.read_csv("/home/gsiqueira/dados-unicamp/output/comvest_enem2020.csv")
    
    print("Comparando os arquivos de output do Enem para o ano de 2018...")
    compare_enems(enem2018_pre, enem2018_pos, 2018)
    
    print("Comparando os arquivos de output do Enem para o ano de 2019...")
    compare_enems(enem2019_pre, enem2019_pos, 2019)
    
    print("Comparando os arquivos de output do Enem para o ano de 2020...")
    compare_enems(enem2020_pre, enem2020_pos, 2020)
    

if __name__ == "__main__":
    main()
    