import subprocess
import glob
import pandas as pd

def create_folder(path, folder_name):
    command = 'mkdir ' + path + folder_name
    subprocess.run(command, shell=True)

def change_file_format(file, file_format):
    names = file.split('.')
    names[-1] = file_format
    names = '.'.join(names)
    return names

def change_folder_name(file, folder):
    names = file.split('/')
    names[-2] = folder
    names = '/'.join(names)
    return names

def get_year_path(year, path):
    path_year = path + str(year) + '/'
    return path_year

def get_all_files(path, extension):
    files = glob.glob(path + '*.' + extension)
    return files

def read_csv(file, dtype, index=None, squeeze=False):
    df = pd.read_csv(file, sep=';', encoding='latin', dtype=dtype, index_col=index, squeeze=squeeze)
    return df

def to_csv(df, file, index=False):
    df.to_csv(file, sep=';', header=True, index=index)
