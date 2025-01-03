"""
Módulo para normalização de respostas dos questionários Comvest.

Este módulo contém funções para uniformizar os valores das questões do questionário dos candidatos.

Funções:
- normalizar(df, ano): Uniformiza os valores das questões do questionário.
- paais(df, ano): Normaliza a questão sobre o PAAIS.
- isento(df, ano): Normaliza a questão sobre isenção de taxa.
- reg_campinas(df, ano): Normaliza a questão sobre a região de Campinas.
- local_resid(df, ano): Normaliza a questão sobre o local de residência.
- em_exterior(df, ano): Normaliza a questão sobre estudos no exterior.
- tipo_esc_ef(df, ano): Normaliza a questão sobre o tipo de escola do ensino fundamental.
- tipo_esc_em(df, ano): Normaliza a questão sobre o tipo de escola do ensino médio.
- tipo_curso_em(df, ano): Normaliza a questão sobre o tipo de curso do ensino médio.
- periodo_em(df, ano): Normaliza a questão sobre o período do ensino médio.
- reprovacao_em(df, ano): Normaliza a questão sobre reprovação no ensino médio.
- cursinho(df, ano): Normaliza a questão sobre cursinho.
- cursinho_motivo(df, ano): Normaliza a questão sobre o motivo do cursinho.
- cursinho_tempo(df, ano): Normaliza a questão sobre o tempo de cursinho.
- curso_interesse(df, ano): Normaliza a questão sobre o curso de interesse.
- vest_primeiro(df, ano): Normaliza a questão sobre o primeiro vestibular.
- vest_qts_inst(df, ano): Normaliza a questão sobre a quantidade de instituições de vestibular.
- univ_outra(df, ano): Normaliza a questão sobre outra universidade.
- disciplina_favorita(df, ano): Normaliza a questão sobre a disciplina favorita.
- opc1_escolha(df, ano): Normaliza a questão sobre a escolha da primeira opção.
- opcao1_motivo(df, ano): Normaliza a questão sobre o motivo da primeira opção.
- unicamp_motivo(df, ano): Normaliza a questão sobre o motivo de escolher a Unicamp.
- idiomas(df, ano): Normaliza a questão sobre idiomas.
- idiomas_familia(df, ano): Normaliza a questão sobre idiomas na família.
- idioma_vest_escolha(df, ano): Normaliza a questão sobre a escolha do idioma no vestibular.
- situacao_pais(df, ano): Normaliza a questão sobre a situação dos pais.
- subordinados_mae(df, ano): Normaliza a questão sobre subordinados da mãe.
- educacao_pais(df, ano): Normaliza a questão sobre a educação dos pais.
- ocupacao_pais(df, ano): Normaliza a questão sobre a ocupação dos pais.
- trabalha_pais(df, ano): Normaliza a questão sobre o trabalho dos pais.
- opiniao_pais(df, ano): Normaliza a questão sobre a opinião dos pais.
- trabalha(df, ano): Normaliza a questão sobre o trabalho do candidato.
- contribui_renda_fam(df, ano): Normaliza a questão sobre a contribuição para a renda familiar.
- renda_sm(df, ano): Normaliza a questão sobre a renda em salários mínimos.
- renda_contrib_qtas(df, ano): Normaliza a questão sobre a quantidade de contribuintes para a renda.
- ativ_extra_quais(df, ano): Normaliza a questão sobre as atividades extracurriculares.
- ativ_extra_principal(df, ano): Normaliza a questão sobre a principal atividade extracurricular.
- leitura_tipo(df, ano): Normaliza a questão sobre o tipo de leitura.
- inform_meio(df, ano): Normaliza a questão sobre o meio de informação.
- revistas_tipo(df, ano): Normaliza a questão sobre o tipo de revistas.
- geladeira(df, ano): Normaliza a questão sobre a quantidade de geladeiras.
- freezer(df, ano): Normaliza a questão sobre a quantidade de freezers.
- maq_roupa(df, ano): Normaliza a questão sobre a quantidade de máquinas de lavar roupa.
- maq_louca(df, ano): Normaliza a questão sobre a quantidade de máquinas de lavar louça.
- internet(df, ano): Normaliza a questão sobre o acesso à internet.
- cozinha_qtas(df, ano): Normaliza a questão sobre a quantidade de cozinhas.
- sala_qtas(df, ano): Normaliza a questão sobre a quantidade de salas.
- quarto_qts(df, ano): Normaliza a questão sobre a quantidade de quartos.
- banheiro_qts(df, ano): Normaliza a questão sobre a quantidade de banheiros.
- radio_qts(df, ano): Normaliza a questão sobre a quantidade de rádios.
- tv_qts(df, ano): Normaliza a questão sobre a quantidade de televisores.
- dvd_vhs_qts(df, ano): Normaliza a questão sobre a quantidade de aparelhos de DVD/VHS.
- computador_qtos(df, ano): Normaliza a questão sobre a quantidade de computadores.
- carro_qtos(df, ano): Normaliza a questão sobre a quantidade de carros.
- aspirador(df, ano): Normaliza a questão sobre a quantidade de aspiradores de pó.
- jornal_le(df, ano): Normaliza a questão sobre a leitura de jornais.


Como usar:
Implemente e execute as funções para normalizar os valores das questões do questionário dos candidatos.
"""


