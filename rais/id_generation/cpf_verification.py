import pandas as pd
import numpy as np
from difflib import SequenceMatcher
from unidecode import unidecode

from rais.utilities.read import read_dac_comvest
from rais.utilities.read import read_rais_identification
from rais.utilities.write import write_dac_comvest_valid
from rais.utilities.file import get_all_tmp_files

from rais.utilities.logging import log_remove_invalid_cpf


def remove_invalid_cpf():
    log_remove_invalid_cpf()
    df_dac_comvest = read_dac_comvest()
    df_dac_comvest = clean_names(df_dac_comvest)
    df_dac_comvest["merge_id"] = range(len(df_dac_comvest))
    df_dac_comvest.dta_nasc = df_dac_comvest.dta_nasc.replace("00000nan", "-")
    df_dac_comvest_merge = prepare_dac_comvest(df_dac_comvest)
    df_result = merge_by_cpf(df_dac_comvest_merge)
    df_result = get_invalid_cpf(df_result)
    df_result = change_invalid_cpf(df_dac_comvest, df_result)
    df_result = recover_cpf_inside_union(df_result)
    write_dac_comvest_valid(df_result)


def prepare_dac_comvest(df):
    df = df[df["cpf"] != "-"]
    df.drop_duplicates(subset=["cpf"], inplace=True)
    df.rename(columns={"cpf": "cpf_r"}, inplace=True)
    return df


def merge_by_cpf(df_dac_comvest):
    dfs = []
    for year in range(2002, 2019):
        print(f"Merging year {year}")
        df = merge_year(df_dac_comvest, year)
        dfs.append(df)
    df_result = pd.concat(dfs, sort=False)
    return df_result


# Merge rais from year with df_dac_comvest
def merge_year(df_dac_comvest, year):
    files = get_all_tmp_files(year, "identification_data", "pkl")
    dfs = []
    for file_rais in files:
        df_rais = read_rais_identification(file_rais)
        df = merge_dfs(df_rais, df_dac_comvest)
        dfs.append(df)

    df_result = pd.concat(dfs, sort=False)
    return df_result


# Merge rais df with dac/comvest df and remove invalid cpfs
def merge_dfs(df_rais, df_dac_comvest):
    result = df_rais.merge(df_dac_comvest)
    return result


def get_invalid_cpf(df):
    df["is_same_person"] = df.apply(
        lambda x: is_same_person(x["nome_r"], x["nome"]), axis=1
    )
    df_same_person = df[df["is_same_person"]]
    df_not_same_person = df[~df["is_same_person"]]
    df_total = pd.concat([df_same_person, df_not_same_person], sort=True)
    df_total.drop_duplicates(subset=["cpf_r"], keep="first", inplace=True)
    df_cpf_invalid = df_total[~df_total["is_same_person"]]
    vec = np.vectorize(get_similarity)
    df_cpf_invalid["similarity"] = vec(df_cpf_invalid.nome, df_cpf_invalid.nome_r)
    df_cpf_invalid = df_cpf_invalid[df_cpf_invalid.similarity < 0.9]
    df_cpf_invalid = df_cpf_invalid.loc[:, ["cpf_r"]]
    df_cpf_invalid.rename(columns={"cpf_r": "cpf"}, inplace=True)
    return df_cpf_invalid


