from dac.clr_vida_academica import vida_academica
from dac.clr_vida_academica import dados_ingressantes

def main():
    vida_academica.generate_clean_data()
    dados_ingressantes.generate()

if __name__ == '__main__':
    main()