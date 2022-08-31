import pandas as pd


def paais(df, ano):
    if 2005 <= ano <= 2013:
        df["paais_a"] = df["paais"].copy()

        df["paais_a"] = df["paais_a"].map(lambda x: x if x in {0, 1, 2} else pd.NA)
        df["paais"] = df["paais"].map({0: 0, 1: 1, 2: 1})
    elif 2014 <= ano <= 2018:
        df["paais_b"] = df["paais"].copy()

        df["paais_b"] = df["paais_b"].map(lambda x: x if x in {0, 1, 2} else pd.NA)
        df["paais"] = df["paais"].map({0: 0, 1: 1, 2: 1})
    elif 2019 <= ano:
        df["paais_c"] = df["paais"].copy()

        df["paais_c"] = df["paais_c"].map(lambda x: x if x in {0, 1, 2, 3} else pd.NA)
        df["paais"] = df["paais"].map({0: 0, 1: 2, 2: 3, 3: 4})

    return df


def isento(df, ano):
    if ano >= 2005:
        df["isento"] = df["isento"].map({0: 0, 1: 1, 2: 1, 3: 1})

    return df


def reg_campinas(df, ano):
    if ano >= 2004:
        df["reg_campinas"] = df["local_resid"].map(lambda row: 1 if row == 2 else "")
        df["reg_campinas"] = pd.to_numeric(df["reg_campinas"], errors="coerce").astype(
            "Int64"
        )

    return df


def em_exterior(df, ano):
    if 1989 <= ano <= 1999:
        df["em_exterior"] = df["tipo_curso_em"].map(lambda x: 1 if x == 8 else 0)
    elif 2000 <= ano <= 2003:
        df["em_exterior"] = df["tipo_curso_em"].map(lambda x: 1 if x == 5 else 0)
    elif 2004 <= ano <= 2012:
        df["em_exterior"] = df["tipo_curso_em"].map(lambda x: 1 if x == 6 else 0)
    elif 2013 <= ano:
        df["em_exterior"] = df["tipo_esc_em"].map(lambda x: 1 if x == 5 else 0)

    return df


def local_resid(df, ano):
    if 2004 <= ano:
        df["local_resid"] = df["local_resid"].map({0: 0, 1: 1, 2: 2, 3: 3, 4: 2, 5: 4})
    elif 1999 <= ano <= 2003:
        df["local_resid"] = df["local_resid"].map(
            {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 4, 6: 4}
        )

    return df


def tipo_esc_ef(df, ano):
    if 1987 <= ano <= 1988:
        df["tipo_esc_ef"] = df["tipo_esc_ef"].map({0: 0, 1: 2, 2: 1, 3: 3, 4: 4, 5: 5})
    elif 1989 <= ano <= 2012:
        df["tipo_esc_ef"] = df["tipo_esc_ef"].map(
            {0: 0, 1: 2, 2: 1, 3: 3, 4: 4, 5: 5, 6: 5}
        )
    elif 2013 <= ano <= 2016:
        df["tipo_esc_ef"] = df["tipo_esc_ef"].map(
            {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 5}
        )
    elif 2017 <= ano:
        df["tipo_esc_ef_1"] = df["tipo_esc_ef_1"].map(
            {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 5}
        )
        df["tipo_esc_ef_2"] = df["tipo_esc_ef_2"].map(
            {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 5}
        )

    return df


def tipo_esc_em(df, ano):
    if 1987 <= ano <= 1988:
        df["tipo_esc_em"] = df["tipo_esc_em"].map({0: 0, 1: 2, 2: 1, 3: 3, 4: 4, 5: 5})
    elif 1989 <= ano <= 2012:
        df["tipo_esc_em"] = df["tipo_esc_em"].map(
            {0: 0, 1: 2, 2: 1, 3: 3, 4: 4, 5: 5, 6: 5}
        )
    elif 2013 <= ano:
        df["tipo_esc_em"] = df["tipo_esc_em"].map(
            {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 5}
        )

    return df


