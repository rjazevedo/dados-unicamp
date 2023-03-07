import yaml
import pandas as pd
from pathlib import Path

stream = open("simples/configuration.yaml")
config = yaml.safe_load(stream)


def list_dirs_simples_input():
    path = Path(config["path_input"])
    return [f for f in path.iterdir() if f.is_dir()]


def read_simples(path):
    cols = [
        "cnpj_basico",
        "opcao_pelo_simples",
        "data_opcao_pelo_simples",
        "data_exclusao_do_simples",
        "opcao_pelo_mei",
        "data_opcao_pelo_mei",
        "data_exclusao_do_mei",
    ]
    dtypes = {
        "cnpj_basico": "string",
        "opcao_pelo_simples": "string",
        "data_opcao_pelo_simples": "string",
        "data_exclusao_do_simples": "string",
        "opcao_pelo_mei": "string",
        "data_opcao_pelo_mei": "string",
        "data_exclusao_do_mei": "string",
    }
    return pd.read_csv(path, sep=";", names=cols, dtype=dtypes)


def write_simples_amostra(df):
    path = Path(config["path_output"]) / "simples_amostra.csv"
    df.to_csv(path, sep=";", index=False)
