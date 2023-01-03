import pandas as pd
import yaml
from pathlib import Path
from fuvest.utilities.dtype import DTYPES_DADOS


stream = open("fuvest/configuration.yaml")
config = yaml.safe_load(stream)
path_input = Path(config["path_input"])


def list_dirs_fuvest_input():
    return [x for x in path_input.iterdir() if x.is_dir()]


def get_all_files(path):
    return [x for x in path.iterdir() if x.is_file()]


def read_fuvest(path):
    fuv = pd.read_excel(
        path,
        dtype={"NOME": str, "NÚMERO": str, "CURSO": str},
    )
    fuv = fuv.rename(
        columns={"NOME": "nome_fuv", "NÚMERO": "numero_fuv", "CURSO": "curso_fuv"}
    )
    return fuv


def read_comvest():
    return pd.read_csv(config["path_comvest_dados"], dtype=DTYPES_DADOS)


def read_ids():
    file = config["database_ids"]
    dtype = get_dtype_dac_comvest()
    df = pd.read_csv(file, sep=",", dtype=dtype)
    return df

def write_fuvest_amostra(df):
    file_out = config["path_output"] + "fuvest_amostra.csv"
    df.to_csv(file_out, sep=",", index=False)

def get_dtype_dac_comvest():
    return {
        "ano_ingresso_curso": "int64",
        "cpf": str,
        "cpf_comvest": str,
        "cpf_dac": str,
        "curso_comvest": "Int32",
        "curso_dac": "Int32",
        "doc": str,
        "doc_comvest": str,
        "doc_dac": str,
        "dta_nasc": str,
        "dta_nasc_comvest": str,
        "dta_nasc_dac": str,
        "identif": "Int64",
        "insc_vest": "Int64",
        "insc_vest_comvest": "Int64",
        "insc_vest_dac": "Int64",
        "nome": str,
        "nome_comvest": str,
        "nome_dac": str,
        "origem": str,
        "tipo_ingresso": str,
        "tipo_ingresso_comvest": "Int32",
        "origem_cpf": "int64",
    }
