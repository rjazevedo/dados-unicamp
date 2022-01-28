from clear_dados import limpeza_dados
from clear_perfil import limpeza_perfil
from clear_notas import limpeza_notas
from extract_cities import extrair_cidades
from extract_courses import extrair_cursos
from extract_enrolled import extrair_matriculados


def extraction():
    extrair_cidades.extraction()
    extrair_cursos.extraction()
    extrair_matriculados.extraction()
    limpeza_dados.extraction()
    limpeza_perfil.extraction()
    limpeza_notas.extraction()