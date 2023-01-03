from dac.create_names_ids import create_ids
from dac.clr_dados_cadastrais import dados_pre_and_pos
from dac.utilities.io import Bases
import os

PRE_AND_POS = "dados_cadastrais_intermediario.csv"
DADOS_COMVEST = "dados_comvest.csv"

def main():
    pre_processing()
    create_ids.create_ids()


def pre_processing():
    if not(os.path.exists(Bases.RESULT_DAC.value + PRE_AND_POS)):
        dados_pre_and_pos.load_dados_cadastais()
    
    if not(os.path.exists(Bases.RESULT_COMVEST.value + DADOS_COMVEST)):
        print("sem dados da comvest")
            
if __name__ == '__main__':
    main()