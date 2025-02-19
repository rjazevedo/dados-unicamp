import pandas as pd
import yaml

from rais.utilities.dtypes import get_dtype_rais_original
from rais.utilities.dtypes import get_dtype_dac_comvest
from rais.utilities.dtypes import get_dtype_rais_clean
from rais.utilities.file import get_file_name
from rais.utilities.file import get_extension

stream = open("rais/configuration.yaml")
config = yaml.safe_load(stream)


def read_rais_original(file, year):
    dtype = get_dtype_rais_original(year)
    return read_database(file, dtype)


def read_rais_identification(file):
    columns = ["nome_r", "cpf_r", "dta_nasc_r", "pispasep", "mun_estbl", "ano_base"]
    df = pd.read_parquet(file, dtype_backend="pyarrow", columns=columns)
    return df


def read_rais_merge(file):
    dtype = get_dtype_rais_clean()
    df = pd.read_csv(file, sep=";", dtype=dtype, index_col="index")
    return df


def read_rais_merge_by_identification(file_identification, year):
    path = config["path_output_data"] + "tmp/" + str(year) + "/rais_dac_comvest/"
    file_name = get_file_name(file_identification)
    file = path + file_name + ".csv"
    dtype = get_dtype_rais_clean()
    df = pd.read_csv(file, sep=";", dtype=dtype, index_col="index")
    return df


def read_rais_original_pre_processed(file_merge, year):
    path = config["path_pre_processed"] + str(year) + "/"
    file_name = get_file_name(file_merge)
    file = path + file_name + ".parquet"
    df = read_database_pre_processed(file)
    return df


def read_rais_clean(file):
    dtype = get_dtype_rais_clean()
    df = pd.read_csv(file, sep=";", dtype=dtype, index_col=0)
    return df


def read_rais_sample():
    file = config["path_output_data"] + "rais_amostra.csv"
    dtype = get_dtype_rais_clean()
    df = pd.read_csv(file, sep=";", dtype=dtype)
    return df


# ------------------------------------------------------------------------------------------------
def read_dac_comvest():
    file = config["uniao_dac_comvest"]
    dtype = get_dtype_dac_comvest()
    df = pd.read_csv(file, sep=",", dtype=dtype)
    return df


def read_dac_comvest_valid():
    file = config["path_output_data"] + "tmp/uniao_dac_comvest_valid.csv"
    dtype = get_dtype_dac_comvest()
    df = pd.read_csv(file, sep=",", dtype=dtype)
    return df


def read_dac_comvest_recovered():
    file = config["path_output_data"] + "tmp/uniao_dac_comvest_recovered.csv"
    dtype = get_dtype_dac_comvest()
    df = pd.read_csv(file, sep=",", dtype=dtype)
    return df


def read_ids():
    file = config["path_intermediario"] + "dac_comvest_ids.csv"
    dtype = get_dtype_dac_comvest()
    df = pd.read_csv(file, sep=",", dtype=dtype)
    return df


# ------------------------------------------------------------------------------------------------
def read_database(file, dtype, index=None, squeeze=False):
    df = pd.read_csv(
        file, sep=";", encoding="latin", dtype=dtype, index_col=index,
    )
    if squeeze:
        return df.squeeze()
    return df

def read_database_pre_processed(file):
    df = pd.read_parquet(file, dtype_backend="pyarrow")
    return df