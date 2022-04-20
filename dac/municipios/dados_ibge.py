from dac.utilities.columns import dados_cadastrais_cols
from dac.utilities.io import read_from_database
from dac.municipios.utility_mun import CODE_UF_EQUIV
from dac.municipios.utility_mun import create_key_for_merge
from dac.municipios.utility_mun import create_concat_key_for_merge
from dac.municipios.utility_mun import create_dictonary_ufs
import pandas as pd

def generate_ibge_data():
    brasil_municipios = read_from_database('RELATORIO_DTB_BRASIL_MUNICIPIO.xls')
    brasil_municipios = brasil_municipios[['UF', 'Nome_UF', 'Código Município Completo', 'Nome_Município']]
    brasil_municipios.columns = ['uf_codigo', 'nome_uf', 'codigo_municipio', 'municipio']
    brasil_municipios['uf'] = brasil_municipios['uf_codigo'].map(CODE_UF_EQUIV)
    return brasil_municipios

def get_ibge_data_dict(): 
    ibge_data = generate_ibge_data()
    create_key_for_merge(ibge_data)
    dict = create_dictonary_ufs(ibge_data)
    return dict

def get_ibge_data():
    ibge_data = generate_ibge_data()
    create_concat_key_for_merge(ibge_data)
    return ibge_data