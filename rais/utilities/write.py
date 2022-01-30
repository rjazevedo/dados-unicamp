import pandas
import yaml

from rais.utilities.file import get_file_name

stream = open('rais/configuration.yaml')
config = yaml.safe_load(stream)

def write_rais_identification(df, year, file):
    path = config['path_output_data'] + 'tmp/' + str(year) + '/identification_data/'
    file_name = get_file_name(file)
    file_out = path + file_name + '.pkl'
    df.to_pickle(file_out)

def write_rais_merge(df, year, file):
    path = config['path_output_data'] + 'tmp/' + str(year) + '/rais_dac_comvest/'
    file_name = get_file_name(file)
    file_out = path + file_name + '.csv'
    df.to_csv(file_out, sep=';', index=True)

def write_rais_clean(df, year, file):
    path = config['path_output_data'] + 'tmp/' + str(year) + '/clean_data/'
    file_name = get_file_name(file)
    file_out = path + file_name + '.csv'
    df.to_csv(file_out, sep=';', index=True)

def write_rais_sample(df):
    file_out = config['path_output_data'] + 'rais_amostra.csv'
    df.to_csv(file_out, sep=';', index=False)

#------------------------------------------------------------------------------------------------
def write_dac_comvest_valid(df):
    file_out = config['path_output_data'] + 'tmp/' + 'uniao_dac_comvest_valid.csv'
    df.to_csv(file_out, sep=';', index=False)

def write_dac_comvest_recovered(df):
    file_out = config['path_output_data'] + 'tmp/' + 'uniao_dac_comvest_recovered.csv'
    df.to_csv(file_out, sep=';', index=False)

def write_dac_comvest_ids(df):
    file_out = config['path_output_data'] + 'dac_comvest_ids.csv'
    df.to_csv(file_out, sep=';', index=False)

#------------------------------------------------------------------------------------------------
def write_database(df, file, index=False):
    df.to_csv(file, sep=';', index=index)
