import pandas as pd
import logging
from comvest.utilities.io import files, read_from_db, write_result
from comvest.utilities.logging import progresslog, resultlog


def leitura_notas(path, date):
    notas_f1 = read_from_db(path, sheet_name="notasf1")

    try:
        notas_f2 = read_from_db(path, sheet_name="notasfin")
    except:
        try:
            notas_f2 = read_from_db(path, sheet_name="notasfinal")
        except:
            notas_f2 = read_from_db(path, sheet_name="notasf2")

    # 2010 e 2011 nao tem dados sobre o ENEM
    # ENEM passa a ser usado como complemento no vestibular Comvest a partir de 2000
    try:
        notas_enem = read_from_db(path, sheet_name="enem{}".format(date))
        notas_enem.columns = ["insc", "nota_enem"]
        if date in {2010, 2011}:
            notas_enem = pd.DataFrame(columns=["insc", "nota_enem"])
    except:
        try:
            notas_enem = read_from_db(path, sheet_name="ve_notas")
        except:
            notas_enem = pd.DataFrame(columns=["insc", "nota_enem"])

    try:
        notas_vi = read_from_db(path, sheet_name="vi_notas")
    except:
        notas_vi = None

    try:
        notas_vo = read_from_db(path, sheet_name="vo_notas")
    except:
        try:
            notas_vo = read_from_db(path, sheet_name="vo_class")
        except:
            notas_vo = None

    try:
        notas_profis = read_from_db(path, sheet_name="profis_class")
    except:
        notas_profis = None

    try:
        notas_he = read_from_db(path, sheet_name="notashe")
    except:
        notas_he = None

    notas_f1.columns = notas_f1.columns.str.lower()
    notas_f2.columns = notas_f2.columns.str.lower()
    notas_enem.columns = notas_enem.columns.str.lower()

    return (notas_f1, notas_f2, notas_enem, notas_vi, notas_vo, notas_profis, notas_he)


def tratar_notas_f1(notas_f1, date):
    for col in notas_f1.columns:
        if col in {"red", "red0c0o"}:
            notas_f1["redacao"] = notas_f1[col]
        elif col in {"nf", "nf1", "fase1", "f0se1"}:
            notas_f1.rename({col: "nf_f1"}, axis=1, inplace=True)
        elif col in {"npf1", "notpadf1"}:
            notas_f1.rename({col: "notpad_f1"}, axis=1, inplace=True)
        elif col in {"sit", "presf1", "1resf1"}:
            notas_f1.rename({col: "presente_f1"}, axis=1, inplace=True)
            # 0 = Ausente; 1 = Presente
            notas_f1["presente_f1"] = notas_f1["presente_f1"].map(
                {0: "A", 1: "P", "P": "P", "A": "A"}
            )

    if all(questao not in notas_f1.columns for questao in {"questoes", "qustoes"}):
        notas_f1["questoes"] = (
            notas_f1[["qui", "geo", "fis", "bio", "mat", "his"]].sum(axis=1).round(2)
        )

        # 2014 e 2013 possuem 'texto1' e 'texto2' compondo a 'redacao' da 1a fase
    if "redacao" not in notas_f1.columns and (date == 2014 or date == 2013):
        redacao = notas_f1["texto1"] + notas_f1["texto2"]
        notas_f1["redacao"] = redacao.round(2)

    notas_f1.rename(
        {
            "qustoes": "questoes",
            "his": "not_his",
            "fis": "not_fis",
            "qui": "not_qui",
            "bio": "not_bio",
            "mat": "not_mat",
            "geo": "not_geo",
            "redacao": "not_red",
            "apt_musica": "not_apt_mus",
            "npm": "notpad_apt_mus",
        },
        axis=1,
        inplace=True,
    )
    notas_f1 = notas_f1.reindex(
        columns=[
            "insc",
            "questoes",
            "not_qui",
            "not_geo",
            "not_fis",
            "not_bio",
            "not_mat",
            "not_his",
            "not_red",
            "not_apt_mus",
            "notpad_apt_mus",
            "nf_f1",
            "notpad_f1",
            "presente_f1",
        ]
    )
    return notas_f1


