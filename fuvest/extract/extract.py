import pandas as pd
from unidecode import unidecode
from fuvest.utilities.io import (
    list_dirs_fuvest_input,
    get_all_files,
    read_ids,
    read_fuvest,
    write_fuvest_amostra,
)


def extract_fuvest():
    list_dirs = list_dirs_fuvest_input()
    list_dirs = sorted(list_dirs)

    ids = read_ids()
    ids = ids.loc[
        :, ["ano_ingresso_curso", "nome", "id", "origem_cpf"]
    ].drop_duplicates()
    ids.nome = ids.nome.apply(clean_name)
    merged_list = []

    for dir in list_dirs:
        extract_fuvest_year(dir, ids, merged_list)

    amostra = pd.concat(merged_list)
    amostra = amostra.drop(
        columns=["nome", "_merge", "ano_ingresso_curso", "nome_fuv", "numero_fuv"]
    )
    amostra = amostra.drop_duplicates()
    amostra.id = amostra.id.astype("int64")
    amostra.origem_cpf = amostra.origem_cpf.astype("int64")
    write_fuvest_amostra(amostra)


def extract_fuvest_year(dir, ids, merged_list):
    year = dir.parts[-1][-4:]
    print(f"Extraindo dados da Fuvest do ano {year}")
    files = sorted(get_all_files(dir))
    chamadas_l = []
    for file in files:
        filename = file.parts[-1]
        chamada = filename.split(".")[0].split("_")[-1]
        df = read_fuvest(file)
        df["chamada_fuv"] = int(chamada)
        chamadas_l.append(df)

    fuv = pd.concat(chamadas_l)
    fuv = fuv.drop_duplicates()
    fuv.nome_fuv = fuv.nome_fuv.apply(clean_name)
    fuv["ano_vest_fuv"] = int(year)

    merged = fuv.merge(
        ids,
        how="left",
        left_on=["nome_fuv", "ano_vest_fuv"],
        right_on=["nome", "ano_ingresso_curso"],
        indicator=True,
    )

    mask = merged.duplicated(subset=fuv.columns, keep=False)

    # Todas as tuplas que deram match unico
    merged = merged.loc[(~mask) & (merged._merge == "both"), :]

    merged_list.append(merged)


def clean_name(name):
    if pd.isnull(name):
        return ""
    else:
        x = unidecode(name).upper().strip()
        return " ".join(x.split())
