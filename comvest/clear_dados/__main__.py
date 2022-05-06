from comvest.clear_dados import limpeza_dados
from comvest.clear_dados import validacao_mun

def main():
    limpeza_dados.extraction()
    validacao_mun.validation()


if __name__ == '__main__':
    main()