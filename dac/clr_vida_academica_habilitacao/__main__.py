from dac.clr_vida_academica_habilitacao import cursos_habilitacoes
from dac.clr_vida_academica_habilitacao import vida_academica_habilitacao
from dac.utilities.io import write_result
from dac.utilities.io import write_output
import pandas as pd

RESULT_NAME = 'vida_academica_habilitacao.csv'

def main():
    habilitacoes_df = cursos_habilitacoes.generate_clean_data()
    vida_habilitacao_df = vida_academica_habilitacao.generate()

    print(vida_habilitacao_df['codigo_habilitacao'].unique())
    print(habilitacoes_df['codigo_habilitacao'].unique())

    print(vida_habilitacao_df['curso'].unique())
    print(habilitacoes_df['curso'].unique())

    print(vida_habilitacao_df['ano_ingresso'].unique())
    print(habilitacoes_df['ano_ingresso'].unique())       

    print(vida_habilitacao_df.shape)
    merged_df = pd.merge(vida_habilitacao_df, habilitacoes_df, on=['curso', 'ano_ingresso', 'codigo_habilitacao'], how='left')
    print(merged_df.shape)
    write_result(merged_df, RESULT_NAME)

    for c in merged_df.columns:
        print(merged_df[c].unique())

if __name__ == '__main__':
    main()