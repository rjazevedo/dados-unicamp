import pandas as pd
import numpy as np
from dac.utilities.io import write_result
from dac.uniao_dac_comvest.cursos_especiais import deal_special_students
from dac.uniao_dac_comvest.doc_part import merge_by_doc_part
from dac.uniao_dac_comvest.utilities import (
    get_wrong_and_right,
    select_doc,
    select_dta,
    select_insc_vest,
    select_name,
)
from dac.uniao_dac_comvest.utilities import concat_dac_comvest
from dac.uniao_dac_comvest.utilities import validar_CPF
from dac.uniao_dac_comvest.utilities import select_CPF
from dac.uniao_dac_comvest.utilities import setup_comvest
from dac.uniao_dac_comvest.utilities import setup_dac
from dac.uniao_dac_comvest.utilities import set_origemCPF
from dac.uniao_dac_comvest.closest_name import get_closest_name

RESULT_NAME = "uniao_dac_comvest.csv"


def generate():
    print("Lendo dados da Comvest")
    dados_comvest = setup_comvest()
    print("Lendo dados da Dac")
    dados_dac = setup_dac()
    correct_merge_list = []

    uniao_dac_comvest = pd.merge(
        dados_dac,
        dados_comvest,
        how="left",
        on=["insc_vest", "ano_ingresso_curso"],
        suffixes=("", "_comvest"),
    )
    wrong_and_right = get_wrong_and_right(uniao_dac_comvest, correct_merge_list)

    uniao_dac_comvest = pd.merge(
        wrong_and_right[1],
        dados_comvest,
        how="left",
        on=["nome", "ano_ingresso_curso", "dta_nasc"],
        suffixes=("", "_comvest"),
    )
    wrong_and_right = get_wrong_and_right(uniao_dac_comvest, correct_merge_list)

    uniao_dac_comvest = pd.merge(
        wrong_and_right[1],
        dados_comvest,
        how="left",
        on=["ano_ingresso_curso", "dta_nasc", "doc"],
        suffixes=("", "_comvest"),
    )
    wrong_and_right = get_wrong_and_right(uniao_dac_comvest, correct_merge_list)

    uniao_dac_comvest = pd.merge(
        wrong_and_right[1],
        dados_comvest,
        how="left",
        on=["nome", "ano_ingresso_curso", "doc"],
        suffixes=("", "_comvest"),
    )
    wrong_and_right = get_wrong_and_right(uniao_dac_comvest, correct_merge_list)

    wrong = deal_special_students(wrong_and_right[1], correct_merge_list)
    wrong = merge_by_doc_part(wrong, dados_comvest, correct_merge_list)
    get_closest_name(wrong, dados_comvest, correct_merge_list)

    concat = concat_dac_comvest(correct_merge_list, dados_comvest)
    final_df = padronize_colums(concat)
    write_result(final_df, RESULT_NAME)


def generate_planilha_paulo(merge_list):
    dac_df = pd.concat(merge_list[1:])
    df_paulo = dac_df.loc[
        :,
        [
            "identif",
            "insc_vest",
            "insc_vest_comvest",
            "ano_ingresso_curso",
            "nome",
            "nome_comvest",
            "dta_nasc",
            "dta_nasc_comvest",
            "curso",
            "curso_comvest",
            "doc",
            "doc_comvest",
            "tipo_ingresso",
            "tipo_ingresso_comvest",
        ],
    ]
    df_paulo["tipo_ingresso_comvest"] = df_paulo["tipo_ingresso_comvest"].map(
        {
            "1": "Vestibular Comum",
            "2": "Vestibular Indígena",
            "3": "Vagas Olímpicas",
            "4": "Enem-Unicamp",
        }
    )
    write_result(df_paulo, "planilha_paulo.csv")


def padronize_colums(df):
    df["cpf_dac"].fillna("-", inplace=True)
    df["cpf_comvest"].fillna("-", inplace=True)

    valida_cpf = np.vectorize(validar_CPF)
    df["cpf_dac"] = valida_cpf(df["cpf_dac"])
    df["cpf_comvest"] = valida_cpf(df["cpf_comvest"])
    select_cpf = np.vectorize(select_CPF)
    df["cpf"] = select_cpf(df["cpf_dac"], df["cpf_comvest"])
    # Coloca a coluna 'cpf' ao lado das outras 2 colunas de cpf
    cpf_column = df.pop("cpf")
    df.insert(1, "cpf", cpf_column)

    df["nome_dac"].fillna("-", inplace=True)
    df["nome_comvest"].fillna("-", inplace=True)
    select_name_v = np.vectorize(select_name)
    df["nome"] = select_name_v(df.nome_dac, df.nome_comvest)
    # Coloca a coluna 'nome' ao lado das outras 2 colunas de nome
    nome_column = df.pop("nome")
    df.insert(13, "nome", nome_column)

    df["doc_dac"].fillna("-", inplace=True)
    df["doc_comvest"].fillna("-", inplace=True)
    select_doc_v = np.vectorize(select_doc)
    df["doc"] = select_doc_v(df.doc_dac, df.doc_comvest)
    # Coloca a coluna 'doc' ao lado das outras 2 colunas de doc
    doc_column = df.pop("doc")
    df.insert(6, "doc", doc_column)

    df["dta_nasc_dac"].fillna("-", inplace=True)
    df["dta_nasc_comvest"].fillna("-", inplace=True)
    select_dta_v = np.vectorize(select_dta)
    df["dta_nasc"] = select_dta_v(df.dta_nasc_dac, df.dta_nasc_comvest)
    df.dta_nasc = df.dta_nasc.replace("00000nan", "-")
    # Coloca a coluna 'dta' ao lado das outras 2 colunas de dta
    dta_nasc_column = df.pop("dta_nasc")
    df.insert(9, "dta_nasc", dta_nasc_column)

    df.insc_vest_comvest = df.insc_vest_comvest.replace(r"", np.nan)
    select_insc_vest_v = np.vectorize(select_insc_vest)
    df["insc_vest"] = select_insc_vest_v(df.insc_vest_dac, df.insc_vest_comvest)

    origem_cpf = np.vectorize(set_origemCPF)
    df["origem_cpf"] = origem_cpf(df["cpf_dac"], df["cpf_comvest"])

    return df
