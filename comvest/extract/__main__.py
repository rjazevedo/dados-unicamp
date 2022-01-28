from extract import extract_comvest
from extract import merge_sheets

def main():
    extract_comvest.extraction()
    merge_sheets.merge()

if __name__ == '__main__':
    main()