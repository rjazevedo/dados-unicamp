from dac.clr_dados_cadastrais import dados_cadastrais
from dac.clr_dados_cadastrais import dados_pre_and_pos
import dac.create_ufs_codes.__main__ as create_ufs_codes
import dac.create_names_ids.__main__ as create_names_ids
from dac.utilities.io import check_if_need_result_file
from dac.clr_dados_cadastrais.dados_cadastrais import DADOS_CADASTRAIS
from dac.clr_dados_cadastrais.dados_cadastrais import UF_CODE_NAME
from dac.clr_dados_cadastrais.dados_cadastrais import SCHOOL_CODES
from dac.clr_dados_cadastrais.dados_cadastrais import ID_NAMES

def main():
    pre_processing()
    dados_cadastrais.generate_clean_data()

def pre_processing():
    if check_if_need_result_file(DADOS_CADASTRAIS):
        dados_pre_and_pos.load_dados_cadastais()
    if check_if_need_result_file(UF_CODE_NAME):
        create_ufs_codes.main()
    if check_if_need_result_file(SCHOOL_CODES):
        #clear_dados.main()
        print("Sem base da comvest")
    if check_if_need_result_file(ID_NAMES):
        create_names_ids.main()
        
if __name__ == '__main__':
    main()