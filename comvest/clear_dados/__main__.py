from comvest.clear_dados import limpeza_dados, cod_ibge, cod_inep, ids_nomes
from comvest.extract_courses.__main__ as extrair_cursos

CURSOS = "cursos.csv"

def main():
    pre_processing()
    limpeza_dados.extraction()
    cod_ibge.merge()
    cod_inep.merge()
    ids_nomes.merge()

def pre_processing():
    if check_if_need_result_file(CURSOS):
        extrair_cursos.main()
    #TODO: IMPLEMENTAR AS OUTRAS CHECAGENS 


if __name__ == "__main__":
    main()
