from comvest.extract_enrolled import extrair_matriculados, extrair_convocados
from dac.utilities.io import check_if_need_result_file
import comvest.extract_courses.__main__ as extrair_cursos

CURSOS = "cursos.csv"

def main():
    pre_processing()
    extrair_matriculados.extraction()
    extrair_convocados.extraction()

def pre_processing():
    if check_if_need_result_file(CURSOS):
        extrair_cursos.main()

if __name__ == "__main__":
    main()
