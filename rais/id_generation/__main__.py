import logging

from rais.id_generation import cpf_verification
from rais.id_generation import recover_cpf_dac_comvest
from rais.id_generation import random_index


def generate_ids():
    logging.basicConfig(level=logging.INFO)
    cpf_verification.remove_invalid_cpf()
    recover_cpf_dac_comvest.recover_cpf_dac_comvest()
    random_index.generate_index()


if __name__ == "__main__":
    generate_ids()
