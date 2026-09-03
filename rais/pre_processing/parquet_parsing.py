from tqdm import tqdm
import yaml

from rais.extract.clear import rename_columns

from rais.utilities.file import create_folder, get_all_original_files_year
from rais.utilities.dtypes import get_dtype_rais_original

from rais.extract.cleaning_functions import (
    clean_cpf_column,
    clean_pispasep_column,
    clean_name_column,
    clean_birthdate_column,
)

import pandas as pd

stream = open("rais/configuration.yaml")
config = yaml.safe_load(stream)

pre_processed_folder = "pre_processed"


# Le o RAIS bruto e grava um cache colunar em parquet por arquivo/ano, com as
# colunas de identificacao (nome/cpf/data nasc/pispasep) ja limpas -- substitui
# identification.py (pkl+bz2, 6 colunas) por um cache mais rico (37 colunas do
# registro bruto + ano_base), usado por recover_cpf_dac_comvest.py (Tier A) via
# read_rais_identification_parquet(). Ver plan.md, item 6, para os numeros
# medidos (33,7x mais rapido pra ler so as colunas de identificacao).
def parse_rais():
    intervalo = config["intervalo_rais"]

    create_folder(path=config["path_output_data"], folder_name=pre_processed_folder)

    for year in tqdm(range(intervalo[0], intervalo[1] + 1), desc="Total"):
        parse_rais_year(year)


def parse_rais_year(year):
    create_folder(
        path=config["path_output_data"] + pre_processed_folder + "/",
        folder_name=str(year),
    )

    output_path = (
        config["path_output_data"] + pre_processed_folder + "/" + str(year) + "/"
    )

    files = get_all_original_files_year(year)

    for file in tqdm(files, desc=f"Parsing {year}", leave=True):
        parse_rais_file(file, year, output_path)


def parse_rais_file(file, year, output_path):
    file_name = file.split("/")[-1].split(".")[0]
    file_name += ".parquet"
    output_path += file_name

    dtype = get_dtype_rais_original(year)

    columns = ["nome_r", "cpf_r", "dta_nasc_r", "pispasep", "mun_estbl"]

    append = False
    for df in pd.read_csv(
        file,
        sep=";",
        encoding="latin",
        dtype=dtype,
        chunksize=7000 * 1000,
        na_values=["{ñ"],
    ):
        df = rename_columns(df, year, columns)

        df.insert(0, "ano_base", year, True)

        clean_cpf_column(df)
        clean_pispasep_column(df)
        clean_name_column(df)
        clean_birthdate_column(df)

        df.to_parquet(
            output_path, compression="lz4", engine="fastparquet", append=append
        )

        append = True
