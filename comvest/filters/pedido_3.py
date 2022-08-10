import pandas as pd
import numpy as np
from comvest.utilities.io import read_output
from comvest.utilities.dtypes import DTYPES_DADOS, DTYPES_PERFIL, DTYPES_MATRICULADOS, DTYPES_NOTAS
from filters import filters as filter_db

def extract():
    ''' Leitura das bases '''
    COMVEST_SAMPLE = read_output('comvest_amostra.csv', dtype={**DTYPES_DADOS, **DTYPES_PERFIL, **DTYPES_MATRICULADOS, **DTYPES_NOTAS})
    DAC_VACH_SAMPLE = read_output('vida_academica_habilitacao.csv')
    # DAC_DC_SAMPLE = read_output('dados_cadastrais.csv')
    # DAC_HE_SAMPLE = read_output('historico_escolar.csv')
    # DAC_RPP_SAMPLE = read_output('resumo_por_periodo.csv')
    # SOCIO_SAMPLE = read_output('socio_amostra.csv')
    RAIS_SAMPLE = read_output('rais_amostra.csv', dtype={'dta_admissao':object}, sep=';')

    # Filtragem de matriculados nos anos de 2003/2004
    # matr = set(filter_db.filterby_joindate(DAC_VACH_SAMPLE, year=2003)).union(set(filter_db.filterby_joindate(DAC_VACH_SAMPLE, year=2004)))

    matr = set(filter_db.filterby_year(COMVEST_SAMPLE, years=[2003,2004]))

    courses = [11,12]
    alunos = set(filter_db.filterby_course(COMVEST_SAMPLE, courses, db='comvest'))
    # Filtragem a partir dos cursos
    # courses = [12,34,10,11,41,9,39]
    # alunos = set(filter_db.filterby_course(DAC_VACH_SAMPLE, courses, db='dac'))

    filtered_ids = matr.intersection(alunos)

    comvest_cols = [
        'id',
        'ano_vest',
        'curso_matric',
        'nat_esc_em_c',
        'ano_nasc_c',
        'sexo_c',
        'isento',
        'raca',
        'local_resid',
        'reg_campinas',
        'tipo_esc_ef',
        'tipo_esc_ef_1',
        'tipo_esc_ef_2',
        'tipo_esc_em',
        'tipo_curso_em',
        'periodo_em',
        'cursinho',
        'cursinho_motivo',
        'cursinho_tempo',
        'cursinho_tipo',
        'cursinho_nao_motivo',
        'univ_outra',
        'unicamp_motivo',
        'opc1_motivo_a',
        'opc1_motivo_b',
        'renda_sm',
        'renda_sm_a',
        'renda_sm_b',
        'renda_sm_c',
        'renda_sm_d',
        'renda_qtas',
        'renda_contrib_qtas',
        'moradia_situacao',
        'ocup_pai',
        'ocup_mae',
        'educ_pai',
        'educ_mae',
        'trabalha_pai',
        'trabalha_mae',
        'trabalha',
        'contribui_renda_fam',
        'jornal_le',
        'livros_qtos',
        'lugar_calmo_casa',
        'jornal_assina',
        'revistas_assina',
        'enciclopedia',
        'atlas',
        'dicionario',
        'calculadora',
        'empr_domest_qtas',
        'idiomas',
        'internet',
        'internet_onde',
        'cozinha_qtas',
        'sala_qtas',
        'quarto_qts',
        'banheiro_qts',
        'radio_qts',
        'tv_qts',
        'dvd_vhs_qts',
        'computador_qtos',
        'carro_qtos',
        'geladeira',
        'maq_roupa',
        'aspirador',
        'freezer',
        'maq_louca',
    ]

    COMVEST_FILTERED = COMVEST_SAMPLE[(COMVEST_SAMPLE['id'].isin(filtered_ids) & COMVEST_SAMPLE['curso_matric'].isin(courses))][comvest_cols]
    DAC_VACH_FILTERED = DAC_VACH_SAMPLE[(DAC_VACH_SAMPLE['id'].isin(filtered_ids) & DAC_VACH_SAMPLE['curso'].isin(courses))]

    COMVEST_FILTERED.to_csv('pedido_3/teste.csv', index=False)
    DAC_VACH_FILTERED.to_csv('pedido_3/teste2.csv', index=False)
'''
    dac_cols = [
        'id',
        'ano_ingresso',
        'ano_saida',
        'motivo_saida',
    ]

    DAC_VACH_FILTERED = DAC_VACH_SAMPLE[DAC_VACH_SAMPLE['id'].isin(filtered_ids)][dac_cols]

    rais_cols = [
        'id',
        'ano_base',
        'vinculo_tipo',
        'escolaridade',
        'raca_r',
        'nat_juridica',
        'dta_admissao',
        'rem_media',
        'rem_media_sm',
        'vinculo_tempo',
        'horas_contr',
        'rem_ultima',
        'sal_contr',
        'cbo02',
        'ibge_subsetor',
    ]

    RAIS_FILTERED = RAIS_SAMPLE[RAIS_SAMPLE['id'].isin(filtered_ids)][rais_cols]

    # Escrita das bases filtradas conforme o pedido especifico
    COMVEST_FILTERED.to_csv('pedido_3/comvest_pedido3.csv', index=False)
    DAC_VACH_FILTERED.to_csv('pedido_3/dac_pedido3.csv', index=False)
    RAIS_FILTERED.to_csv('pedido_3/rais_pedido3.csv', index=False)
'''