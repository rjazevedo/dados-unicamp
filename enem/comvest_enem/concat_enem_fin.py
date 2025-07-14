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
    enem = pd.read_csv(f'/home/output/intermediario/Enem_Comvest/EnemComvest{year}.csv', low_memory=False)
    fin = pd.read_csv(f'/home/output/intermediario/Enem_Comvest/fin_stand{year}.csv', low_memory=False)
    enem_comvest = pd.concat([enem, fin]).drop_duplicates(subset=["CPF"]).reset_index(drop=True)

    write_result(enem_comvest, f'Enem_Comvest/EnemComvest{year}.csv')
    

def concat_enemfin_profis_pre_comvest(year: int) -> None:
    """
    Junta os dados do Enem e fin com os dados do ProFIS para os anos de 2011 a 2022
    
    Parâmetros
    ----------
    year : int
        O ano para o qual os dados serão mesclados.
    """
    enem = pd.read_csv(f'/home/output/intermediario/Enem_Comvest/EnemComvest{year}.csv', low_memory=False)
    profis = pd.read_csv(f'/home/output/intermediario/ProfisDivided/notas_enem/notas_enem_profis{year}.csv', low_memory=False)
    enem_comvest = pd.concat([enem, profis]).drop_duplicates(subset=["CPF"], keep="last").reset_index(drop=True)

    write_result(enem_comvest, f'Enem_Comvest/EnemComvest{year}.csv')


def main() -> None:
    for year in range(2019, 2024):
        if year == 2021:
            continue
        else:
            print(f"Concating Enem {year} and Fin {year} pre Comvest data for year")
            concat_enemfin_pre_comvest(year)

    for year in range(2012, 2021):
        print(f"Concating Enem {year} and ProFIS {year} pre Comvest data for year")
        concat_enemfin_profis_pre_comvest(year)


if __name__ == "__main__":
    main()
