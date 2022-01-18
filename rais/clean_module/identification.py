import pandas as pd
import clean_module.file
import clean_module.dtypes
import clean_module.clean_columns

# Clean all csv files from all years. Each year must must have a folder named "original_data"
def get_identification_from_all_years(path):
    for year in range(2002, 2019):
        get_identification_from_year(year, path)

# Clean all csv files from specified year, that must be in folder "original_data"
def get_identification_from_year(year, path):
    path_year = clean_module.file.get_year_path(year, path)
    clean_module.file.create_folder(path_year, 'identification_data')

    path_files = path_year + 'original_data/'
    extension = clean_module.dtypes.get_extension(year)
    files = clean_module.file.get_all_files(path_files, extension)

    for file in files:
        get_identification_from_file(file, year)

# Clean csv file and save in folder "identification_data"
def get_identification_from_file(file, year):
    dtype = clean_module.dtypes.get_dtype_rais_original(year)
    df = clean_module.file.read_csv(file, dtype)

    columns = ['nome_r', 'cpf_r', 'dta_nasc_r', 'pispasep', 'mun_estbl']
    df = clean_module.clean_columns.rename_columns(df, year, columns)
    df_filtered = df.loc[:, columns]
    df_filtered.insert(0, 'ano_base', year, True)
    df_filtered = clean_identification(df_filtered)

    file_out = clean_module.file.change_file_format(file, 'pkl')
    file_out = clean_module.file.change_folder_name(file_out, 'identification_data')
    df_filtered.to_pickle(file_out)

# Clean columns with identification data
def clean_identification(df):
    clean_module.clean.clean_cpf_column(df)
    clean_module.clean.clean_pispasep_column(df)
    clean_module.clean.clean_name_column(df)
    df = clean_module.clean.clean_birthdate_column(df)
    return df
