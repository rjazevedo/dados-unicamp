import pandas as pd
from pandas import DataFrame
import numpy as np
from enem.utilities.io import write_result


def merge(year: int) -> None:
    """
    Junta os dados do Enem com os dados do fin para os anos de 2018 a 2022
    
    Para o ano de 2019 do enem, só há informações do fin de um ano anterior (2018)
    
    Parâmetros
    ----------
    year : int
        O ano para o qual os dados serão mesclados.
    """
    enem = pd.read_csv(f'/home/output/intermediario/Enem_Comvest/EnemComvest{year}.csv')
    
    if year == 2019:
        fin = pd.read_csv(f'/home/output/intermediario/Enem_Comvest/fin{year - 1}.csv')
        enem_comvest = pd.concat([enem, fin]).drop_duplicates(subset=["CPF"]).reset_index(drop=True)
        
    else:
        # Respectivamente, as informações do fin para os dois anos anteriores ao do arquivo do enem em questão
        fin_1 = pd.read_csv(f'/home/output/intermediario/Enem_Comvest/fin{year - 1}.csv')
        fin_2 = pd.read_csv(f'/home/output/intermediario/Enem_Comvest/fin{year - 2}.csv')
        enem_comvest = pd.concat([enem, fin_1]).drop_duplicates(subset=["CPF"]).reset_index(drop=True)
        enem_comvest = pd.concat([enem_comvest, fin_2]).drop_duplicates(subset=["CPF"]).reset_index(drop=True)
        enem_comvest = enem_comvest.iloc[:, :15]
        
    write_result(enem_comvest, f'Enem_Comvest/EnemComvest{year}.csv')
    

def main() -> None:
    for year in range(2019, 2024):
        if year == 2021:
            continue
        else:
            print(f"Merging Enem {year} and Fin {year - 1} data for year")
            merge(year)


if __name__ == "__main__":
    main()
    