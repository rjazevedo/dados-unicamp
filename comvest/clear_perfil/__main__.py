"""
Módulo principal para a limpeza e extração de perfil Comvest.

Este módulo executa a função principal para limpar e extrair perfil Comvest usando os módulos `limpeza_perfil`, `extract_courses` e `extract_cities`.

Funções:
- main(): Função principal que chama as funções de extração e limpeza de perfil.
- pre_processing(): Função que verifica a necessidade de arquivos de resultado e chama as funções de criação correspondentes.

Como usar:
Execute este script para realizar a limpeza e extração de perfil Comvest.

Exemplo:
python -m comvest.clear_perfil
"""


from comvest.clear_perfil import limpeza_perfil
from dac.utilities.io import check_if_need_result_file
import comvest.extract_courses.__main__ as extrair_cursos
import comvest.extract_cities.__main__ as extrair_cidades

CIDADES = "cidades_comvest.csv"
CURSOS = "cursos.csv"

def main():
    pre_processing()
    limpeza_perfil.extraction()

def pre_processing():
    """
    Função que verifica a necessidade de arquivos de resultado e chama as funções de criação correspondentes.

    Retorna
    -------
    None
    """
    if check_if_need_result_file(CURSOS):
        extrair_cursos.main()
    if check_if_need_result_file(CIDADES):
        extrair_cidades.main()


if __name__ == "__main__":
    main()
