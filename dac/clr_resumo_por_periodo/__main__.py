from dac.clr_resumo_por_periodo import resumo_por_periodo
from dac.clr_resumo_por_periodo import resumo_periodo_cr

def main():
    resumo_por_periodo.generate_clean_data()
    resumo_periodo_cr.generate_cr()   

    
if __name__ == '__main__':
    main()