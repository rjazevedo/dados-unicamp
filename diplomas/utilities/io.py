import pandas as pd
import glob
from enum import Enum

class Bases(Enum):
    USP = "/home/input/diplomados/"
    RESULT = "/home/output/intermediario/"
    FINAL = "/home/processados/diplomados/"

def read_result(FILENAME):
    return pd.read_csv(Bases.RESULT.value + FILENAME)

def write_result(df, FILENAME):
    df.to_csv(Bases.RESULT.value + FILENAME, index=False)

usp_files = glob.glob(Bases.USP.value + "*.html")