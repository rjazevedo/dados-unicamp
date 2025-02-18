"""
Esse script serve para limpar e padronizar os dados dos arquivos fin, compatibilizando-os com o enem e permitindo o merge com a comvest.

Módulos necessários:
- pandas: Para manipulação de dados em DataFrames.
- tqdm: Para exibir uma barra de progresso.
- enem.utilities.io: Para escrever os resultados (não utilizado no trecho fornecido).

Funções:
- clear_fin(year): Limpa os dados dos arquivos fin para um ano específico.
- main(): Função principal que inicia o processo de limpeza dos dados.

Como usar:
Execute o script para limpar os dados dos arquivos fin para os anos de 2018 a 2022.
"""

from tqdm import tqdm
from enem.utilities.io import write_result
import pandas as pd
import numpy as np


def standardize_fin(year: str) -> None:
    """
    Limpa os dados dos arquivos fin para os anos de 2018 a 2022
    
    Padroniza o arquivo para que ele seja compatível com os arquivos do enem para o ano em questão
    
    Parâmetros
    ----------
    year : str
        O ano para o qual os dados serão limpos (dois últimos dígitos).
    """
    year_suffix = str(year)[-2:]
    FIN_PATH = f'/home/input/Enem_Unicamp/fin{year_suffix}.xlsx'

    fin = pd.read_excel(FIN_PATH)
    
    # Ajustando as colunas do fin para ficar com as mesmas do enem
    fin = fin.iloc[:, :9]
    fin = fin.rename(columns={
        "INSC": f"comvest_{year + 1}",
        "cpf": "CPF",
        "nome": "NOME",
        "ncnt": f"ncnt{year}",
        "ncht": f"ncht{year}",
        "nlct": f"nlct{year}",
        "nmt": f"nmt{year}",
        "nred": f"nred{year}"
    })
    fin = fin[[f"comvest_{year + 1}", f"enem{year}", "NOME", "CPF", f"ncnt{year}", f"ncht{year}", f"nlct{year}", f"nmt{year}", f"nred{year}"]]

    cols_to_add = [f'enem{year - 1}' ,f'ncnt{year - 1}', f'ncht{year - 1}', f'nlct{year - 1}', 
                    f'nmt{year - 1}', f'nred{year - 1}']
    
    # Preenche as novas colunas com valores nulos
    for col in cols_to_add:
        fin[col] = np.nan
    
    # Ajusta a ordem das colunas do fin para que seja a mesma do df do enem
    fin = fin[[f'comvest_{year + 1}', f'enem{year - 1}', f'enem{year}', 'NOME', 'CPF',
             f'ncnt{year - 1}', f'ncht{year - 1}', f'nlct{year - 1}', f'nmt{year - 1}', f'nred{year - 1}',
             f'ncnt{year}', f'ncht{year}', f'nlct{year}', f'nmt{year}', f'nred{year}']]

    if year == 2020:
        write_result(fin, f'Enem_Comvest/EnemComvest{year + 1}.csv')
    
    write_result(fin, f'Enem_Comvest/fin_stand{year + 1}.csv')


def main() -> None:
    for year in tqdm(range(2018, 2023)):
        print(f"Standardizing fin {year}...")
        standardize_fin(year)


if __name__ == "__main__":
    main()
