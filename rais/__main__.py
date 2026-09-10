import logging

from rais.pre_processing import identification
from rais.id_generation import cpf_verification
from rais.id_generation import recover_cpf_dac_comvest
from rais.id_generation import random_index
from rais.extract import merge
from rais.extract import recover_cpf_rais
from rais.extract import clear


def get_identification_data():
    identification.get_identification_from_all_years()


def generate_ids():
    cpf_verification.remove_invalid_cpf()
    recover_cpf_dac_comvest.recover_cpf_dac_comvest()
    random_index.generate_index()


def clear_databse():
    merge.merge_all_years()
    recover_cpf_rais.recover_cpf_all_years()
    clear.clear_all_years()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    get_identification_data()
    generate_ids()
    clear_databse()
