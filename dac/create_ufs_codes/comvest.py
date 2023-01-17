from dac.utilities.columns import dados_cadastrais_cols
from dac.utilities.io import read_result
from dac.create_ufs_codes.utilities import concat_and_drop_duplicates
import re

DADOS_COMVEST = "dados_comvest.csv"

def generate_comvest():
    comvest = read_result(DADOS_COMVEST)

    nasc = comvest[['mun_nasc_c', 'uf_nasc_c']]
    resid = comvest[['mun_resid_c', 'uf_resid']]
    esc = comvest[['mun_esc_em_c', 'uf_esc_em']]

    nasc.columns = ['municipio', 'uf']
    resid.columns = ['municipio', 'uf']
    esc.columns = ['municipio', 'uf']

    result = concat_and_drop_duplicates([nasc, resid, esc])
    return result