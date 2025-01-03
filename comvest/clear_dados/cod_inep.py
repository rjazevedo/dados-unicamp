"""
Módulo para correção de códigos INEP das escolas nos dados Comvest.

Este módulo contém a função para corrigir os códigos INEP das escolas nos dados lidos de arquivos CSV.

Funções:
- merge(): Corrige os códigos INEP das escolas nos dados e salva o resultado em um arquivo CSV.

Como usar:
Implemente e execute a função `merge` para corrigir os códigos INEP das escolas nos dados.
"""


import pandas as pd
from comvest.utilities.io import read_result, write_result
from comvest.utilities.dtypes import DTYPES_DADOS


def merge():
    """
    Corrige os códigos INEP das escolas nos dados e salva o resultado em um arquivo CSV.

    Lê os dados de arquivos CSV, corrige os códigos INEP das escolas e salva o resultado em um novo arquivo CSV.

    Retorna
    -------
    None
    """
    df_comvest = read_result("dados_comvest_com_uf.csv", dtype=DTYPES_DADOS)
    res = read_result("escola_codigo_inep.csv", dtype={"Código INEP": "Int64"})

    merged_dados = df_comvest.merge(
        res,
        left_on=["esc_em_c", "mun_esc_em_c", "uf_esc_em"],
        right_on=["escola_base", "municipio_original", "uf_original"],
        how="left",
        suffixes=("", "_todrop"),
    )

    merged_dados["Código INEP"] = pd.to_numeric(
        merged_dados["Código INEP"], errors="coerce", downcast="integer"
    ).astype("Int64")
    todrop = [col for col in merged_dados.columns if "_todrop" in col] + [
        "escola_base",
        "municipio_base",
        "UF_base",
        "chave_seq",
        "UF_inep",
        "municipio_inep",
        "Etapas e Modalidade de Ensino Oferecidas",
        "chave_tok",
        "codigo_municipio",
        "municipio_original",
        "uf_original",
        "chave_seq_escs",
        "uf_novo",
        "municipio_novo",
        "chave_seq_inep",
    ]

    merged_dados.drop(columns=todrop, inplace=True, errors="ignore")
    merged_dados.rename({"Código INEP": "cod_esc_inep"}, axis=1, inplace=True)

    write_result(merged_dados, "dados_comvest.csv")
