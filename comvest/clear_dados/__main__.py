from comvest.clear_dados import limpeza_dados, cod_ibge, cod_inep, ids_nomes


def main():
    limpeza_dados.extraction()
    cod_ibge.merge()
    cod_inep.merge()
    ids_nomes.merge()


if __name__ == "__main__":
    main()