import pandas as pd


def paais(df, ano):
    """
    Normaliza a questão sobre o PAAIS.

    Parâmetros
    ----------
    df : DataFrame
        O DataFrame contendo os dados de perfil dos candidatos.
    ano : int
        O ano de referência para a normalização das respostas.

    Retorna
    -------
    DataFrame
        O DataFrame com a questão do PAAIS normalizada.
    """
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
    """
    Normaliza a questão sobre isenção de taxa.

    Parâmetros
    ----------
    df : DataFrame
        O DataFrame contendo os dados de perfil dos candidatos.
    ano : int
        O ano de referência para a normalização das respostas.

    Retorna
    -------
    DataFrame
        O DataFrame com a questão sobre isenção de taxa normalizada.
    """
    if ano >= 2005:
        df["isento"] = df["isento"].map({0: 0, 1: 1, 2: 1, 3: 1})

    return df


def reg_campinas(df, ano):
    """
    Normaliza a questão sobre a região de Campinas.

    Parâmetros
    ----------
    df : DataFrame
        O DataFrame contendo os dados de perfil dos candidatos.
    ano : int
        O ano de referência para a normalização das respostas.

    Retorna
    -------
    DataFrame
        O DataFrame com a questão sobre a região de Campinas normalizada.
    """
    if ano >= 2004:
        df["reg_campinas"] = df["local_resid"].map(lambda row: 1 if row == 2 else "")
        df["reg_campinas"] = pd.to_numeric(df["reg_campinas"], errors="coerce").astype(
            "Int64"
        )

    return df


def em_exterior(df, ano):
    """
    Normaliza a questão sobre estudos no exterior.

    Parâmetros
    ----------
    df : DataFrame
        O DataFrame contendo os dados de perfil dos candidatos.
    ano : int
        O ano de referência para a normalização das respostas.

    Retorna
    -------
    DataFrame
        O DataFrame com a questão sobre estudos no exterior normalizada.
    """
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
    """
    Normaliza a questão sobre o local de residência.

    Parâmetros
    ----------
    df : DataFrame
        O DataFrame contendo os dados de perfil dos candidatos.
    ano : int
        O ano de referência para a normalização das respostas.

    Retorna
    -------
    DataFrame
        O DataFrame com a questão sobre o local de residência normalizada.
    """
    if 2004 <= ano:
        df["local_resid"] = df["local_resid"].map({0: 0, 1: 1, 2: 2, 3: 3, 4: 2, 5: 4})
    elif 1999 <= ano <= 2003:
        df["local_resid"] = df["local_resid"].map(
            {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 4, 6: 4}
        )

    return df


def tipo_esc_ef(df, ano):
    """
    Normaliza a questão sobre o tipo de escola do ensino fundamental.

    Parâmetros
    ----------
    df : DataFrame
        O DataFrame contendo os dados de perfil dos candidatos.
    ano : int
        O ano de referência para a normalização das respostas.

    Retorna
    -------
    DataFrame
        O DataFrame com a questão sobre o tipo de escola do ensino fundamental normalizada.
    """
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
    """
    Normaliza a questão sobre o tipo de escola do ensino médio.

    Parâmetros
    ----------
    df : DataFrame
        O DataFrame contendo os dados de perfil dos candidatos.
    ano : int
        O ano de referência para a normalização das respostas.

    Retorna
    -------
    DataFrame
        O DataFrame com a questão sobre o tipo de escola do ensino médio normalizada.
    """
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
    """
    Normaliza a questão sobre o tipo de curso do ensino médio.

    Parâmetros
    ----------
    df : DataFrame
        O DataFrame contendo os dados de perfil dos candidatos.
    ano : int
        O ano de referência para a normalização das respostas.

    Retorna
    -------
    DataFrame
        O DataFrame com a questão sobre o tipo de curso do ensino médio normalizada.
    """
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
    """
    Normaliza a questão sobre o período do ensino médio.

    Parâmetros
    ----------
    df : DataFrame
        O DataFrame contendo os dados de perfil dos candidatos.
    ano : int
        O ano de referência para a normalização das respostas.

    Retorna
    -------
    DataFrame
        O DataFrame com a questão sobre o período do ensino médio normalizada.
    """
    if 1987 <= ano <= 2012:
        df["periodo_em"] = df["periodo_em"].map(
            {0: 0, 1: 1, 2: 1, 3: 3, 4: 4, 5: 5, 6: 2, 7: 6}
        )

    return df


