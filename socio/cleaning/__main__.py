from socio.cleaning import clear
import logging


def pre_process():
    logging.basicConfig(level=logging.INFO)
    clear.clear_socio()


if __name__ == "__main__":
    pre_process()
