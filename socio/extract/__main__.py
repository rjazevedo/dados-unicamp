from socio.extract import merge
import logging


def extract_ids():
    logging.basicConfig(level=logging.INFO)
    merge.merge_socio_dac_comvest()


if __name__ == "__main__":
    extract_ids()
