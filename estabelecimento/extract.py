from estabelecimento.utils import (
    list_dirs_estabelecimento_input,
    read_estabelecimento,
    read_socio_amostra,
    write_estabelecimento_amostra,
)
import pandas as pd


def extract_estabelecimento_amostra():
    estabelecimentos_folders = list_dirs_estabelecimento_input()
    folder = sorted(estabelecimentos_folders)[-1]

    socio_amostra = read_socio_amostra()
    socio_amostra["cnpj_basico"] = socio_amostra.cnpj.str[0:8]
    socio_amostra = socio_amostra.drop_duplicates(subset="cnpj_basico").loc[
        :, "cnpj_basico"
    ]

    cols = [
        "cnpj_basico",
        "cnpj_ordem",
        "cnpj_dv",
        "identificador_matriz_filial",
        "nome_fantasia",
        "situacao_cadastral",
        "data_situacao_cadastral",
        "motivo_situacao_cadastral",
        "data_inicio_atividade",
        "cnae_fiscal_principal",
        "cnae_fiscal_secundaria",
        "cep",
        "uf",
        "codigo_municipio",
    ]

    estab_merges = []
    for f in [f for f in folder.iterdir() if f.is_file()]:
        print(f"Reading file {f.name}")
        estab = read_estabelecimento(f)
        estab = estab.loc[:, cols]
        estab_merge = estab.merge(socio_amostra, how="inner", on="cnpj_basico")
        print(f"Merging file {f.name} with socios.")
        estab_merge = estab.merge(socio_amostra, how="inner", on="cnpj_basico")
        estab_merge = estab_merge.loc[:, cols]
        estab_merges.append(estab_merge.copy())

    estab_amostra = pd.concat(estab_merges)
    write_estabelecimento_amostra(estab_amostra)
