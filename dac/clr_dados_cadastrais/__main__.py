from dac.clr_dados_cadastrais import dados_cadastrais
from dac.clr_dados_cadastrais import dados_pre_and_pos
import dac.create_ufs_codes.__main__ as create_ufs_codes
import dac.create_names_ids.__main__ as create_names_ids
from dac.utilities.io import Bases
import os

PRE_AND_POS =  "dados_cadastrais_intermediario.csv"
UF_CODE_NAME = 'final_counties.csv'
SCHOOL_CODES = "escola_codigo_inep.csv"
ID_NAMES = "ids_of_names.csv"


def main():
    pre_processing()
    dados_cadastrais.generate_clean_data()

def pre_processing():
    if not(os.path.exists(Bases.RESULT_DAC.value + PRE_AND_POS)):    
        dados_pre_and_pos.load_dados_cadastais()

    if not(os.path.exists(Bases.RESULT_DAC.value + UF_CODE_NAME)):    
        print("create uf codes")
        create_ufs_codes.main()
    
    if not(os.path.exists(Bases.RESULT_COMVEST.value + SCHOOL_CODES)):    
        # TODO: Rodar o código da comvest
        print("Sem base da comvest")

    if not(os.path.exists(Bases.RESULT_DAC.value + ID_NAMES)):    
        print("create ids")
        create_names_ids.main()


if __name__ == '__main__':
    main()