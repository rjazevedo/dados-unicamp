from comvest.clear_dados import limpeza_dados, cod_ibge, validacao_esc, cod_inep


def main():
    limpeza_dados.extraction()
    cod_ibge.merge()
    # validacao_esc.validation()
    cod_inep.merge()


if __name__ == "__main__":
    main()
