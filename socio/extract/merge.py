import pandas as pd
import numpy as np
from socio.utilities.io import (
    get_all_files,
    list_dirs_socio_output_merges,
    write_socio_merges,
)

from socio.utilities.io import read_socio_clean
from socio.utilities.io import read_ids
from socio.utilities.io import write_socio_sample
from socio.utilities.io import (
    list_dirs_socio_output_tmp,
    create_folder_merges_date,
    create_folder_merges,
)

from socio.extract.standardization_functions import get_first_name
from socio.extract.standardization_functions import get_reduced_cpf
from socio.extract.standardization_functions import get_similarity

from socio.utilities.logging import (
    log_concatenating_ids,
    log_extracting_ids,
    log_reading_file_extraction,
    log_reading_file,
)


def merge_socio_dac_comvest(tipo_extracao):

    log_extracting_ids()
    df_dac_comvest = read_ids()
    df_dac_comvest = prepare_dac_comvest(df_dac_comvest)

    create_folder_merges()
    merge_socio_individual_files(df_dac_comvest)

    log_concatenating_ids()
    merged_files = []
    socio_folders = list_dirs_socio_output_merges()
    for folder in socio_folders:
        files = get_all_files(folder)
        for file in files:
            log_reading_file(file)
            df = read_socio_clean(file)
            merged_files.append(df)

    sample = pd.concat(merged_files)
    sample = sample.drop(
        columns=[
            "codigo_tipo_socio",
            "tipo_socio",
            "identificador_de_socio",
        ]
    )
    sample = (
        sample.sort_values(by=["data_coleta"], ascending=False)
        # Mantém apenas a linha com a coleta mais recente
        .drop_duplicates(subset=[x for x in list(sample.columns) if x != "data_coleta"])
        # Coloca linhas com mesmo id em ordem para facilitar analise visual
        .sort_values(
            by=[
                "id",
                "data_coleta",
                "cnpj",
            ],
            ascending=False,
        ).drop(columns="origem_socios")
        # Muda a ordem das colunas para facilitar analise visual
        .loc[
            :,
            [
                "id",
                "origem_cpf",
                "cnpj",
                "cnpj_raiz",
                "data_coleta",
                "data_entrada_sociedade",
                "razao_social",
                "qualificacao_socio",
                "codigo_qualificacao_socio",
                "faixa_etaria",
                "pais",
            ],
        ]
    )
    sample["ano_entrada_sociedade"] = sample.data_entrada_sociedade.astype("str").str[0:4]

    if tipo_extracao == "limitada":
        sample.loc[:, ["id", "origem_cpf", "ano_entrada_sociedade", "data_coleta"]]
    elif tipo_extracao == "completa":
        sample.loc[
            :,
            [
                "id",
                "origem_cpf",
                "cnpj",
                "cnpj_raiz",
                "data_coleta",
                "data_entrada_sociedade",
                "razao_social",
                "qualificacao_socio",
                "codigo_qualificacao_socio",
                "faixa_etaria",
                "pais",
            ],
        ]

    write_socio_sample(sample)


def merge_socio_individual_files(df_dac_comvest):
    socio_folders = sorted(list_dirs_socio_output_tmp())

    for folder in socio_folders:
        date = folder.split("/")[-1]
        year = int(date[0:4])
        create_folder_merges_date(date)
        files = get_all_files(folder)
        for file in files:
            filename = file.split("/")[-1]
            log_reading_file_extraction(file)
            df = read_socio_clean(file)
            df = prepare_socio(df, year)
            df = merge(df, df_dac_comvest)
            write_socio_merges(df, filename, date)


def prepare_socio(df, year):
    df = df.drop_duplicates()
    df["nome_socio"] = df["nome_socio"].replace("", np.nan)
    df = df.dropna(subset=["nome_socio"])
    df["primeiro_nome"] = df["nome_socio"].map(get_first_name)
    if year > 2020:
        df.cnpj = df.cnpj.str[0:8]
        df = df.rename(columns={"cnpj": "cnpj_raiz"})
    return df


