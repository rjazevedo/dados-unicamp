"""
Módulo utilitário para processamento de dados das escolas Comvest.

Este módulo contém funções utilitárias para ler, limpar e processar os dados das escolas dos candidatos.

Funções:
- standardize_str(s): Padroniza uma string.
- remove_countie_name_from_school(df, column): Remove o nome do município do nome da escola.
- merge_inep_ibge(df_inep, df_ibge): Mescla os dados do INEP com os dados do IBGE.
- concat_and_drop_duplicates(df1, df2): Concatena dois DataFrames e remove duplicatas.
- get_match(element, serie): Obtém a melhor correspondência para um elemento em uma série.
- create_dictionary_ufs(df): Cria um dicionário de códigos de UF.
- merge_by_uf(df1, df2): Mescla dois DataFrames por UF.
- counties_merge(df1, df2): Mescla dois DataFrames por municípios.
- get_the_closest_matche(element, serie): Obtém a correspondência mais próxima para um elemento em uma série.

Como usar:
Implemente e execute as funções utilitárias para processar os dados das escolas dos candidatos.
"""


import pandas as pd
import swifter
import difflib as dff
import textdistance
import re
from unidecode import unidecode


def standardize_str(s):
    """
    Padroniza uma string.

    Parâmetros
    ----------
    s : str
        A string a ser padronizada.

    Retorna
    -------
    str
        A string padronizada.
    """
    return (
        re.sub(r"[^\w\s]", "", unidecode(str(s)).upper())
        .replace('ADVENTISTA', "A")
        .replace('ADV', "A")
        .replace('AVANCADO', "A") 
        .replace("PRIMEIRO E SEGUNDO GRAUS", "E")
        .replace("PROFISSIONALIZANTE", "P")
        .replace("ESCOLA DE 1 E 2 GRAUS", "E")
        .replace("ESCOLA DE 1 E 2 GRAU", "E")
        .replace("ESC DE 1 E 2GRAU", "E")
        .replace("EE DE 1 E 2GRAU", "E")
        .replace("EE 2 GRAU", "E")
        .replace("EE 1 E 2GRAU", "E")
        .replace("1 E 2 GRAUS", "E")
        .replace("EDUCACAO INFANTIL", "EI")
        .replace("ENSINO FUNDAMENTAL", "EF")
        .replace("TEMPO INTEGRAL", "TI")
        .replace("ESCOLA MUNICIPAL", "E")
        .replace("CENTRO DE ENSINO", "E")
        .replace("ENSINO MEDIO", "EM")
        .replace("CENTRO EDUCACIONAL", "E")
        .replace('EDUCACIONAL', 'E')
        .replace("EDUCATIVA", "E")
        .replace("EDUCAR", "E")
        .replace("ESTUDANTE", "E")
        .replace("EDUCANDARIO", "E")
        .replace('ESCOLA', "E")
        .replace('ESTUDOS', "E")
        .replace('EDUCACAO', 'E')
        .replace('ENSINO', 'E')
        .replace("ESTADUAL", "E")
        .replace('EDUC',"E")
        #.replace('ETEC', 'E')
        .replace("1 E 2 GRAU", "")
        .replace("2GRAU", "")
        .replace("2OGRAU", "")
        .replace("MUNICIPAL", "M")
        .replace('MEDIO', 'M') 
        .replace('MODULO', "M") 
        .replace('INSTITUTOS', 'I')
        .replace('INST ', 'I')
        .replace('INST. ', 'I')
        .replace('INTEGRADA', "I")
        .replace('INTEGRADO', "I")
        .replace("INSTITUTO", "I")
        .replace("INFANTIL", "I")
        .replace("INTEGRAL", "I") 
        .replace('IMACULADA', "I")
        .replace("INTERESCOLAR", "I")
        .replace("PERIODO INTEGRAL", "I")
        .replace('PROFESSORA', 'P')
        .replace('PROFESSOR', 'P') 
        .replace('PROFA', 'P')
        .replace('PROF', 'P')
        .replace('COMENDADOR', "C")
        .replace('COOPERATIVA', "C")
        .replace('CURSOS', "")
        .replace('CURSO', "C")
        .replace('CAMPUS', 'C')
        .replace("CENTRO", "C")
        .replace('COLEGIO', "C")
        .replace('CIENCIA', 'C') 
        .replace('COMUNITARIA', "C")
        .replace('CULTURA', "C")
        .replace('CULTURAL', "C")
        .replace("UNIVERSITARIO", "U")
        .replace('UNIDADE', 'U')
        .replace("TECNICO", "TEC")
        .replace('TECNICA', "TEC")
        .replace('TECNOLOGICA', "TEC")
        .replace('TECNOLOGIA', 'TEC')
        .replace('TEC', "TEC")
        .replace("SISTEMA", "S")
        #.replace('SESI', 'S')
        .replace('SENHORA', 'S')
        .replace('SANTO', 'S')
        .replace('SABER', "S")
        #.replace('MILITAR', 'M')
        .replace("MAJOR", "M")
        .replace('POLICIA', 'P')
        .replace("DOUTOR", "DR")
        .replace("DOUTORA", "DR")
        .replace('DR.', "DR")
        .replace('DOM.', "D")
        .replace('DONA.', "D")
        .replace('GENERAL', "G")
        .replace('VEREADOR', "V")
        .replace("PERIODO INTEGRAL", "PI")
        .replace("CENTRO DE ENSINO EM", "CEEM")
        .replace('FUNDACAO', "F") 
        .replace("FEDERAL", "F")
        .replace("FUND", "F")
        .replace("FUN", "F")
        .replace("FUNDAMENTAL", "F")
        .replace('FEDERAL', 'F')
        .replace("ORGANIZACAO", "O")
        .replace("JARDIM", "J")
        .replace('RENOVACAO', "R")
        .replace('NOSSA', 'N')
        .replace("UNED", "")
        .replace('REDE', "")
        #.replace("UNED", "")
        .replace('CEFET-MG', "CEFET")
        .replace('EEIFM', "")
        .replace('EQUIPE', "")
        #.replace('EEFMT', "")
        .replace('SER', "")
        .replace('E.E.', "")
        .replace('EAG', "")
        .replace('UNIAO', "")
        .replace('FECAP', "") 
        #.replace('EEIEFM', "")
        #.replace('EEI', "")
        .replace('EXTERNATO', "")
        .replace('ZONA', "")
        .replace('NHN', "")
        #.replace('EF', "") 
        #.replace("CEES", "")
        #.replace("EEIEEF", "")
        #.replace("EEEPSG", "")
        #.replace("EEPGG", "")
        #.replace("EEPG", "")
        #.replace("EEIPSGES", "")
        #.replace("EEIEFEM", "")
        #.replace("EMPSGES", "")
        #.replace("EPSGEI", "")
        #.replace("EMEFMP", "")
        #.replace("EIEFEM", "")
        #.replace("EEIEFM", "")
        #.replace("EEIPSG", "")
        #.replace("EMEFEM", "")
        #.replace("EPSGE", "")
        #.replace("EEPSG", "")
        #.replace("IIPSG", "")
        #.replace("EEIPG", "")
        #.replace("EMPSG", "")
        #.replace("EEENS", "")
        #.replace("EEPEM", "")
        #.replace("ERPSG", "")
        #.replace("EPSG", "")
        #.replace("EEMF", "")
        #.replace("EEBP", "")
        #.replace("EEFM", "")
        #.replace("EFMT", "")
        #.replace("EMSG", "")
        #.replace("EEPG", "")
        #.replace("EIEF", "")
        #.replace("EESG", "")
        #.replace("EMEF", "")
        #.replace("EIE", "")
        #.replace("EEB", "")
        #.replace("EFM", "")
        #.replace("PSG", "")
        #.replace("EEI", "")
        #.replace("EPE", "")
        #.replace("EME", "")
        #.replace("ENS", "")
        #.replace("ESG", "")
        #.replace("IEE", "")
        #.replace('ITB', "")
        #.replace("LTDA", "")
        #.replace('IFSP', "")
        #.replace('EIFM', "")
        .replace("COL.", "")
        .replace("COL", "")
        .replace("RONDONIA", "RO")
        .replace("ACRE", "AC")
        .replace("AMAZONAS", "AM")
        .replace("RORAIMA", "RR")
        .replace("PARA", "PA")
        .replace("AMAPA", "AP")
        .replace("TOCANTINS", "TO")
        .replace("MARANHAO", "MA")	
        .replace("PIAUI", "PI")
        .replace("CEARA", "CE")
        .replace("RIO GRANDE DO NORTE", "RN")
        .replace("PARAIBA", "PB")
        .replace("PERNAMBUCO", "PE")
        .replace("ALAGOAS", "AL")
        .replace("SERGIPE", "SE")	
        .replace("BAHIA", "BA")
        .replace("MINAS GERAIS", "MG")
        .replace("ESPIRITO SANTO", "ES")
        .replace("RIO DE JANEIRO", "RJ")
        .replace("SAO PAULO", "SP")
        .replace("PARANA", "PR")
        .replace("SANTA CATARINA", "SC")
        .replace("RIO GRANDE DO SUL", "RS")
        .replace("MATO GROSSO DO SUL", "MS")
        .replace("MATO GROSSO", " MT")
        .replace("GOIAS", "GO")
        .replace("DISTRITO FEDERAL", "DF")
        .replace(' E ', "")
        .replace(' DE ', "")
        .replace(' DA ', "")
        .replace(' DO ', "")
        .replace(' DOS ', "")
        .replace(' DAS ', "")
        .replace(" ", "")
        )


