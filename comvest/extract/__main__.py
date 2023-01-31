from comvest.extract import extract_comvest
from comvest.extract import merge_sheets
from comvest.assign_ids import comvest_ids


def extract():
    extract_comvest.extraction()
    merge_sheets.merge()
    comvest_ids.assign_ids()


if __name__ == "__main__":
    extract()
