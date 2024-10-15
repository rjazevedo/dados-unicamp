import logging


def log_cleaning_database(database):
    """Registra informações sobre a limpeza de um banco de dados.

    Args:
        database (str): O nome do banco de dados que está sendo limpo.
    """
    logging.info(f"Cleaning {database} Database\nThis might take a while\n")


def log_cleaning_column(column):
    """Registra informações sobre a limpeza de uma coluna específica.

    Args:
        column (str): O nome da coluna que está sendo limpa.
    """
    logging.debug(f"Cleaning column: {column}")


def log_cleaning_file(path, file):
    """Registra informações sobre a limpeza de um arquivo em um caminho específico.

    Args:
        path (str): O caminho onde o arquivo está localizado.
        file (str): O nome do arquivo que está sendo limpo.
    """
    logging.info(f"Cleaning file: {file} in {path}")


def log_reading_file_extraction(file):
    """Registra informações sobre a leitura de um arquivo para extração.

    Args:
        file (str): O nome do arquivo que está sendo lido para extração.
    """
    logging.info(f"Reading file for extraction: {file}")


def log_extracting_ids():
    """Registra informações sobre a criação de uma amostra com indivíduos de duas fontes específicas."""
    logging.info("Creating sample with individuals from dac and comvest\n")


def log_verifying_database(database):
    """Registra informações sobre a verificação de um banco de dados.

    Args:
        database (str): O nome do banco de dados que está sendo verificado.
    """
    logging.info(f"Verifying {database} Database\n")


def log_verifying_column(column):
    """Registra informações sobre a verificação de uma coluna específica.

    Args:
        column (str): O nome da coluna que está sendo verificada.
    """
    logging.info(f"Verifying column: {column}")


def log_show_result(df):
    """Registra os resultados de uma operação, mostrando se há entradas falhas.

    Args:
        df (DataFrame): O DataFrame a ser verificado e registrado.
    """
    if df.empty:
        logging.info("All entries are OK\n")
    else:
        num_fail = df.shape[0]
        logging.info(f"Failed in {num_fail} entries\nHead:\n{df.head()}\n")
