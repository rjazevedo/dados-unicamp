import yaml
import pandas as pd
from pathlib import Path

stream = open("estabelecimento/configuration.yaml")
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


def list_dirs_estabelecimento_input():
    path = Path(config["path_input"])
    return [f for f in path.iterdir() if f.is_dir()]


def read_estabelecimento(path):
    cols = [
        "cnpj_basico",
        "cnpj_ordem",
        "cnpj_dv",
        "identificador_matriz_filial",
        "nome_fantasia",
        "situacao_cadastral",
        "data_situacao_cadastral",
        "motivo_situacao_cadastral",
        "nome_cidade_exterior",
        "pais",
        "data_inicio_atividade",
        "cnae_fiscal_principal",
        "cnae_fiscal_secundaria",
        "descricao_tipo_logradouro",
        "logradouro",
        "numero_logradouro",
        "complemento_logradouro",
        "bairro",
        "cep",
        "uf",
        "codigo_municipio",
        "ddd_telefone_1",
        "num_telefone_1",
        "ddd_telefone_2",
        "num_telefone_2",
        "ddd_fax",
        "num_fax",
        "correio_eletronico",
        "situacao_especial",
        "data_situacao_especial",
    ]
    dtypes = {
        "cnpj_basico": "string",
        "cnpj_ordem": "string",
        "cnpj_dv": "string",
        "identificador_matriz_filial": "Int64",
        "nome_fantasia": "string",
        "situacao_cadastral": "Int64",
        "data_situacao_cadastral": "string",
        "motivo_situacao_cadastral": "Int64",
        "data_inicio_atividade": "string",
        "cnae_fiscal_principal": "string",
        "cnae_fiscal_secundaria": "string",
        "cep": "string",
        "uf": "string",
        "codigo_municipio": "Int64",
    }
    return pd.read_csv(
        path, sep=";", names=cols, encoding="latin", dtype=dtypes, low_memory=False
    )


def write_estabelecimento_amostra(df):
    path = Path(config["path_output"]) / "estabelecimento_amostra.csv"
    df.to_csv(path, sep=";", index=False)