def reprovacao_em(df, ano):
    """
    Normaliza a questão sobre reprovação no ensino médio.

    Parâmetros
    ----------
    df : DataFrame
        O DataFrame contendo os dados de perfil dos candidatos.
    ano : int
        O ano de referência para a normalização das respostas.

    Retorna
    -------
    DataFrame
        O DataFrame com a questão sobre reprovação no ensino médio normalizada.
    """
    if 1987 <= ano <= 2004:
        validation = lambda x: x if x in {0, 1, 2, 3, 4, 5} else pd.NA

        df["reprovacao_em"] = df["reprovacao_em"].map(validation)

    return df


def cursinho(df, ano):
    """
    Normaliza a questão sobre cursinho.

    Parâmetros
    ----------
    df : DataFrame
        O DataFrame contendo os dados de perfil dos candidatos.
    ano : int
        O ano de referência para a normalização das respostas.

    Retorna
    -------
    DataFrame
        O DataFrame com a questão sobre cursinho normalizada.
    """
    if 2013 <= ano:
        df["cursinho"] = df["cursinho"].map({0: 0, 1: 2, 2: 1, 3: 1, 4: 1, 5: 1})

    df["cursinho"] = df["cursinho"].map(lambda x: x if x in {0, 1, 2} else pd.NA)

    return df


def cursinho_motivo(df, ano):
    """
    Normaliza a questão sobre o motivo do cursinho.

    Parâmetros
    ----------
    df : DataFrame
        O DataFrame contendo os dados de perfil dos candidatos.
    ano : int
        O ano de referência para a normalização das respostas.

    Retorna
    -------
    DataFrame
        O DataFrame com a questão sobre o motivo do cursinho normalizada.
    """
    if 1987 <= ano <= 1998:
        df["cursinho_motivo"] = df["cursinho_motivo"].map(
            {0: 0, 1: 1, 2: 2, 3: 3, 4: 6, 5: 4, 6: 5, 7: 6}
        )

    df["cursinho_motivo"] = df["cursinho_motivo"].map(
        lambda x: x if x in {0, 1, 2, 3, 4, 5, 6} else pd.NA
    )

    return df


def cursinho_tempo(df, ano):
    """
    Normaliza a questão sobre o tempo de cursinho.

    Parâmetros
    ----------
    df : DataFrame
        O DataFrame contendo os dados de perfil dos candidatos.
    ano : int
        O ano de referência para a normalização das respostas.

    Retorna
    -------
    DataFrame
        O DataFrame com a questão sobre o tempo de cursinho normalizada.
    """
    df["cursinho_tempo"] = df["cursinho_tempo"].map(
        lambda x: x if x in {0, 1, 2, 3, 4, 5} else pd.NA
    )

    return df


def curso_interesse(df, ano):
    """
    Normaliza a questão sobre o curso de interesse.

    Parâmetros
    ----------
    df : DataFrame
        O DataFrame contendo os dados de perfil dos candidatos.
    ano : int
        O ano de referência para a normalização das respostas.

    Retorna
    -------
    DataFrame
        O DataFrame com a questão sobre o curso de interesse normalizada.
    """
    if 1987 <= ano <= 1998:
        validation = lambda x: x if x in {0, 1, 2, 3, 4, 5} else pd.NA

        df["curso_interesse"] = df["curso_interesse"].map(validation)

    return df


def vest_primeiro(df, ano):
    """
    Normaliza a questão sobre o primeiro vestibular.

    Parâmetros
    ----------
    df : DataFrame
        O DataFrame contendo os dados de perfil dos candidatos.
    ano : int
        O ano de referência para a normalização das respostas.

    Retorna
    -------
    DataFrame
        O DataFrame com a questão sobre o primeiro vestibular normalizada.
    """
    if 1987 <= ano <= 1998:
        df["vest_primeiro"] = df["vest_primeiro"].map(
            {0: 0, 1: 1, 2: 2, 3: 3, 4: 3, 5: 3, 6: 3, 7: 3, 8: 3, 9: 3}
        )

    return df


def vest_qts_inst(df, ano):
    """
    Normaliza a questão sobre a quantidade de instituições de vestibular.

    Parâmetros
    ----------
    df : DataFrame
        O DataFrame contendo os dados de perfil dos candidatos.
    ano : int
        O ano de referência para a normalização das respostas.

    Retorna
    -------
    DataFrame
        O DataFrame com a questão sobre a quantidade de instituições de vestibular normalizada.
    """
    if 1987 <= ano <= 2004 and ano != 2001:
        if ano <= 1998:
            df["vest_qts_inst"] = df["vest_qts_inst"].map(
                {0: 0, 1: 2, 2: 3, 3: 4, 4: 5, 5: 5, 6: 5, 7: 5, 8: 5, 9: 1}
            )

        validation = lambda x: x if x in {0, 1, 2, 3, 4, 5} else pd.NA
        df["vest_qts_inst"] = df["vest_qts_inst"].map(validation)

    return df


