from clr_vida_academica import vida_academica
from clr_dados_cadastrais import dados_cadastrais
from clr_historico_escolar import historico_escolar
from clr_resumo_por_periodo import resumo_por_periodo
from clr_resumo_por_periodo import resumo_periodo_cr

def extract():
    vida_academica.generate_clean_data()
    dados_cadastrais.generate_clean_data()
    historico_escolar.generate_clean_data()
    resumo_por_periodo.generate_clean_data()
    resumo_periodo_cr.generate_cr()
