"""
Módulo para correção de códigos de municípios IBGE nos dados Comvest.

Este módulo contém a função para corrigir os códigos de municípios IBGE nos dados lidos de arquivos CSV.

Funções:
- merge(): Corrige os códigos de municípios IBGE nos dados e salva o resultado em um arquivo CSV.

Como usar:
Implemente e execute a função `merge` para corrigir os códigos de municípios IBGE nos dados.
"""


import pandas as pd
from comvest.utilities.io import read_result, read_output, write_result
from comvest.utilities.dtypes import DTYPES_DADOS


def merge():
    """
    Corrige os códigos de municípios IBGE nos dados e salva o resultado em um arquivo CSV.

    Lê os dados de arquivos CSV, corrige os códigos de municípios IBGE e salva o resultado em um novo arquivo CSV.

    Retorna
    -------
    None
    """
    dados = read_result("dados_comvest.csv", DTYPES_DADOS)
    tabela_mun = read_result("final_counties.csv")

    tabela_mun = tabela_mun[["municipio", "uf", "codigo_municipio", "municipio_ibge"]]
    tabela_mun = tabela_mun.drop_duplicates(["municipio", "uf"])

    tabela_mun.columns = [
        "mun_nasc_c",
        "uf_nasc_c",
        "cod_mun_nasc_c",
        "mun_nasc_corrigido",
    ]
    dados = pd.merge(dados, tabela_mun, how="left", on=["mun_nasc_c", "uf_nasc_c"])

    tabela_mun.columns = [
        "mun_resid_c",
        "uf_resid",
        "cod_mun_resid_c",
        "mun_resid_corrigido",
    ]
    dados = pd.merge(dados, tabela_mun, how="left", on=["mun_resid_c", "uf_resid"])

    tabela_mun.columns = [
        "mun_esc_em_c",
        "uf_esc_em",
        "cod_mun_esc_em_c",
        "mun_esc_corrigido",
    ]
    dados = pd.merge(
        dados,
        tabela_mun,
        how="left",
        on=["mun_esc_em_c", "uf_esc_em"],
    )

    dados["cod_mun_nasc_c"] = pd.to_numeric(
        dados["cod_mun_nasc_c"], errors="coerce", downcast="integer"
    ).astype("Int64")
    dados["cod_mun_resid_c"] = pd.to_numeric(
        dados["cod_mun_resid_c"], errors="coerce", downcast="integer"
    ).astype("Int64")
    dados["cod_mun_esc_em_c"] = pd.to_numeric(
        dados["cod_mun_esc_em_c"], errors="coerce", downcast="integer"
    ).astype("Int64")

    write_result(dados, "dados_comvest_com_uf.csv")
