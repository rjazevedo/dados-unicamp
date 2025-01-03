"""
Este script realiza a limpeza dos dados do Enem para a Unicamp, removendo colunas desnecessárias e renomeando colunas para um formato padronizado.

Módulos necessários:
- tqdm: Para exibir uma barra de progresso.
- pandas: Para manipulação de dados em DataFrames.
- enem.utilities.io: Para escrever os resultados (não utilizado no trecho fornecido).
- numpy: Para manipulação de arrays.

Funções:
- main(): Função principal que inicia o processo de limpeza.
- clean_all(): Limpa os dados para todos os anos especificados.
- clean_year(YEAR): Limpa os dados para um ano específico.

Como usar:
Execute o script para limpar os dados do Enem para a Unicamp.
"""


from tqdm import tqdm
from enem.utilities.io import write_result
import pandas as pd
import numpy as np

def clean_all() -> None:
    """
    Limpa os dados para todos os anos especificados, exceto 2021.
    """
    for y in tqdm(range(2012, 2024)):
        if y == 2021: 
            continue
        elif y == 2023:
            clean_2023(y)
        else:
            clean_year(y)
        
        print(f"Cleaning {y}...")


def clean_year(YEAR: int) -> None:
    """
    Limpa os dados para um ano específico.

    Parâmetros
    ----------
    YEAR : int
        O ano para o qual os dados serão limpos.
    """
    COMVEST_PATH = f'/home/input/Enem_Unicamp/Enem{YEAR}.xlsx'

    COMVEST_COLUMNS = [f'comvest_{YEAR}', f'enem{YEAR - 2}', f'enem{YEAR - 1}', 'NOME', 'CPF', 
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
    
    for cols in DROP_PAD: 
        comvest.drop(columns=cols, inplace=True, errors='ignore')

    comvest = comvest.drop(comvest.iloc[:, 25:], axis=1)
    comvest.columns = COMVEST_COLUMNS

    for cols in DROP_COLUMNS: comvest.drop(columns=cols, inplace=True)

    write_result(comvest, f'Enem_Comvest/EnemComvest{YEAR}.csv')


def clean_2023(year: int) -> None:
    """
    Limpa os dados para o ano de 2023.
    
    É necessário uma função separada já que esse ano não possui dados  de 2 anos anteriores (apenas de um)
    Parâmetros
    ----------
    year : int
        O ano para o qual os dados serão limpos.
    """
    COMVEST_PATH = f'/home/input/Enem_Unicamp/Enem{year}.xlsx'

    comvest = pd.read_excel(COMVEST_PATH)
    
   # Ajusta a ordem inicial das colunas
    comvest = comvest[["insc", "enem2022", "nome", "cpf", "ncnt22", "ncht22", "nlct22", "nmt22", "nred22"]]
    comvest.columns = ['comvest_2023', 'enem2022', 'NOME', 'CPF', 'ncnt2022', 'ncht2022', 'nlct2022', 'nmt2022', 'nred2022']
    
    # Inicializa colunas de 2021
    cols_2021 = ['enem2021', 'ncnt2021', 'ncht2021', 'nlct2021', 'nmt2021', 'nred2021']
    for col in cols_2021:
        comvest[col] = np.nan
    
    # Reordena as colunas
    comvest = comvest[[
        "comvest_2023", "enem2022", "enem2021", "NOME", "CPF",
        "ncnt2021", "ncht2021", "nlct2021", "nmt2021", "nred2021",
        "ncnt2022", "ncht2022", "nlct2022", "nmt2022", "nred2022"
    ]]  
 
    write_result(comvest, f'Enem_Comvest/EnemComvest{year}.csv')
    

def main() -> None:
    clean_all()


if __name__ == '__main__':
    main()
