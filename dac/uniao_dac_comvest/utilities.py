import pandas as pd
import re
import numpy as np
from dac.utilities.format import fill_doc
from dac.utilities.io import read_result as read_result_dac
from comvest.utilities.io import read_result as read_result_comvest
from dac.utilities.io import write_result
from dac.utilities.io import read_result as read_result_dac, write_output


def validar_CPF(cpf: str) -> str:
    """
    Assume que CPF não nulo é uma string de 11 dígitos
    Assume que CPF nulo é '-'
    """
    if len(cpf) != 11:
        return "-"

    # CPF com 1 dígito repetido 11 vezes é considerado inválido
    if len(set(cpf)) == 1:
        return "-"

    cpf_num = [int(char) for char in cpf if char.isdigit()]

    # Verifica se o CPF contém um caracterer não numerico
    if len(cpf_num) != 11:
        return "-"

    #  Valida os dois dígitos verificadores
    for i in range(9, 11):
        valor = sum((cpf_num[num] * (i + 1 - num) for num in range(0, i)))
        digito = ((valor * 10) % 11) % 10
        if digito != cpf_num[i]:
            return "-"

    return cpf


def set_origemCPF(cpf_dac, cpf_comvest):
    """
    Coluna Origem CPF:
        2 se veio da DAC
        1 se veio da Comvest
        0 se não temos CPF nem na DAC nem na Comvest
    """

    if cpf_dac == "-" and cpf_comvest == "-":
        return 0
    if cpf_dac == "-" and cpf_comvest != "-":
        return 1
    if cpf_dac != "-":
        return 2


def select_CPF(cpf_dac, cpf_comvest):
    if cpf_dac != "-":
        return cpf_dac
    elif cpf_comvest != "-":
        return cpf_comvest
    else:
        return "-"


def select_name(nome_dac, nome_comvest):
    if nome_dac != "-":
        return nome_dac
    elif nome_comvest != "-":
        return nome_comvest
    else:
        return "-"


def select_doc(doc_dac, doc_comvest):
    if doc_dac != "-":
        return doc_dac
    elif doc_comvest != "-":
        return doc_comvest
    else:
        return "-"


def select_dta(dta_dac, dta_comvest):
    if dta_dac != "-":
        return dta_dac
    elif dta_comvest != "-":
        return dta_comvest
    else:
        return "-"

def select_insc_vest(insc_vest_dac, insc_vest_comvest):
    if not pd.isnull(insc_vest_dac):
        return insc_vest_dac
    elif not pd.isnull(insc_vest_comvest):
        return insc_vest_comvest
    else:
        return np.nan


def setup_comvest():
    curso = read_result_comvest("matriculados_comvest.csv", dtype=str).loc[
        :, ["ano_vest", "insc_vest", "curso_matric"]
    ]
    curso.columns = ["ano_ingresso_curso", "insc_vest", "curso"]

    comvest = read_result_comvest("dados_comvest.csv", dtype=str).loc[
        :,
        [
            "nome_c",
            "cpf",
            "doc_c",
            "dta_nasc_c",
            "insc_vest",
            "ano_vest",
            "tipo_ingresso_comvest",
        ],
    ]
    comvest.columns = [
        "nome",
        "cpf",
        "doc",
        "dta_nasc",
        "insc_vest",
        "ano_ingresso_curso",
        "tipo_ingresso_comvest",
    ]

    df = pd.merge(comvest, curso, how="left", on=["ano_ingresso_curso", "insc_vest"])

    df.dta_nasc = df.dta_nasc.astype(str).str.replace(".0", "", regex=False)
    df.insc_vest = df.insc_vest.astype("float64")
    df.doc = df.doc.astype(str)
    df.doc = fill_doc(df.doc, 15)
    df.doc = df.doc.replace("0" * 15, "-")
    df.dta_nasc = df.dta_nasc.astype(str).str.zfill(8)

    df["merge_id"] = range(0, len(df))
    return df