def tipo_curso_em(df, ano):
    if 1987 <= ano <= 1988:
        df["tipo_curso_em"] = df["tipo_curso_em"].map(
            {0: 0, 1: 2, 2: 3, 3: 1, 4: 1, 5: 1, 6: 1, 7: 4, 8: 6}
        )
    elif 1989 <= ano <= 1999:
        df["tipo_curso_em"] = df["tipo_curso_em"].map(
            {0: 0, 1: 2, 2: 3, 3: 1, 4: 1, 5: 1, 6: 1, 7: 4, 8: 6, 9: 6}
        )
    elif 2000 <= ano <= 2003:
        df["tipo_curso_em"] = df["tipo_curso_em"].map(
            {0: 0, 1: 2, 2: 3, 3: 1, 4: 4, 5: 6, 6: 6}
        )
    elif 2004 <= ano <= 2012:
        df["tipo_curso_em"] = df["tipo_curso_em"].map(
            {0: 0, 1: 2, 2: 3, 3: 1, 4: 1, 5: 4, 6: 6, 7: 6}
        )

    return df


def periodo_em(df, ano):
    if 1987 <= ano <= 2012:
        df["periodo_em"] = df["periodo_em"].map(
            {0: 0, 1: 1, 2: 1, 3: 3, 4: 4, 5: 5, 6: 2, 7: 6}
        )

    return df


def cursinho(df, ano):
    if 2013 <= ano:
        df["cursinho"] = df["cursinho"].map({0: 0, 1: 2, 2: 1, 3: 1, 4: 1, 5: 1})

    df["cursinho"] = df["cursinho"].map(lambda x: x if x in {0, 1, 2} else pd.NA)

    return df


def cursinho_motivo(df, ano):
    if 1987 <= ano <= 1998:
        df["cursinho_motivo"] = df["cursinho_motivo"].map(
            {0: 0, 1: 1, 2: 2, 3: 3, 4: 6, 5: 4, 6: 5, 7: 6}
        )

    df["cursinho_motivo"] = df["cursinho_motivo"].map(
        lambda x: x if x in {0, 1, 2, 3, 4, 5, 6} else pd.NA
    )

    return df


def cursinho_tempo(df, ano):
    df["cursinho_tempo"] = df["cursinho_tempo"].map(
        lambda x: x if x in {0, 1, 2, 3, 4, 5} else pd.NA
    )

    return df


def vest_primeiro(df, ano):
    if 1987 <= ano <= 1998:
        df["vest_primeiro"] = df["vest_primeiro"].map(
            {0: 0, 1: 1, 2: 2, 3: 3, 4: 3, 5: 3, 6: 3, 7: 3, 8: 3, 9: 3}
        )

    return df


def vest_qts_inst(df, ano):
    if 1987 <= ano <= 2004 and ano != 2001:
        if ano <= 1998:
            df["vest_qts_inst"] = df["vest_qts_inst"].map(
                {0: 0, 1: 2, 2: 3, 3: 4, 4: 5, 5: 5, 6: 5, 7: 5, 8: 5, 9: 1}
            )

        validation = lambda x: x if x in {0, 1, 2, 3, 4, 5} else pd.NA
        df["vest_qts_inst"] = df["vest_qts_inst"].map(validation)

    return df


def univ_outra(df, ano):
    if 2013 <= ano:
        df["univ_outra"] = df["univ_outra"].map(
            {0: 0, 1: 2, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1}
        )

    df["univ_outra"] = df["univ_outra"].map(lambda x: x if x in {0, 1, 2} else pd.NA)

    return df


def disciplina_favorita(df, ano):
    if 1987 <= ano <= 1990:
        df["disciplina_favorita"] = df["disciplina_favorita"].map(
            {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 4, 6: 5, 7: 6, 8: 7, 9: 8, 10: 9, 11: 0}
        )

    return df


def opc1_escolha(df, ano):
    if not 1999 <= ano <= 2003:
        df = df.drop("opc1_escolha", axis=1, errors="ignore")

    return df


def opcao1_motivo(df, ano):
    if 1987 <= ano <= 1998:
        df["opc1_motivo_a"] = df["opc1_motivo"].map(
            {0: 0, 1: 1, 2: 9, 3: 2, 4: 3, 5: 4, 6: 5, 7: 6, 8: 7, 9: 8, 10: 9}
        )
    elif 1999 <= ano:
        df["opc1_motivo_b"] = df["opc1_motivo"].copy()

    return df


def unicamp_motivo(df, ano):
    if 1989 <= ano:
        df["unicamp_motivo"] = df["unicamp_motivo"].map(
            {0: 0, 1: 2, 2: 3, 3: 5, 4: 6, 5: 7, 6: 8, 7: 8, 8: 8}
        )

    return df


def idiomas(df, ano):
    if 1987 <= ano <= 1998:
        df["idiomas"] = df["idiomas"].map({0: 0, 1: 1, 2: 2, 3: 2, 4: 3, 5: 3})

    return df


