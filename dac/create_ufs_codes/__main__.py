from dac.create_ufs_codes import ufs_codes
from dac.utilities.io import check_if_need_result_file
from comvest.clear_dados import limpeza_dados
from dac.clr_dados_cadastrais import setup_dados

DADOS_CADASTRAIS = "dados_cadastrais_intermediario.csv"
DADOS_COMVEST = "dados_comvest.csv"

def main():
    pre_processing()
    ufs_codes.generate_clean_data()

def pre_processing():
    if check_if_need_result_file(DADOS_CADASTRAIS):
        setup_dados.dados_pre_and_pos()

    if check_if_need_result_file(DADOS_COMVEST):
        limpeza_dados.extraction()


if __name__ == '__main__':
    main()