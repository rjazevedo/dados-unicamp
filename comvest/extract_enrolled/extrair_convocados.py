"""
Módulo para extração de dados dos convocados Comvest.

Este módulo contém a função principal para extrair e processar dados dos convocados nos exames Comvest.

Funções:
- extraction(): Executa a extração e processamento dos dados dos convocados Comvest.

Como usar:
Implemente e execute a função para realizar a extração e processamento dos dados dos convocados Comvest.
"""


import pandas as pd
from comvest.utilities.io import (
    files,
    read_auxiliary,
    read_result,
    write_result,
    read_from_db,
)


def extraction():
    """
    Executa a extração e processamento dos dados dos convocados Comvest.

    Esta função lê os dados dos convocados de diferentes anos, realiza a limpeza dos dados e os concatena em um único DataFrame.

    Retorna
    -------
    None
    """
    convocados_frames = []

    for path, date in files.items():
        if "Profis" in path:
            continue
        
        try:
            if date in (2023, 2024):
                convocados = read_from_db(path, sheet_name="convocados_matriculados")
            else:
                convocados = read_from_db(path, sheet_name="convocadosMatriculados")
                
            convocados_frames.append(convocados)
        except:
            pass
    
        print(f"Extraindo os convocados para o ano {date}...")
    
    convocados_file = read_auxiliary(
        "ConvocadosMatriculadosLista87a21.xlsx",
        dtype={"ano": "Int64", "insc": "Int64", "curso": "Int64", "lista": "Int64"},
    )

    convocados_frames.append(convocados_file)

    convocados = pd.concat(convocados_frames)

    matriculados = read_result(
        "matriculados_comvest.csv",
        dtype={"curso_matric": "Int64", "insc_vest": "Int64"},
    )

    convocados.rename(
        columns={
            "ano": "ano_vest",
            "insc": "insc_vest",
            "curso": "curso_convocado",
            "convocado": "convoc",
            "matrfim": "matric",
            "lista": "chamada_vest",
        },
        inplace=True,
    )

    convocados["insc_vest"] = convocados.apply(
        lambda row: int(str(row["ano_vest"])[-1] + str(row["insc_vest"]))
        if row["ano_vest"] in [2002, 2003]
        else int(row["insc_vest"]),
        axis=1,
    )

    convocados = convocados.merge(
        matriculados, on=["ano_vest", "insc_vest"], how="outer"
    )
    convocados.sort_values(by="ano_vest", ascending=False, inplace=True)
    convocados.drop_duplicates(subset=["ano_vest", "insc_vest"], inplace=True)

    FILE_NAME = "matriculados_comvest.csv"
    write_result(convocados, FILE_NAME)