def idiomas_familia(df, ano):
    if 1987 <= ano <= 1998:
        if ano <= 1990:
            df["idiomas_familia"] = df["idiomas_familia"].map(
                {
                    0: 0,
                    1: 1,
                    2: 2,
                    3: 3,
                    4: 4,
                    5: 5,
                    6: 6,
                    7: 7,
                    8: 9,
                    9: 8,
                    10: 9,
                    11: 9,
                    12: 9,
                    13: 9,
                    14: 9,
                    15: 9,
                }
            )

        validation = lambda x: x if x in {0, 1, 2, 3, 4, 5, 6, 7, 8, 9} else pd.NA
        df["idiomas_familia"] = df["idiomas_familia"].map(validation)

    return df


def situacao_pais(df, ano):
    if 1987 <= ano <= 1998:
        validation = lambda x: x if x in {0, 1, 2, 3, 4, 5, 6, 7, 8} else pd.NA
        df["situacao_pai"] = df["situacao_pai"].map(validation)
        df["situacao_mae"] = df["situacao_mae"].map(validation)

    return df


def educacao_pais(df, ano):
    if 1987 <= ano <= 2012:
        df["educ_pai"] = df["educ_pai"].map(
            {0: 0, 1: 1, 2: 2, 3: 2, 4: 2, 5: 3, 6: 4, 7: 5, 8: 6, 9: 7, 10: 8, 11: 9}
        )
        df["educ_mae"] = df["educ_mae"].map(
            {0: 0, 1: 1, 2: 2, 3: 2, 4: 2, 5: 3, 6: 4, 7: 5, 8: 6, 9: 7, 10: 8, 11: 9}
        )

    return df


def ocupacao_pais(df, ano):
    if 2004 <= ano <= 2007:
        df["ocup_pai"] = df["ocup_pai"].map(
            {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 10}
        )
        df["ocup_mae"] = df["ocup_mae"].map(
            {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 10}
        )

    return df


def trabalha_pais(df, ano):
    if 1987 <= ano <= 2004:
        df["trabalha_pai"] = df["trabalha_pai"].map(
            lambda x: x if x in {0, 1, 2, 3, 4, 5} else pd.NA
        )
        df["trabalha_mae"] = df["trabalha_mae"].map(
            lambda x: x if x in {0, 1, 2, 3, 4, 5, 6} else pd.NA
        )

    return df


def trabalha(df, ano):
    if 1987 <= ano <= 1999:
        df["trabalha"] = df["trabalha"].map({0: 0, 1: 1, 2: 3, 3: 4, 4: 2})
    elif 2000 <= ano <= 2012:
        df["trabalha"] = df["trabalha"].map({0: 0, 1: 1, 2: 2, 3: 3, 4: 3, 5: 4})

    return df


def contribui_renda_fam(df, ano):
    df["contribui_renda_fam"] = df["contribui_renda_fam"].map(
        lambda x: x if x in {0, 1, 2, 3, 4, 5} else pd.NA
    )

    return df


def renda_sm(df, ano):
    if 2013 <= ano:
        df["renda_sm_a"] = df["renda_sm"].copy()
        df["renda_sm"] = df["renda_sm"].map(
            {0: 0, 1: 1, 2: 1, 3: 1, 4: 2, 5: 3, 6: 3, 7: 4, 8: 5, 9: 5}
        )
    elif ano <= 2012 and ano not in [1994, 1995, 2011]:
        df["renda_sm_b"] = df["renda_sm"].copy()
        df["renda_sm"] = df["renda_sm"].map(
            {0: 0, 1: 1, 2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 7: 5, 8: 5, 9: 5}
        )
    elif ano == 2011:
        df["renda_sm_c"] = df["renda_sm"].copy()
    elif ano == 1994 or ano == 1995:
        df["renda_sm_d"] = df["renda_sm"].copy()
        df["renda_sm"] = ""

    return df


def renda_contrib_qtas(df, ano):
    if 2004 <= ano <= 2012:
        df["renda_contrib_qtas"] = df["renda_contrib_qtas"].map(
            {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 4, 6: 4}
        )

    return df


def ativ_extra_quais(df, ano):
    if 1987 <= ano <= 2004:
        if ano >= 1999:
            df["ativ_extra_quais"] = df["ativ_extra_quais"].map(
                {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 5, 7: 6}
            )

        validation = lambda x: x if x in {0, 1, 2, 3, 4, 5, 6} else pd.NA
        df["ativ_extra_quais"] = df["ativ_extra_quais"].map(validation)

    return df


