import os
from diplomas.extract_usp import scrapper 
from diplomas.utilities.io import Bases
from diplomas.utilities.io import usp_files

def main():
    RESULT_FILES = []
    OUTPUT_FILE = Bases.OUTPUT + "diplomas_usp.csv"

    for i, f in enumerate(usp_files):
        SAVE_FILE = Bases.RESULT_USP + f"DIPLOMAs{i}" + ".csv"
        RESULT_FILES.append(SAVE_FILE)
        scrapper.scrap(f, SAVE_FILE)
    
    scrapper.merge(RESULT_FILES, OUTPUT_FILE)
    
    for f in RESULT_FILES: os.remove(f)