def tratar_notas_f2(notas_f2, date):
    notas_f2.rename(
        {
            "presen_he": "papt",
            "notpad_he": "notpad_aptidao",
            "napt": "not_apt",
            "apaptidao": "aprov_apt",
            "aptidao": "not_apt",
            "fase1": "nf_f1",
            "nfase1": "nf_f1",
            "notpadf1": "notpad_f1",
            "fase1op2": "not_f1_opc2",
            "notpadf1op2": "notpad_f1_opc2",
            "red": "not_red",
            "notpadred": "notpad_red",
            "presen_inter": "pinter",
            "inter": "not_inter",
            "notpad8": "notpad_inter",
            "sit": "pres_f2_d4",
            "ing": "not_est",
            "est": "not_est",
            "notpad_ing": "notpad_est",
            "presen_por": "ppor",
            "presen_port": "ppor",
            "notpad1": "notpad_por",
            "por": "not_por_f2",
            "npor": "not_por_f2",
            "notpad6": "notpad_bio",
            "presen_bio": "pbio",
            "bio": "not_bio",
            "nbio": "not_bio",
            "notpad7": "notpad_qui",
            "presen_qui": "pqui",
            "qui": "not_qui",
            "nqui": "not_qui",
            "notpad4": "notpad_his",
            "presen_his": "phis",
            "his": "not_his",
            "nhis": "not_his",
            "notpad5": "notpad_fis",
            "presen_fis": "pfis",
            "fis": "not_fis",
            "nfis": "not_fis",
            "notpad3": "notpad_geo",
            "presen_geo": "pgeo",
            "geo": "not_geo",
            "ngeo": "not_geo",
            "notpad2": "notpad_mat",
            "presen_math": "pmath",
            "math": "not_math",
            "presen_mat": "pmat",
            "mat": "not_mat",
            "nmat": "not_mat",
            "cha": "not_cha",
            "cn": "not_cn",
            "plin": "pest",
            "nlin": "not_est",
            "clas1": "clas_opc1",
            "clas2": "clas_opc2",
            "clas3": "clas_opc3",
            "clacur1": "clas_opc1",
            "clacur2": "clas_opc2",
            "clacur3": "clas_opc3",
            "nf2_opcao1": "nf_f2_opc1",
            "nf2_opcao2": "nf_f2_opc2",
            "npfinal1": "npo1",
            "npfinal2": "npo2",
            "npfinal3": "npo3",
            "npfinal": "np_unica",
        },
        axis=1,
        inplace=True,
    )

    try:
        notas_f2["pres_f2_d4"] = notas_f2["pres_f2_d4"].map(
            {"A": "A", "P": "P", "E": ""}
        )
    except:
        logging.debug("Comvest {} file doesn't have a 'pres_f2_d4' column".format(date))

    try:
        notas_f2["papt"] = notas_f2["papt"].map({"A": "A", "P": "P", "N": "A"})
    except:
        logging.debug("Comvest {} file doesn't have a 'papt' column".format(date))

    try:
        notas_f2["clas_opc1"] = notas_f2["clas_opc1"].replace(0, pd.NA).astype("Int64")
    except:
        logging.debug("Comvest {} file doesn't have a 'clas_opc1' column".format(date))

    try:
        notas_f2["clas_opc2"] = notas_f2["clas_opc2"].replace(0, pd.NA).astype("Int64")
    except:
        logging.debug("Comvest {} file doesn't have a 'clas_opc2' column".format(date))

    try:
        notas_f2["clas_opc3"] = notas_f2["clas_opc3"].replace(0, pd.NA).astype("Int64")
    except:
        logging.debug("Comvest {} file doesn't have a 'clas_opc3' column".format(date))

    if "np_unica" in notas_f2.columns:
        if 1000 < notas_f2["np_unica"].max() <= 10000:
            notas_f2["np_unica"] = notas_f2["np_unica"].div(10)
        elif 10000 < notas_f2["np_unica"].max() <= 100000:
            notas_f2["np_unica"] = notas_f2["np_unica"].div(100)

    if date == 1987:
        notas_f2["pbio"] = notas_f2["pbio"].map({"A": "A", "S": "P"})

    # No caso em que a pagina de notas final (notas da fase 2) tem o número de inscrição dada por uma string
    # sem a possibilidade de ser convertida para número pelo próprio método read_excel, deve-se fazer a conversão
    if notas_f2["insc"].dtype == object:
        notas_f2["insc"] = (
            notas_f2["insc"].str.replace(r"\D", "", regex=True).astype(int)
        )

    notas_f2 = notas_f2.reindex(
        columns=[
            "insc",
            "nf_f1",
            "notpad_f1",
            "not_f1_opc2",
            "notpad_f1_opc2",
            "aprov_apt",
            "papt",
            "not_apt",
            "notpad_aptidao",
            "pqui",
            "not_qui",
            "notpad_qui",
            "pgeo",
            "not_geo",
            "notpad_geo",
            "pfis",
            "not_fis",
            "notpad_fis",
            "pbio",
            "not_bio",
            "notpad_bio",
            "pmath",
            "not_math",
            "notpad_math",
            "pmat",
            "not_mat",
            "notpad_mat",
            "phis",
            "not_his",
            "notpad_his",
            "ppor",
            "not_por_f2",
            "notpad_por",
            "pest",
            "not_est",
            "notpad_est",
            "pcha",
            "not_cha",
            "notpad_cha",
            "pcn",
            "not_cn",
            "notpad_cn",
            "pinter",
            "not_inter",
            "notpad_inter",
            "not_red",
            "notpad_red",
            "npo1",
            "npo2",
            "npo3",
            "np_unica",
            "area",
            "grupo1",
            "grupo2",
            "grupo3",
            "clas_opc1",
            "clas_opc2",
            "clas_opc3",
            "clacar",
            "nf_f2_opc1",
            "nf_f2_opc2",
            "pres_f2_d4",
        ]
    )
    return notas_f2


