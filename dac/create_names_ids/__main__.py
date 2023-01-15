from dac.create_names_ids import create_ids
from dac.create_names_ids.create_ids import DADOS_DAC
from dac.create_names_ids.create_ids import DADOS_COMVEST
from dac.clr_dados_cadastrais import dados_pre_and_pos
from dac.utilities.io import Bases
import os

def main():
    pre_processing()
    create_ids.create_ids()

def pre_processing():
    if not(os.path.exists(Bases.RESULT_DAC.value + DADOS_DAC)):
        dados_pre_and_pos.load_dados_cadastais()
    
    if not(os.path.exists(Bases.RESULT_COMVEST.value + DADOS_COMVEST)):
        print("sem dados da comvest")
            
if __name__ == '__main__':
    main()