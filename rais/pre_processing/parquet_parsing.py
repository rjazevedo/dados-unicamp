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
import os


# Obtém o caminho absoluto do diretório onde o script está localizado
base_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(base_dir, "../configuration.yaml")

# Abre o arquivo de configuração
stream = open(config_path)
config = yaml.safe_load(stream)
pre_processed_folder = "pre_processed"

def parse_rais():
    intervalo = config["intervalo_rais"]

    # Cria a pasta onde os arquivos pré processados .parquet serão salvos
    create_folder(
        path=config["path_output_data"],
        folder_name=pre_processed_folder 
    )

    for year in tqdm(range(intervalo[0], intervalo[1] + 1), desc="Total"):
        parse_rais_year(year)


def parse_rais_year(year):
    # Cria a pasta onde os arquivos pré processados .parquet serão salvos 
    create_folder(
        path=config["path_output_data"] + pre_processed_folder + "/",
        folder_name=str(year) 
    )

    output_path = config["path_output_data"] + pre_processed_folder + "/" + str(year) + "/"

    # Lê o nome de todos os arquivos originais do ano
    files = get_all_original_files_year(year)

    # Chama a função parse_rais_file para cada arquivo
    for file in tqdm(files, desc=f"Parsing {year}", leave=True):
        parse_rais_file(file, year, output_path)

def parse_rais_file(file, year, output_path):
    # Extrai o nome do arquivo
    file_name = file.split("/")[-1].split(".")[0]
    file_name += ".parquet"
    output_path += file_name

    # Lê o arquivo original
    dtype = get_dtype_rais_original(year)

    columns = ["nome_r", "cpf_r", "dta_nasc_r", "pispasep", "mun_estbl"]

    append = False
    for df in pd.read_csv(
        file, sep=";", encoding="latin", dtype=dtype, chunksize=7000*1000, na_values=['{ñ']
    ):
        
        # Renomeia as colunas
        df = rename_columns(df, year, columns)

        # Adiciona a coluna "ano_base" ao dataframe
        df.insert(0, "ano_base", year, True)

        # Limpa as colunas com dados de identificação
        clean_cpf_column(df)
        clean_pispasep_column(df)
        clean_name_column(df)
        clean_birthdate_column(df)

        # Salva o arquivo em formato parquet
        df.to_parquet(
            output_path, 
            compression="lz4", 
            engine="fastparquet",
            append=append
        )