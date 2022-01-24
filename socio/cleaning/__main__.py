from socio.cleaning import clear

def pre_process():
    clear.clear_socio()
    clear.clear_empresa()
    clear.clear_cnae_secundaria()

if __name__ == '__main__':
    pre_process()