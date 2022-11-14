import pandas as pd
from comvest.utilities.io import read_auxiliary, write_auxiliary
from comvest.utilities.dtypes import DTYPES_DADOS
from comvest.escolas.utility import standardize_str
from comvest.escolas.utility import remove_countie_name_from_school
from comvest.utilities.io import read_result, write_result

COLUMNS = ["escola", 'codigo_municipio', 'municipio_original', 'uf_original']

def load_esc_bases():
    df_comvest = read_auxiliary("dados_comvest.csv", dtype=DTYPES_DADOS)
    df_dac = read_auxiliary("dados_cadastrais.csv")

    comvest_esc = df_comvest.loc[:, ["esc_em_c", "cod_mun_esc_em_c", "mun_esc_em_c", "uf_esc_em"]]
    dac_esc = df_dac.loc[:, ["escola_em_d", "cod_mun_form_em", 'mun_esc_form_em', 'uf_esc_form_em']]

    comvest_esc.columns = COLUMNS
    filt = comvest_esc['escola'].isnull()
    comvest_esc = comvest_esc[~filt]

    dac_esc.columns = COLUMNS
    filt = dac_esc['escola'].isnull()
    dac_esc = dac_esc[~filt]

    escs = pd.concat([comvest_esc, dac_esc])
    escs = escs.drop_duplicates(subset=["escola", "codigo_municipio"])

    escs = escs[~escs["escola"].isin(["ENEM", "ENCCEJA", "EJA","NAN", "", "0", "1", "00", "000"])]
    escs = escs[~escs["codigo_municipio"].isin(["NAN", ""])]

    escs = remove_countie_name_from_school(escs, 'municipio_original')
    escs = escs.drop_duplicates(subset=["escola", "codigo_municipio"])
    
    escs["chave_seq"] = escs['chave_seq'].apply(lambda r: standardize_str(r))
    escs["chave_seq_escs"] = escs['chave_seq']
    
    return escs