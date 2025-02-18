import pandas as pd
from pandas import DataFrame
import numpy as np
from enem.utilities.io import write_result


def concat_enemfin_pre_comvest(year: int) -> None:
    """
    Junta os dados do Enem com os dados do fin para os anos de 2018 a 2022
    
    Para o ano de 2019 do enem, só há informações do fin de um ano anterior (2018)
    
    Parâmetros
    ----------
    year : int
        O ano para o qual os dados serão mesclados.
    """
    enem = pd.read_csv(f'/home/output/intermediario/Enem_Comvest/EnemComvest{year}.csv')
    fin = pd.read_csv(f'/home/output/intermediario/Enem_Comvest/fin_stand{year}.csv')
    enem_comvest = pd.concat([enem, fin]).drop_duplicates(subset=["CPF"]).reset_index(drop=True)

    write_result(enem_comvest, f'Enem_Comvest/EnemComvest{year}.csv')
    

def main() -> None:
    for year in range(2019, 2024):
        if year == 2021:
            continue
        else:
            print(f"Concating Enem {year} and Fin {year} pre Comvest data for year")
            concat_enemfin_pre_comvest(year)


if __name__ == "__main__":
    main()
