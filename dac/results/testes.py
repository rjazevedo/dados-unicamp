import pandas as pd 
import numpy as np

df = pd.read_csv('/home/fernando/dados-unicamp/dac/results/dados_cadastrais.csv')

# trocar valores 0 por <NA>
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
print(df['cep_resid_d'].head(5))