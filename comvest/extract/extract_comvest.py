from comvest.clear_dados import limpeza_dados
from comvest.clear_perfil import limpeza_perfil
from comvest.clear_notas import limpeza_notas, presenca
from comvest.extract_enrolled import extrair_matriculados, extrair_convocados
from comvest.extract_cities import extrair_cidades
from comvest.extract_courses import extrair_cursos, dict_cursos


def extraction():
    extrair_cidades.extraction()
    extrair_cursos.extraction()
    dict_cursos.get()
    extrair_matriculados.extraction()
    extrair_convocados.extraction()
    limpeza_dados.extraction()
    # validacao_mun.validation()
    # validacao_esc.validation()
    limpeza_perfil.extraction()
    limpeza_notas.extraction()
    presenca.get()
