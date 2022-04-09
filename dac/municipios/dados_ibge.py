from dac.utilities.columns import dados_cadastrais_cols
from dac.utilities.io import read_from_database
from dac.utilities.io import write_output
import pandas as pd

def generate_ibge_data():
                                          
    brasil_municipios = read_from_database('RELATORIO_DTB_BRASIL_MUNICIPIO.xls')
    brasil_municipios = brasil_municipios[['UF', 'Nome_UF', 'Município', 'Código Município Completo', 'Nome_Município']]
    brasil_municipios.columns = ['uf_codigo', 'nome_uf', 'municipio', 'codigo_municipio', 'nome_municipio']
    
    equiv = { 11: 'RO', 12: 'AC', 13: 'AM', 14: 'RR', 15: 'PA', 16: 'AP', 17: 'TO', 21: 'MA', 22: 'PI', 
              23: 'CE', 24: 'RN', 25: 'PB', 26: 'PE', 27: 'AL', 28: 'SE', 29: 'BA', 31: 'MG', 32: 'ES',
              33: 'RJ', 35: 'SP', 41: 'PR', 42: 'SC', 43: 'RS', 50: 'MS', 51: 'MT', 52: 'GO', 53: 'DF' }

    brasil_municipios['uf'] = brasil_municipios['uf_codigo'].map(equiv)
    #brasil_municipios.drop_duplicates(keep=False,inplace=True)

    write_output(brasil_municipios, 'ue.csv')
    return brasil_municipios