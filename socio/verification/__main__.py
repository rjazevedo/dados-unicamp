from socio.verification import verify
import logging

def verify_databases():
    logging.basicConfig(level=logging.INFO)
    verify.verify_socio()
    verify.verify_empresa()
    verify.verify_cnae_secundaria()

if __name__ == '__main__':
    verify_databases()
