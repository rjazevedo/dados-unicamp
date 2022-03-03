from comvest.extract_courses import extrair_cursos
from comvest.extract_courses import dict_cursos

def main():
    extrair_cursos.extraction()
    dict_cursos.get()


if __name__ == '__main__':
    main()