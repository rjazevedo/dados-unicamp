import dac.clr_dados_cadastrais.__main__ as dados_cadastrais
import dac.clr_historico_escolar.__main__ as clr_historico_escolar
import dac.clr_resumo_por_periodo.__main__ as clr_resumo_por_periodo
import dac.clr_vida_academica.__main__ as clr_vida_academica
import dac.clr_vida_academica_habilitacao.__main__ as clr_vida_academica_habilitacao
import dac.uniao_dac_comvest.__main__ as uniao_dac_comvest
import dac.create_ids.__main__ as create_ids

def extract():
    dados_cadastrais.main()
    clr_historico_escolar.main()
    clr_resumo_por_periodo.main()
    clr_vida_academica.main()
    clr_vida_academica_habilitacao.main()
    uniao_dac_comvest.main()
    create_ids.main()