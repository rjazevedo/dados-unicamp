import pandas as pd
from pandas import DataFrame
# Importando cleaning_utils
from utilities.cleaning_utils import clean_string

def compare(df_1: DataFrame, df_2: DataFrame):
    """
    Compara dois DataFrames e retorna as diferenças entre eles.

    Parâmetros
    ----------
    df_1 : DataFrame
        O DataFrame que será comparado com o novo.
    df_2 : DataFrame
        O novo DataFrame que será usado para a comparação.

    Retorna
    -------
    """
    if df_1.equals(df_2):
        return df_1
    else:
        missing_columns, new_columns, commom_columns = compare_columns_name(df_1, df_2)
        
    cat_columns_1, num_columns_1 = get_categorical_or_numeric_columns(df_1)
    cat_columns_2, num_columns_2 = get_categorical_or_numeric_columns(df_2)
    
    missing_categories, new_categories = compare_categorical_columns(set(cat_columns_1), set(cat_columns_2))
        

def compare_columns_name(df_1: DataFrame, df_2: DataFrame) -> set:
    """
    Compara as colunas de dois DataFrames e retorna as diferenças entre elas.

    Parâmetros
    ----------
    df_1 : DataFrame
        O DataFrame que será comparado com o novo.
    df_2 : DataFrame
        O novo DataFrame que será usado para a comparação.

    Retorna
    -------
    missing_columns : set
        As colunas que estão presentes no primeiro DataFrame, mas não estão no segundo.
    new_columns : set
        As colunas que estão presentes no segundo DataFrame, mas não estão no primeiro.
    commom_columns : set
        As colunas que estão presentes em ambos os DataFrames
    """
    df_1.columns.map(clean_string)
    df_2.columns.map(clean_string)
    columns_1 = set(df_1.columns)
    columns_2 = set(df_2.columns)
    
    missing_columns = columns_1 - columns_2
    new_columns = columns_2 - columns_1
    commom_columns = columns_1 & columns_2
    
    return missing_columns, new_columns, commom_columns
    

def compare_rows(df_1: DataFrame, df_2: DataFrame, identifier: str) -> set:
    """
    Compara as linhas de dois DataFrames e retorna as diferenças entre elas.

    Parâmetros
    ----------
    df_1 : DataFrame
        O DataFrame que será comparado com o novo.
    df_2 : DataFrame
        O novo DataFrame que será usado para a comparação.
    identifier : str
        O nome da coluna que será usada para identificar se há diferenças entre as linhas.

    Retorna
    -------
    missing_rows : set
        As linhas que estão presentes no primeiro DataFrame, mas não estão no segundo.
    new_rows : set
        As linhas que estão presentes no segundo DataFrame, mas não estão no primeiro.
    """
    # Se os identificadores forem iguais, então não foi adicionada ou removida nenhuma amostra
    # Ainda é possível que haja diferenças entre os valores das amostras para outras colunas que não o identificador
    if df_1[identifier].equals(df_2[identifier]):
        return df_1
   
    # Se os identificadores forem diferentes, então houve adição ou remoção de amostras
    missing_rows = df_1[~df_1[identifier].isin(df_2[identifier])]
    missing_rows = set(missing_rows[identifier])

    new_rows = df_2[~df_2[identifier].isin(df_1[identifier])]
    new_rows = set(new_rows[identifier])

    return missing_rows, new_rows

# def get_categorical_or_numeric_columns(df: DataFrame) -> tuple:
#     """
#     Retorna as colunas categóricas e numéricas de um DataFrame.

#     Para saber se uma coluna é categórica é verificado se a quantidade de elementos únicos é menor que 6000

#     Parâmetros
#     ----------
#     df : DataFrame
#         O DataFrame que será usado para a extração das colunas.

#     Retorna
#     -------
#     categorical_columns : set
#         As colunas categóricas do DataFrame.
#     numeric_columns : set
#         As colunas numéricas do DataFrame.
#     """
#     categorical_columns = []
#     numeric_columns = []
    
#     for column in df.columns:
#         n_elements = len(df[column].unique())

#         if n_elements < 6000:
#             categorical_columns.append(column)
#         else:
#             numeric_columns.append(column)

#     return categorical_columns, numeric_columns


