import pandas as pd
import glob
from enum import Enum

class Bases(Enum):
    USP = "/home/input/diplommas/usp/"
    RESULT = "/home/output/intermediario/"
    OUTPUT = "/home/output/diplomas/"
    FINAL = "/home/processados/diplomados/"

def read_result(FILENAME):
    return pd.read_csv(FILENAME)

def write_result(df, FILENAME):
    df.to_csv(Bases.OUTPUT.value + FILENAME, index=False)

usp_files = glob.glob(Bases.USP.value + "*.html")