def tratar_notas_enem(notas_enem, inscritos, date):
    column_names = [
        "insc",
        "nota_enem",
        "notpad_lc_ve",
        "notpad_mat_ve",
        "notpad_cn_ve",
        "notpad_ch_ve",
        "notpad_red_ve",
        "not_red_ve",
        "notpad_he_ve",
        "not_he_ve",
        "npo1_ve",
        "npo2_ve",
        "grupo1_ve",
        "grupo2_ve",
        "clas_opc1_ve",
        "clas_opc2_ve",
        "ano_enem",
    ]

    if notas_enem.empty:
        notas_enem["insc"] = inscritos

    notas_enem.rename(
        {
            "lc": "notpad_lc_ve",
            "mt": "notpad_mat_ve",
            "cn": "notpad_cn_ve",
            "ch": "notpad_ch_ve",
            "red": "notpad_red_ve",
            "redb": "not_red_ve",
            "he": "notpad_he_ve",
            "heb": "not_he_ve",
            "npo1": "npo1_ve",
            "npo2": "npo2_ve",
            "grupo1": "grupo1_ve",
            "grupo2": "grupo2_ve",
            "clas1": "clas_opc1_ve",
            "clas2": "clas_opc2_ve",
            "anousado": "ano_enem",
        },
        axis=1,
        inplace=True,
        errors="ignore",
    )
    notas_enem = notas_enem.reindex(columns=column_names)

    return notas_enem


def tratar_notas_vi(notas_vi, date):
    column_names = [
        "insc",
        "questoes_vi",
        "pontuacao_vi",
        "not_red_vi",
        "not_musica_vi",
        "nf_opc1_vi",
        "nf_opc2_vi",
        "grupo1_vi",
        "grupo2_vi",
        "clas_opc1_vi",
        "clas_opc2_vi",
        "presente_vi",
    ]

    if notas_vi is None:
        return pd.DataFrame(columns=column_names)

    # Vestibular Indigena em 2019 nao tem registro de presença
    try:
        notas_vi["sit"] = notas_vi["sit"].map(lambda pres: pres if pres == "A" else "P")
    except:
        logging.debug(
            "Comvest {} file doesn't have a 'cid_inscricao' column".format(date)
        )

    notas_vi.rename(
        {
            "questoes": "questoes_vi",
            "questoespontos": "pontuacao_vi",
            "redacao": "not_red_vi",
            "musica": "not_musica_vi",
            "nf1": "nf_opc1_vi",
            "nf2": "nf_opc2_vi",
            "grupo1": "grupo1_vi",
            "grupo2": "grupo2_vi",
            "clas1": "clas_opc1_vi",
            "clas2": "clas_opc2_vi",
            "sit": "presente_vi",
        },
        axis=1,
        inplace=True,
        errors="ignore",
    )
    notas_vi = notas_vi.reindex(columns=column_names)

    return notas_vi


def tratar_notas_vo(notas_vo, date):
    column_names = [
        "insc",
        "olimpiada1_vo",
        "participacao1_vo",
        "olimpiada2_vo",
        "participacao2_vo",
        "npo1_vo",
        "npo2_vo",
        "grupo1_vo",
        "grupo2_vo",
        "clas_opc1_vo",
        "clas_opc2_vo",
    ]

    if notas_vo is None:
        return pd.DataFrame(columns=column_names)

    notas_vo.rename(
        {
            "olimpiada1": "olimpiada1_vo",
            "olimpiada2": "olimpiada2_vo",
            "participacao1": "participacao1_vo",
            "participacao2": "participacao2_vo",
            "npo1": "npo1_vo",
            "npo2": "npo2_vo",
            "grupo1": "grupo1_vo",
            "grupo2": "grupo2_vo",
            "clas1": "clas_opc1_vo",
            "clas2": "clas_opc2_vo",
        },
        axis=1,
        inplace=True,
    )
    notas_vo = notas_vo.reindex(columns=column_names)

    return notas_vo


