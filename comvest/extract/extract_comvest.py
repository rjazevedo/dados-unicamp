"""
Módulo para extração e processamento de dados Comvest.

Este módulo contém a função principal para extrair e processar dados Comvest usando vários submódulos.

Funções:
- extraction(): Executa a extração e processamento dos dados Comvest.

Como usar:
Implemente e execute a função para realizar a extração e processamento dos dados Comvest.
"""


from comvest.clear_dados import limpeza_dados, cod_ibge, cod_inep, ids_nomes
from comvest.clear_perfil import limpeza_perfil
from comvest.clear_notas import limpeza_notas, presenca
from comvest.extract_enrolled import extrair_matriculados, extrair_convocados
from comvest.extract_cities import extrair_cidades
from comvest.extract_courses import extrair_cursos, dict_cursos


def extraction():
    """
    Executa a extração e processamento dos dados Comvest.

    Esta função chama várias funções de submódulos para realizar a extração e processamento dos dados.

    Retorna
    -------
    None
    """
    extrair_cidades.extraction()
    extrair_cursos.extraction()
    dict_cursos.get()
    extrair_matriculados.extraction()
    extrair_convocados.extraction()
    limpeza_dados.extraction()
    cod_ibge.merge()
    cod_inep.merge()
    ids_nomes.merge()
    limpeza_perfil.extraction()
    limpeza_notas.extraction()
    presenca.get()
