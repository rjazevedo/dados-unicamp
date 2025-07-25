import logging

from rais.pre_processing.__main__ import pre_process_data
from rais.id_generation import cpf_verification
from rais.id_generation import recover_cpf_dac_comvest
from rais.id_generation import random_index
from rais.extract import merge
from rais.extract import recover_cpf_rais
from rais.extract import clear
from rais.count_empreg import __main__ as count_empreg

def generate_ids():
    cpf_verification.remove_invalid_cpf()
    recover_cpf_dac_comvest.recover_cpf_dac_comvest()
    random_index.generate_index()


def clear_database():
    merge.merge_all_years()
    recover_cpf_rais.recover_cpf_years()
    clear.clear_all_years()
    count_empreg.count_empreg()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    pre_process_data()
    generate_ids()
    clear_database()
