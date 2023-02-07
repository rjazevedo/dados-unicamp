import pandas as pd
from unidecode import unidecode
from difflib import SequenceMatcher

from capes.utilities.io import (
    list_dirs_capes_tmp,
    read_capes_clean,
    read_ids,
    write_sample,
)
from capes.utilities.io import get_all_files
from capes.cleaning.clean import clean_columns

from capes.utilities.logging import log_extracting_ids, log_reading_file_extraction


def extract_ids():
    log_extracting_ids()
    capes_folders = sorted(list_dirs_capes_tmp())

    dac_comvest_ids = read_ids()
    dac_comvest_ids = prepare_dac_comvest_ids(dac_comvest_ids)

    # Este drop_duplicates é feito para que o merge abaixo
    # não crie match duplicados entre 1 pessoa da capes e
    # varias linhas no dac_comvest_ids todas com o mesmo id.
    # Dessa forma, após este drop_duplicates, se ocorrer
    # algum caso de 1 pessoa da capes der match em mais de 1
    # linha do dac_comvest_ids, entao podemos identificar
    # esse caso corretamente como homonimos, ou seja,
    # 1 mesma pessoa da CAPES dando match com 2 ids distindos.
    dac_comvest_ids = dac_comvest_ids.drop_duplicates(
        subset=["nome", "ano_nasc_dac", "id"]
    )

    merge_year_list = []

    for folder in capes_folders:
        extract_date_capes(folder, dac_comvest_ids, merge_year_list)

    result = pd.concat(merge_year_list)

    string_cols = [
        "nm_grande_area",
        "nm_entidade_ensino",
        "cs_status_juridico",
        "nm_regiao",
        "nm_programa_ies",
        "nm_modalidade_programa",
        "nm_nivel_programa",
        "nm_area_avaliacao",
        "pais_nac_a",
        "nm_situacao_discente",
        "nm_nivel_titulacao_discente",
        "nm_nivel_conclusao_discente",
        "nm_grande_area",
        "ds_depend_adm",
        "nm_municipio_programa_ies",
        "ds_grau_acad_discente",
        "st_ingressante",
        "nm_grau_programa",
    ]

    result = clean_columns(result, string_cols)
    result = remove_columns(result)
    write_sample(result)


# Clean capes files from a given year
def extract_date_capes(path_folder, dac_comvest_ids, merge_year_list):
    date = path_folder.split("/")[-1]
    print(f"Extraindo ano {date}")
    log_reading_file_extraction()
    if int(date) <= 2012:
        result = extract_date_capes_pre2013(path_folder, dac_comvest_ids)
    else:
        result = extract_date_capes_post2013(path_folder, dac_comvest_ids)

    merge_year_list.append(result)


