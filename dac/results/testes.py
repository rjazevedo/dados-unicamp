import pandas as pd 
import numpy as np

def testarMissing(serie):
    if '' in serie.unique():
        print('deu ruim')
    else:
        print('deu bom')

DTYPES_HISTORICO_ESCOLAR = {
    'identif'                  :         'int64',
    'periodo'                  :         'int64',
    'ano'                      :         'int64',
    'dt_inicio'                :             str,
    'dt_fim'                   :             str,
    'cod_curricularidade'      :         'int64',
    'curricularidade'          :          object,
    'disc'                     :          object,
    'turma'                    :          object,
    'cod_situacao'             :         'int64',  
    'situacao'                 :          object,  
    'nota'                     :       'float64',
    'frequencia'               :         'int64',  
    'creditos'                 :         'int64',
}

df = pd.read_csv('/home/fernando/dados-unicamp/dac/results/vida_academica.csv')

# teste 0 deve ser transformado em missing ano_conclu_em
#print(df['ano_conclu_em'].unique())

# testar se cep_nasc tem '-'
#testarMissing(df['cep_escola_em'])
#testarMissing(df['cep_atual'])

# testar se eu consegui converter coluna pra um certo tipo
#print(df['ano_conclu_em'].head())
#print(df['ano_conclu_em'].unique())

print(df['ano_saida'].unique())