from dac.utilities.columns import dados_cadastrais_cols
from dac.utilities.io import read_result
from dac.utilities.io import read_from_database
from dac.utilities.io import read_csv_from_database
from dac.utilities.io import write_result
from dac.clr_dados_cadastrais.dados_cadastrais import clear_dados_cadastrais_pre_99
from dac.create_ufs_codes.utilities import concat_and_drop_duplicates
import re


def generate_comvest():
    comvest = read_csv_from_database("dados_comvest.csv")

    nasc = comvest[['mun_nasc_c', 'uf_nasc_c']]
    resid = comvest[['mun_resid_c', 'uf_resid']]
    esc = comvest[['mun_esc_em', 'uf_esc_em']]

    nasc.columns = ['municipio', 'uf']
    resid.columns = ['municipio', 'uf']
    esc.columns = ['municipio', 'uf']

    result = concat_and_drop_duplicates([nasc, resid, esc])
    return result