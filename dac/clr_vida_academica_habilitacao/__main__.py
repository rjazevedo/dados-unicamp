from dac.clr_vida_academica_habilitacao import cursos_habilitacoes
from dac.clr_vida_academica_habilitacao import vida_academica_habilitacao
from dac.utilities.io import write_result
from dac.utilities.io import write_output
import pandas as pd

RESULT_NAME = 'vida_academica_habilitacao.csv'

def main():
    habilitacoes_df = cursos_habilitacoes.generate_clean_data()
    vida_habilitacao_df = vida_academica_habilitacao.generate()       
    merged_df = pd.merge(vida_habilitacao_df, habilitacoes_df, on=['curso', 'ano_ingresso', 'codigo_habilitacao'], how='left')
    
    filt = merged_df['total_creditos_curso_hab'].notnull()

    corect_merge = merged_df[filt]
    wrong_merge = merged_df[~filt]

    write_result(corect_merge, RESULT_NAME)
    
if __name__ == '__main__':
    main()