import pandas as pd
import glob
import yaml
from comvest.utilities.io import read_auxiliary, read_result, write_result
from comvest.utilities.dtypes import DTYPES_NOTAS


def get():
    stream = open("comvest/configuration.yaml")
    config = yaml.safe_load(stream)
    AUXILIARY_PATH = config["auxiliary"]

    files_path = glob.glob(AUXILIARY_PATH + r"*sitF*")
    files = [file.split("/")[-1] for file in files_path]

    f1 = []
    f2 = []

    for file in files:
        df_pres = read_auxiliary(file)

        if "F1" in file:
            df_pres.columns = ["insc_vest", "presente_f1"]
            df_pres.insert(0, column="ano_vest", value=int(file[:4]))
            df_pres["insc_vest"] = pd.to_numeric(df_pres["insc_vest"]).astype("Int64")
            df_pres["presente_f1"] = df_pres["presente_f1"].fillna("P")
            f1.append(df_pres)
        else:
            df_pres.rename(
                columns={
                    "INSC": "insc_vest",
                    "inscricao": "insc_vest",
                    "presen_port": "ppor",
                    "presen_bio": "pbio",
                    "presen_qui": "pqui",
                    "presen_hist": "phis",
                    "presen_his": "phis",
                    "presen_fis": "pfis",
                    "presen_geo": "pgeo",
                    "presen_mat": "pmat",
                    "presen_ing": "pest",
                    "presen_aptidao": "papt",
                    "presen_he": "papt",
                    "presen_cha": "pcha",
                    "presen_cn": "pcn",
                    "presen_inter": "pinter",
                },
                inplace=True,
            )
            df_pres.insert(0, column="ano_vest", value=int(file[:4]))
            df_pres["insc_vest"] = pd.to_numeric(df_pres["insc_vest"]).astype("Int64")
            df_pres = df_pres.reindex(
                columns=[
                    "ano_vest",
                    "insc_vest",
                    "ppor",
                    "pbio",
                    "pqui",
                    "phis",
                    "pfis",
                    "pgeo",
                    "pmat",
                    "pest",
                    "papt",
                    "pcha",
                    "pcn",
                    "pinter",
                ]
            )
            f2.append(df_pres)

    df_notas = read_result("notas_comvest.csv", DTYPES_NOTAS)

    vi_2019 = read_auxiliary("VI2019_DivulgaNotas.xlsx", dtype={"insc": "Int64"}).loc[
        :, ["insc", "sit"]
    ]
    vi_2019.insert(0, "ano_vest", 2019)

    vi_2020 = read_auxiliary("VI2020_DivulgaNotas.xlsx", dtype={"insc": "Int64"}).loc[
        :, ["insc", "sit"]
    ]
    vi_2020.insert(0, "ano_vest", 2020)

    vi_2021 = read_auxiliary("VI2021_DivulgaNotas.xlsx", dtype={"insc": "Int64"}).loc[
        :, ["insc", "sit"]
    ]
    vi_2021.insert(0, "ano_vest", 2021)

    vi_2022 = df_notas[df_notas["ano_vest"] == 2022].loc[
        :, ["ano_vest", "insc_vest", "presente_vi"]
    ]
    vi_2022.rename(columns={"presente_vi": "sit", "insc_vest": "insc"}, inplace=True)

    com_presenca_f1 = df_notas[
        ~df_notas["ano_vest"].isin([i for i in range(2005, 2011)])
    ].loc[:, ["ano_vest", "insc_vest", "presente_f1"]]
    f1.append(com_presenca_f1)

    com_presenca_f2 = df_notas[
        df_notas["ano_vest"].isin([i for i in range(1987, 2005)] + [2022])
    ].loc[
        :,
        [
            "ano_vest",
            "insc_vest",
            "ppor",
            "pbio",
            "pqui",
            "phis",
            "pfis",
            "pgeo",
            "pmat",
            "pest",
            "papt",
            "pcha",
            "pcn",
            "pinter",
        ],
    ]
    f2.append(com_presenca_f2)

    pres_f1 = pd.concat(f1)
    pres_f2 = pd.concat(f2)
    pres_vi = pd.concat([vi_2019, vi_2020, vi_2021, vi_2022])
    pres_vi.columns = ["ano_vest", "insc_vest", "presente_vi"]

    df_notas = df_notas.drop(columns="presente_f1").merge(
        pres_f1, how="left", on=["ano_vest", "insc_vest"]
    )
    df_notas = df_notas.drop(
        columns=[
            "ppor",
            "pbio",
            "pqui",
            "phis",
            "pfis",
            "pgeo",
            "pmat",
            "pest",
            "papt",
            "pcha",
            "pcn",
            "pinter",
        ]
    ).merge(pres_f2, how="left", on=["ano_vest", "insc_vest"])
    df_notas = df_notas.drop(columns="presente_vi").merge(
        pres_vi, how="left", on=["ano_vest", "insc_vest"]
    )

    FILE_NAME = "notas_comvest.csv"
    write_result(df_notas, FILE_NAME)
