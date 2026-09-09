import pandas as pd
import re
import logging

from rais.utilities.read import read_dac_comvest_recovered
from rais.utilities.write import write_dac_comvest_ids
from rais.utilities.logging import log_create_index
from rais.id_generation.blake_id import (
    generate_blake_id_column,
    load_secret_key,
    SECRET_KEY_PATH,
)


def generate_index():
    log_create_index()

    df = read_dac_comvest_recovered()

    # Linhas que foram identificadas como tendo o CPF dos pais
    # e não tiveram o cpf recuperado recebem origem_cpf = 7
    df.loc[(df.invalid) & (df.cpf == "-"), "origem_cpf"] = 7

    # Remove o CPF dos casos em que foram encontrado homonimos na RAIS
    df.loc[df.origem_cpf == 4, "cpf"] = "-"

    df["doc"] = df["doc"].apply(clear_document)
    df_cpf_present = get_index_by_cpf(df)
    df_cpf_present.id = df_cpf_present.id + 1

    df_cpf_missing = get_index_missing_cpf(df)
    df_cpf_missing.id = df_cpf_missing.id + df_cpf_present["id"].max() + 1
    result = pd.concat([df_cpf_present, df_cpf_missing], sort=True)

    # Corrigindo os casos com pessoas diferentes com mesmo id dentro do mesmo ano
    # Para isso é mantido o id com menor origem_cpf e o outro é descartado

    aux = (
        result.groupby(by=["id", "ano_ingresso_curso"])
        .size()
        .reset_index(name="tam")
        .merge(
            result,
            how="inner",
            left_on=["id", "ano_ingresso_curso"],
            right_on=["id", "ano_ingresso_curso"],
        )
    )
    aux = aux[aux["tam"] > 1]

    aux2 = aux.merge(aux, how="inner", on=["id", "ano_ingresso_curso"])

    cols = [
        "id",
        "ano_ingresso_curso",
        "merge_id_x",
        "insc_vest_x",
        "nome_x",
        "cpf_x",
        "origem_cpf_x",
        "dta_nasc_x",
        "doc_x",
        "doc_y",
    ]

    problem_matches = (
        aux2[
            (aux2.origem_cpf_x != aux2.origem_cpf_y)
            & (
                ((aux2.origem_cpf_x == 5) | (aux2.origem_cpf_y == 5))
                | ((aux2.origem_cpf_x == 6) | (aux2.origem_cpf_y == 6))
            )
        ]
        .loc[:, cols]
        .drop_duplicates()
        .sort_values(by=["id", "origem_cpf_x"])
    )

    problem_matches.columns = problem_matches.columns.str.rstrip("_x")

    filter = ~problem_matches.duplicated(subset=["id"], keep="first")
    wrong_matches = problem_matches[~filter].copy()
    del wrong_matches["id"]

    wrong_matches["join"] = wrong_matches.apply(
        lambda x: str(x["doc"]) + str(x["dta_nasc"]), axis=1
    )
    wrong_matches = wrong_matches.sample(frac=1, random_state=1).reset_index(drop=True)
    codes, uniques = pd.factorize(wrong_matches["join"])
    wrong_matches.insert(0, "id", codes, True)
    wrong_matches.id = result["id"].max() + 1

    wrong_matches.loc[:, ["origem_cpf"]] = 0
    wrong_matches["wrong"] = True
    wrong_matches = wrong_matches.loc[:, ["id", "merge_id", "origem_cpf", "wrong"]]

    result = result.merge(
        wrong_matches, on=["merge_id"], how="left", suffixes=[None, "_y"]
    )
    result = result.fillna({"wrong": False})
    # O merge left (poucas linhas em wrong_matches contra ~2M em result)
    # introduz NaN na coluna "wrong", o que faz o dtype virar "object" em vez
    # de voltar a bool mesmo depois do fillna -- pandas novo (2.x) exige
    # dtype bool de verdade em .where(), senao ~result.wrong aplica o ~
    # bitwise do Python em int (bool eh subclasse de int: ~True == -2),
    # gerando int64 e quebrando a linha abaixo. Cast explicito corrige sem
    # mudar nenhum valor logico (True/False continuam os mesmos).
    result["wrong"] = result["wrong"].astype(bool)

    result.id = result.id.where(~result.wrong, result.id_y)
    result.id = result.id.astype("int64")

    result.origem_cpf = result.origem_cpf.where(~result.wrong, result.origem_cpf_y)
    result.origem_cpf = result.origem_cpf.astype("int64")

    del result["wrong"]
    del result["id_y"]
    del result["origem_cpf_y"]

    # ID estavel por CPF (BLAKE2s), coluna adicional ao lado do "id"
    # sequencial de sempre -- decisao deliberada do usuario (2026-09-08) de
    # manter os dois durante o periodo de migracao, nao substituir de uma
    # vez. Linhas sem CPF real ficam com id_blake2s vazio (ver
    # generate_blake_id_column) -- o "id" sequencial continua sendo a unica
    # cobertura pra esses casos, como sempre foi.
    blake_key = load_secret_key(str(SECRET_KEY_PATH))
    result["id_blake2s"] = generate_blake_id_column(result["cpf"], blake_key)

    result = result.loc[
        :,
        [
            "id",
            "id_blake2s",
            "ano_ingresso_curso",
            "insc_vest_dac",
            "insc_vest_comvest",
            "cpf",
            "nome",
            "doc",
            "dta_nasc",
            "identif",
            "origem_cpf",
        ],
    ]
    write_dac_comvest_ids(result)


