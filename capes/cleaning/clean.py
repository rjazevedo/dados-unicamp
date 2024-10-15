from capes.utilities.io import (
    create_folder_capes_tmp_date,
    create_folder_capes_tmp,
    read_capes_original,
)
from capes.utilities.io import list_dirs_capes_input, get_all_files
from capes.utilities.io import write_database

from capes.utilities.logging import log_cleaning_database
from capes.utilities.logging import log_cleaning_column
from capes.utilities.logging import log_cleaning_file

from capes.utilities.capes_information import get_columns_info_capes, get_columns_names


def clean_capes():
    """
    Limpa os arquivos CAPES em diretórios de entrada e cria pastas temporárias.

    Registra a operação de limpeza no log e processa cada pasta de entrada,
    chamando a função `clean_date_capes` para limpar os arquivos em cada pasta.
    """
    log_cleaning_database("Capes")
    capes_folders = sorted(list_dirs_capes_input())
    create_folder_capes_tmp()

    for folder in capes_folders:
        clean_date_capes(folder)


# Clean capes files from a given year
def clean_date_capes(path_folder):
    """
    Limpa os arquivos CAPES de um ano específico contidos na pasta fornecida.

    Para cada arquivo na pasta, lê o arquivo original, renomeia as colunas,
    limpa os dados e escreve o DataFrame resultante de volta no arquivo.

    Parâmetros:
        path_folder (str): O caminho da pasta que contém os arquivos CAPES.
    """
    date = path_folder.split("/")[-1]
    create_folder_capes_tmp_date(date)
    files = get_all_files(path_folder)

    for file in files:
        print(f'Limpando: {file.split("/")[-1]}')

        if int(date) == 2020:
            df = read_capes_original(file, "ascii")
        else:
            df = read_capes_original(file, "latin-1")

        df = rename_columns(df)
        df = clean_columns(df)

        print(f'Escrevendo: {file.split("/")[-1]}')
        write_database(df, file, date)


def rename_columns(df):
    """
    Renomeia as colunas do DataFrame com base nas informações de mapeamento de colunas.

    Parâmetros:
        df (DataFrame): O DataFrame cujas colunas devem ser renomeadas.

    Retorna:
        DataFrame: O DataFrame com as colunas renomeadas.
    """
    new_names = get_columns_names()
    return df.rename(columns=new_names)


def clean_columns(df, columns=None):
    """
    Limpa as colunas do DataFrame, aplicando funções de limpeza e convertendo os tipos de dados.

    Parâmetros:
        df (DataFrame): O DataFrame cujas colunas devem ser limpas.
        columns (list, opcional): Lista de colunas a serem limpas. Se None, limpa todas as colunas.

    Retorna:
        DataFrame: O DataFrame com as colunas limpas.
    """
    columns_info = get_columns_info_capes()
    if columns is None:
        columns = list(df.columns)

    for column in columns:
        function = columns_info[column]["cleaning_function"]
        clean_type = columns_info[column]["clean_type"]

        if function is not None:
            df[column] = df[column].apply(function)
        if bug_pandas(str(df[column].dtype), clean_type):
            df[column] = df[column].astype("float").astype(clean_type)
        else:
            df[column] = df[column].astype(clean_type)

    return df


def bug_pandas(old_type, new_type):
    """
    Verifica se há um bug conhecido do pandas ao tentar converter tipos de dados.

    Parâmetros:
        old_type (str): O tipo de dados atual da coluna.
        new_type (str): O novo tipo de dados desejado.

    Retorna:
        bool: Verdadeiro se houver um bug conhecido, falso caso contrário.
    """
    return old_type == "object" and new_type[0:3] == "Int"
