import pandas as pd
import glob
from enum import Enum

from config.settings import get_config

_config = get_config("diplomas")

Bases = Enum(
    "Bases",
    {
        "USP": _config["usp_input"],
        "RESULT": _config["result"],
        "FINAL": _config["final"],
    },
)

def read_result(FILENAME):
    return pd.read_csv(Bases.RESULT.value + FILENAME)

def write_result(df, FILENAME):
    df.to_csv(Bases.RESULT.value + FILENAME, index=False)

usp_files = glob.glob(Bases.USP.value + "*.html")