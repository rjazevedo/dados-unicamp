"""
Módulo principal para a extração de dados das cidades Comvest.

Este módulo executa a função principal para extrair dados das cidades Comvest usando o submódulo `extrair_cidades`.

Funções:
- main(): Executa a extração dos dados das cidades Comvest.

Como usar:
Execute este script para realizar a extração dos dados das cidades Comvest.

Exemplo:
python -m comvest.extract_cities
"""


from comvest.extract_cities import extrair_cidades

# No preprocessing needed
def main():
    extrair_cidades.extraction()

if __name__ == '__main__':
    main()
