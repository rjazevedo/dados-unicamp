"""
Módulo principal para a limpeza e extração de notas Comvest.

Este módulo executa a função principal para limpar e extrair notas Comvest usando os módulos `limpeza_notas` e `presenca`.

Funções:
- main(): Função principal que chama as funções de extração e limpeza de notas.

Como usar:
Execute este script para realizar a limpeza e extração de notas Comvest.

Exemplo:
python -m comvest.clear_notas
"""


from comvest.clear_notas import limpeza_notas, presenca

def main():
    limpeza_notas.extraction()
    presenca.get()

if __name__ == '__main__':
    main()