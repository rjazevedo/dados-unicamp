import glob
from enum import Enum

class Bases(Enum):
    USP = "/home/input/diplommas/usp/"
    RESULT_USP = "/home/output/intermediario/"
    OUTPUT = "/home/output/diplomas/"


usp_files = glob.glob(Bases.USP.value + "*.html")