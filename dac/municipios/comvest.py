from dac.utilities.columns import dados_cadastrais_cols
from dac.utilities.io import read_from_database
from dac.utilities.io import write_output
from comvest.utilities.dtypes import DTYPES_DADOS
import pandas as pd

def generate_mun_comvest():
    dfs = []
    for year in range(1997, 2021):
        path = '/home/fernando/dados-unicamp/input/comvest/vest' +  str(year) + '.xlsx'
        df = pd.read_excel(path, sheet_name='dados')
        df.columns = DTYPES_DADOS.keys()

        df1 = df[['mun_nasc_c', 'uf_nasc_c']]
        df2 = df[['mun_resid_c', 'uf_resid']] 
        df3 = df[['mun_esc_em_c', 'uf_esc_em']]
        df_concat = concat_and_drop_duplicates([df1, df2, df3])
        dfs.append(concat)
    
    result = concat_and_drop_duplicates(dfs)
    return result

def concat_and_drop_duplicates(dfs):
    concat = pd.concat(dfs, ignore_index = True)
    concat = concat.drop_duplicates(keep=False)
    return concat