def univ_outra(df, ano):
    """
    Normaliza a questão sobre outra universidade.

    Parâmetros
    ----------
    df : DataFrame
        O DataFrame contendo os dados de perfil dos candidatos.
    ano : int
        O ano de referência para a normalização das respostas.

    Retorna
    -------
    DataFrame
        O DataFrame com a questão sobre outra universidade normalizada.
    """
    if 2013 <= ano:
        df["univ_outra"] = df["univ_outra"].map(
            {0: 0, 1: 2, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1}
        )

    df["univ_outra"] = df["univ_outra"].map(lambda x: x if x in {0, 1, 2} else pd.NA)

    return df


def disciplina_favorita(df, ano):
    """
    Normaliza a questão sobre a disciplina favorita.

    Parâmetros
    ----------
    df : DataFrame
        O DataFrame contendo os dados de perfil dos candidatos.
    ano : int
        O ano de referência para a normalização das respostas.

    Retorna
    -------
    DataFrame
        O DataFrame com a questão sobre a disciplina favorita normalizada.
    """
    if 1987 <= ano <= 1990:
        df["disciplina_favorita"] = df["disciplina_favorita"].map(
            {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 4, 6: 5, 7: 6, 8: 7, 9: 8, 10: 9, 11: 0}
        )

    return df


def opc1_escolha(df, ano):
    """
    Normaliza a questão sobre a escolha da primeira opção.

    Parâmetros
    ----------
    df : DataFrame
        O DataFrame contendo os dados de perfil dos candidatos.
    ano : int
        O ano de referência para a normalização das respostas.

    Retorna
    -------
    DataFrame
        O DataFrame com a questão sobre a escolha da primeira opção normalizada.
    """
    if not 1999 <= ano <= 2003:
        df = df.drop("opc1_escolha", axis=1, errors="ignore")

    return df


def opcao1_motivo(df, ano):
    """
    Normaliza a questão sobre o motivo da primeira opção.

    Parâmetros
    ----------
    df : DataFrame
        O DataFrame contendo os dados de perfil dos candidatos.
    ano : int
        O ano de referência para a normalização das respostas.

    Retorna
    -------
    DataFrame
        O DataFrame com a questão sobre o motivo da primeira opção normalizada.
    """
    if 1987 <= ano <= 1998:
        df["opc1_motivo_a"] = df["opc1_motivo"].map(
            {0: 0, 1: 1, 2: 9, 3: 2, 4: 3, 5: 4, 6: 5, 7: 6, 8: 7, 9: 8, 10: 9}
        )
    elif 1999 <= ano:
        df["opc1_motivo_b"] = df["opc1_motivo"].copy()

    return df


def unicamp_motivo(df, ano):
    """
    Normaliza a questão sobre o motivo de escolher a Unicamp.

    Parâmetros
    ----------
    df : DataFrame
        O DataFrame contendo os dados de perfil dos candidatos.
    ano : int
        O ano de referência para a normalização das respostas.

    Retorna
    -------
    DataFrame
        O DataFrame com a questão sobre o motivo de escolher a Unicamp normalizada.
    """
    if 1989 <= ano:
        df["unicamp_motivo"] = df["unicamp_motivo"].map(
            {0: 0, 1: 2, 2: 3, 3: 5, 4: 6, 5: 7, 6: 8, 7: 8, 8: 8}
        )

    return df


def idiomas(df, ano):
    """
    Normaliza a questão sobre idiomas.

    Parâmetros
    ----------
    df : DataFrame
        O DataFrame contendo os dados de perfil dos candidatos.
    ano : int
        O ano de referência para a normalização das respostas.

    Retorna
    -------
    DataFrame
        O DataFrame com a questão sobre idiomas normalizada.
    """
    if 1987 <= ano <= 1998:
        df["idiomas"] = df["idiomas"].map({0: 0, 1: 1, 2: 2, 3: 2, 4: 3, 5: 3})

    return df


def idiomas_familia(df, ano):
    """
    Normaliza a questão sobre idiomas na família.

    Parâmetros
    ----------
    df : DataFrame
        O DataFrame contendo os dados de perfil dos candidatos.
    ano : int
        O ano de referência para a normalização das respostas.

    Retorna
    -------
    DataFrame
        O DataFrame com a questão sobre idiomas na família normalizada.
    """
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


def idioma_vest_escolha(df, ano):
    """
    Normaliza a questão sobre a escolha do idioma no vestibular.

    Parâmetros
    ----------
    df : DataFrame
        O DataFrame contendo os dados de perfil dos candidatos.
    ano : int
        O ano de referência para a normalização das respostas.

    Retorna
    -------
    DataFrame
        O DataFrame com a questão sobre a escolha do idioma no vestibular normalizada.
    """
    if 1987 <= ano <= 2005:
        validation = lambda x: x if x in {0, 1, 2} else pd.NA
        df["idioma_vest_escolha"] = df["idioma_vest_escolha"].map(validation)

    return df


