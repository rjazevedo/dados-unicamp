import logging
from fuvest.extract.extract import extract_fuvest

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    extract_fuvest()
