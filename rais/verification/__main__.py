import logging

from rais.verification import verification

# TODO: Esse script precisa ser atualizado pra funcionar!!!!!
# Dá uma olhada no verification do módulo socio, que é uma versão mais atual que eu fiz, e creio que ela pode servir aqui também

def verify_databases():
    logging.basicConfig(level=logging.INFO)
    verification.verify_output()

if __name__ == '__main__':
    verify_databases()
