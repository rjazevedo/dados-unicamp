import pandas as pd

from capes.utilities.io import (
    create_folder_capes_tmp_date,
    create_folder_capes_tmp,
    read_capes_original,
)
from capes.utilities.io import list_dirs_capes_input, get_all_files
from capes.utilities.io import read_database, write_database

from capes.utilities.logging import log_cleaning_database
from capes.utilities.logging import log_cleaning_column
from capes.utilities.logging import log_cleaning_file

from capes.utilities.capes_information import get_columns_info_capes, get_columns_names


def clean_capes():
    log_cleaning_database("Capes")
    capes_folders = sorted(list_dirs_capes_input())
    create_folder_capes_tmp()

    for folder in capes_folders:
        clean_date_capes(folder)


# Clean capes files from a given year
def clean_date_capes(path_folder):
    date = path_folder.split("/")[-1]
    create_folder_capes_tmp_date(date)
    files = get_all_files(path_folder)

    for file in files:
        print(f'Limpando: {file.split("/")[-1]}')
        df = read_capes_original(file)
        df = rename_columns(df)
        df = clean_columns(df)
        df = remove_columns(df)
        print(f'Escrevendo: {file.split("/")[-1]}')
        write_database(df, file, date)


def rename_columns(df):
    new_names = get_columns_names()
    return df.rename(columns=new_names)


def clean_columns(df):
    columns_info = get_columns_info_capes()
    columns = list(df.columns)

    for column in columns:
        function = columns_info[column]["cleaning_function"]
        clean_type = columns_info[column]["clean_type"]

        if function is not None:
            df[column] = df[column].apply(function)
        if bug_pandas(str(df[column].dtype), clean_type):
            df[column] = df[column].astype("float").astype(clean_type)
        else:
            df[column] = df[column].astype(clean_type)

    return df


def remove_columns(df):
    return df.drop(
        [
            "id_add_foto_programa",
            "id_add_foto_programa_ies",
            "id_pessoa",
            "nm_orientador",
            "nm_tese_dissertacao",
            "nm_tipo_orientador",
            "nr_seq_orientador",
            "nr_seq_discente",
            "nr_seq_tese",
        ],
        axis=1,
        errors="ignore",
    )


def bug_pandas(old_type, new_type):
    return old_type == "object" and new_type[0:3] == "Int"
