import logging

from rais.verification import verification

def verify_databases():
    logging.basicConfig(level=logging.INFO)
    verification.verify_output()

if __name__ == '__main__':
    verify_databases()