# Gera id para linhas que não possuem CPF
def get_index_missing_cpf(df):
    df2 = df.copy()

    df_cpf_missing_not_null = df2.loc[
        (df["cpf"] == "-") & ~((df2.dta_nasc == "-") & (df2.doc == "000000000000000")),
        :,
    ]
    df_cpf_missing_not_null["join"] = df_cpf_missing_not_null.apply(
        lambda x: str(x["doc"]) + str(x["dta_nasc"]), axis=1
    )
    df_cpf_missing_not_null = df_cpf_missing_not_null.sample(
        frac=1, random_state=1
    ).reset_index(drop=True)
    codes, uniques = pd.factorize(df_cpf_missing_not_null["join"])
    df_cpf_missing_not_null.insert(0, "id", codes, True)

    # Gera id para linhas que não possuem nem dta_nasc nem doc
    df_cpf_missing_null = df2.loc[
        (df2["cpf"] == "-") & ((df2.dta_nasc == "-") & (df2.doc == "000000000000000")),
        :,
    ]
    codes, uniques = pd.factorize(df_cpf_missing_null["nome"])
    df_cpf_missing_null.insert(0, "id", codes, True)

    df_cpf_missing_null.id = df_cpf_missing_null.id + df_cpf_missing_not_null["id"].max() + 1

    df_cpf_missing = pd.concat(
        [df_cpf_missing_null, df_cpf_missing_not_null], sort=True
    )
    del df_cpf_missing["join"]
    return df_cpf_missing


def get_index_by_cpf(df):
    df_cpf_present = df[df["cpf"] != "-"]
    df_cpf_present = df_cpf_present.sample(frac=1, random_state=1).reset_index(
        drop=True
    )
    codes, uniques = pd.factorize(df_cpf_present["cpf"])
    df_cpf_present.insert(0, "id", codes, True)
    return df_cpf_present


def get_index_by_doc(df):
    df_cpf_missing = df[df["cpf"] == "-"]
    df_cpf_missing["join"] = df_cpf_missing.apply(
        lambda x: str(x["doc"]) + str(x["dta_nasc"]), axis=1
    )
    df_cpf_missing = df_cpf_missing.sample(frac=1, random_state=1).reset_index(
        drop=True
    )
    codes, uniques = pd.factorize(df_cpf_missing["join"])
    df_cpf_missing.insert(0, "id", codes, True)
    del df_cpf_missing["join"]
    return df_cpf_missing


def clear_document(value):
    if type(value) != str:
        return value
    new_string = re.sub(r"[x]", "X", value)
    new_string = re.sub(r"[^X0-9]", "", new_string)
    new_string = new_string.zfill(15)
    return new_string


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    generate_index()
