import pandas as pd
import swifter
import difflib as dff
import textdistance
import re
from unidecode import unidecode


def standardize_str(s):
    return (
        re.sub(r"[^\w\s]", "", unidecode(str(s)).upper())
        .replace('ADVENTISTA', "A")
        .replace('ADV', "A")
        .replace('AVANCADO', "A") 
        .replace("PRIMEIRO E SEGUNDO GRAUS", "E")
        .replace("PROFISSIONALIZANTE", "P")
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
        .replace('EDUCACAO', 'E')
        .replace('ENSINO', 'E')
        .replace("ESTADUAL", "E")
        .replace('EDUC',"E")
        .replace('ETEC', 'E')
        .replace("1 E 2 GRAU", "")
        .replace("2GRAU", "")
        .replace("2OGRAU", "")
        .replace("MUNICIPAL", "M")
        .replace('MEDIO', 'M') 
        .replace('MODULO', "M") 
        .replace('INSTITUTOS', 'I')
        .replace('INTEGRADA', "I")
        .replace('INTEGRADO', "I")
        .replace("INSTITUTO", "I")
        .replace("INFANTIL", "I")
        .replace("INTEGRAL", "I") 
        .replace('IMACULADA', "I")
        .replace("INTERESCOLAR", "I")
        .replace("PERIODO INTEGRAL", "I")
        .replace('PROFESSOR', 'P') 
        .replace('PROFESSORA', 'P')
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
        .replace("UNIVERSITARIO", "U")
        .replace('UNIDADE', 'U')
        .replace('TEC', "T")
        .replace("TECNICO", "T")
        .replace('TECNICA', "T")
        .replace('TECNOLOGICA', "T")
        .replace('TECNOLOGIA', 'T')
        .replace("SISTEMA", "S")
        .replace('SESI', 'S')
        .replace('SENHORA', 'S')
        .replace('SANTO', 'S')
        .replace('SABER', "S")
        .replace('MILITAR', 'M')
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
        .replace("UNED", "")
        .replace('CEFET-MG', "")
        .replace('EEIFM', "")
        .replace('EQUIPE', "")
        .replace('EEFMT', "")
        .replace('SER', "")
        .replace('E.E.', "")
        .replace('EAG', "")
        .replace('UNIAO', "")
        .replace('FECAP', "") 
        .replace('EEIEFM', "")
        .replace('EEI', "")
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
        #.replace("ETEC", "")
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
        .replace(' DE ', "")
        .replace(' DA ', "")
        .replace(' DO ', "")
        .replace(' DOS ', "")
        .replace(' DAS ', "")
        .replace(" ", "")
        )


def get_match(escola, escolas_series, cutoff):
    values = dff.get_close_matches(escola, escolas_series, cutoff=cutoff)
    
    if len(values) > 0:
        return values[0]
    else:
        return ""


def merge_inep_ibge(escolas, uf_codes):
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
    ufs = df['uf'].unique()
    dict = {}
    for value in ufs:
        filter_condition = (df['uf'] == value)
        df_uf = df[filter_condition]
        dict[value] = df_uf
    return dict


def merge_by_uf(dict_df, ibge_data):
    correct_dfs = []

    for key,value in dict_df.items():
        ibge_data_filtered = ibge_data[ibge_data['uf'] == key]
        merged_df = counties_merge(value, ibge_data_filtered)
        correct_dfs.append(merged_df)

    return concat_and_drop_duplicates(correct_dfs)


def counties_merge(value, ibge_data):
    new = value.copy()
    new['municipio'] = new['municipio'].map(lambda x: get_the_closest_matche(x, ibge_data['municipio']))
    merged_df = pd.merge(new, ibge_data, left_on = ['uf', 'municipio'], right_on = ['uf', 'municipio'], how='left')
    return merged_df


def get_the_closest_matche(element, serie):
    values = dff.get_close_matches(element, serie, cutoff=0.6)
    if len(values) > 0:
        return values[0]
    else:
        return ''


def concat_and_drop_duplicates(dfs):
    concat = pd.concat(dfs, ignore_index = True)
    concat = concat.drop_duplicates()
    return concat