from pathlib import Path
import pandas as pd
import yaml
import os
import subprocess

from socio.utilities.dtype import get_dtype

from socio.database_information.socio import get_columns_info_socio

stream = open("socio/configuration.yaml")
config = yaml.safe_load(stream)


def read_ids():
    file = config["database_ids"]
    dtype = {"nome": "string", "cpf": "string", "id": "Int64"}
    df = pd.read_csv(file, dtype=dtype, sep=",", low_memory=False)
    return df


def read_socio_original(path, date):
    columns_info = get_columns_info_socio()

    if int(date[0:4]) >= 2022:
        columns = [
            "cnpj",
            "codigo_tipo_socio",
            "nome_socio",
            "cnpj_cpf_do_socio",
            "codigo_qualificacao_socio",
            "data_entrada_sociedade",
            "pais",
            "cpf_representante_legal",
            "nome_representante_legal",
            "codigo_qualificacao_representante_legal",
            "faixa_etaria",
        ]
        return read_database(
            path, columns_info, cols=columns, sep=";", encoding="latin"
        )

    else:
        return read_database(path, columns_info)


def read_socio_clean(path):
    return pd.read_parquet(path)


def write_socio(df):
    file = config["path_output"] + "socio.csv"
    write_database(df, file)


def write_socio_sample(df):
    file = config["path_output"] + "socio_amostra.csv"
    write_database(df, file)


def write_socio_tmp(df, filename, date):
    file = Path(config["path_output"] + "tmp/" + date + "/" + filename)
    file = file.with_suffix(".parquet")
    df.to_parquet(file, compression="brotli")


def write_socio_merges(df, filename, date):
    file = Path(config["path_output"] + "merges/" + date + "/" + filename)
    file = file.with_suffix(".parquet")
    df.to_parquet(file, compression="brotli")


def write_estabelecimento_tmp(df, filename, date):
    file = config["database_output"] + "tmp/" + date + "/" + filename
    write_database(df, file)


# ------------------------------------------------------------------------------------------------
def read_database(
    file,
    columns_info,
    is_original=True,
    low_memory=True,
    sep=",",
    cols=None,
    encoding=None,
    date=None,
):
    dtype = get_dtype(columns_info, is_original=is_original)
    dtype["cnpj_empresa"] = str
    dtype["cpf_cnpj_socio"] = str

    df = pd.read_csv(
        file,
        dtype=dtype,
        low_memory=low_memory,
        sep=sep,
        encoding=encoding,
        on_bad_lines="warn",
        names=cols,
    )
    return df


def write_database(df, file):
    df.to_csv(file, index=False, sep=";")


# -------------------------------------------------------------------------------------------------
def create_folder_socio_tmp():
    path = config["path_output"]
    create_folder(path, "tmp")


def create_folder_socio_tmp_date(year):
    path = config["path_output"] + "tmp/"
    create_folder(path, str(year))


def create_folder_merges():
    path = config["path_output"]
    create_folder(path, "merges")


def create_folder_merges_date(date):
    path = config["path_output"] + "merges/"
    create_folder(path, str(date))


def create_folder(path, folder_name):
    command = "mkdir -p " + path + folder_name
    subprocess.run(command, shell=True)


def get_all_files(path):
    return [f.path for f in os.scandir(path) if f.is_file()]


def list_dirs_socio_input():
    return [f.path for f in os.scandir(config["path_socio"]) if f.is_dir()]


def list_dirs_socio_output_tmp():
    return [f.path for f in os.scandir(config["path_output"] + "tmp/") if f.is_dir()]


def list_dirs_socio_output_merges():
    return [f.path for f in os.scandir(config["path_output"] + "merges/") if f.is_dir()]
