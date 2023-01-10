from dac.uniao_dac_comvest import uniao_dac_comvest
import dac.clr_vida_academica.__main__ as clr_vida_academica
from dac.uniao_dac_comvest.utilities import DADOS_INGRESSANTE
from dac.uniao_dac_comvest.utilities import MATRICULADOS
from dac.uniao_dac_comvest.utilities import COMVEST
from dac.utilities.io import Bases
import os


def main():
    pre_processing()
    uniao_dac_comvest.generate()


def pre_processing():
    if not(os.path.exists(Bases.RESULT_DAC.value + DADOS_INGRESSANTE)):    
        clr_vida_academica.main()

    if not(os.path.exists(Bases.RESULT_COMVEST.value + MATRICULADOS)):    
        # TODO: Rodar o código da comvest
        print("Sem base da comvest")
    
    if not(os.path.exists(Bases.RESULT_COMVEST.value + COMVEST)):    
        # TODO: Rodar o código da comvest
        print("Sem base da comvest")


if __name__ == '__main__':
    main()