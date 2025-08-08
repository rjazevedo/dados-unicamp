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
import difflib as dff
import re
from unidecode import unidecode

from comvest.escolas.escolas_dict import STOPWORDS_GRAMATICAIS, TERMOS_QUALIFICADORES_NORMALIZACAO

def standardize_str(text):
    """
    Normaliza uma string de texto (nome de escola ou município) removendo stopwords
    e aplicando transformações específicas para uso em matching.

    A ordem das operações é crucial:
    1. Normalização básica (minúsculas, sem acentos).
    2. Tokenização.
    3. Remoção de stopwords gramaticais.
    4. Aplicação das padronizações de termos qualificadores (priorizando termos mais longos).
    5. Reconstrução da string.

    Parâmetros
    ----------
    text : str
        A string de texto a ser limpa e padronizada.

    Retorna
    -------
    str
        A string padronizada.
    """
    if pd.isna(text):
        return text

    # 1. Normaliza para maiúsculas e remove acentos para processamento consistente
    text_processed = unidecode(str(text)).upper()

    # 2. Tokeniza a string em palavras
    tokens = re.findall(r'\b\w+\b', text_processed)

    # 3. Remove stopwords gramaticais (convertendo para maiúsculas para comparação consistente)
    # Cria um set de stopwords em maiúsculas para busca eficiente
    stopwords_upper = {s.upper() for s in STOPWORDS_GRAMATICAIS}
    filtered_tokens = [token for token in tokens if token not in stopwords_upper]

    # 4. Aplica transformações específicas (TERMOS_QUALIFICADORES_NORMALIZACAO)
    # Ordena os termos por comprimento decrescente para lidar com termos multi-palavras primeiro
    # Converte as chaves do dicionário para maiúsculas para corresponder aos tokens
    sorted_qualifiers = sorted(
        [(unidecode(k).upper(), v.upper()) for k, v in TERMOS_QUALIFICADORES_NORMALIZACAO.items()],
        key=lambda item: len(item[0]),
        reverse=True
    )

    # Junta os tokens filtrados para aplicar as substituições de termos qualificadores
    # É importante fazer isso em uma string para termos multi-palavras
    temp_text = " ".join(filtered_tokens)

    for termo_original, termo_substituto in sorted_qualifiers:
        # Usa regex para substituir palavras ou frases inteiras
        # \b garante que apenas a palavra/frase completa seja substituída
        # re.escape lida com caracteres especiais no termo_original
        temp_text = re.sub(r'\b' + re.escape(termo_original) + r'\b', termo_substituto, temp_text)
    
    # 5. Re-tokeniza após as substituições para limpar quaisquer novos espaços ou palavras mescladas
    final_tokens = re.findall(r'\b\w+\b', temp_text)

    # 6. Junta os tokens finais e remove múltiplos espaços, trimando a string
    final_string = " ".join(final_tokens)
    final_string = re.sub(r'\s+', ' ', final_string).strip()

    return final_string

def get_tokens(s):
    """
    Obtém tokens de uma string para matching baseado em tokens.
    Assume que a string de entrada 's' (chave_tok) já foi padronizada
    por 'standardize_key' e 'clean_text_for_matching'.
    """
    if pd.isna(s) or len(s) == 0:
        return []
    
    s_processed = re.sub(r'\s+', ' ', str(s)).strip()

    # Se a string for muito curta, não há como gerar trigramas
    if len(s_processed) < 3:
        return [s_processed]

    # Gera todos os trigramas sobrepostos da string
    # Ex: "ABCDE" -> ["ABC", "BCD", "CDE"]
    n = 3
    tokens_list = [s_processed[i:i+n] for i in range(len(s_processed) - n + 1)]
    
    return tokens_list


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
