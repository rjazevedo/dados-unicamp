import pandas as pd
import yaml
import os
import subprocess
import glob

from socio.utilities.dtype import get_dtype

from socio.database_information.socio import get_columns_info_socio
from socio.database_information.empresa import get_columns_info_empresa
from socio.database_information.cnae_secundaria import get_columns_info_cnae_secundaria

stream = open("socio/configuration.yaml")
config = yaml.safe_load(stream)


def read_ids():
    file = config["database_ids"]
    dtype = {"nome": "object", "cpf": "object", "id": "Int64"}
    df = pd.read_csv(file, dtype=dtype, sep=";", low_memory=False)
    return df


# ------------------------------------------------------------------------------------------------
def read_socio_original(path):
    columns_info = get_columns_info_socio()
    return read_database(path, columns_info)


def read_empresa_original(file):
    columns_info = get_columns_info_empresa()
    dtype = get_dtype(columns_info, True)
    cols = [col for col in columns_info]
    df = pd.read_csv(
        file,
        dtype=dtype,
        low_memory=False,
        sep=",",
        encoding="latin",
        warn_bad_lines=True,
        error_bad_lines=False,
    )
    return df


def read_cnae_original():
    file = config["database_cnae"]
    dtype = {0: "object", 1: "object"}
    df = pd.read_csv(file, dtype=dtype, header=None)
    df = rename_columns_cnae(df)
    return df


# ------------------------------------------------------------------------------------------------
def read_socio_clean(path):
    columns_info = get_columns_info_socio()
    return read_database(path, columns_info, is_original=False)


def read_empresa_clean():
    file = config["path_output"] + "empresa.csv"
    columns_info = get_columns_info_empresa()
    df = read_database(file, columns_info, is_original=False)
    return df


def read_cnae_clean():
    file = config["path_output"] + "cnae_secundaria.csv"
    columns_info = get_columns_info_cnae_secundaria()
    df = read_database(file, columns_info, is_original=False)
    return df


# ------------------------------------------------------------------------------------------------
def write_socio(df):
    file = config["path_output"] + "socio.csv"
    write_database(df, file)


def write_empresa(df):
    file = config["path_output"] + "empresa.csv"
    write_database(df, file)


def write_cnae(df):
    file = config["path_output"] + "cnae_secundaria.csv"
    write_database(df, file)


def write_socio_sample(df):
    file = config["path_output"] + "socio_amostra.csv"
    write_database(df, file)


def write_socio_tmp(df, filename, date):
    file = config["path_output"] + "tmp/" + date + "/" + filename
    write_database(df, file)


# ------------------------------------------------------------------------------------------------
def read_database(file, columns_info, is_original=True, low_memory=True):
    dtype = get_dtype(columns_info, is_original=is_original)
    df = pd.read_csv(
        file,
        dtype=dtype,
        low_memory=low_memory,
        sep=";",
        encoding="latin",
        warn_bad_lines=True,
        error_bad_lines=False,
    )
    return df


def rename_columns_cnae(df):
    df["cnpj"] = df[0]
    df["cnae"] = df[1]
    df = df.loc[:, ["cnpj", "cnae"]]
    return df


def write_database(df, file):
    df.to_csv(file, index=False, sep=";")


# -------------------------------------------------------------------------------------------------
def create_folder_socio_tmp():
    path = config["path_output"]
    create_folder(path, "tmp")


def create_folder_empresa_tmp():
    path = config["database_output"]
    create_folder(path, "tmp")


def create_folder_socio_tmp_date(year):
    path = config["path_output"] + "tmp/"
    create_folder(path, str(year))


def create_folder_empresa_tmp_date(year):
    path = config["database_output"] + "tmp/"
    create_folder(path, str(year))


def create_folder_merges():
    path = config["path_output"]
    create_folder(path, "merges")


def create_folder_merges_date(year):
    path = config["path_output"] + "merges/"
    create_folder(path, str(year))


def create_folder(path, folder_name):
    command = "mkdir -p " + path + folder_name
    subprocess.run(command, shell=True)


def get_all_files(path):
    return [f.path for f in os.scandir(path) if f.is_file()]


def list_dirs_socio_input():
    return [f.path for f in os.scandir(config["path_socio"]) if f.is_dir()]


def list_dirs_empresa_input():
    return [f.path for f in os.scandir(config["path_socio"]) if f.is_dir()]


def list_dirs_socio_output():
    return [f.path for f in os.scandir(config["path_output"] + "tmp/") if f.is_dir()]
