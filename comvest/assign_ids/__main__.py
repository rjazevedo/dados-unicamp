"""
Módulo principal para a atribuição de IDs Comvest.

Este módulo executa a função principal para atribuir IDs Comvest usando o módulo `comvest_ids`.

Funções:
- main(): Função principal que chama a função `assign_ids` do módulo `comvest_ids`.

Como usar:
Execute este script para atribuir IDs Comvest.

Exemplo:
python -m comvest.assign_ids
"""


from comvest.assign_ids import comvest_ids


def main():
    comvest_ids.assign_ids()

if __name__ == '__main__':
    main()
