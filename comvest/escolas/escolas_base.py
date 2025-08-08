"""
Módulo para carregar e processar as bases de dados das escolas Comvest.

Este módulo contém funções para ler, limpar e processar os dados das escolas dos candidatos lidos de arquivos CSV.

Funções:
- load_esc_bases(): Carrega e processa as bases de dados das escolas.

Como usar:
Implemente e execute a função para carregar e processar os dados das escolas dos candidatos.
"""


import pandas as pd
from comvest.utilities.dtypes import DTYPES_DADOS
from comvest.escolas.utility import standardize_str
from comvest.utilities.io import read_result, write_result


COLUMNS = ["escola", 'codigo_municipio', 'municipio_original', 'uf_original']


def load_esc_bases():
    """
    Carrega e processa as bases de dados das escolas.

    Retorna
    -------
    DataFrame
        O DataFrame contendo os dados das escolas processados.
    """
    df_comvest = read_result("dados_comvest_com_uf.csv", dtype=DTYPES_DADOS)
    df_dac = read_result("dados_cadastrais_com_uf.csv")

    comvest_esc = df_comvest.loc[:, ["esc_em_c", "cod_mun_esc_em_c", "mun_esc_em_c", "uf_esc_em"]]
    dac_esc = df_dac.loc[:, ["escola_em_d", "cod_mun_form_em", 'mun_esc_form_em', 'uf_esc_form_em']]

    comvest_esc.columns = COLUMNS
    filt = comvest_esc['escola'].isnull()
    comvest_esc = comvest_esc[~filt]

    dac_esc.columns = COLUMNS
    filt = dac_esc['escola'].isnull()
    dac_esc = dac_esc[~filt]

    escs = pd.concat([comvest_esc, dac_esc])
    escs = escs.drop_duplicates(subset=["escola", "codigo_municipio", "uf_original"])

    escs = escs[~escs["escola"].isin(["ENEM", "ENCCEJA", "EJA","NAN", "", "0", "1", "00", "000"])]
    escs = escs[~escs["codigo_municipio"].isin(["NAN", ""])]

    escs["chave_seq"] = escs['escola'].apply(lambda r: standardize_str(r))
    return escs
