from socio.verification import verify

def verify_databases():
    verify.verify_socio()
    verify.verify_empresa()
    verify.verify_cnae_secundaria()

if __name__ == '__main__':
    verify_databases()