from dac.create_names_ids import create_ids
from dac.create_names_ids.create_ids import DADOS_DAC
from dac.create_names_ids.create_ids import DADOS_COMVEST
from dac.clr_dados_cadastrais import setup_dados
from dac.utilities.io import check_if_need_result_file
from comvest.clear_dados import limpeza_dados

def main():
    pre_processing()
    create_ids.create_ids()

def pre_processing():
    if check_if_need_result_file(DADOS_DAC):
        setup_dados.load_dados_cadastais()
    
    if check_if_need_result_file(DADOS_COMVEST):
        limpeza_dados.extraction()
            
if __name__ == '__main__':
    main()