from rais.pre_processing import identification
import logging

def get_identification_data():
    logging.basicConfig(level=logging.INFO)
    identification.get_identification_from_all_years()

if __name__ == '__main__':
    get_identification_data()
