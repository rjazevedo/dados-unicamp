from dac.create_ufs_codes import ufs_codes 
from dac.clr_vida_academica import vida_academica
from dac.clr_vida_academica import dados_ingressantes
from dac.clr_dados_cadastrais import dados_cadastrais
from dac.clr_historico_escolar import historico_escolar
from dac.clr_resumo_por_periodo import resumo_por_periodo
from dac.clr_resumo_por_periodo import resumo_periodo_cr
from dac.clr_vida_academica_habilitacao import habilitacao
from dac.uniao_dac_comvest import uniao_dac_comvest
from dac.create_ids import identificadores

def extract():
    ufs_codes.generate_clean_data()
    dados_cadastrais.generate_clean_data()
    historico_escolar.generate_clean_data()
    resumo_por_periodo.generate_clean_data()
    resumo_periodo_cr.generate_cr()
    vida_academica.generate_clean_data()
    dados_ingressantes.generate()
    habilitacao.generate()
    uniao_dac_comvest.generate()
    #identificadores.create_ids()