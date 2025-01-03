"""
Este script combina os dados de IDs da Comvest com os dados do Enem para a Unicamp, realizando transformações e filtragens necessárias.

Módulos necessários:
- pandas: Para manipulação de dados em DataFrames.
- os: Para manipulação de arquivos e diretórios.
- tqdm: Para exibir uma barra de progresso.

Funções:
- merge_ids_per_year(comvest_enem, comvest_ids, year): Mescla os dados de IDs da Comvest com os dados do Enem para um ano específico.
- retrieve_ids(comvest_ids_year, year): Recupera e processa os dados de IDs para um ano específico.
- retrieve(): Recupera e processa os dados de IDs para todos os anos especificados.
- main(): Função principal que inicia o processo de combinação.

Como usar:
Execute o script para combinar os dados de IDs da Comvest com os dados do Enem.
"""


import pandas as pd
from pandas import DataFrame
import os
from tqdm import tqdm
from enem.utilities.io import write_result

COMVEST_IDS_PATH = '/home/gsiqueira/dados-unicamp/input/ids/dac_comvest_ids.csv'
COMVEST_ENEM_PATH = '/home/gsiqueira/dados-unicamp/output/insc_comvest_enem/'
RESULT_PATH = '/home/output/intermediario/Enem-Comvest/ids_comvest_enem/'

def merge_ids_per_year(comvest_enem: DataFrame, comvest_ids: DataFrame, year: int) -> DataFrame:
    """
    Mescla os dados de IDs da Comvest com os dados do Enem para um ano específico.

    Parâmetros
    ----------
    comvest_enem : DataFrame
        DataFrame contendo os dados do Enem para o ano específico.
    comvest_ids : DataFrame
        DataFrame contendo os IDs da Comvest.
    year : int
        O ano para o qual os dados serão mesclados.

    Retorna
    -------
    DataFrame
        DataFrame resultante da mescla dos dados.
    """
    comvest_enem_ids_year = comvest_ids.merge(comvest_enem, left_on='insc_vest_comvest', right_on=f'comvest_{year}')
    comvest_enem_ids_year = comvest_enem_ids_year.drop(columns=[f'comvest_{year}', 'insc_vest_comvest', 'ano_ingresso_curso'])
    comvest_enem_ids_year = comvest_enem_ids_year.rename(columns={"id" : f'id_comvest_{year}'})
    return comvest_enem_ids_year


def retrieve_ids(comvest_ids_year: DataFrame, year: int) -> None:
    """
    Recupera e processa os dados de IDs para um ano específico.

    Parâmetros
    ----------
    comvest_ids_year : DataFrame
        DataFrame contendo os IDs da Comvest para o ano específico.
    year : int
        O ano para o qual os dados serão recuperados.

    Retorna
    -------
    None
    """
    COMVEST_PATHS = [f"{COMVEST_ENEM_PATH}INSC{y}_COMV{year}.csv" for y in range(year - 2, year)]
    RESULT_PATHS = [f'{RESULT_PATH}insc{y}_comv{year}_ids.csv' for y in range(year - 2, year)]
   
    comvest_enem_dfs = [pd.read_csv(FILE) for FILE in COMVEST_PATHS if os.path.isfile(FILE)]
    
    comvest_enem_ids = list(map(lambda comvest_enem : merge_ids_per_year(comvest_enem, comvest_ids_year, year), comvest_enem_dfs))

    os.makedirs(RESULT_PATH, exist_ok=True)
    
    for i, ids in enumerate(comvest_enem_ids): 
        ids.to_csv(RESULT_PATHS[i], index=False)


def retrieve() -> None:
    """
    Recupera e processa os dados de IDs para todos os anos especificados.

    Retorna
    -------
    None
    """
    comvest_ids = pd.read_csv(COMVEST_IDS_PATH)
    comvest_ids = comvest_ids.loc[:, ['id', 'insc_vest_comvest', 'ano_ingresso_curso']]

    for year in tqdm(range(2012, 2024)):
        print(f"retrieving ids from year {year} from DAC_COMVEST_IDS to COMVEST_ENEM_{year}")
        comvest_ids_year = comvest_ids[comvest_ids['ano_ingresso_curso'] == year]
        retrieve_ids(comvest_ids_year, year)


def main() -> None:
    retrieve()


if __name__ == '__main__':
    main()
    