def get_match(escola, escolas_series, cutoff):
    """
    Obtém a melhor correspondência para o nome de uma escola em uma série.

    Parâmetros
    ----------
    escola : str
        O nome da escola a ser correspondido.
    escolas_series : Series
        A série contendo os nomes das escolas para correspondência.
    cutoff : float
        O limite de similaridade para considerar uma correspondência.

    Retorna
    -------
    str
        O nome da escola mais próximo encontrado ou uma string vazia se nenhuma correspondência for encontrada.
    """
    values = dff.get_close_matches(escola, escolas_series, cutoff=cutoff)
    
    if len(values) > 0:
        return values[0]
    else:
        return ""


def merge_inep_ibge(escolas, uf_codes):
    """
    Mescla os dados de escolas com os códigos de UF (INEP e IBGE).

    Parâmetros
    ----------
    escolas : DataFrame
        O DataFrame contendo os dados das escolas.
    uf_codes : DataFrame
        O DataFrame contendo os códigos de UF do IBGE.

    Retorna
    -------
    DataFrame
        O DataFrame resultante da mesclagem dos dados.
    """    
    base_escolas = pd.merge(escolas, uf_codes, how="left", on=['uf', 'municipio'])
    base_escolas = base_escolas.drop_duplicates(subset=None)

    filt = base_escolas['codigo_municipio'].isnull()
    correct = base_escolas[~filt]

    wrong = base_escolas[filt]
    wrong = wrong[['escola', 'Código INEP', 'uf', 'municipio',
       'Etapas e Modalidade de Ensino Oferecidas']]

    wrong_dict = create_dictonary_ufs(wrong)
    wrong = merge_by_uf(wrong_dict, uf_codes)
    
    total = concat_and_drop_duplicates([correct, wrong])
    return total


