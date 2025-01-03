"""
Módulo principal para a extração de dados dos cursos Comvest.

Este módulo executa a função principal para extrair dados dos cursos Comvest usando os submódulos `extrair_cursos` e `dict_cursos`.

Funções:
- main(): Executa a extração dos dados dos cursos Comvest.

Como usar:
Execute este script para realizar a extração dos dados dos cursos Comvest.

Exemplo:
python -m comvest.extract_courses
"""


from comvest.extract_courses import extrair_cursos
from comvest.extract_courses import dict_cursos

# No preprocessing needed
def main():
    extrair_cursos.extraction()
    dict_cursos.get()


if __name__ == '__main__':
    main()
