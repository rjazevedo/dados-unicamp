from comvest.extract_enrolled import extrair_matriculados, extrair_convocados


def main():
    extrair_matriculados.extraction()
    extrair_convocados.extraction()


if __name__ == "__main__":
    main()