def create_dictonary_ufs(df):
    """
    Cria um dicionário de códigos de UF.

    Parâmetros
    ----------
    df : DataFrame
        O DataFrame contendo os dados das UFs.

    Retorna
    -------
    dict
        Um dicionário com os códigos de UF.
    """
    ufs = df['uf'].unique()
    dict = {}
    for value in ufs:
        filter_condition = (df['uf'] == value)
        df_uf = df[filter_condition]
        dict[value] = df_uf
    return dict


def merge_by_uf(dict_df, ibge_data):
    """
    Mescla DataFrames de um dicionário por UF utilizando dados do IBGE.

    Parâmetros
    ----------
    dict_df : dict
        Um dicionário com DataFrames separados por UF.
    ibge_data : DataFrame
        O DataFrame contendo os dados do IBGE.

    Retorna
    -------
    DataFrame
        O DataFrame resultante da mesclagem.
    """
    correct_dfs = []

    for key,value in dict_df.items():
        ibge_data_filtered = ibge_data[ibge_data['uf'] == key]
        merged_df = counties_merge(value, ibge_data_filtered)
        correct_dfs.append(merged_df)

    return concat_and_drop_duplicates(correct_dfs)


def counties_merge(value, ibge_data):
    """
    Mescla um DataFrame filtrado com dados do IBGE por município.

    Parâmetros
    ----------
    value : DataFrame
        O DataFrame filtrado por UF.
    ibge_data : DataFrame
        O DataFrame contendo os dados do IBGE.

    Retorna
    -------
    DataFrame
        O DataFrame resultante da mesclagem por município.
    """
    new = value.copy()
    new['municipio'] = new['municipio'].map(lambda x: get_the_closest_matche(x, ibge_data['municipio']))
    merged_df = pd.merge(new, ibge_data, left_on = ['uf', 'municipio'], right_on = ['uf', 'municipio'], how='left')
    return merged_df


def get_the_closest_matche(element, serie):
    """
    Obtém a correspondência mais próxima para um elemento em uma série.

    Parâmetros
    ----------
    element : str
        O elemento a ser correspondido.
    serie : Series
        A série onde procurar a correspondência.

    Retorna
    -------
    str
        A correspondência mais próxima encontrada ou uma string vazia se nenhuma correspondência for encontrada.
    """
    values = dff.get_close_matches(element, serie, cutoff=0.6)
    if len(values) > 0:
        return values[0]
    else:
        return ''


def remove_countie_name_from_school(df, column):
    """
    Remove o nome do município do nome da escola.

    Parâmetros
    ----------
    df : DataFrame
        O DataFrame contendo os dados das escolas.
    column : str
        O nome da coluna que contém os nomes dos municípios.

    Retorna
    -------
    DataFrame
        O DataFrame com os nomes dos municípios removidos dos nomes das escolas.
    """
    counties = df[column].unique()
    correct = []
    for countie in counties:
        filt = (df[column] == countie)
        df_countie = df[filt].copy()
        df_dummy = df_countie['escola']
        df_countie['chave_seq'] = df_dummy.map(lambda x: x.replace(countie, ""))
        correct.append(df_countie)

    result = pd.concat(correct)
    return result


def concat_and_drop_duplicates(dfs):
    """
    Concatena dois DataFrames e remove duplicatas.

    Parâmetros
    ----------
    dfs : list of DataFrame
        Lista de DataFrames a serem concatenados.

    Retorna
    -------
    DataFrame
        O DataFrame resultante da concatenação dos DataFrames com duplicatas removidas.
    """
    concat = pd.concat(dfs, ignore_index = True)
    concat = concat.drop_duplicates()
    return concat