def compare_categorical_columns(df_1_categorical: DataFrame, df_2_categorical: DataFrame) -> set:
    """
    Compara as categorias existentes nas colunas categóricas de dois DataFrames e retorna as diferenças entre elas.

    Parâmetros
    ----------
    df_1_categorical : DataFrame
        Um subconjunto do primeiro DataFrame que contém apenas as colunas categóricas.
    df_2_categorical : DataFrame
        Um subconjunto do segundo DataFrame que contém apenas as colunas categóricas.

    Retorna
    -------
    missing_categories : set
        As categorias que estão presentes no primeiro DataFrame, mas não estão no segundo.
    new_categories : set
        As categorias que estão presentes no segundo DataFrame, mas não estão no primeiro.
    """
    missing_categories = set()
    new_categories = set()
    
    for column in df_1_categorical.columns:
        missing_categories.update(set(df_1_categorical[column].unique()) - set(df_2_categorical[column].unique()))
        new_categories.update(set(df_2_categorical[column].unique()) - set(df_1_categorical[column].unique()))
    
    return missing_categories, new_categories


def compare_values(df_original: DataFrame, df_updated: DataFrame):
    """
    Compara os valores de um DataFrame original com um DataFrame atualizado e retorna as diferenças entre eles.
    
    Parâmetros
    ----------
    df_original : DataFrame
        O DataFrame original que será comparado com o atualizado.
    df_updated : DataFrame
        O DataFrame atualizado que será usado para a comparação.
    
    Retorna
    -------
    modified_lines : DataFrame
        As linhas que foram modificadas.
    """
    df_modified_lines = df_original[df_original != df_updated]
    return df_modified_lines


def merge_new_columns(df_1: DataFrame, df_2: DataFrame) -> DataFrame:
    """
    Mescla dois DataFrames, adicionando as colunas do segundo DataFrame ao primeiro.

    Parâmetros
    ----------
    df_1 : DataFrame
        O DataFrame que será mesclado com o novo.
    df_2 : DataFrame
        O novo DataFrame que será usado para a mescla.

    Retorna
    -------
    df : DataFrame
        O DataFrame resultante da mescla.
    """
    return pd.concat([df_1, df_2], axis=1)


def merge_new_rows(df_1: DataFrame, df_2: DataFrame) -> DataFrame:
    """
    Mescla dois DataFrames, adicionando as linhas do segundo DataFrame ao primeiro.
    
    Parâmetros
    ----------
    df_1 : DataFrame
        O DataFrame que será mesclado com o novo.
    df_2 : DataFrame
        O novo DataFrame que será usado para a mescla.
        
    Retorna
    -------
    df : DataFrame
        O DataFrame resultante da mescla.
    """
    return pd.concat([df_1, df_2], axis=0)
    

def main() -> None:
    input_data_1 = "../../input/capes/2018/br-capes-colsucup-discentes-2018-2021-11-10.csv"
    output_data = "/giovani/testes"
    input_data_2 = "../../input/capes/2018/br-capes-colsucup-discentes-2018-2023-12-01.csv"
    
    df1 = pd.read_csv(input_data_1, encoding="latin-1", sep=';', low_memory=False)
    df2 = pd.read_csv(input_data_2, encoding="latin-1", sep=';', low_memory=False)
    
    cat_columns = ['CD_AREA_AVALIACAO', 'NM_AREA_AVALIACAO', 'CD_CONCEITO_CURSO', 'CD_CONCEITO_PROGRAMA', 'CS_STATUS_JURIDICO', 'DS_DEPENDENCIA_ADMINISTRATIVA', 'DS_FAIXA_ETARIA', 'DS_GRAU_ACADEMICO_DISCENTE', 'DS_TIPO_NACIONALIDADE_DISCENTE', 'NM_GRANDE_AREA_CONHECIMENTO', 'NM_GRAU_PROGRAMA', 'NM_MODALIDADE_PROGRAMA', 'NM_REGIAO', 'NM_SITUACAO_DISCENTE', 'SG_UF_PROGRAMA', 'ST_INGRESSANTE', 'TP_DOCUMENTO_DISCENTE', 'NM_MUNICIPIO_PROGRAMA_IES', 'NM_ENTIDADE_ENSINO', 'ID_ADD_FOTO_PROGRAMA', 'CD_PROGRAMA_IES', 'NM_PAIS_NACIONALIDADE_DISCENTE', 'NM_PROGRAMA_IES', 'CD_ENTIDADE_EMEC', 'ID_ADD_FOTO_PROGRAMA_IES', 'CD_ENTIDADE_CAPES', 'SG_ENTIDADE_ENSINO']
    # df1_columns = set(df1.columns)
    # df2_columns = set(df2.columns)
    # print(cat_columns - df1_columns)
    # print(cat_columns - df2_columns)
    
    df1_cat = df1[cat_columns]
    df2_cat = df2[cat_columns]
    
    print(compare_categorical_columns(df1_cat, df2_cat))
    #print(compare_columns_name(df, df2))
    #print(compare_rows(df, df2, "ID_PESSOA"))


if __name__ == "__main__":
    main()