def prepare_dac_comvest(df):
    df = df.loc[:, ["cpf", "nome", "id", "origem_cpf"]].drop_duplicates()
    df["cnpj_cpf_do_socio"] = df["cpf"].map(get_reduced_cpf)
    df["primeiro_nome"] = df["nome"].map(get_first_name)
    df = df.drop(columns="cpf")

    # Modifica o origem_cpf para que o sort funcione corretamente
    # Isto é, para que o menor valor de origem_cpf seja sempre o mais desejável
    df.origem_cpf = df.origem_cpf.replace(0, 11)
    df = df.sort_values(
        by=["cnpj_cpf_do_socio", "nome", "id", "origem_cpf"]
    ).drop_duplicates(subset=["cnpj_cpf_do_socio", "nome", "id"], keep="first")

    return df


def merge(df, df_dac_comvest):
    # Vai ser utilizado para identificar qual o método usado no merge
    df["origem_socios"] = 0

    merges = []
    socios_cols = list(df.columns)
    merge_cols = list(df.columns) + ["id", "origem_cpf"]

    merged = df.merge(
        df_dac_comvest,
        how="left",
        left_on=["cnpj_cpf_do_socio", "nome_socio"],
        right_on=["cnpj_cpf_do_socio", "nome"],
        indicator=True,
        suffixes=(None, "_y"),
    )

    # Valor 1 indica que foi encontrada usando match-exato e nao possuía homonimos.
    # Atribui inicialmente o valor 1 para todos os matches e em seguida corrige atribuindo 2
    # para os casos com homonimos.
    merged.loc[merged._merge == "both", "origem_socios"] = 1

    # Modificando o origem_capes dos casos com homonino para 2,
    # ao final do merge esses casos serão dropados.
    merged.loc[
        (merged._merge == "both")
        & (merged[merged._merge == "both"].duplicated(subset=socios_cols, keep=False)),
        ["origem_socios"],
    ] = 2
    merges.append(merged.loc[merged.origem_socios == 1, merge_cols].copy())

    df_fail_exact_match = merged.loc[merged._merge == "left_only", list(socios_cols)]

    merged_approx = df_fail_exact_match.merge(
        df_dac_comvest,
        how="left",
        on=["cnpj_cpf_do_socio", "primeiro_nome"],
        indicator=True,
    )

    merged_approx = merged_approx.loc[
        merged_approx._merge == "both", merge_cols + ["nome"]
    ]
    merged_approx["passou"] = False

    if merged_approx.empty:
        return concat_merges(merges)

    merged_approx["similaridade"] = merged_approx.apply(
        lambda x: get_similarity(x["nome_socio"], x["nome"]), axis=1
    )

    merged_approx.loc[merged_approx["similaridade"] >= 0.50, "passou"] = True
    merged_approx_matches = merged_approx[merged_approx.passou].sort_values(
        by=["similaridade", "origem_cpf"], ascending=[False, True]
    )

    # O valor origem_capes 3 é utilizado para os casos em que
    # apenas 1 match aproximado teve similaridade acima do cutoff
    merged_approx_matches.loc[
        ~merged_approx_matches.duplicated(subset=socios_cols, keep=False),
        ["origem_socios"],
    ] = 3

    # O valor origem_capes 4 é utilizado para os casos em que
    # 1 linha da CAPES teve mais de 1 match com similaridade acima do cutoff.
    #  Nesse caso foi mantido o match com a similaridade mais alta.
    merged_approx_matches.loc[
        (~merged_approx_matches.duplicated(subset=socios_cols, keep="first"))
        & (merged_approx_matches.origem_socios == 0),
        ["origem_socios"],
    ] = 4

    merges.append(
        merged_approx_matches.loc[
            merged_approx_matches.origem_socios != 0, merge_cols
        ].copy()
    )

    return concat_merges(merges)


def concat_merges(merges):
    final_merge = pd.concat(merges)
    final_merge.origem_cpf = final_merge.origem_cpf.replace(11, 0)
    final_merge.origem_cpf = final_merge.origem_cpf.astype("int64")
    final_merge.id = final_merge.id.astype("int64")
    final_merge = final_merge.drop(
        columns=[
            "nome_socio",
            "primeiro_nome",
            "cnpj_cpf_do_socio",
        ]
    )
    return final_merge
