"""
Este script recupera os dados do Enem e os combina com os dados da Comvest para a Unicamp, realizando transformações e filtragens necessárias.

Módulos necessários:
- os: Para manipulação de arquivos e diretórios.
- pandas: Para manipulação de dados em DataFrames.
- numpy: Para operações numéricas.
- enem.utilities.format: Para leitura dos parâmetros de formatação.

Funções:
- retrieve_enem(YEAR, parameters): Recupera e processa os dados do Enem para um ano específico.

Como usar:
Execute o script para recuperar e processar os dados do Enem e combiná-los com os dados da Comvest.
"""


import os 
import pandas as pd
import numpy as np
from enem.utilities.format import reading_parameters


def retrieve_enem(YEAR: int) -> None:
    """
    Recupera e processa os dados do Enem para um ano específico.

    Parâmetros
    ----------
    YEAR : int
        O ano para o qual os dados do Enem serão recuperados.

    Retorna
    -------
    None
    """
    COMVEST_PATH_1 = f'/home/output/intermediario/Enem-Comvest/ids_comvest_enem/insc{YEAR}_comv{YEAR + 1}_ids.csv'
    COMVEST_PATH_2 = f'/home/output/intermediario/Enem-Comvest/ids_comvest_enem/insc{YEAR}_comv{YEAR + 2}_ids.csv'

    ENEM_PATH = f'/home/input/Enem/enem/MICRODADOS_ENEM_{YEAR}.csv'
    OUTPUT_FILE = f'/home/output/enem/comvest_enem{YEAR}.csv'

    NEW_COLUMNS = ['insc_enem', f'ncnt{YEAR}', f'ncht{YEAR}', f'nlct{YEAR}', f'nmt{YEAR}', f'nred{YEAR}']
    GRADES = NEW_COLUMNS[1:]

    if YEAR in range(2012, 2021):
        parameters = reading_parameters[YEAR]
        COLUMNS_ENEM = parameters["columns"]
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
        enem_comvest = enem.replace(np.nan, 0)
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

    """
    elif YEAR in range(2021, 2023):
        if YEAR == 2021:
            enem_comvest = pd.read_csv(f'/home/output/intermediario/Enem_Comvest/EnemComvest{YEAR + 1}.csv')
            enem_comvest.rename(columns={f'enem{YEAR}' : 'insc_enem'}, inplace=True)
            enem_comvest.drop(columns=[f'enem{YEAR - 1}', 'NOME', 'CPF', f'ncnt{YEAR - 1}', f'ncht{YEAR - 1}', f'nlct{YEAR - 1}', 
                                       f'nmt{YEAR - 1}', f'nred{YEAR - 1}'], inplace=True)
            
        elif YEAR == 2022:
            enem_comvest = pd.read_csv(f'/home/output/intermediario/Enem_Comvest/EnemComvest{YEAR + 1}.csv')
            enem_comvest.rename(columns={f'enem{YEAR}' : 'insc_enem'}, inplace=True)
            enem_comvest.drop(columns=[f'enem{YEAR - 1}', 'NOME', 'CPF', f'ncnt{YEAR - 1}', f'ncht{YEAR - 1}', f'nlct{YEAR - 1}', 
                                       f'nmt{YEAR - 1}', f'nred{YEAR - 1}'], inplace=True)    
            
        # Removendo pessoas com, pelo menos, duas notas vazias
        enem_comvest = enem_comvest[['insc_enem', f'ncnt{YEAR}', f'ncht{YEAR}', f'nlct{YEAR}', f'nmt{YEAR}', f'nred{YEAR}', f'comvest_{YEAR + 1}']]
        enem_comvest = enem_comvest.replace(0, pd.NA)
        enem_comvest = enem_comvest.dropna(subset=[f"ncnt{YEAR}", f"ncht{YEAR}", f"nlct{YEAR}", f"nmt{YEAR}", f"nred{YEAR}"], thresh=2)
        enem_comvest = enem_comvest.fillna(0)
  """

    print(f'Saving database into {OUTPUT_FILE}\n')
    enem_comvest.to_csv(OUTPUT_FILE, index=False)


def merge() -> None:
    for year in range(2012, 2021): 
        retrieve_enem(year)
    

def main() -> None:
    merge()
    
    
if __name__ == '__main__':
    main()
