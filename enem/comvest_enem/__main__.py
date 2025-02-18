"""
Este script principal executa uma série de processos para limpar, combinar e dividir os dados do Enem e da Comvest para a Unicamp.
/home/giovani/dados-unicamp/enem/comvest_enem/__pycache__
Módulos necessários:
- clear_comvest: Para limpar os dados do Enem.
- divide_comvest: Para dividir os dados do Enem combinados com os dados da Comvest.
- comvest_enem: Para combinar os dados do Enem com os dados da Comvest.
- comvest_vest_ids: Para recuperar e processar os dados de IDs da Comvest.
- comvest_enem_ids: Para mesclar os dados de IDs da Comvest com os dados do Enem.

Funções:
- main(): Função principal que executa todos os processos de limpeza, combinação e divisão dos dados.

Como usar:
Execute este script para realizar todas as operações de limpeza, combinação e divisão dos dados do Enem e da Comvest.
"""


from enem.comvest_enem import clear_comvest 
from enem.comvest_enem import divide_comvest
from enem.comvest_enem import comvest_enem
from enem.comvest_enem import comvest_vest_ids
from enem.comvest_enem import comvest_enem_ids
from enem.comvest_enem import stand_fin
from enem.comvest_enem import concat_enem_fin


def main():
    clear_comvest.clean_all()
    stand_fin.main()
    concat_enem_fin.main()
    comvest_enem.merge()
    divide_comvest.split_all()
    comvest_vest_ids.retrieve()
    comvest_enem_ids.merge()


if __name__ == '__main__':
    main()
