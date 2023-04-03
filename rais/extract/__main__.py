import logging

from rais.extract import merge
from rais.extract import recover_cpf_rais
from rais.extract import clear


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

    logging.basicConfig(level=logging.DEBUG)
    merge.merge_all_years()
    recover_cpf_rais.recover_cpf_all_years()
    clear.clear_all_years(tipo_extracao_rais)


if __name__ == "__main__":
    clear_databse()
