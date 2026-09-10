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
    d = {1: "limitada", 2: "completa"}

    while True:
        rais_in = int(
            input(
                "Digite 1 para realizar a extração limitada da base RAIS ou 2 para a extração completa:"
            )
        )
        if rais_in != 1 and rais_in != 2:
            print("Entrada inválida, digite novamente.")
        else:
            tipo_extracao_rais = d[rais_in]
            break

    merge.merge_all_years()
    recover_cpf_rais.recover_cpf_all_years()
    clear.clear_all_years(tipo_extracao_rais)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    get_identification_data()
    generate_ids()
    clear_databse()
