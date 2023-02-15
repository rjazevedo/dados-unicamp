import pandas as pd
from unidecode import unidecode
from unesp.utilities.io import (
    list_dirs_unesp_input,
    get_all_files,
    read_ids,
    read_unesp,
    write_unesp_amostra,
)


def extract_unesp():
    list_dirs = list_dirs_unesp_input()
    list_dirs = sorted(list_dirs)

    ids = read_ids()
    ids = ids.loc[
        :, ["ano_ingresso_curso", "nome", "id", "origem_cpf"]
    ].drop_duplicates()
    ids.nome = ids.nome.apply(clean_name)
    merged_list = []

    for dir in list_dirs:
        extract_unesp_year(dir, ids, merged_list)

    amostra = pd.concat(merged_list)
    amostra = amostra.drop(columns=["nome", "_merge", "ano_ingresso_curso", "nome_unesp"])
    amostra = amostra.drop_duplicates()
    amostra.id = amostra.id.astype("int64")
    amostra.origem_cpf = amostra.origem_cpf.astype("int64")
    amostra.aprovado_unesp = 1
    write_unesp_amostra(amostra)


def extract_unesp_year(dir, ids, merged_list):
    year = dir.parts[-1][-4:]
    print(f"Extraindo dados da Unesp do ano {year}")
    files = sorted(get_all_files(dir))
    chamadas_l = []
    for file in files:
        df = read_unesp(file)
        chamadas_l.append(df)

    unesp = pd.concat(chamadas_l)
    unesp = unesp.drop_duplicates()
    unesp.nome_unesp = unesp.nome_unesp.apply(clean_name)

    merged = unesp.merge(
        ids,
        how="left",
        left_on=["nome_unesp", "ano_vest_unesp"],
        right_on=["nome", "ano_ingresso_curso"],
        indicator=True,
    )

    mask = merged.duplicated(subset=unesp.columns, keep=False)

    # Todas as tuplas que deram match unico
    merged = merged.loc[(~mask) & (merged._merge == "both"), :]

    merged_list.append(merged)


def clean_name(name):
    if pd.isnull(name):
        return ""
    else:
        x = unidecode(name).upper().strip()
        return " ".join(x.split())
