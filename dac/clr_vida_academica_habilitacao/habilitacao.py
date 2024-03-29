from dac.clr_vida_academica_habilitacao import cursos_habilitacoes
from dac.clr_vida_academica_habilitacao import vida_academica_habilitacao
from dac.utilities.io import write_result
from dac.utilities.io import write_output
import pandas as pd

RESULT_NAME = 'vida_academica_habilitacao.csv'

def generate():
    habilitacoes_df = cursos_habilitacoes.generate_clean_data()
    vida_habilitacao_df = vida_academica_habilitacao.generate() 
    merged_df = pd.merge(vida_habilitacao_df, habilitacoes_df, on=['curso', 'ano_ingresso', 'codigo_habilitacao'], how='left')
    merged_df = merged_df.drop_duplicates()
    write_result(merged_df, RESULT_NAME)

if __name__ == '__main__':
    main()