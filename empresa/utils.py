import yaml
import pandas as pd
from pathlib import Path

stream = open("empresa/configuration.yaml")
config = yaml.safe_load(stream)


def read_socio_amostra():
    path = Path(config["path_socio"])
    return pd.read_csv(
        path,
        sep=";",
        low_memory=False,
        dtype={
            "codigo_tipo_socio": "Int8",
            "cnpj": "string",
            "data_entrada_sociedade": "string",
            "data_coleta": "string",
            "id": "int64",
            "origem_cpf": "int8",
            "faixa_etaria": "Int8",
            "qualificacao_socio": "string",
            "tipo_socio": "string",
            "pais": "Int32",
        },
    )


def list_dirs_empresa_input():
    path = Path(config["path_input"])
    return [f for f in path.iterdir() if f.is_dir()]


def read_empresa(path):
    cols = [
        "cnpj_basico",
        "razao_social",
        "codigo_natureza_juridica",
        "qualificao_responsavel",
        "capital_social",
        "porte_empresa",
        "ente_federativo",
    ]
    dtypes = {
        "cnpj_basico": "string",
        "razao_social": "string",
        "porte_empresa": "Int8",
        "ente_federativo": "string",
    }
    return pd.read_csv(path, sep=";", names=cols, encoding="latin", dtype=dtypes)


def write_empresa_amostra(df):
    path = Path(config["path_output"]) / "empresa_amostra.csv"
    df.to_csv(path, sep=";", index=False)