def tratar_notas_profis(notas_profis, date):
    column_names = [
        "insc",
        "escola_profis",
        "cod_esc_profis",
        "nf_profis",
        "clas_esc_profis",
    ]

    if notas_profis is None:
        return pd.DataFrame(columns=column_names)

    notas_profis.rename(
        {
            "insc_cand": "insc",
            "nome_escola": "escola_profis",
            "escola": "cod_esc_profis",
            "nf": "nf_profis",
            "clasescola": "clas_esc_profis",
        },
        axis=1,
        inplace=True,
    )
    notas_profis = notas_profis.reindex(columns=column_names)

    return notas_profis


def tratar_notas_he(notas_he, date):
    column_names = [
        "insc",
        "he1_arquitetura",
        "he2_arquitetura",
        "he3_arquitetura",
        "sala_cenicas",
        "palco_cenicas",
        "teorica_cenicas",
        "tecnica_danca",
        "criatividade_danca",
        "nglobal_danca",
        "historia_artes_visuais",
        "desenho_artes_visuais",
        "entrevista_artes_visuais",
        "nf_he",
    ]

    if notas_he is None:
        return pd.DataFrame(columns=column_names)

    notas_he.rename(
        {
            "insc_cand": "insc",
            "parte1": "he1_arquitetura",
            "parte2": "he2_arquitetura",
            "parte3": "he3_arquitetura",
            "sala": "sala_cenicas",
            "palco": "palco_cenicas",
            "teorica": "teorica_cenicas",
            "tecnica": "tecnica_danca",
            "criatividade": "criatividade_danca",
            "nglobal": "nglobal_danca",
            "historia": "historia_artes_visuais",
            "desenho": "desenho_artes_visuais",
            "entrevista": "entrevista_artes_visuais",
        },
        axis=1,
        inplace=True,
    )

    notas_he.replace(-1, pd.NA, inplace=True)

    notas_he = notas_he.reindex(columns=column_names)

    return notas_he


def extraction():
    notas_comvest = []

    for path, date in files.items():
        (
            notas_f1,
            notas_f2,
            notas_enem,
            notas_vi,
            notas_vo,
            notas_profis,
            notas_he,
        ) = leitura_notas(path, date)
        progresslog("notas", date)

        notas_f1 = tratar_notas_f1(notas_f1, date)
        notas_f2 = tratar_notas_f2(notas_f2, date)
        notas_enem = tratar_notas_enem(notas_enem, notas_f1["insc"], date)
        notas_vi = tratar_notas_vi(notas_vi, date)
        notas_vo = tratar_notas_vo(notas_vo, date)
        notas_profis = tratar_notas_profis(notas_profis, date)
        notas_he = tratar_notas_he(notas_he, date)

        notas_vc = notas_f1.merge(
            notas_f2, how="left", on="insc", suffixes=("_f1", "_f2")
        )
        notas_vc_enem = notas_vc.merge(notas_enem, how="outer", on="insc")
        notas_vc_enem_vi = notas_vc_enem.merge(notas_vi, how="outer", on="insc")
        notas_vc_enem_vi_vo = notas_vc_enem_vi.merge(notas_vo, how="outer", on="insc")
        notas_vc_enem_vi_vo_he = notas_vc_enem_vi_vo.merge(
            notas_he, how="outer", on="insc"
        )
        notas_final = notas_vc_enem_vi_vo_he.merge(notas_profis, how="outer", on="insc")

        # Insere data (ano) no dataframe final
        notas_final.insert(loc=0, column="ano_vest", value=date)

        # Renomeia a variável da inscrição para insc_vest para posteriormente fazer o merge com os outros DFs.
        notas_final.rename({"insc": "insc_vest"}, axis=1, inplace=True)
        notas_final["insc_vest"] = pd.to_numeric(
            notas_final["insc_vest"], errors="coerce", downcast="integer"
        ).astype("Int64")
        notas_final.dropna(subset=["insc_vest"], inplace=True)

        notas_comvest.append(notas_final)

    # Exportar CSV
    notas_comvest = pd.concat(notas_comvest)
    notas_comvest.sort_values(by="ano_vest", ascending=False, inplace=True)

    FILE_NAME = "notas_comvest.csv"
    write_result(notas_comvest, FILE_NAME)
    resultlog(FILE_NAME)