def ativ_extra_principal(df, ano):
    if 1987 <= ano <= 1990:
        df["ativ_extra_principal"] = df["ativ_extra_principal"].map(
            {0: 0, 1: 1, 2: 2, 3: 2, 4: 3, 5: 5, 6: 5, 7: 4, 8: 5}
        )
    elif 1991 <= ano <= 1998:
        df["ativ_extra_principal"] = df["ativ_extra_principal"].map(
            {0: 0, 1: 1, 2: 2, 3: 2, 4: 3, 5: 5, 6: 5, 7: 4, 8: 5, 9: 5}
        )
    elif 1999 <= ano <= 2004:
        df["ativ_extra_principal"] = df["ativ_extra_principal"].map(
            {0: 0, 1: 1, 2: 2, 3: 3, 4: 5, 5: 4, 6: 5, 7: 5, 8: 5}
        )

    return df


def leitura_tipo(df, ano):
    if 1987 <= ano <= 1996:
        df["leitura_tipo"] = df["leitura_tipo"].map(
            {0: 0, 1: 1, 2: 1, 3: 1, 4: 2, 5: 4}
        )
    elif 1997 <= ano <= 2001:
        df["leitura_tipo"] = df["leitura_tipo"].map(
            {0: 0, 1: 1, 2: 1, 3: 1, 4: 2, 5: 1, 6: 3, 7: 4}
        )
    elif 2002 <= ano <= 2004:
        df["leitura_tipo"] = df["leitura_tipo"].map(
            {0: 0, 1: 1, 2: 1, 3: 3, 4: 1, 5: 3, 6: 2, 7: 2, 8: 4}
        )

    return df


def revistas_tipo(df, ano):
    if 1987 <= ano <= 1989:
        df["revistas_tipo"] = df["revistas_tipo"].map(
            {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 7}
        )
    elif 1999 <= ano <= 2002:
        df["revistas_tipo"] = df["revistas_tipo"].map(
            {0: 0, 1: 1, 2: 2, 3: 2, 4: 3, 5: 4, 6: 5, 7: 6, 8: 7}
        )

    return df


def geladeira(df, ano):
    if ano == 2004:
        df["geladeira"] = df["geladeira"].map({0: 0, 1: 2, 2: 1, 3: 1, 4: 1, 5: 1})
    elif ano >= 2020:
        df["geladeira"] = df["geladeira"].map({0: 0, 1: 1, 2: 1, 3: 1, 4: 1, 5: 2})

    return df


def freezer(df, ano):
    if ano == 2004:
        df["freezer"] = df["freezer"].map({0: 0, 1: 2, 2: 1, 3: 1, 4: 1, 5: 1})
    elif ano >= 2020:
        df["freezer"] = df["freezer"].map({0: 0, 1: 1, 2: 1, 3: 1, 4: 1, 5: 2})

    return df


def maq_roupa(df, ano):
    if ano == 2004:
        df["maq_roupa"] = df["maq_roupa"].map({0: 0, 1: 2, 2: 1, 3: 1, 4: 1, 5: 1})
    elif ano >= 2020:
        df["maq_roupa"] = df["maq_roupa"].map({0: 0, 1: 1, 2: 1, 3: 1, 4: 1, 5: 2})

    return df


def maq_louca(df, ano):
    if ano >= 2020:
        df["maq_louca"] = df["maq_louca"].map({0: 0, 1: 1, 2: 1, 3: 1, 4: 1, 5: 2})

    return df


def internet(df, ano):
    if ano == 2011 or ano == 2012:
        df["internet"] = df["internet"].map({0: 0, 1: 1, 2: 1, 3: 2})

    return df


def cozinha_qtas(df, ano):
    if ano == 2004:
        df["cozinha_qtas"] = df["cozinha_qtas"].map(
            {0: 0, 1: 5, 2: 1, 3: 2, 4: 3, 5: 4}
        )

    return df


def sala_qtas(df, ano):
    if ano == 2004:
        df["sala_qtas"] = df["sala_qtas"].map({0: 0, 1: 5, 2: 1, 3: 2, 4: 3, 5: 4})

    return df


def quarto_qts(df, ano):
    if ano == 2004:
        df["quarto_qts"] = df["quarto_qts"].map({0: 0, 1: 5, 2: 1, 3: 2, 4: 3, 5: 4})

    return df


