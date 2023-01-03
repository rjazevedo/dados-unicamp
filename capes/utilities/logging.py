import logging


def log_cleaning_database(database):
    logging.info(f"Cleaning {database} Database\nThis might take a while\n")


def log_cleaning_column(column):
    logging.debug(f"Cleaning column: {column}")


def log_cleaning_file(path, file):
    logging.info(f"Cleaning file: {file} in {path}")


def log_reading_file_extraction(file):
    logging.info(f"Reading file for extraction: {file}")


def log_extracting_ids():
    logging.info("Creating sample with individuals from dac and comvest\n")


def log_verifying_database(database):
    logging.info(f"Verifying {database} Database\n")


def log_verifying_column(column):
    logging.info(f"Verifying column: {column}")


def log_show_result(df):
    if df.empty:
        logging.info("All entries are OK\n")
    else:
        num_fail = df.shape[0]
        logging.info(f"Failed in {num_fail} entries\nHead:\n{df.head()}\n")