def situacao_pais(df, ano):
    """
    Normaliza a questão sobre a situação dos pais.

    Parâmetros
    ----------
    df : DataFrame
        O DataFrame contendo os dados de perfil dos candidatos.
    ano : int
        O ano de referência para a normalização das respostas.

    Retorna
    -------
    DataFrame
        O DataFrame com a questão sobre a situação dos pais normalizada.
    """
    if 1987 <= ano <= 1998:
        validation = lambda x: x if x in {0, 1, 2, 3, 4, 5, 6, 7, 8} else pd.NA
        df["situacao_pai"] = df["situacao_pai"].map(validation)
        df["situacao_mae"] = df["situacao_mae"].map(validation)

    return df


def subordinados_mae(df, ano):
    """
    Normaliza a questão sobre subordinados da mãe.

    Parâmetros
    ----------
    df : DataFrame
        O DataFrame contendo os dados de perfil dos candidatos.
    ano : int
        O ano de referência para a normalização.

    Retorna
    -------
    DataFrame
        O DataFrame com a questão sobre subordinados da mãe normalizada.
    """
    if 1987 <= ano <= 1998:
        validation = lambda x: x if x in {0, 1, 2, 3, 4, 5} else pd.NA
        df["subordinados_mae"] = df["subordinados_mae"].map(validation)

    return df


def educacao_pais(df, ano):
    """
    Normaliza a questão sobre a educação dos pais.

    Parâmetros
    ----------
    df : DataFrame
        O DataFrame contendo os dados de perfil dos candidatos.
    ano : int
        O ano de referência para a normalização.

    Retorna
    -------
    DataFrame
        O DataFrame com a questão sobre a educação dos pais normalizada.
    """
    if 1987 <= ano <= 2012:
        df["educ_pai"] = df["educ_pai"].map(
            {0: 0, 1: 1, 2: 2, 3: 2, 4: 2, 5: 3, 6: 4, 7: 5, 8: 6, 9: 7, 10: 8, 11: 9}
        )
        df["educ_mae"] = df["educ_mae"].map(
            {0: 0, 1: 1, 2: 2, 3: 2, 4: 2, 5: 3, 6: 4, 7: 5, 8: 6, 9: 7, 10: 8, 11: 9}
        )

    return df


def ocupacao_pais(df, ano):
    """
    Normaliza a questão sobre a ocupação dos pais.

    Parâmetros
    ----------
    df : DataFrame
        O DataFrame contendo os dados de perfil dos candidatos.
    ano : int
        O ano de referência para a normalização.

    Retorna
    -------
    DataFrame
        O DataFrame com a questão sobre a ocupação dos pais normalizada.
    """
    if 2004 <= ano <= 2007:
        df["ocup_pai"] = df["ocup_pai"].map(
            {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 10}
        )
        df["ocup_mae"] = df["ocup_mae"].map(
            {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 10}
        )

    return df


def trabalha_pais(df, ano):
    """
    Normaliza a questão sobre o trabalho dos pais.

    Parâmetros
    ----------
    df : DataFrame
        O DataFrame contendo os dados de perfil dos candidatos.
    ano : int
        O ano de referência para a normalização.

    Retorna
    -------
    DataFrame
        O DataFrame com a questão sobre o trabalho dos pais normalizada.
    """
    if 1987 <= ano <= 2004:
        df["trabalha_pai"] = df["trabalha_pai"].map(
            lambda x: x if x in {0, 1, 2, 3, 4, 5} else pd.NA
        )
        df["trabalha_mae"] = df["trabalha_mae"].map(
            lambda x: x if x in {0, 1, 2, 3, 4, 5, 6} else pd.NA
        )

    return df


def opiniao_pais(df, ano):
    """
    Normaliza a questão sobre a opinião dos pais.

    Parâmetros
    ----------
    df : DataFrame
        O DataFrame contendo os dados de perfil dos candidatos.
    ano : int
        O ano de referência para a normalização.

    Retorna
    -------
    DataFrame
        O DataFrame com a questão sobre a opinião dos pais normalizada.
    """
    if 1987 <= ano <= 1998:
        validation = lambda x: x if x in {0, 1, 2, 3, 4, 5} else pd.NA
        df["opiniao_pais"] = df["opiniao_pais"].map(validation)

    return df


def trabalha(df, ano):
    """
    Normaliza a questão sobre o trabalho do candidato.

    Parâmetros
    ----------
    df : DataFrame
        O DataFrame contendo os dados de perfil dos candidatos.
    ano : int
        O ano de referência para a normalização.

    Retorna
    -------
    DataFrame
        O DataFrame com a questão sobre o trabalho do candidato normalizada.
    """
    if 1987 <= ano <= 1999:
        df["trabalha"] = df["trabalha"].map({0: 0, 1: 1, 2: 3, 3: 4, 4: 2})
    elif 2000 <= ano <= 2012:
        df["trabalha"] = df["trabalha"].map({0: 0, 1: 1, 2: 2, 3: 3, 4: 3, 5: 4})

    return df


