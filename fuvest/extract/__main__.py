import logging
from fuvest.utilities.io import list_dirs_fuvest_input, get_all_files
from fuvest.extract.extract import extract_fuvest

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    extract_fuvest()
