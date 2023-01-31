import pandas as pd
import yaml
from pathlib import Path


stream = open("unesp/configuration.yaml")
config = yaml.safe_load(stream)
path_input = Path(config["path_input"])


def list_dirs_unesp_input():
    return [x for x in path_input.iterdir() if x.is_dir()]


def get_all_files(path):
    return [x for x in path.iterdir() if x.is_file()]


def read_unesp(path):
    unesp = pd.read_excel(path)
    unesp = unesp.rename(
        columns={
            "Aluno": "nome_unesp",
            "Ano": "ano_vest_unesp",
            "Curso": "curso_unesp",
            "Curso_Unesp": "curso_unesp",
            "Turno_Unesp": "turno_unesp",
            "Turno": "turno_unesp",
            "Cidade": "cidade_unesp",
            "Cidade_Unesp": "cidade_unesp",
            "Código Curso Turno e Cidade_Unesp": "codigo_curso_unesp",
            "Código Curso Turno e Cidade": "codigo_curso_unesp",
            "Aprovado_Unesp": "aprovado_unesp"
        }
    )
    return unesp


def read_ids():
    file = config["database_ids"]
    dtype = get_dtype_dac_comvest()
    df = pd.read_csv(file, sep=",", dtype=dtype)
    return df


def write_unesp_amostra(df):
    file_out = config["path_output"] + "unesp_amostra.csv"
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
