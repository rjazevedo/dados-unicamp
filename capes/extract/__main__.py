from capes.extract import merge
import logging


def extract():
    logging.basicConfig(level=logging.INFO)
    merge.extract_ids()

if __name__ == "__main__":
    extract()