def banheiro_qts(df, ano):
    if ano == 2004:
        df["banheiro_qts"] = df["banheiro_qts"].map(
            {0: 0, 1: 5, 2: 1, 3: 2, 4: 3, 5: 4}
        )

    return df


def radio_qts(df, ano):
    if ano == 2004:
        df["radio_qts"] = df["radio_qts"].map({0: 0, 1: 5, 2: 1, 3: 2, 4: 3, 5: 4})

    return df


def tv_qts(df, ano):
    if ano == 2004:
        df["tv_qts"] = df["tv_qts"].map({0: 0, 1: 5, 2: 1, 3: 2, 4: 3, 5: 4})

    return df


def dvd_vhs_qts(df, ano):
    if ano == 2004:
        df["dvd_vhs_qts"] = df["dvd_vhs_qts"].map({0: 0, 1: 5, 2: 1, 3: 2, 4: 3, 5: 4})

    df = df.loc[:, ~df.columns.duplicated()]

    return df


def computador_qtos(df, ano):
    if ano == 2004:
        df["computador_qtos"] = df["computador_qtos"].map(
            {0: 0, 1: 5, 2: 1, 3: 2, 4: 3, 5: 4}
        )

    if "computador" not in df.columns and "computador_qtos" in df.columns:
        df["computador"] = df["computador_qtos"].map(
            {0: 0, 1: 1, 2: 1, 3: 1, 4: 1, 5: 2}
        )

    return df


def carro_qtos(df, ano):
    if ano == 2004:
        df["carro_qtos"] = df["carro_qtos"].map({0: 0, 1: 5, 2: 1, 3: 2, 4: 3, 5: 4})

    return df


def aspirador(df, ano):
    if ano == 2004:
        df["aspirador"] = df["aspirador"].map({0: 0, 1: 2, 2: 1, 3: 1, 4: 1, 5: 1})

    return df


def jornal_le(df, ano):
    if 1987 <= ano <= 2019:
        validation = lambda x: x if x in {0, 1, 2, 3, 4, 5} else pd.NA
        df["jornal_le"] = df["jornal_le"].map(validation)

    return df


def normalizar(df, ano):
    """
    Desc: Uniformiza os valores das questões do questionário.
            Checar documento das propostas para normalização de respostas dos questionários (drive)
    Args: Dataframe do perfil, ano da base
    Returns: Dataframe do perfil com valores normalizados
    """

    df = paais(df, ano)
    df = isento(df, ano)

    df = reg_campinas(df, ano)
    df = local_resid(df, ano)

    df = em_exterior(df, ano)
    df = tipo_esc_ef(df, ano)
    df = tipo_esc_em(df, ano)
    df = tipo_curso_em(df, ano)
    df = periodo_em(df, ano)
    df = cursinho(df, ano)
    df = cursinho_motivo(df, ano)
    df = cursinho_tempo(df, ano)
    df = vest_primeiro(df, ano)
    df = vest_qts_inst(df, ano)
    df = univ_outra(df, ano)
    df = disciplina_favorita(df, ano)
    df = opc1_escolha(df, ano)
    df = opcao1_motivo(df, ano)
    df = unicamp_motivo(df, ano)
    df = idiomas(df, ano)
    df = idiomas_familia(df, ano)

    df = situacao_pais(df, ano)
    df = educacao_pais(df, ano)
    df = ocupacao_pais(df, ano)
    df = trabalha_pais(df, ano)

    df = trabalha(df, ano)
    df = contribui_renda_fam(df, ano)
    df = renda_sm(df, ano)
    df = renda_contrib_qtas(df, ano)

    df = ativ_extra_quais(df, ano)
    df = ativ_extra_principal(df, ano)
    df = leitura_tipo(df, ano)
    df = revistas_tipo(df, ano)
    df = geladeira(df, ano)
    df = freezer(df, ano)
    df = maq_roupa(df, ano)
    df = maq_louca(df, ano)
    df = internet(df, ano)
    df = cozinha_qtas(df, ano)
    df = sala_qtas(df, ano)
    df = quarto_qts(df, ano)
    df = banheiro_qts(df, ano)
    df = radio_qts(df, ano)
    df = tv_qts(df, ano)
    df = dvd_vhs_qts(df, ano)
    df = computador_qtos(df, ano)
    df = carro_qtos(df, ano)
    df = aspirador(df, ano)
    df = jornal_le(df, ano)

    return df
