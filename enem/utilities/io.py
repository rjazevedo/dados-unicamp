import pandas as pd
from enum import Enum
import glob
import re
import os


class Bases(Enum):
    IDS = ""
    RESULT = "/home/output/intermediario/"
    ENEM_COMVEST = "/home/output/intermediario/Enem_Comvest/"

def read_result(FILENAME):
    return pd.read_csv(Bases.RESULT.value + FILENAME)

def write_result(df, FILENAME):
    df.to_csv(Bases.RESULT.value + FILENAME, index=False)

def read_comvest_grades():
    grades = {}

    for file in os.listdir(Bases.ENEM_COMVEST.value):
        if 'Notas' not in file:
            grade = pd.read_csv(Bases.ENEM_COMVEST.value + file, low_memory=False)
            year = int(file[11:15])
            grades.update({year : grade})

    return grades