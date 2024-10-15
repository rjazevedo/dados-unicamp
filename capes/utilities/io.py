import pandas as pd
import yaml
import os
from pathlib import Path

from capes.utilities.capes_information import get_capes_clean_dtypes
from capes.utilities.capes_information import get_columns_names
from capes.utilities.logging import log_discrepancies

stream = open("capes/configuration.yaml")
config = yaml.safe_load(stream)


def get_all_files(path):
    """Retorna uma lista de todos os arquivos no diretório especificado.

    Args:
        path (str): O caminho do diretório a ser explorado.

    Returns:
        list: Lista de caminhos dos arquivos encontrados no diretório.
    """
    return [f.path for f in os.scandir(path) if f.is_file()]


def list_dirs_capes_input():
    """Lista os diretórios de entrada especificados na configuração.

    Returns:
        list: Lista de caminhos dos diretórios de entrada.
    """
    return [f.path for f in os.scandir(config["path_input"]) if f.is_dir()]


def list_dirs_capes_tmp():
    """Lista os diretórios temporários de saída especificados na configuração.

    Returns:
        list: Lista de caminhos dos diretórios temporários de saída.
    """
    return [f.path for f in os.scandir(config["path_output"] + "tmp/") if f.is_dir()]


def create_folder_capes_tmp_date(year):
    """Cria um diretório temporário para o ano especificado.

    Args:
        year (int): O ano para o qual o diretório temporário será criado.
    """
    path = config["path_output"] + "tmp/"
    create_folder(path, str(year))


def create_folder_capes_tmp():
    """Cria um diretório temporário no caminho de saída especificado na configuração."""
    path = config["path_output"]
    create_folder(path, "tmp")


def create_folder(path, folder_name):
    """Cria um diretório no caminho especificado, se ele não existir.

    Args:
        path (str): O caminho onde o diretório será criado.
        folder_name (str): O nome do diretório a ser criado.
    """
    os.makedirs(path + folder_name, exist_ok=True)


def read_ids():
    """Lê os IDs de um arquivo CSV e retorna um DataFrame.

    Returns:
        DataFrame: DataFrame contendo os IDs lidos do arquivo.
    """
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
    """Lê um arquivo CAPES limpo e retorna um DataFrame.

    Args:
        file (str): O caminho do arquivo a ser lido.

    Returns:
        DataFrame: DataFrame contendo os dados limpos do arquivo.
    """
    dtype = get_capes_clean_dtypes()
    return read_database(file, dtype=dtype)


def read_capes_original(file, encoding):
    """Lê um arquivo CAPES original com o encoding especificado e retorna um DataFrame.

    Args:
        file (str): O caminho do arquivo a ser lido.
        encoding (str): O encoding a ser usado ao ler o arquivo.

    Returns:
        DataFrame: DataFrame contendo os dados do arquivo original.
    """
    df = pd.read_csv(file, sep=";", encoding=encoding, low_memory=False)
    return df


def read_database(file, dtype={}):
    """Lê um arquivo CSV e retorna um DataFrame com o tipo de dado especificado.

    Args:
        file (str): O caminho do arquivo a ser lido.
        dtype (dict, optional): Dicionário especificando os tipos de dados das colunas.

    Returns:
        DataFrame: DataFrame contendo os dados do arquivo.
    """
    df = pd.read_csv(file, dtype=dtype, sep=";", low_memory=False)
    return df


def write_database(df, file, date):
    """Escreve um DataFrame em um arquivo CSV no diretório temporário especificado.

    Args:
        df (DataFrame): O DataFrame a ser escrito no arquivo.
        file (str): O caminho do arquivo original, usado para nomear o arquivo de saída.
        date (str): A data usada para criar um subdiretório no caminho de saída.
    """
    path = config["path_output"] + "tmp/" + date + "/" + file.split("/")[-1]
    df.to_csv(path, sep=";", index=False)


def write_sample(df):
    """Escreve um DataFrame em um arquivo CSV com uma amostra dos dados.

    Args:
        df (DataFrame): O DataFrame a ser escrito no arquivo.
    """
    path = config["path_output"] + "capes_amostra.csv"
    df.to_csv(path, sep=";", index=False)
