import pandas

from rais.extract.clear import rename_columns

from rais.extract.cleaning_functions import clear_cpf_column
from rais.extract.cleaning_functions import clear_pispasep_column
from rais.extract.cleaning_functions import clear_name_column
from rais.extract.cleaning_functions import clear_birthdate_column

from rais.utilities.file import create_folder_tmp
from rais.utilities.file import create_folder_year
from rais.utilities.file import create_folder_inside_year
from rais.utilities.file import get_all_original_files_year

from rais.utilities.read import read_rais_original
from rais.utilities.write import write_rais_identification

from rais.utilities.logging import log_pre_process

# Clean all csv files from all years. Each year must must have a folder named "original_data"
def get_identification_from_all_years():
    create_folder_tmp()
    for year in range(2002, 2019):
        log_pre_process(year)
        create_folder_year(year)
        get_identification_from_year(year)

# Clean all csv files from specified year, that must be in folder "original_data"
def get_identification_from_year(year):
    create_folder_inside_year(year, 'identification_data')
    files = get_all_original_files_year(year)
    for file in files:
        get_identification_from_file(file, year)

# Clean csv file and save in folder "identification_data"
def get_identification_from_file(file, year):
    df = read_rais_original(file, year)
    df = filter_columns(df, year)
    df.insert(0, 'ano_base', year, True)
    df = clear_identification(df)
    write_rais_identification(df, year, file)

def filter_columns(df, year):
    columns = ['nome_r', 'cpf_r', 'dta_nasc_r', 'pispasep', 'mun_estbl']
    df = rename_columns(df, year, columns)
    return df.loc[:, columns]

# Clean columns with identification data
def clear_identification(df):
    clear_cpf_column(df)
    clear_pispasep_column(df)
    clear_name_column(df)
    clear_birthdate_column(df)
    return df
