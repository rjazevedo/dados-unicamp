from comvest.clear_dados import limpeza_dados
from comvest.clear_perfil import limpeza_perfil
from comvest.clear_notas import limpeza_notas
from comvest.extract_enrolled import extrair_matriculados
from comvest.extract_cities import extrair_cidades
from comvest.extract_courses import extrair_cursos


def extraction():
    extrair_cidades.extraction()
    extrair_cursos.extraction()
    extrair_matriculados.extraction()
    limpeza_dados.extraction()
    limpeza_perfil.extraction()
    limpeza_notas.extraction()