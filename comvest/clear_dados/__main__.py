from comvest.clear_dados import limpeza_dados, cod_ibge, cod_inep, ids_nomes
from comvest.extract_courses.__main__ as extrair_cursos

import dac.create_names_ids.__main__ as create_names_ids
from dac.clr_dados_cadastrais import school_codes
from dac.clr_dados_cadastrais import setup_dados
from dac.clr_dados_cadastrais import uf_codes
from dac.utilities.io import check_if_need_result_file
import dac.create_ufs_codes.__main__ as create_ufs_codes
import dac.create_names_ids.__main__ as create_names_ids

SCHOOL_CODES = "escola_codigo_inep.csv"
ID_NAMES = "ids_of_names.csv"
UF_CODE_NAME = 'final_counties.csv'
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
    if check_if_need_result_file(UF_CODE_NAME):
        create_ufs_codes.main()
    if check_if_need_result_file(SCHOOL_CODES):
        escolas.main()
    if check_if_need_result_file(ID_NAMES):
        create_names_ids.main()

if __name__ == "__main__":
    main()
