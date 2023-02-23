from functools import reduce
from comvest.utilities.io import read_result, write_output
from comvest.utilities.dtypes import (
    DTYPES_DADOS,
    DTYPES_PERFIL,
    DTYPES_MATRICULADOS,
    DTYPES_NOTAS,
)
import pandas as pd


def merge(
    dropcolumns=[
        "nome_c",
        "doc_c",
        "cpf",
        "dta_nasc_c",
        "nome_pai_c",
        "nome_mae_c",
    ]
):
    dados = read_result("dados_comvest.csv", dtype=DTYPES_DADOS)
    perfil = read_result("perfil_comvest.csv", dtype=DTYPES_PERFIL)
    notas = read_result("notas_comvest.csv", dtype=DTYPES_NOTAS)
    matriculados = read_result("matriculados_comvest.csv", dtype=DTYPES_MATRICULADOS)

    dfs = [dados, perfil, notas, matriculados]

    base_comvest = reduce(
        lambda left, right: pd.merge(
            left, right, on=["ano_vest", "insc_vest"], how="left"
        ),
        dfs,
    )

    # Retira variáveis que não serão disponibilizadas na base final
    base_comvest.drop(columns=dropcolumns, errors="ignore", inplace=True)

    base_comvest.loc[
        (base_comvest.ano_vest == 2006) & (base_comvest.insc_vest == 61079002),
        "mun_esc_em_c",
    ] = "UNAI-MG"
    base_comvest.loc[
        (base_comvest.ano_vest == 2006) & (base_comvest.insc_vest == 61551889),
        ["mun_nasc_c", "mun_resid_c"],
    ] = "TABAPUA-SP"
    base_comvest.loc[
        (base_comvest.ano_vest == 2007) & (base_comvest.insc_vest == 71108481),
        ["mun_nasc_c", "mun_resid_c", "mun_esc_em_c"],
    ] = "JACAREI-SP"
    base_comvest.loc[
        (base_comvest.ano_vest == 2007) & (base_comvest.insc_vest == 71124054),
        "esc_em_c",
    ] = "MULTIRAO COTIA-SP"

    FILE_NAME = "comvest_amostra.csv"
    write_output(base_comvest, FILE_NAME)
