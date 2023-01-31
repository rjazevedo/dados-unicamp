from socio.database_information.estabelecimento import get_columns_info_estabelecimento
from socio.database_information.socio import get_columns_info_socio
from socio.database_information.empresa import get_columns_info_empresa

from socio.utilities.io import (
    read_estabelecimento_original_novolayout,
    read_socio_original,
    write_estabelecimento_tmp,
)
from socio.utilities.io import read_empresa_original
from socio.utilities.io import read_cnae_original

from socio.utilities.io import write_socio_tmp
from socio.utilities.io import write_empresa
from socio.utilities.io import write_cnae

from socio.utilities.io import create_folder_socio_tmp_date
from socio.utilities.io import create_folder_socio_tmp
from socio.utilities.io import create_folder_empresa_tmp_date
from socio.utilities.io import list_dirs_socio_input
from socio.utilities.io import list_dirs_empresa_input
from socio.utilities.io import get_all_files

from socio.utilities.logging import log_cleaning_database
from socio.utilities.logging import log_cleaning_column
from socio.utilities.logging import log_cleaning_file


def clear_socio():
    log_cleaning_database("Socio")
    socio_folders = list_dirs_socio_input()
    socio_folders = sorted(socio_folders)
    create_folder_socio_tmp()

    for folder in socio_folders:
        clear_date_socio(folder)


def clear_cnae_secundaria():
    log_cleaning_database("CNAE")
    df = read_cnae_original()
    write_cnae(df)


# ------------------------------------------------------------------------------------------------
def clear_empresa():
    log_cleaning_database("Empresa")
    date = path.split("/")[-1]
    date_clean = date.replace("-", "")

    create_folder_empresa_tmp_date(date)
    files = get_all_files(path)
    for file in files:
        filename = file.split("/")[-1]
        log_cleaning_file(path, filename)
        df = read_empresa_original(file)


# Usado para os arquivos a partir de 2022, eles tem um novo layout
def clear_estabelecimento():
    date = path.split("/")[-1]
    date_clean = date.replace("-", "")

    create_folder_empresa_tmp_date(date)
    files = get_all_files(path)
    for file in files:
        filename = file.split("/")[-1]
        log_cleaning_file(path, filename)
        df = read_estabelecimento_original_novolayout(file)

        df["data_coleta"] = date_clean

        df = clear_file_estabelecimento(df)

        write_estabelecimento_tmp(df, filename, date)


def clear_date_socio(path):
    date = path.split("/")[-1]
    date_clean = date.replace("-", "")
    create_folder_socio_tmp_date(date)
    files = get_all_files(path)
    for file in files:
        filename = file.split("/")[-1]
        log_cleaning_file(path, filename)
        df = read_socio_original(file, date_clean)

        df = filter_columns_socio(df)
        df["data_coleta"] = date_clean

        df = clear_file_socio(df)
        print(f"Saving cleaned file: {file}")

        write_socio_tmp(df, filename, date)


def clear_file_socio(df):
    columns_info = get_columns_info_socio()
    return clear_columns(df, columns_info)


def clear_file_estabelecimento(df):
    columns_info = get_columns_info_estabelecimento()
    return clear_columns(df, columns_info)


def clear_columns(df, columns_info):
    for column in columns_info:
        log_cleaning_column(column)
        clear_column(df, column, columns_info)
    return df


def filter_columns_socio(df):
    df = df.rename(
        columns={
            "cnpj_empresa": "cnpj",
            "nome_empresa": "razao_social",
            "cpf_cnpj_socio": "cnpj_cpf_do_socio",
            "unidade_federativa": "uf",
        }
    )
    columns_info = get_columns_info_socio()
    valid_cols = set(columns_info.keys()).intersection(set(df.columns))

    if "codigo_tipo_socio" in valid_cols:
        df = df.loc[df.codigo_tipo_socio == 2, valid_cols]
    else:
        df = df.loc[:, valid_cols]

    df.drop("nome_representante_legal", axis=1, inplace=True, errors="ignore")
    df.drop("cpf_representante_legal", axis=1, inplace=True, errors="ignore")
    df.drop(
        "codigo_qualificacao_representante_legal", axis=1, inplace=True, errors="ignore"
    )
    return df


def clear_column(df, column, columns_info):
    function = columns_info[column]["cleaning_function"]
    if function is not None and column in df.columns:
        df[column] = df[column].map(function)
        df[column] = df[column].astype(columns_info[column]["type"])
