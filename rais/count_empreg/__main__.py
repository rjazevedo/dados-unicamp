import pandas as pd
import yaml
import os

# Obtém o caminho absoluto do diretório onde o script está localizado
base_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(base_dir, "configuration.yaml")
from rais.utilities.file import get_all_files
from rais.utilities.rais_information import get_column

# Abre o arquivo de configuração
stream = open(config_path)
config = yaml.safe_load(stream)
intervalo = [2002, 2022]

# Merge rais from year with df_dac_comvest
def count_empreg_year(year):
    path = config["path_output_data"] + "pre_processed/" + str(year) + "/"
    files = get_all_files(path, "parquet")
    dfs = []
    for file_rais in files:
        df_rais = pd.read_parquet(
            file_rais, 
            dtype_backend="pyarrow",
            columns=[
                "ano_base",
                get_column("cnpj", year),
                "pispasep",
                "cpf_r",
                get_column("estbl_tamanho", year)
            ]
        )
        df_rais.columns = [
            "ano_base",
            "cnpj",
            "pispasep",
            "cpf",
            "estbl_tamanho"
        ]

        # Contar CPFs únicos por CNPJ
        cpfs_unicos = df_rais.groupby("cnpj")["cpf"].nunique().reset_index(name="cpfs")

        # Contar PIS/PASEPs únicos por CNPJ
        pispaseps_unicos = df_rais.groupby("cnpj")["pispasep"].nunique().reset_index(name="pispaseps")

        df_rais = df_rais.merge(cpfs_unicos[["cnpj", "cpfs"]], on="cnpj", how="left")
        df_rais = df_rais.merge(pispaseps_unicos[["cnpj", "pispaseps"]], on="cnpj", how="left")
        df_rais = df_rais.drop(columns=["cpf", "pispasep"], errors='ignore')
        df_rais = df_rais.drop_duplicates(keep="first")

        dfs.append(
            df_rais
        )
    df_result = pd.concat(dfs, sort=False)
    return df_result


def count_empreg():
    dfs = []
    for year in range(intervalo[0], intervalo[1] + 1):
        print(f"Merging year {year}")
        df = count_empreg_year(year)
        dfs.append(df)

    df_result = pd.concat(dfs)
    df_result = df_result.drop(columns=["cpf"], errors='ignore')
    df_result.to_csv(config["path_output_data"] + "empreg_rais.csv", index=False)