from empresa.utils import (
    list_dirs_empresa_input,
    read_empresa,
    read_socio_amostra,
    write_empresa_amostra,
)
import pandas as pd


def extract_empresa_amostra():
    empresa_folders = list_dirs_empresa_input()
    folder = sorted(empresa_folders)[-1]

    socio_amostra = read_socio_amostra()
    socio_amostra["cnpj_basico"] = socio_amostra.cnpj.str[0:8]
    socio_amostra = socio_amostra.drop_duplicates(subset="cnpj_basico").loc[
        :, "cnpj_basico"
    ]

    empresa_merges = []
    for f in [f for f in folder.iterdir() if f.is_file()]:
        print(f"Reading file {f.name}")
        empresa = read_empresa(f)
        print(f"Merging file {f.name} with socios.")
        empresa_merge = empresa.merge(socio_amostra, how="inner", on="cnpj_basico")
        empresa_merge = empresa_merge.loc[:, empresa.columns]
        empresa_merges.append(empresa_merge.copy())

    empresa_amostra = pd.concat(empresa_merges)
    empresa_amostra.capital_social = empresa_amostra.capital_social.str.replace(
        ",", "."
    ).astype("float64")

    write_empresa_amostra(empresa_amostra)
