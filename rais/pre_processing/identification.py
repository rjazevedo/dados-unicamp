from rais.extract.clear import rename_columns

from rais.extract.cleaning_functions import clean_cpf_column
from rais.extract.cleaning_functions import clean_pispasep_column
from rais.extract.cleaning_functions import clean_name_column
from rais.extract.cleaning_functions import clean_birthdate_column

from rais.utilities.file import create_folder_tmp
from rais.utilities.file import create_folder_year
from rais.utilities.file import create_folder_inside_year
from rais.utilities.file import get_all_original_files_year

from rais.utilities.read import read_rais_original
from rais.utilities.write import write_rais_identification

from rais.utilities.logging import (
    log_cleaning_file,
    log_pre_process,
    log_reading_file,
    log_writing_file,
)


def get_identification_from_all_years():
    create_folder_tmp()
    for year in range(2002, 2019):
        log_pre_process(year)
        create_folder_year(year)
        get_identification_from_year(year)


def get_identification_from_year(year):
    create_folder_inside_year(year, "identification_data")
    files = get_all_original_files_year(year)
    for file in files:
        get_identification_from_file(file, year)


def get_identification_from_file(file, year):
    log_reading_file
    df = read_rais_original(file, year)
    log_cleaning_file(file)
    df = filter_columns(df, year)
    df.insert(0, "ano_base", year, True)
    df = clean_identification(df)
    log_writing_file
    write_rais_identification(df, year, file)


def filter_columns(df, year):
    columns = ["nome_r", "cpf_r", "dta_nasc_r", "pispasep", "mun_estbl"]
    df = rename_columns(df, year, columns)
    return df.loc[:, columns]


# Clean columns with identification data
def clean_identification(df):
    clean_cpf_column(df)
    clean_pispasep_column(df)
    clean_name_column(df)
    clean_birthdate_column(df)
    return df
