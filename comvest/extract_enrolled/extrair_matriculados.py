"""
Módulo para extração de dados dos matriculados Comvest.

Este módulo contém funções para extrair e processar dados dos matriculados nos exames Comvest.

Funções:
- cleandata(df, date): Realiza a limpeza dos dados dos matriculados.
- validacao_curso(df, date): Valida os códigos dos cursos dos matriculados.
- extraction(): Executa a extração e processamento dos dados dos matriculados Comvest.

Como usar:
Implemente e execute as funções para realizar a extração e processamento dos dados dos matriculados Comvest.
"""


import logging
import pandas as pd
from comvest.utilities.io import files, read_from_db, read_result, write_result
from comvest.utilities.logging import progresslog, resultlog


def cleandata(df, date):
    """
    Realiza a limpeza dos dados dos matriculados.

    Parâmetros
    ----------
    df : DataFrame
        O DataFrame contendo os dados dos matriculados.
    date : int
        O ano do exame Comvest.

    Retorna
    -------
    DataFrame
        O DataFrame contendo os dados dos matriculados limpos.
    """
    df.insert(loc=0, column="ano_vest", value=date)
    df.drop("nome", axis=1, errors="ignore", inplace=True)
    df = df.iloc[:, 0:3]
    df.columns = ["ano_vest", "insc_vest", "curso_matric"]
    df["insc_vest"] = pd.to_numeric(
        df["insc_vest"], errors="coerce", downcast="integer"
    ).astype("Int64")
    df.dropna(inplace=True)

    return df


def validacao_curso(df, date):
    """
    Valida os códigos dos cursos dos matriculados.

    Parâmetros
    ----------
    df : DataFrame
        O DataFrame contendo os dados dos matriculados.
    date : int
        O ano do exame Comvest.

    Retorna
    -------
    DataFrame
        O DataFrame contendo os dados dos matriculados com códigos de cursos validados.
    """
    df_cursos = read_result("cursos.csv")
    cursos = df_cursos.loc[df_cursos["ano_vest"] == date]["cod_curso"].tolist()

    # Codigos que nao constam na lista de cursos serao remapeados para missing
    df["curso_matric"] = df["curso_matric"].fillna(-1)
    df["curso_matric"] = df["curso_matric"].map(
        lambda cod: int(cod) if int(cod) in cursos else pd.NA
    )
    df["curso_matric"] = pd.to_numeric(df["curso_matric"], errors="coerce").astype(
        "Int64"
    )
    df.dropna(subset=["curso_matric"], inplace=True)

    return df


def extraction():
    """
    Executa a extração e processamento dos dados dos matriculados Comvest.

    Esta função lê os dados dos matriculados de diferentes anos, realiza a limpeza e validação dos dados e os concatena em um único DataFrame.

    Retorna
    -------
    None
    """
    matriculados_frames = []

    for path, date in files.items():
        if "Profis" in path:
            continue
        
        elif date == 2023:
            matriculados = read_from_db(path, sheet_name="matriculados_final")
            matriculados = matriculados.drop(columns=["CPF", "nome"])
        
        else:
            matriculados = read_from_db(path, sheet_name="matriculados")
        
        print(f"Processando os matriculados para o ano {date}...")
        progresslog("matriculados", date)

        matriculados = cleandata(matriculados, date)
        matriculados = validacao_curso(matriculados, date)
        matriculados_frames.append(matriculados)

    # Exportar CSV
    all_matriculados = pd.concat(matriculados_frames)
    all_matriculados.sort_values(by="ano_vest", ascending=False, inplace=True)

    FILE_NAME = "matriculados_comvest.csv"
    write_result(all_matriculados, FILE_NAME)
    resultlog(FILE_NAME)
