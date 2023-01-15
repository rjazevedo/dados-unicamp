from dac.utilities.io import read_input
from dac.utilities.io import Bases
from dac.create_ufs_codes.utilities import CODE_UF_EQUIV

DADOS_IBGE = "RELATORIO_DTB_BRASIL_MUNICIPIO.xls"

def generate_ibge_data():
    brasil_create_ufs_codes = read_input(DADOS_IBGE, base=Bases.MUNICIPIOS)
    brasil_create_ufs_codes = brasil_create_ufs_codes[['UF', 'Nome_UF', 'Código Município Completo', 'Nome_Município']]
    brasil_create_ufs_codes.columns = ['uf_codigo', 'nome_uf', 'codigo_municipio', 'municipio']
    brasil_create_ufs_codes['uf'] = brasil_create_ufs_codes['uf_codigo'].map(CODE_UF_EQUIV)
    return brasil_create_ufs_codes