def extract_date_capes_pre2013(path_folder, dac_comvest_ids):
    merges = []
    files = get_all_files(path_folder)

    for file in files:
        df_clean = read_capes_clean(file)
        df_clean["ano_nasc_a"] = df_clean.ano_nasc_a.astype(str)
        df_clean["primeiro_nome_capes"] = df_clean.nm_discente.apply(
            lambda x: x.split()[0]
        )
        df_clean[
            "origem_capes"
        ] = 0  # Vai ser utilizado para identificar qual o método usado no merge

        merge_cols = list(df_clean.columns) + ["id", "origem_cpf"]

        merged = df_clean.merge(
            dac_comvest_ids,
            how="left",
            left_on=["ano_nasc_a", "nm_discente"],
            right_on=["ano_nasc_dac", "nome"],
            indicator=True,
        )

        # Valor 1 indica que foi encontrada usando match-exato, pre2013, e nao possuía homonimos.
        # Atribui inicialmente o valor 1 para todos os matches e em seguida corrige atribuindo 2
        # para os casos com homonimos.
        merged.loc[merged._merge == "both", "origem_capes"] = 1

        # Modificando o origem_capes dos casos com homonino para 2,
        # ao final do merge esses casos serão dropados.
        merged.loc[
            (merged._merge == "both")
            & (
                merged[merged._merge == "both"].duplicated(
                    subset=df_clean.columns, keep=False
                )
            ),
            ["origem_capes"],
        ] = 2
        merges.append(merged.loc[merged.origem_capes == 1, merge_cols].copy())

        df_clean_fail_exact_match = merged.loc[
            merged._merge == "left_only", list(df_clean.columns)
        ]

        merged_approx = df_clean_fail_exact_match.merge(
            dac_comvest_ids,
            how="left",
            left_on=["primeiro_nome_capes", "ano_nasc_a"],
            right_on=["primeiro_nome_dac", "ano_nasc_dac"],
            indicator=True,
        )
        merged_approx = merged_approx.loc[
            merged_approx._merge == "both", merge_cols + ["nome"]
        ]
        merged_approx["passou"] = False

        merged_approx["similaridade"] = merged_approx.apply(
            lambda x: get_similarity(x["nm_discente"], x["nome"]), axis=1
        )
        merged_approx.loc[merged_approx["similaridade"] >= 0.85, "passou"] = True
        merged_approx_matches = merged_approx[merged_approx.passou].sort_values(
            by="similaridade", ascending=False
        )

        # O valor origem_capes 3 é utilizado para os casos em que
        # apenas 1 match aproximado teve similaridade acima do cutoff
        merged_approx_matches.loc[
            ~merged_approx_matches.duplicated(subset=df_clean.columns, keep=False),
            ["origem_capes"],
        ] = 3

        # O valor origem_capes 4 é utilizado para os casos em que
        # 1 linha da CAPES teve mais de 1 match com similaridade acima do cutoff.
        #  Nesse caso foi mantido o match com a similaridade mais alta.
        merged_approx_matches.loc[
            (~merged_approx_matches.duplicated(subset=df_clean.columns, keep="first"))
            & (merged_approx_matches.origem_capes == 0),
            ["origem_capes"],
        ] = 4

        merges.append(
            merged_approx_matches.loc[
                merged_approx_matches.origem_capes != 0, merge_cols
            ].copy()
        )

        return pd.concat(merges)


