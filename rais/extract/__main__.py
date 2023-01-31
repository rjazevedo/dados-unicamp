import logging

from rais.extract import merge
from rais.extract import recover_cpf_rais
from rais.extract import clear


def clear_databse():
    logging.basicConfig(level=logging.DEBUG)
    merge.merge_all_years()
    recover_cpf_rais.recover_cpf_all_years()
    clear.clear_all_years()


if __name__ == "__main__":
    clear_databse()
