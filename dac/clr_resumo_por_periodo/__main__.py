from dac.clr_resumo_por_periodo import resumo_por_periodo
from dac.clr_resumo_por_periodo import resumo_periodo_cr
import dac.clr_historico_escolar.__main__ as clr_historico_escolar
from dac.utilities.io import Bases
import os

HIST_FILE = 'historico_creditos.csv'

def main():
    pre_processing()
    resumo_por_periodo.generate_clean_data()
    resumo_periodo_cr.generate_cr()   

def pre_processing():
    if not(os.path.exists(Bases.RESULT_DAC.value + HIST_FILE)):    
        clr_historico_escolar.main()

    
if __name__ == '__main__':
    main()