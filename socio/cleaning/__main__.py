from socio.cleaning import clear
import logging

def pre_process():
    logging.basicConfig(level=logging.INFO)
    clear.clear_socio()
    clear.clear_empresa()
    clear.clear_cnae_secundaria()

if __name__ == '__main__':
    pre_process()