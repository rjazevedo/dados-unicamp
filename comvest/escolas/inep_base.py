import pandas as pd
import difflib as dff
from comvest.utilities.io import read_auxiliary, write_auxiliary
from comvest.escolas.utility import merge_inep_ibge
from comvest.escolas.utility import concat_and_drop_duplicates
from unidecode import unidecode


CODE_UF_EQUIV = { 11: 'RO', 12: 'AC', 13: 'AM', 14: 'RR', 15: 'PA', 16: 'AP', 17: 'TO', 21: 'MA', 22: 'PI', 
                  23: 'CE', 24: 'RN', 25: 'PB', 26: 'PE', 27: 'AL', 28: 'SE', 29: 'BA', 31: 'MG', 32: 'ES',
                  33: 'RJ', 35: 'SP', 41: 'PR', 42: 'SC', 43: 'RS', 50: 'MS', 51: 'MT', 52: 'GO', 53: 'DF' }


def load_inep_base():
    uf_codes = load_counties()
    escolas = load_schools()

    merged = merge_inep_ibge(escolas, uf_codes)
    result = remove_school_duplicated_by_counties(merged)

    result = result[['escola', 'Código INEP', 'codigo_municipio', 'uf', 'municipio']]
    result.columns = ['escola', 'Código INEP', 'codigo_municipio', 'uf_novo', 'municipio_novo']
    result = result.sort_values(by=['codigo_municipio'], ascending=True)
    return result


def load_schools():
    open_schools = read_auxiliary("INEP data.csv", dtype=object, sep=";").loc[:,["Escola", "Código INEP", "UF", "Município", "Etapas e Modalidade de Ensino Oferecidas"]]
    closed_schools = read_auxiliary("cadescfechadassh19952021.csv", dtype=object, sep=";", encoding="latin1").loc[:, ["NO_ENTIDADE", "CO_ENTIDADE", "SG_UF", "NO_MUNICIPIO"]]
    closed_schools.insert(loc=len(closed_schools.columns), column="Etapas e Modalidade de Ensino Oferecidas", value="Médio")
    closed_schools.columns = open_schools.columns

    base_escolas = pd.concat([open_schools, closed_schools])
    base_escolas.columns = ["escola", "Código INEP", "uf", "municipio", "Etapas e Modalidade de Ensino Oferecidas"]
    base_escolas['municipio'] = base_escolas['municipio'].map(lambda x: unidecode(x).upper())
    
    alteracoes = load_alteracoes()
    new_esc = pd.merge(base_escolas, alteracoes, how='left', on=['uf', 'municipio'])
    filt = new_esc['municipio_novo'].isnull()
    correcto = new_esc[filt]

    wrong = new_esc[~filt].copy()
    wrong['municipio'] = wrong['municipio_novo']
    new_esc = concat_and_drop_duplicates([wrong, correcto])

    new_esc = new_esc.drop(['municipio_novo'], axis=1)
    return new_esc


def load_counties():
    brasil_create_ufs_codes = read_auxiliary('RELATORIO_DTB_BRASIL_MUNICIPIO.xls').loc[:,['UF', 'Nome_UF','Código Município Completo', 'Nome_Município']]
    brasil_create_ufs_codes.columns = ['uf_codigo', 'nome_uf', 'codigo_municipio', 'municipio']
    brasil_create_ufs_codes['uf'] = brasil_create_ufs_codes['uf_codigo'].map(CODE_UF_EQUIV)
    brasil_create_ufs_codes['municipio'] = brasil_create_ufs_codes['municipio'].map(lambda x: unidecode(x).upper())
    return brasil_create_ufs_codes


def load_alteracoes():
    alteracoes = read_auxiliary('Alteracoes_Toponimicas_Municipais_2021.xls').loc[:, ['UF', 'NOME_ANTERIOR', 'NOME_ATUAL']]
    alteracoes.columns = ['uf_codigo', 'municipio', 'municipio_novo']
    alteracoes['uf'] = alteracoes['uf_codigo'].map(CODE_UF_EQUIV)
    alteracoes['municipio'] = alteracoes['municipio'].map(lambda x: unidecode(x).upper())
    alteracoes['municipio_novo'] = alteracoes['municipio_novo'].map(lambda x: unidecode(x).upper())
    return alteracoes


def remove_school_duplicated_by_counties(df):
    codigos = df['codigo_municipio'].unique()
    correct_dfs = []

    suma = 0
    for codigo in codigos:        
        filt = (df['codigo_municipio'] == codigo)
        df_uf = df[filt]

        filt = df_uf.duplicated(subset=['escola'], keep=False) 

        nome_duplicado_municipio = df_uf[filt]
        nome_unico_municipio = df_uf[~filt]
        correct_dfs.append(nome_unico_municipio)

        filt = nome_duplicado_municipio['Etapas e Modalidade de Ensino Oferecidas'].str.contains("Médio", na=False)
        right = nome_duplicado_municipio[filt]
        correct_dfs.append(right)

    total = concat_and_drop_duplicates(correct_dfs)
    return total