from socio.cleaning import clear
import logging


def pre_process():
    logging.basicConfig(level=logging.INFO)
    clear.clear_socio()
    # clear.clear_empresa()
    # clear.clear_cnae_secundaria()
    # clear_date_estabelecimento(
    #     "/home/luisfelipe/dados-unicamp/input/empresa/2022-03-12"
    # )


if __name__ == "__main__":
    pre_process()
