"""
Módulo principal para a extração de dados dos filtros Comvest.

Este módulo executa a função principal para extrair dados dos filtros Comvest usando os submódulos `pedido_1`, `pedido_2` e `pedido_3`.

Funções:
- main(): Executa a extração dos dados dos filtros Comvest.

Como usar:
Execute este script para realizar a extração dos dados dos filtros Comvest.

Exemplo:
python -m comvest.filters
"""


from comvest.filters import pedido_1, pedido_2, pedido_3


def main():
    pedido_1.extract()
    pedido_2.extract()
    pedido_3.extract()


if __name__ == "__main__":
    main()
