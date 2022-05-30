from dac.utilities.io import read_from_database
import pandas as pd

FILE_NAME = 'Rodolfo_Complementacao.xlsx' 
RESULT_NAME = 'Pre_99'

def generate_clean_data():
    vida_academica = read_from_database(FILE_NAME, sheet_name='Vida Academica Curso')
    print(vida_academica.columns)
    print(vida_academica.shape)
    vida_academica_habilitacao = read_from_database(FILE_NAME, sheet_name='VIda Academica Habilitacao')
    print(vida_academica_habilitacao.columns)
    print(vida_academica_habilitacao.shape)
    dados_cadastrais = read_from_database(FILE_NAME, sheet_name='Dados Cadastrais')
    print(dados_cadastrais.columns)
    print(dados_cadastrais.shape)
    historico =  read_from_database(FILE_NAME, sheet_name='Historico')
    print(historico.columns)
    print(historico.shape)