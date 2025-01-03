"""
Módulo para atribuição de IDs Comvest.

Este módulo contém a função para atribuir IDs Comvest aos dados lidos de arquivos CSV.

Funções:
- assign_ids(): Atribui IDs Comvest aos dados e salva o resultado em um arquivo CSV.

Como usar:
Implemente e execute a função `assign_ids` para atribuir IDs Comvest aos dados.
"""


import pandas as pd
from comvest.utilities.io import read_output, write_output, read_result
from comvest.utilities.dtypes import (
    DTYPES_DADOS,
    DTYPES_PERFIL,
    DTYPES_MATRICULADOS,
    DTYPES_NOTAS,
)


def assign_ids():
    """
    Atribui IDs Comvest aos dados e salva o resultado em um arquivo CSV.

    Lê os dados de arquivos CSV, atribui IDs Comvest aos registros e salva o resultado em um novo arquivo CSV.

    Retorna
    -------
    None
    """
    comvest = read_output(
        "comvest_amostra.csv",
        dtype={**DTYPES_DADOS, **DTYPES_PERFIL, **DTYPES_MATRICULADOS, **DTYPES_NOTAS},
    )

    # 5 registros com número de inscrição igual a 'n'
    ids = read_result(
        "dac_comvest_ids.csv",
        dtype={
            "id": "Int64",
            "insc_vest_comvest": "Int64",
            "ano_ingresso_curso": "Int64",
        },
        na_values="n",
    ).loc[:, ["id", "insc_vest_comvest", "ano_ingresso_curso"]]
    ids.columns = ["id", "insc_vest", "ano_vest"]

    comvest_with_ids = pd.merge(comvest, ids, on=["insc_vest", "ano_vest"], how="left")
    comvest_without_ids = comvest_with_ids[comvest_with_ids["id"].isna()]

    comvest_with_ids.drop(columns=["insc_vest"], inplace=True)

    write_output(comvest_with_ids, "comvest_amostra.csv")
