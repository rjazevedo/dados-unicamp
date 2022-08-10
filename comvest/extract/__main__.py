from comvest.extract import extract_comvest
from comvest.extract import merge_sheets


def extract():
    extract_comvest.extraction()
    merge_sheets.merge()


if __name__ == "__main__":
    extract()
