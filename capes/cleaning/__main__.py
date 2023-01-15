from capes.cleaning import clean
import logging


def pre_process():
    logging.basicConfig(level=logging.INFO)
    clean.clean_capes()


if __name__ == "__main__":
    pre_process()
