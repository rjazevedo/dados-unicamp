import pandas as pd
import functools

from socio.database_information.socio import get_columns_info_socio
from socio.database_information.empresa import get_columns_info_empresa

from socio.utilities.io import read_socio_original
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
    create_folder_socio_tmp()

    for folder in socio_folders:
        clear_date_socio(folder)


def clear_empresa():
    log_cleaning_database("Empresa")
    # df = read_empresa_original()
    empresa_folders = list_dirs_empresa_input()

    for folder in empresa_folders:
        clear_date_empresa(folder)

    # columns_info = get_columns_info_empresa()
    # df = clear_columns(df, columns_info)
    # write_empresa(df)


def clear_cnae_secundaria():
    log_cleaning_database("CNAE")
    df = read_cnae_original()
    write_cnae(df)


# ------------------------------------------------------------------------------------------------
def clear_date_empresa(path):
    date = path.split("/")[-1]
    date_clean = date.replace("-", "")


    create_folder_empresa_tmp_date(date)
    files = get_all_files(path)
    for file in files:
        filename = file.split("/")[-1]
        log_cleaning_file(path, filename)
        df = read_empresa_original(file)

        # df = filter_columns(df, date) TODO
        df["data_coleta"] = date_clean

        df = clear_file(df)

        # write_socio_tmp(df, filename, date) TODO


def clear_date_socio(path):
    date = path.split("/")[-1]
    date_clean = date.replace("-", "")
    create_folder_socio_tmp_date(date)
    files = get_all_files(path)
    for file in files:
        filename = file.split("/")[-1]
        log_cleaning_file(path, filename)
        df = read_socio_original(file)

        df = filter_columns(df, date)
        df["data_coleta"] = date_clean

        df = clear_file(df)

        write_socio_tmp(df, filename, date)


def clear_file(df):
    # nao precisa df = read_socio_original(path, date) TODO
    columns_info = get_columns_info_socio()
    return clear_columns(df, columns_info)


def clear_columns(df, columns_info):
    # change_column_types(df, columns_info) # A princípio nao é necessário TODO
    for column in columns_info:
        log_cleaning_column(column)
        print(f"cleaning column: {column}")  # TODO remover
        clear_column(df, column, columns_info)
    return df


def filter_columns(df, date):
    columns_info = get_columns_info_socio()
    columns = []
    for column in columns_info:
        if date in columns_info[column]["available_dates"]:
            columns.append(column)
    df = df.loc[:, columns]
    df.drop("nome_representante_legal", axis=1, inplace=True)
    df.drop("cpf_representante_legal", axis=1, inplace=True)
    df.drop("codigo_qualificacao_representante_legal", axis=1, inplace=True)
    return df


def change_column_types(df, columns_info):
    for column in columns_info:
        if "has_null_value" in columns_info[column]:
            df[column] = df[column].fillna(-1)
            type_column = columns_info[column]["type"]
            df[column] = df[column].astype(type_column)


def clear_column(df, column, columns_info):
    function = columns_info[column]["cleaning_function"]
    if function is not None:
        df[column] = df[column].map(function)
        df[column] = df[column].astype(columns_info[column]["type"])
