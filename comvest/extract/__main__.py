"""
Módulo principal para a extração e processamento de dados Comvest.

Este módulo executa a função principal para extrair e processar dados Comvest usando os módulos `extract_comvest`, `merge_sheets` e `comvest_ids`.

Funções:
- extract(): Executa a extração e processamento dos dados Comvest.

Como usar:
Execute este script para realizar a extração e processamento dos dados Comvest.

Exemplo:
python -m comvest.extract
"""


from comvest.extract import extract_comvest
from comvest.extract import merge_sheets
from comvest.assign_ids import comvest_ids


def extract():
    """
    Executa a extração e processamento dos dados Comvest.

    Retorna:
    -------
    None
    """
    extract_comvest.extraction()
    merge_sheets.merge()
    comvest_ids.assign_ids()


if __name__ == "__main__":
    extract()
