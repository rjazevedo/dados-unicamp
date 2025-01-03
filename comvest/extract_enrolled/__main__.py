"""
Módulo principal para a extração de dados dos matriculados e convocados Comvest.

Este módulo executa a função principal para extrair dados dos matriculados e convocados Comvest usando os submódulos `extrair_matriculados` e `extrair_convocados`.

Funções:
- main(): Executa a extração dos dados dos matriculados e convocados Comvest.
- pre_processing(): Verifica se é necessário gerar o arquivo de cursos antes de extrair os dados dos matriculados e convocados.

Como usar:
Execute este script para realizar a extração dos dados dos matriculados e convocados Comvest.

Exemplo:
python -m comvest.extract_enrolled
"""


from comvest.extract_enrolled import extrair_matriculados, extrair_convocados
from dac.utilities.io import check_if_need_result_file
import comvest.extract_courses.__main__ as extrair_cursos


CURSOS = "cursos.csv"


def main():
    pre_processing()
    extrair_matriculados.extraction()
    extrair_convocados.extraction()


def pre_processing():
    """
    Verifica se é necessário gerar o arquivo de cursos antes de extrair os dados dos matriculados e convocados.

    Retorna
    -------
    None
    """
    if check_if_need_result_file(CURSOS):
        extrair_cursos.main()

if __name__ == "__main__":
    main()