def contribui_renda_fam(df, ano):
    """
    Normaliza a questão sobre a contribuição para a renda familiar.

    Parâmetros
    ----------
    df : DataFrame
        O DataFrame contendo os dados de perfil dos candidatos.
    ano : int
        O ano de referência para a normalização.

    Retorna
    -------
    DataFrame
        O DataFrame com a questão sobre a contribuição para a renda familiar normalizada.
    """
    df["contribui_renda_fam"] = df["contribui_renda_fam"].map(
        lambda x: x if x in {0, 1, 2, 3, 4, 5} else pd.NA
    )

    return df


def renda_sm(df, ano):
    """
    Normaliza a questão sobre a renda em salários mínimos.

    Parâmetros
    ----------
    df : DataFrame
        O DataFrame contendo os dados de perfil dos candidatos.
    ano : int
        O ano de referência para a normalização.

    Retorna
    -------
    DataFrame
        O DataFrame com a questão sobre a renda em salários mínimos normalizada.
    """
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
    """
    Normaliza a questão sobre a quantidade de contribuintes para a renda.

    Parâmetros
    ----------
    df : DataFrame
        O DataFrame contendo os dados de perfil dos candidatos.
    ano : int
        O ano de referência para a normalização.

    Retorna
    -------
    DataFrame
        O DataFrame com a questão sobre a quantidade de contribuintes para a renda normalizada.
    """
    if 2004 <= ano <= 2012:
        df["renda_contrib_qtas"] = df["renda_contrib_qtas"].map(
            {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 4, 6: 4}
        )

    return df


def ativ_extra_quais(df, ano):
    """
    Normaliza a questão sobre as atividades extracurriculares.

    Parâmetros
    ----------
    df : DataFrame
        O DataFrame contendo os dados de perfil dos candidatos.
    ano : int
        O ano de referência para a normalização.

    Retorna
    -------
    DataFrame
        O DataFrame com a questão sobre as atividades extracurriculares normalizada.
    """
    if 1987 <= ano <= 2004:
        if ano >= 1999:
            df["ativ_extra_quais"] = df["ativ_extra_quais"].map(
                {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 5, 7: 6}
            )

        validation = lambda x: x if x in {0, 1, 2, 3, 4, 5, 6} else pd.NA
        df["ativ_extra_quais"] = df["ativ_extra_quais"].map(validation)

    return df


def ativ_extra_principal(df, ano):
    """
    Normaliza a questão sobre a principal atividade extracurricular.

    Parâmetros
    ----------
    df : DataFrame
        O DataFrame contendo os dados de perfil dos candidatos.
    ano : int
        O ano de referência para a normalização.

    Retorna
    -------
    DataFrame
        O DataFrame com a questão sobre a principal atividade extracurricular normalizada.
    """
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
    """
    Normaliza a questão sobre o tipo de leitura.

    Parâmetros
    ----------
    df : DataFrame
        O DataFrame contendo os dados de perfil dos candidatos.
    ano : int
        O ano de referência para a normalização.

    Retorna
    -------
    DataFrame
        O DataFrame com a questão sobre o tipo de leitura normalizada.
    """
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


def inform_meio(df, ano):
    """
    Normaliza a questão sobre o meio de informação.

    Parâmetros
    ----------
    df : DataFrame
        O DataFrame contendo os dados de perfil dos candidatos.
    ano : int
        O ano de referência para a normalização.

    Retorna
    -------
    DataFrame
        O DataFrame com a questão sobre o meio de informação normalizada.
    """
    if 1987 <= ano <= 2004:
        validation = lambda x: x if x in {0, 1, 2, 3, 4, 5, 6} else pd.NA
        df["inform_meio"] = df["inform_meio"].map(validation)

    return df


def revistas_tipo(df, ano):
    """
    Normaliza a questão sobre o tipo de revistas.

    Parâmetros
    ----------
    df : DataFrame
        O DataFrame contendo os dados de perfil dos candidatos.
    ano : int
        O ano de referência para a normalização.

    Retorna
    -------
    DataFrame
        O DataFrame com a questão sobre o tipo de revistas normalizada.
    """
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
    """
    Normaliza a questão sobre a quantidade de geladeiras.

    Parâmetros
    ----------
    df : DataFrame
        O DataFrame contendo os dados de perfil dos candidatos.
    ano : int
        O ano de referência para a normalização.

    Retorna
    -------
    DataFrame
        O DataFrame com a questão sobre a quantidade de geladeiras normalizada.
    """
    if ano == 2004:
        df["geladeira"] = df["geladeira"].map({0: 0, 1: 2, 2: 1, 3: 1, 4: 1, 5: 1})
    elif ano >= 2020:
        df["geladeira"] = df["geladeira"].map({0: 0, 1: 1, 2: 1, 3: 1, 4: 1, 5: 2})

    return df


