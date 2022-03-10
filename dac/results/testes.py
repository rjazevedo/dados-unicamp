import pandas as pd 
import numpy as np

df = pd.read_csv('/home/fernando/dados-unicamp/dac/results/dados_cadastrais.csv')

# trocar valores 0 por <NA>
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
#df['ano_conclu_em'].replace(0, pd.NA, inplace=True)
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# trocar valores - por string()
# df['cep_nasc'].replace('-', '', inplace=True)
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

unique = df['cep_resid']
print(unique.head(5))