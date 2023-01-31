from dac.uniao_dac_comvest import uniao_dac_comvest
import dac.clr_vida_academica.__main__ as clr_vida_academica
import comvest.extract_enrolled.__main__ as extrair_enrolled
from comvest.clear_dados import limpeza_dados
from dac.uniao_dac_comvest.utilities import DADOS_INGRESSANTE
from dac.uniao_dac_comvest.utilities import MATRICULADOS
from dac.uniao_dac_comvest.utilities import COMVEST
from dac.utilities.io import check_if_need_result_file

def main():
    pre_processing()
    uniao_dac_comvest.generate()

def pre_processing():
    if check_if_need_result_file(DADOS_INGRESSANTE):
        clr_vida_academica.main()

    if check_if_need_result_file(MATRICULADOS):
        extrair_enrolled.main()

    if check_if_need_result_file(COMVEST):
        limpeza_dados.extraction()


if __name__ == '__main__':
    main()