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
    df = pd.read_pickle(file, compression="bz2")
    return df


# Le so as colunas de identificacao do cache parquet pre-processado (colunas
# podadas na leitura, parquet e colunar), usado por recover_cpf_dac_comvest.py
# (Tier A) em vez do cache pkl+bz2 acima -- ver rais/pre_processing/parquet_parsing.py.
# Os outros consumidores de read_rais_identification (merge.py, cpf_verification.py,
# recover_cpf_rais.py) continuam no pkl por ora, troca isolada de proposito.
# Sem dtype_backend="pyarrow" (usado no codigo de origem/giovani) de proposito:
# strings Arrow-backed quebram is_valid_cpf() -- .str.extract() com grupos
# posicionais (sem nome) nao e suportado nesse backend, so com nomeados
# (achado real rodando o teste de integracao 2002+2013, nao teorico). O
# ganho de poda de colunas (33,7x medido) independe do dtype_backend.
def read_rais_identification_parquet(file):
    columns = ["nome_r", "cpf_r", "dta_nasc_r", "pispasep", "mun_estbl", "ano_base"]
    df = pd.read_parquet(file, columns=columns)
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


def read_rais_original_by_merge(file_merge, year):
    path = config["path_input_data"] + str(year) + "/"
    file_name = get_file_name(file_merge)
    extension = get_extension(year)
    file = path + file_name + "." + extension
    dtype = get_dtype_rais_original(year)
    df = read_database(file, dtype)
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
    df = pd.read_csv(file, sep=";", encoding="latin", dtype=dtype, index_col=index)
    if squeeze:
        df = df.squeeze("columns")
    return df
