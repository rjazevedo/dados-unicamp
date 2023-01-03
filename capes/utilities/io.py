import pandas as pd
import yaml
import os

from capes.utilities.capes_information import get_capes_clean_dtypes

stream = open("capes/configuration.yaml")
config = yaml.safe_load(stream)


def get_all_files(path):
    return [f.path for f in os.scandir(path) if f.is_file()]


def list_dirs_capes_input():
    return [f.path for f in os.scandir(config["path_input"]) if f.is_dir()]


def list_dirs_capes_tmp():
    return [f.path for f in os.scandir(config["path_output"] + "tmp/") if f.is_dir()]


def create_folder_capes_tmp_date(year):
    path = config["path_output"] + "tmp/"
    create_folder(path, str(year))


def create_folder_capes_tmp():
    path = config["path_output"]
    create_folder(path, "tmp")


def create_folder(path, folder_name):
    os.makedirs(path + folder_name, exist_ok=True)


def read_ids():
    file = config["database_ids"]
    dtype = {
        "nome": str,
        "cpf": str,
        "origem_cpf": "Int32",
        "id": "Int64",
        "dta_nasc": str,
        "doc": str,
    }

    df = pd.read_csv(
        file,
        dtype=dtype,
        sep=",",
        low_memory=False,
        usecols=["nome", "cpf", "origem_cpf", "id", "dta_nasc", "doc"],
    )
    return df


def read_capes_clean(file):
    dtype = get_capes_clean_dtypes()
    return read_database(file, dtype=dtype)


def read_capes_original(file):
    df = pd.read_csv(file, sep=";", encoding="latin-1", low_memory=False)
    return df


def read_database(file, dtype={}):
    df = pd.read_csv(file, dtype=dtype, sep=";", low_memory=False)
    return df


def write_database(df, file, date):
    path = config["path_output"] + "tmp/" + date + "/" + file.split("/")[-1]
    df.to_csv(path, sep=";", index=False)


def write_sample(df):
    path = config["path_output"]
    df.to_csv(path, sep=";", index=False)
