from dac.clr_dados_cadastrais import limpeza_dados
from dac.clr_dados_cadastrais import school_codes
from dac.clr_dados_cadastrais import setup_dados
from dac.clr_dados_cadastrais import uf_codes
import dac.create_ufs_codes.__main__ as create_ufs_codes
import dac.create_names_ids.__main__ as create_names_ids
from dac.utilities.io import check_if_need_result_file
import comvest.escolas.__main__ as escolas
from dac.clr_dados_cadastrais.limpeza_dados import DADOS_CADASTRAIS
from dac.clr_dados_cadastrais.limpeza_dados import ID_NAMES
from dac.clr_dados_cadastrais.uf_codes import UF_CODE_NAME
from dac.clr_dados_cadastrais.school_codes import SCHOOL_CODES

def main():
    pre_processing()
    limpeza_dados.generate_clean_data()
    uf_codes.generate_uf_code()
    school_codes.generate_school_codes()

def pre_processing():
    if check_if_need_result_file(DADOS_CADASTRAIS):
        setup_dados.load_dados_cadastais()
    if check_if_need_result_file(UF_CODE_NAME):
        create_ufs_codes.main()
    if check_if_need_result_file(SCHOOL_CODES):
        escolas.main()
    if check_if_need_result_file(ID_NAMES):
        create_names_ids.main()
        
if __name__ == '__main__':
    main()