def freezer(df, ano):
    """
    Normaliza a questão sobre a quantidade de freezers.

    Parâmetros
    ----------
    df : DataFrame
        O DataFrame contendo os dados de perfil dos candidatos.
    ano : int
        O ano de referência para a normalização.

    Retorna
    -------
    DataFrame
        O DataFrame com a questão sobre a quantidade de freezers normalizada.
    """
    if ano == 2004:
        df["freezer"] = df["freezer"].map({0: 0, 1: 2, 2: 1, 3: 1, 4: 1, 5: 1})
    elif ano >= 2020:
        df["freezer"] = df["freezer"].map({0: 0, 1: 1, 2: 1, 3: 1, 4: 1, 5: 2})

    return df


def maq_roupa(df, ano):
    """
    Normaliza a questão sobre a quantidade de máquinas de lavar roupa.

    Parâmetros
    ----------
    df : DataFrame
        O DataFrame contendo os dados de perfil dos candidatos.
    ano : int
        O ano de referência para a normalização.

    Retorna
    -------
    DataFrame
        O DataFrame com a questão sobre a quantidade de máquinas de lavar roupa normalizada.
    """
    if ano == 2004:
        df["maq_roupa"] = df["maq_roupa"].map({0: 0, 1: 2, 2: 1, 3: 1, 4: 1, 5: 1})
    elif ano >= 2020:
        df["maq_roupa"] = df["maq_roupa"].map({0: 0, 1: 1, 2: 1, 3: 1, 4: 1, 5: 2})

    return df


def maq_louca(df, ano):
    """
    Normaliza a questão sobre a quantidade de máquinas de lavar louça.

    Parâmetros
    ----------
    df : DataFrame
        O DataFrame contendo os dados de perfil dos candidatos.
    ano : int
        O ano de referência para a normalização.

    Retorna
    -------
    DataFrame
        O DataFrame com a questão sobre a quantidade de máquinas de lavar louça normalizada.
    """
    if ano >= 2020:
        df["maq_louca"] = df["maq_louca"].map({0: 0, 1: 1, 2: 1, 3: 1, 4: 1, 5: 2})

    return df


def internet(df, ano):
    """
    Normaliza a questão sobre o acesso à internet.

    Parâmetros
    ----------
    df : DataFrame
        O DataFrame contendo os dados de perfil dos candidatos.
    ano : int
        O ano de referência para a normalização.

    Retorna
    -------
    DataFrame
        O DataFrame com a questão sobre o acesso à internet normalizada.
    """
    if ano == 2011 or ano == 2012:
        df["internet"] = df["internet"].map({0: 0, 1: 1, 2: 1, 3: 2})

    return df


def cozinha_qtas(df, ano):
    """
    Normaliza a questão sobre a quantidade de cozinhas.

    Parâmetros
    ----------
    df : DataFrame
        O DataFrame contendo os dados de perfil dos candidatos.
    ano : int
        O ano de referência para a normalização.

    Retorna
    -------
    DataFrame
        O DataFrame com a questão sobre a quantidade de cozinhas normalizada.
    """
    if ano == 2004:
        df["cozinha_qtas"] = df["cozinha_qtas"].map(
            {0: 0, 1: 5, 2: 1, 3: 2, 4: 3, 5: 4}
        )

    return df


def sala_qtas(df, ano):
    """
    Normaliza a questão sobre a quantidade de salas.

    Parâmetros
    ----------
    df : DataFrame
        O DataFrame contendo os dados de perfil dos candidatos.
    ano : int
        O ano de referência para a normalização.

    Retorna
    -------
    DataFrame
        O DataFrame com a questão sobre a quantidade de salas normalizada.
    """
    if ano == 2004:
        df["sala_qtas"] = df["sala_qtas"].map({0: 0, 1: 5, 2: 1, 3: 2, 4: 3, 5: 4})

    return df


def quarto_qts(df, ano):
    """
    Normaliza a questão sobre a quantidade de quartos.

    Parâmetros
    ----------
    df : DataFrame
        O DataFrame contendo os dados de perfil dos candidatos.
    ano : int
        O ano de referência para a normalização.

    Retorna
    -------
    DataFrame
        O DataFrame com a questão sobre a quantidade de quartos normalizada.
    """
    if ano == 2004:
        df["quarto_qts"] = df["quarto_qts"].map({0: 0, 1: 5, 2: 1, 3: 2, 4: 3, 5: 4})

    return df


def banheiro_qts(df, ano):
    """
    Normaliza a questão sobre a quantidade de banheiros.

    Parâmetros
    ----------
    df : DataFrame
        O DataFrame contendo os dados de perfil dos candidatos.
    ano : int
        O ano de referência para a normalização.

    Retorna
    -------
    DataFrame
        O DataFrame com a questão sobre a quantidade de banheiros normalizada.
    """
    if ano == 2004:
        df["banheiro_qts"] = df["banheiro_qts"].map(
            {0: 0, 1: 5, 2: 1, 3: 2, 4: 3, 5: 4}
        )

    return df


