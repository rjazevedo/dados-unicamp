from comvest.clear_perfil import limpeza_perfil
from dac.utilities.io import check_if_need_result_file
import comvest.extract_courses.__main__ as courses
import comvest.extract_cities.__main__ as courses

CIDADES = "cidades_comvest.csv"
CURSOS = "cursos.csv"

def main():
    pre_processing()
    limpeza_perfil.extraction()

def pre_processing():
    if check_if_need_result_file(CURSOS):
        extrair_cursos.main()
    if check_if_need_result_file(CIDADES):
        extrair_cities.main()


if __name__ == "__main__":
    main()