def recover_cpf_inside_union(df):
    merge_list = []

    df_with_cpf = df.loc[
        df.cpf != "-",
        ["nome", "cpf", "dta_nasc", "doc", "merge_id"],
    ]
    df_without_cpf = df.loc[
        df.cpf == "-",
        ["nome", "dta_nasc", "doc", "merge_id"],
    ]

    merge_nome_dta = df_without_cpf.merge(
        df_with_cpf,
        how="left",
        on=["nome", "dta_nasc"],
        indicator=True,
        suffixes=["", "_y"],
    )
    success = merge_nome_dta.loc[merge_nome_dta._merge == "both", :]
    success = success.drop_duplicates(subset="merge_id")
    merge_list.append(success)
    fail = merge_nome_dta.loc[
        merge_nome_dta._merge == "left_only", df_without_cpf.columns
    ]

    merge_nome_doc = fail.merge(
        df_with_cpf, how="left", on=["nome", "doc"], indicator=True, suffixes=["", "_y"]
    )
    success = merge_nome_doc.loc[merge_nome_doc._merge == "both", :]
    success = success.drop_duplicates(subset="merge_id")
    merge_list.append(success)
    fail = merge_nome_doc.loc[
        merge_nome_doc._merge == "left_only", df_without_cpf.columns
    ]
    fail["first_name"] = fail.nome.apply(get_first)
    df_with_cpf["first_name"] = df_with_cpf.nome.apply(get_first)

    merge_first_name_dta = fail.merge(
        df_with_cpf,
        how="left",
        on=["first_name", "dta_nasc"],
        indicator=True,
        suffixes=["", "_y"],
    )

    match_first_name_and_dta = merge_first_name_dta.loc[
        merge_first_name_dta._merge == "both", :
    ]

    match_first_name_and_dta["sim_nome"] = match_first_name_and_dta.apply(
        get_sim_nome, axis=1
    )

    match_first_name_and_dta = match_first_name_and_dta.drop_duplicates(
        subset="merge_id"
    ).drop(columns="first_name")

    success = match_first_name_and_dta.loc[
        match_first_name_and_dta.sim_nome > 0.8, :
    ].query("doc == doc_y")

    success = success.drop(columns=["nome_y", "sim_nome"])
    merge_list.append(success)
    fail = match_first_name_and_dta.loc[
        match_first_name_and_dta.sim_nome > 0.8, :
    ].query("doc != doc_y")
    fail["sim_doc"] = fail.apply(get_sim_doc, axis=1)
    success = fail[fail.sim_doc > 0.8]
    success = success.drop(columns=["nome_y", "sim_nome"])
    merge_list.append(success)
    dfs = pd.concat(merge_list, sort=False).loc[:, ["cpf", "merge_id"]]
    dfs["origem_cpf"] = 8

    merge = df.merge(dfs, on="merge_id", how="left", suffixes=[None, "_y"])
    merge.loc[merge.origem_cpf_y == 8, "cpf"] = merge.loc[
        merge.origem_cpf_y == 8, "cpf_y"
    ]
    merge.loc[merge.origem_cpf_y == 8, "origem_cpf"] = merge.loc[
        merge.origem_cpf_y == 8, "origem_cpf_y"
    ]
    merge = merge.loc[:, df.columns]
    merge.origem_cpf = merge.origem_cpf.astype("int64")

    return merge


def get_similarity(name_a, name_b):
    similar_rate = SequenceMatcher(None, name_a, name_b).ratio()
    return similar_rate


def get_first(nome):
    return nome.split()[0]


def get_sim_nome(x):
    similar_rate = SequenceMatcher(None, x.nome, x.nome_y).ratio()
    return similar_rate


def get_sim_doc(row):
    doc = row.doc.lstrip("0")
    doc_y = row.doc_y.lstrip("0")
    similar_rate = SequenceMatcher(None, doc, doc_y).ratio()
    return similar_rate


# Says if person_a is person_b based on the probabilistic match between the two first names
def is_same_person(name_a, name_b):
    first_name_a = name_a.split()[0].split(".")[0].split("-")[0]
    first_name_b = name_b.split()[0].split(".")[0].split("-")[0]
    similar_rate = SequenceMatcher(None, first_name_a, first_name_b).ratio()
    return similar_rate > 0.7


def change_invalid_cpf(df_dac_comvest, df_cpf_invalid):
    # A coluna invalid vai ser usada para atribuir o origem_cpf para os cpf invalidos
    df_cpf_invalid["invalid"] = True
    result = df_dac_comvest.merge(df_cpf_invalid, how="left")
    result = result.fillna({"invalid": False})
    result["cpf"] = result.apply(lambda x: get_cpf(x["cpf"], x["invalid"]), axis=1)
    return result


def get_cpf(cpf, is_invalid):
    if is_invalid:
        return "-"
    return cpf


def clean_names(df):
    df.nome_dac = df.nome_dac.apply(clean_name)
    df.nome_comvest = df.nome_comvest.apply(clean_name)
    df.nome = df.nome.apply(clean_name)
    return df


def clean_name(name):
    if pd.isnull(name):
        return ""
    else:
        s = unidecode(name).upper().strip()
        return " ".join(s.split())
