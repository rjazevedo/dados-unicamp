import yaml

import subprocess
import glob
import pandas as pd

stream = open('rais/configuration.yaml')
config = yaml.safe_load(stream)

def create_folder_tmp():
    path = config['path_output_data']
    create_folder(path, 'tmp')

def create_folder_year(year):
    path = config['path_output_data'] + 'tmp/'
    create_folder(path, str(year))

def create_folder_inside_year(year, name_folder):
    path = config['path_output_data'] + 'tmp/' + str(year) + '/'
    create_folder(path, name_folder)

def get_all_original_files_year(year):
    path = config['path_input_data'] + str(year) + '/'
    extension = get_extension(year)
    files = get_all_files(path, extension)
    return files

def get_all_tmp_files(year, directory, extension):
    path = config['path_output_data'] + 'tmp/' + str(year) + '/' + directory + '/'
    files = get_all_files(path, extension)
    return files

def get_file_name(file):
    file = file.split('/')[-1]
    return file.split('.')[0]

#------------------------------------------------------------------------------------------------
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

def get_extension(year):
    if year <= 2010:
        return 'TXT'
    else:
        return 'txt'