def setup_dac():
    df = read_result_dac("dados_ingressante.csv", dtype=str).loc[
        :,
        [
            "identif",
            "nome",
            "cpf",
            "doc",
            "dta_nasc",
            "insc_vest",
            "ano_ingresso_curso",
            "origem",
            "curso",
            "tipo_ingresso",
        ],
    ]
    df.insc_vest.replace("", np.nan, inplace=True)
    df.insc_vest = df.insc_vest.astype("float64")
    df.doc = fill_doc(df.doc, 15)
    df.dta_nasc = df.dta_nasc.astype(str).str.zfill(8)
    df.cpf = df.cpf.replace("\.0", "", regex=True)
    df.cpf = df.cpf.replace(np.nan, "")
    df.cpf = df.cpf.str.zfill(11)
    df.cpf = df.cpf.replace("0" * 11, "-")
    return df


def get_wrong_and_right(df, correct_merge_list):
    filt = pd.Series(dtype=str)
    if "doc_comvest" in df.columns:
        filt = df.doc_comvest.isnull()
    elif "dta_nasc_comvest" in df.columns:
        filt = df.dta_nasc_comvest.isnull()
    else:
        filt = df.nome_comvest.isnull()

    wrong_merge = df[filt]
    wrong_merge = remove_discartable_columns(wrong_merge)
    right_merge = df[~filt].copy()
    right_merge = create_colums_for_concat(right_merge)

    correct_merge_list.append(right_merge)
    return (right_merge, wrong_merge)


def create_colums_for_concat(df, after_merge=True):
    new_df = df.copy()

    if after_merge:
        if "insc_vest_comvest" not in df.columns:
            new_df["insc_vest_comvest"] = df["insc_vest"]
        if "dta_nasc_comvest" not in df.columns:
            new_df["dta_nasc_comvest"] = df["dta_nasc"]
        if "doc_comvest" not in df.columns:
            new_df["doc_comvest"] = df["doc"]
        if "nome_comvest" not in df.columns:
            new_df["nome_comvest"] = df["nome"]

    new_df = new_df.reindex(
        columns=[
            "identif",
            "nome",
            "cpf",
            "doc",
            "dta_nasc",
            "insc_vest",
            "ano_ingresso_curso",
            "origem",
            "curso",
            "nome_comvest",
            "cpf_comvest",
            "doc_comvest",
            "dta_nasc_comvest",
            "insc_vest_comvest",
            "curso_comvest",
            "merge_id",
            "tipo_ingresso",
            "tipo_ingresso_comvest",
        ]
    )

    return new_df


def remove_discartable_columns(df):
    for column in df.columns:
        if "_comvest" in column:
            df = df.drop(columns=[column])
    df = df.drop(columns=["merge_id"])
    return df


def concat_dac_comvest(correct_merge_list, comvest):
    dac_df = pd.concat(correct_merge_list)
    dac_df = rename_dac(dac_df)

    merge_ids = dac_df["merge_id"].unique()
    comvest_filt = comvest["merge_id"].isin(merge_ids)
    comvest = comvest[~comvest_filt]
    comvest = create_columns_comvest_for_concat(comvest)

    uniao_dac_comvest = pd.concat([dac_df, comvest])

    return uniao_dac_comvest


def rename_dac(df):
    return df.rename(
        columns={
            "nome": "nome_dac",
            "cpf": "cpf_dac",
            "doc": "doc_dac",
            "dta_nasc": "dta_nasc_dac",
            "insc_vest": "insc_vest_dac",
            "curso": "curso_dac",
        }
    )


def create_columns_comvest_for_concat(comvest):
    comvest.columns = [
        c + "_comvest"
        if ("_comvest" not in c) and (c != "merge_id" and c != "ano_ingresso_curso")
        else c
        for c in comvest.columns
    ]

    comvest = comvest.reindex(
        columns=[
            "identif",
            "nome_dac",
            "cpf_dac",
            "doc_dac",
            "dta_nasc_dac",
            "insc_vest_dac",
            "ano_ingresso_curso",
            "origem",
            "curso_dac",
            "nome_comvest",
            "cpf_comvest",
            "doc_comvest",
            "dta_nasc_comvest",
            "insc_vest_comvest",
            "curso_comvest",
            "merge_id",
            "tipo_ingresso",
            "tipo_ingresso_comvest",
        ]
    )
    return comvest
