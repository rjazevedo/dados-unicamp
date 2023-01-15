from dac.create_ufs_codes import ufs_codes
from dac.utilities.io import Bases
import os

DADOS_CADASTRAIS = "dados_cadastrais_intermediario.csv"
DADOS_COMVEST = "dados_comvest.csv"


def main():
    pre_processing()
    ufs_codes.generate_clean_data()


def pre_processing():
    if not(os.path.exists(Bases.RESULT_DAC.value + DADOS_CADASTRAIS)):
        dados_cadastrais.dados_pre_and_pos()

    if not(os.path.exists(Bases.RESULT_COMVEST.value + DADOS_COMVEST)):
        print("Sem base da comvest")
        # TODO: implementar


if __name__ == '__main__':
    main()