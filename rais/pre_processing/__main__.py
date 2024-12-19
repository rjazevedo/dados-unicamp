from rais.pre_processing import parquet_parsing
import logging


def pre_process_data():
    logging.basicConfig(level=logging.INFO)
    parquet_parsing.parse_rais()


if __name__ == "__main__":
    pre_process_data()
