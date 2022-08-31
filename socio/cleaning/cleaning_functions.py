import pandas as pd
import numpy as np


def clear_nome(value):
    if (
        value == "Cpf Nao Consta Na Base-Cpf"
        or value == "!"
        or value == "nan"
        or value == "NaN"
        or pd.isnull(value)
    ):
        return ""
    return value


def clear_cnpj_cpf(value):
    if value == "99999999999999" or pd.isnull(value):
        return ""
    return value


def clean_cnpj(value):
    if pd.isnull(value):
        return ""
    return value.zfill(14)


def clear_codigo_qualificacao(value):
    if value == 0:
        return np.nan
    return value


def clear_data(value):
    # Na tabela de 2022-03-12 os dados da coluna 'data_entrada_sociedade' são da forma YYYYMMDD enquanto pras outras datas
    # os dados são da forma YYYY-MM-DD
    return value.replace("-", "")


def clear_cpf(value):
    if value == "00000000000":
        return ""
    return value


def clear_motivo_situacao_cadastral(value):
    if value == 0:
        return np.nan
    return value


def clear_codigo_natureza_juridica(value):
    if value == "8885":
        return ""
    return value


def clear_cnae_fiscal(value):
    if value == "8888888":
        return ""
    return value.zfill(7)


def clear_cep(value):
    if value == "0":
        return ""


def clear_id_municipio_rf(value):
    return value.zfill(4)
