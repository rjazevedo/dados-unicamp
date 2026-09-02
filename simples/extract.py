from simples.utils import (
    list_dirs_simples_input,
    read_simples,
    write_simples_amostra,
)
import pandas as pd


def most_recent_non_empty_folder(folders):
    for folder in sorted(folders, reverse=True):
        if any(f.is_file() for f in folder.iterdir()):
            return folder
        print(f"AVISO: pasta '{folder}' esta vazia, pulando para a proxima mais recente")
    raise FileNotFoundError(
        f"Nenhuma pasta com arquivos encontrada entre: {sorted(folders, reverse=True)}"
    )


def extract_simples_amostra():
    simples_folders = list_dirs_simples_input()
    # A extração é feita sempre com os dados mais recentes (pula pastas vazias)
    folder = most_recent_non_empty_folder(simples_folders)

    simples_merges = []
    for f in [f for f in folder.iterdir() if f.is_file()]:
        print(f"Reading file {f.name}")
        simples = read_simples(f)
        simples.data_opcao_pelo_simples = simples.data_opcao_pelo_simples.replace(
            "0" * 8, pd.NA
        )
        simples.data_opcao_pelo_mei = simples.data_opcao_pelo_mei.replace(
            "0" * 8, pd.NA
        )
        simples.data_exclusao_do_mei = simples.data_exclusao_do_mei.replace(
            "0" * 8, pd.NA
        )
        simples.data_exclusao_do_simples = simples.data_exclusao_do_simples.replace(
            "0" * 8, pd.NA
        )
        simples_merges.append(simples.copy())

    simples_amostra = pd.concat(simples_merges)

    write_simples_amostra(simples_amostra)
