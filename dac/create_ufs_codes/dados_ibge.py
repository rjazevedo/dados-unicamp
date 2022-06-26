from dac.utilities.columns import dados_cadastrais_cols
from dac.utilities.io import read_from_database
from dac.create_ufs_codes.utility_mun import CODE_UF_EQUIV
from dac.create_ufs_codes.utility_mun import create_key_for_merge
from dac.create_ufs_codes.utility_mun import create_concat_key_for_merge
from dac.create_ufs_codes.utility_mun import create_dictonary_ufs
import pandas as pd

def generate_ibge_data():
    brasil_create_ufs_codes = read_from_database('RELATORIO_DTB_BRASIL_MUNICIPIO.xls')
    brasil_create_ufs_codes = brasil_create_ufs_codes[['UF', 'Nome_UF', 'Código Município Completo', 'Nome_Município']]
    brasil_create_ufs_codes.columns = ['uf_codigo', 'nome_uf', 'codigo_municipio', 'municipio']
    brasil_create_ufs_codes['uf'] = brasil_create_ufs_codes['uf_codigo'].map(CODE_UF_EQUIV)
    return brasil_create_ufs_codes

def get_ibge_data_dict(): 
    ibge_data = generate_ibge_data()
    create_key_for_merge(ibge_data)
    dict = create_dictonary_ufs(ibge_data)
    return dict

def get_ibge_data():
    ibge_data = generate_ibge_data()
    create_concat_key_for_merge(ibge_data)
    return ibge_data