import pandas as pd 
import numpy as np

#df = pd.read_csv('/home/fernando/dados-unicamp/dac/results/vida_academica.csv')
df = pd.read_excel('/home/fernando/dados-unicamp/input/dac/VidaAcademicaCursoHabilitacao.xlsx')

colunas = df.columns

for c in colunas:
    print(c)
    print(df[c].unique())