def radio_qts(df, ano):
    """
    Normaliza a questão sobre a quantidade de rádios.

    Parâmetros
    ----------
    df : DataFrame
        O DataFrame contendo os dados de perfil dos candidatos.
    ano : int
        O ano de referência para a normalização.

    Retorna
    -------
    DataFrame
        O DataFrame com a questão sobre a quantidade de rádios normalizada.
    """
    if ano == 2004:
        df["radio_qts"] = df["radio_qts"].map({0: 0, 1: 5, 2: 1, 3: 2, 4: 3, 5: 4})

    return df


def tv_qts(df, ano):
    """
    Normaliza a questão sobre a quantidade de televisores.

    Parâmetros
    ----------
    df : DataFrame
        O DataFrame contendo os dados de perfil dos candidatos.
    ano : int
        O ano de referência para a normalização.

    Retorna
    -------
    DataFrame
        O DataFrame com a questão sobre a quantidade de televisores normalizada.
    """
    if ano == 2004:
        df["tv_qts"] = df["tv_qts"].map({0: 0, 1: 5, 2: 1, 3: 2, 4: 3, 5: 4})

    return df


def dvd_vhs_qts(df, ano):
    """
    Normaliza a questão sobre a quantidade de aparelhos de DVD/VHS.

    Parâmetros
    ----------
    df : DataFrame
        O DataFrame contendo os dados de perfil dos candidatos.
    ano : int
        O ano de referência para a normalização.

    Retorna
    -------
    DataFrame
        O DataFrame com a questão sobre a quantidade de aparelhos de DVD/VHS normalizada.
    """
    if ano == 2004:
        df["dvd_vhs_qts"] = df["dvd_vhs_qts"].map({0: 0, 1: 5, 2: 1, 3: 2, 4: 3, 5: 4})

    df = df.loc[:, ~df.columns.duplicated()]

    return df


def computador_qtos(df, ano):
    """
    Normaliza a questão sobre a quantidade de computadores.

    Parâmetros
    ----------
    df : DataFrame
        O DataFrame contendo os dados de perfil dos candidatos.
    ano : int
        O ano de referência para a normalização.

    Retorna
    -------
    DataFrame
        O DataFrame com a questão sobre a quantidade de computadores normalizada.
    """
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
    """
    Normaliza a questão sobre a quantidade de carros.

    Parâmetros
    ----------
    df : DataFrame
        O DataFrame contendo os dados de perfil dos candidatos.
    ano : int
        O ano de referência para a normalização.

    Retorna
    -------
    DataFrame
        O DataFrame com a questão sobre a quantidade de carros normalizada.
    """
    if ano == 2004:
        df["carro_qtos"] = df["carro_qtos"].map({0: 0, 1: 5, 2: 1, 3: 2, 4: 3, 5: 4})

    return df


def aspirador(df, ano):
    """
    Normaliza a questão sobre a quantidade de aspiradores de pó.

    Parâmetros
    ----------
    df : DataFrame
        O DataFrame contendo os dados de perfil dos candidatos.
    ano : int
        O ano de referência para a normalização.

    Retorna
    -------
    DataFrame
        O DataFrame com a questão sobre a quantidade de aspiradores de pó normalizada.
    """
    if ano == 2004:
        df["aspirador"] = df["aspirador"].map({0: 0, 1: 2, 2: 1, 3: 1, 4: 1, 5: 1})

    return df


def jornal_le(df, ano):
    """
    Normaliza a questão sobre a leitura de jornais.

    Parâmetros
    ----------
    df : DataFrame
        O DataFrame contendo os dados de perfil dos candidatos.
    ano : int
        O ano de referência para a normalização.

    Retorna
    -------
    DataFrame
        O DataFrame com a questão sobre a leitura de jornais normalizada.
    """
    if 1987 <= ano <= 2019:
        validation = lambda x: x if x in {0, 1, 2, 3, 4} else pd.NA
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
    df = reprovacao_em(df, ano)
    df = cursinho(df, ano)
    df = cursinho_motivo(df, ano)
    df = cursinho_tempo(df, ano)
    df = curso_interesse(df, ano)
    df = vest_primeiro(df, ano)
    df = vest_qts_inst(df, ano)
    df = univ_outra(df, ano)
    df = disciplina_favorita(df, ano)
    df = opc1_escolha(df, ano)
    df = opcao1_motivo(df, ano)
    df = unicamp_motivo(df, ano)
    df = idiomas(df, ano)
    df = idiomas_familia(df, ano)
    df = idioma_vest_escolha(df, ano)

    df = situacao_pais(df, ano)
    df = subordinados_mae(df, ano)
    df = educacao_pais(df, ano)
    df = ocupacao_pais(df, ano)
    df = trabalha_pais(df, ano)
    df = opiniao_pais(df, ano)

    df = trabalha(df, ano)
    df = contribui_renda_fam(df, ano)
    df = renda_sm(df, ano)
    df = renda_contrib_qtas(df, ano)

    df = ativ_extra_quais(df, ano)
    df = ativ_extra_principal(df, ano)
    df = leitura_tipo(df, ano)
    df = inform_meio(df, ano)
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
