from comvest.escolas import validacao_esc
from dac.utilities.io import check_if_need_result_file

from dac.clr_dados_cadastrais import limpeza_dados
from dac.clr_dados_cadastrais import setup_dados
from dac.clr_dados_cadastrais import uf_codes

import dac.create_ufs_codes.__main__ as create_ufs_codes
import comvest.extract_courses.__main__ as courses
import comvest.clear_dados.limpeza_dados as limpeza_dados
from comvest.clear_dados import limpeza_dados, cod_ibge
import dac.create_ufs_codes.__main__ as create_ufs_codes

DADOS_CADASTRAIS = "dados_cadastrais_com_uf.csv"
DADOS_COMVEST = "dados_comvest_com_uf.csv"
UF_CODE_NAME = 'final_counties.csv'

def main():
    pre_processing()
    validacao_esc.validation()
    
def pre_processing():   
    if check_if_need_result_file(UF_CODE_NAME):
        create_ufs_codes.main() 

    if check_if_need_result_file(DADOS_CADASTRAIS):
        setup_dados.load_dados_cadastais()
        limpeza_dados.generate_clean_data()
        uf_codes.generate_uf_code()

    if check_if_need_result_file(DADOS_COMVEST):
        limpeza_dados.extraction()
        cod_ibge.merge()

if __name__ == "__main__":
    main()