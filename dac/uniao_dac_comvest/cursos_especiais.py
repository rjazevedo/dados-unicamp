import pandas as pd
from dac.utilities.io import write_result
from dac.uniao_dac_comvest.utilities import create_colums_for_concat
from dac.uniao_dac_comvest.utilities import setup_comvest
from dac.uniao_dac_comvest.utilities import setup_dac


def deal_special_students(df, correct_merge_list):
    correct_special_list = []

    unknow = tecnology_students(df, correct_special_list)
    pedagogy = pedagogy_students(unknow, correct_special_list)
    profis = profis_students(pedagogy, correct_special_list)
    rest = adm_students(profis, correct_special_list)

    correct_df = pd.concat(correct_special_list)
    correct_merge_list.append(correct_df)
    return rest


def tecnology_students(df, correct_special_list):
    pre_filt = df["origem"] == "pre"
    unknow_filt = df["curso"].isin(["36", "33", "32", "31"])
    year_filt = df["ano_ingresso_curso"] == "1987"
    course_filt = pre_filt & unknow_filt & year_filt

    unknow_students = df[course_filt]
    normal_students = df[~course_filt]
    unknow_students = create_colums_for_concat(unknow_students, False)
    correct_special_list.append(unknow_students)
    return normal_students


def pedagogy_students(df, correct_special_list):
    pos_filt = df["origem"] == "pos"
    pre_filt = df["origem"] == "pre"
    pedagogy_filt = df["curso"].isin(["35", "65", "59", "66", "67"])
    courses_filt = (pos_filt & pedagogy_filt) | (pre_filt & (df["curso"] == "35"))

    pedagogy_students = df[courses_filt]
    normal_students = df[~courses_filt]

    pedagogy_students = create_colums_for_concat(pedagogy_students, False)
    correct_special_list.append(pedagogy_students)
    return normal_students


def profis_students(df, correct_special_list):
    pos_filt = df["origem"] == "pos"
    ingresso_filt = df["tipo_ingresso"] == "INGRESSO POR CONCLUSAO NO PROFIS"
    profis_filt = df["curso"] == "200"
    courses_filt = pos_filt & (ingresso_filt | profis_filt)

    profis_students = df[courses_filt]
    normal_students = df[~courses_filt]

    # testar_profis(profis_students)
    profis_students = create_colums_for_concat(profis_students, False)
    correct_special_list.append(profis_students)
    return normal_students


def adm_students(df, correct_special_list):
    pos_filt = df["origem"] == "pos"
    adm_filt = df["curso"].isin(["109", "110"])
    ingresso_filt = adm_filt & pos_filt

    adm_students = df[ingresso_filt]
    normal_students = df[~ingresso_filt]

    adm_students = create_colums_for_concat(adm_students, False)
    correct_special_list.append(adm_students)

    # find_entry_109_110_students(df[ingresso_filt])
    return normal_students


def find_entry_109_110_students(df):
    dados_comvest = setup_comvest()
    dados_comvest = dados_comvest[
        (dados_comvest["curso"].isin(["103", "104", "105", "106"]))
    ]

    dados_dac = setup_dac()
    dados_dac = dados_dac[(dados_dac["curso"].isin(["103", "104", "105", "106"]))]

    merge = pd.merge(
        df, dados_comvest, how="left", on=["doc", "dta_nasc"], suffixes=("", "_comvest")
    )

    return

    df = merge.loc[
        :,
        [
            "identif",
            "nome",
            "dta_nasc",
            "curso_x",
            "insc_vest_y",
            "ano_ingresso_curso_y",
            "curso_y",
        ],
    ]
    df.columns = [
        "identif",
        "nome",
        "dta_nasc",
        "curso",
        "insc_vest",
        "ano_ingresso_curso_comvest",
        "curso_matric",
    ]
    df = df[(df["curso_matric"].isin(["103", "104", "105", "106"]))]

    dados_dac["insc_vest"] = dados_dac["insc_vest"].astype(str)
    df["insc_vest"] = df["insc_vest"].astype(str)
    merge = pd.merge(df, dados_dac, how="left", on=["insc_vest"])
    merge = merge[~(merge["nome_y"].isnull())]

    merge = merge.loc[
        :,
        [
            "identif_x",
            "nome_x",
            "dta_nasc_x",
            "curso_x",
            "ano_ingresso_curso",
            "insc_vest",
            "curso_matric",
            "ano_ingresso_curso_comvest",
        ],
    ]
    merge.columns = [
        "identif",
        "nome",
        "dta_nasc",
        "curso_dac",
        "ano_ingresso_dac",
        "insc_vest",
        "curso_comvest",
        "ano_ingresso_comvest",
    ]

    final_merge = pd.merge(wrong_pos, merge, how="left", on=["nome", "dta_nasc"])
    final_merge = final_merge.loc[
        :,
        [
            "identif_x",
            "nome",
            "cpf",
            "dta_nasc",
            "curso_dac",
            "ano_ingresso_curso",
            "insc_vest_y",
            "curso_comvest",
            "ano_ingresso_comvest",
        ],
    ]
    final_merge.columns = [
        "identif_dac",
        "nome",
        "cpf",
        "dta_nasc",
        "curso_dac",
        "ano_ingresso_dac",
        "insc_vest_comvest",
        "curso_comvest",
        "ano_ingresso_comvest",
    ]
    final_merge = final_merge[~(final_merge["curso_dac"].isnull())]

    write_result(final_merge, "cursos_109_e_110.csv")


def courses_that_are_different_in_both_bases(right_list):
    dfs = right_list.copy()
    dfs = pd.concat(right_list).loc[:, ["origem", "curso", "curso_matric"]]
    dfs = dfs[(dfs["origem"] == "pre")]
    dfs["key"] = dfs["curso"] + dfs["curso_matric"]
    dfs = dfs.drop_duplicates(subset=["curso", "curso_matric"])
    dfs = dfs[~(dfs["curso"] == dfs["curso_matric"])]
    dfs = dfs.loc[:, ["curso", "curso_matric"]]
    write_result(dfs, "cursos_que_diferem_nas_bases.csv")


def testar_profis(df):
    print("total:")
    print(df.shape)

    filt = df.duplicated(subset=["identif"], keep=False)
    profis_e_enem = df[filt]

    print("profis enem:")
    print(profis_e_enem.shape)
    write_result(profis_e_enem, "a_profis_enem.csv")

    profis_ou_enem = df[~filt]

    filt = profis_ou_enem["curso"] == "200"
    enem = profis_ou_enem[filt]
    print("enem:")
    print(enem.shape)

    profis = profis_ou_enem[~filt]
    print("profis:")
    print(profis.shape)

    write_result(enem, "a_enem.csv")
    write_result(profis, "a_profis.csv")