def extract_date_capes_post2013(path_folder, dac_comvest_ids):
    merges = []
    files = get_all_files(path_folder)

    for file in files:
        df_clean = read_capes_clean(file)
        df_clean["ano_nasc_a"] = df_clean.ano_nasc_a.astype(str)
        df_clean.loc[df_clean.tp_documento_discente == "CPF", "cpf_reduzido_capes"] = (
            df_clean.nr_documento_discente.str[4:7]
            + df_clean.nr_documento_discente.str[8:11]
        )
        df_clean.loc[
            df_clean.tp_documento_discente != "CPF", "cpf_reduzido_capes"
        ] = "-"
        df_clean["primeiro_nome_capes"] = df_clean.nm_discente.apply(
            lambda x: x.split()[0]
        )
        df_clean[
            "origem_capes"
        ] = 0  # Vai ser utilizado para identificar qual o método usado no merge

        merge_cols = list(df_clean.columns) + ["id", "origem_cpf"]

        merged = df_clean.merge(
            dac_comvest_ids,
            how="left",
            left_on=["cpf_reduzido_capes", "nm_discente", "ano_nasc_a"],
            right_on=["cpf_reduzido_dac", "nome", "ano_nasc_dac"],
            indicator=True,
        )

        # Valor 5 indica que foi encontrada usando
        # match-exato de (nome, ano_nasc, cpf_reduzido).
        merged.loc[merged._merge == "both", "origem_capes"] = 5

        merges.append(merged.loc[merged.origem_capes == 5, merge_cols].copy())

        df_clean_fail_exact_match = merged.loc[
            merged._merge == "left_only", list(df_clean.columns)
        ]
        ids_no_cpf = dac_comvest_ids.loc[dac_comvest_ids.cpf_reduzido_dac == "", :]
        df_match_name_year = df_clean_fail_exact_match.merge(
            ids_no_cpf,
            how="left",
            left_on=["nm_discente", "ano_nasc_a"],
            right_on=["nome", "ano_nasc_dac"],
            indicator=True,
        )
        merged = df_match_name_year.query('_merge == "both"')

        # Valor 6 indica que foi encontrada usando match-exato de (nome, ano_nasc) pos2013,
        # e nao possuía homonimos. Só foi feito esse segundo match em pessoas
        # da dac_comvest_id que nao tinham cpf.
        merged.loc[
            ~merged.duplicated(subset=df_clean.columns, keep=False), ["origem_capes"]
        ] = 6

        # Modificando o origem_capes dos casos com homonino para 7,
        # ao final do merge esses casos serão dropados.
        merged.loc[
            merged.duplicated(subset=df_clean.columns, keep=False), ["origem_capes"]
        ] = 7
        merges.append(merged.loc[merged.origem_capes == 6, merge_cols].copy())

        df_clean_fail_match_name_year = df_match_name_year.loc[
            df_match_name_year._merge == "left_only", list(df_clean.columns)
        ]
        merged_approx = df_clean_fail_match_name_year.merge(
            dac_comvest_ids,
            how="left",
            left_on=["primeiro_nome_capes", "ano_nasc_a", "cpf_reduzido_capes"],
            right_on=["primeiro_nome_dac", "ano_nasc_dac", "cpf_reduzido_dac"],
            indicator=True,
        )
        merged_approx = merged_approx.loc[
            merged_approx._merge == "both", merge_cols + ["nome"]
        ]
        merged_approx["passou"] = False

        merged_approx["similaridade"] = merged_approx.apply(
            lambda x: get_similarity(x["nm_discente"], x["nome"]), axis=1
        )
        merged_approx.loc[merged_approx["similaridade"] >= 0.80, "passou"] = True
        merged_approx_matches = merged_approx[merged_approx.passou].sort_values(
            by="similaridade", ascending=False
        )

        # O valor origem_capes 8 é utilizado para os casos em que apenas
        # 1 match aproximado teve similiradidade acima do cutoff
        merged_approx_matches.loc[
            ~merged_approx_matches.duplicated(subset=df_clean.columns, keep=False),
            ["origem_capes"],
        ] = 8

        # O valor origem_capes 9 é utilizado para os casos em que
        # 1 linha da CAPES teve mais de 1 match com similaridade acima
        # do cutoff. Nesse caso foi mantido o match com a similaridade mais alta.
        merged_approx_matches.loc[
            (~merged_approx_matches.duplicated(subset=df_clean.columns, keep="first"))
            & (merged_approx_matches.origem_capes == 0),
            ["origem_capes"],
        ] = 9

        merges.append(
            merged_approx_matches.loc[
                merged_approx_matches.origem_capes != 0, merge_cols
            ].copy()
        )

        return pd.concat(merges)


def get_similarity(name_a, name_b):
    last_name_a = name_a.split()[1:]
    last_name_b = name_b.split()[1:]
    similar_rate = SequenceMatcher(None, last_name_a, last_name_b).ratio()
    return similar_rate


def prepare_dac_comvest_ids(df):
    df["cpf_reduzido_dac"] = df.cpf.str[3:9]
    df["nome"] = df.nome.apply(unidecode).str.upper().str.strip()
    df["primeiro_nome_dac"] = df.nome.apply(lambda x: x.split()[0])
    df["ano_nasc_dac"] = df.dta_nasc.str[-4:]

    return df.drop_duplicates()


def remove_columns(df):
    return df.drop(
        [
            "id_add_foto_programa",
            "id_add_foto_programa_ies",
            "id_pessoa",
            "nm_discente",
            "nm_orientador",
            "nm_tese_dissertacao",
            "nm_tipo_orientador",
            "nr_documento_discente",
            "nr_seq_orientador",
            "nr_seq_discente",
            "nr_seq_tese",
            "tp_documento_discente",
            "primeiro_nome_capes",
            "origem_capes",
            "cpf_reduzido_capes",
        ],
        axis=1,
        errors="ignore",
    )
