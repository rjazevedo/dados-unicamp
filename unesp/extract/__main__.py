import logging
from unesp.extract.extract import extract_unesp

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    extract_unesp()
