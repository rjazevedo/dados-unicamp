DTYPES_DADOS = {
    'ano_vest'                 :  'Int64',
    'tipo_ingresso_comvest'    :  'Int64',
    'ano_nasc_c'               :  'Int64',
    'insc_vest'                :  'Int64',
    'opc1'                     :  'Int64',
    'opc2'                     :  'Int64',
    'opc3'                     :  'Int64',
    'nacionalidade_c'          :  'Int64',
    'pais_nasc_c'              :      str,
    'mun_nasc_c'               :      str,
    'uf_nasc_c'                :      str,
    'cep_resid_c'              :      str,
    'mun_resid_c'              :      str,
    'uf_resid'                 :      str,
    'esc_em_c'                 :      str,
    'mun_esc_em_c'             :      str,
    'uf_esc_em'                :      str,
    'nat_esc_em_c'             :  'Int64',
    'ano_conclu_em_c'          :  'Int64',
    'cod_mun_nasc_c'           :  'Int64',
    'cod_mun_resid_c'          :  'Int64',
    'cod_mun_esc_em_c'         :  'Int64',
    'cod_esc_inep'             :  'Int64'
}

DTYPES_PERFIL = {
    'ano_vest'                :  'Int64',
    'insc_vest'               :  'Int64',
    'cid_inscricao'           :      str,
    'instituicao'             :  'Int64',
    'sexo'                    :  'Int64',
    'est_civil'               :  'Int64',
    'local_resid'             :  'Int64',
    'reg_campinas'            :  'Int64',
    'isento'                  :  'Int64',
    'paais'                   :  'Int64',
    'raca'                    :  'Int64',
    'tipo_esc_ef'             :  'Int64',
    'tipo_esc_ef_1'           :  'Int64',
    'tipo_esc_ef_2'           :  'Int64',
    'tipo_esc_em'             :  'Int64',
    'tipo_curso_em'           :  'Int64',
    'periodo_em'              :  'Int64',
    'cursinho'                :  'Int64',
    'cursinho_motivo'         :  'Int64',
    'cursinho_tempo'          :  'Int64',
    'cursinho_tipo'           :  'Int64',
    'cursinho_nao_motivo'     :  'Int64',
    'univ_outra'              :  'Int64',
    'unicamp_motivo'          :  'Int64',
    'opc1_motivo_a'           :  'Int64',
    'opc1_motivo_b'           :  'Int64',
    'renda_sm'                :  'Int64',
    'renda_sm_a'              :  'Int64',
    'renda_sm_b'              :  'Int64',
    'renda_sm_c'              :  'Int64',
    'renda_sm_d'              :  'Int64',
    'renda_qtas'              :  'Int64',
    'renda_contrib_qtas'      :  'Int64',
    'moradia_situacao'        :  'Int64',
    'ocup_pai'                :  'Int64',
    'ocup_mae'                :  'Int64',
    'trabalha_pai'            :  'Int64',
    'trabalha_mae'            :  'Int64',
    'educ_pai'                :  'Int64',
    'educ_mae'                :  'Int64',
    'trabalha'                :  'Int64',
    'contribui_renda_fam'     :  'Int64',
    'jornal_le'               :  'Int64',
    'livros_qtos'             :  'Int64',
    'lugar_calmo_casa'        :  'Int64',
    'jornal_assina'           :  'Int64',
    'revistas_assina'         :  'Int64',
    'enciclopedia'            :  'Int64',
    'atlas'                   :  'Int64',
    'dicionario'              :  'Int64',
    'calculadora'             :  'Int64',
    'empr_domest_qtas'        :  'Int64',
    'idiomas'                 :  'Int64',
    'internet'                :  'Int64',
    'internet_onde'           :  'Int64',
    'cozinha_qtas'            :  'Int64',
    'sala_qtas'               :  'Int64',
    'quarto_qts'              :  'Int64',
    'banheiro_qts'            :  'Int64',
    'radio_qts'               :  'Int64',
    'tv_qts'                  :  'Int64',
    'dvd_vhs_qts'             :  'Int64',
    'computador_qtos'         :  'Int64',
    'carro_qtos'              :  'Int64',
    'geladeira'               :  'Int64',
    'maq_roupa'               :  'Int64',
    'aspirador'               :  'Int64',
    'freezer'                 :  'Int64',
    'maq_louca'               :  'Int64',
    'aprov_f1'                :  'Int64',
    'curso_aprovado'          :  'Int64',
}

DTYPES_MATRICULADOS = {
    'ano_vest'                :  'Int64',
    'insc_vest'               :  'Int64',
    'curso_matric'            :  'Int64',
}

DTYPES_NOTAS = {
    'ano_vest'                 :  'Int64',
    'insc_vest'                :  'Int64',
    'questoes'                 :'float64',
    'not_qui_f1'               :'float64',
    'not_geo_f1'               :'float64',
    'not_fis_f1'               :'float64',
    'not_bio_f1'               :'float64',
    'not_mat_f1'               :'float64',
    'not_his_f1'               :'float64',
    'not_red_f1'               :'float64',
    'not_apt_mus'              :'float64',
    'notpad_apt_mus'           :'float64',
    'nf_f1_f1'                 :'float64',
    'notpad_f1_f1'             :'float64',
    'presente_f1'              :   object,
    'nf_f1_f2'                 :'float64',
    'notpad_f1_f2'             :'float64',
    'not_f1_opc2'              :'float64',
    'notpad_f1_opc2'           :'float64',
    'aprov_apt'                :   object,
    'not_apt'                  :'float64',
    'notpad_aptidao'           :'float64',
    'pqui'                     :   object,
    'not_qui_f2'               :'float64',
    'notpad_qui'               :'float64',
    'pgeo'                     :   object,
    'not_geo_f2'               :'float64',
    'notpad_geo'               :'float64',
    'pfis'                     :   object,
    'not_fis_f2'               :'float64',
    'notpad_fis'               :'float64',
    'pbio'                     :   object,
    'not_bio_f2'               :'float64',
    'notpad_bio'               :'float64',
    'pmat'                     :   object,
    'not_mat_f2'               :'float64',
    'notpad_mat'               :'float64',
    'phis'                     :   object,
    'not_his_f2'               :'float64',
    'notpad_his'               :'float64',
    'ppor'                     :   object,
    'not_por'                  :'float64',
    'notpad_por'               :'float64',
    'pest'                     :   object,
    'not_est'                  :'float64',
    'notpad_est'               :'float64',
    'not_cha'                  :'float64',
    'notpad_cha'               :'float64',
    'not_cn'                   :'float64',
    'notpad_cn'                :'float64',
    'not_inter'                :'float64',
    'notpad_inter'             :'float64',
    'not_red_f2'               :'float64',
    'notpad_red'               :'float64',
    'npo1'                     :'float64',
    'npo2'                     :'float64',
    'npo3'                     :'float64',
    'np_unica'                 :'float64',
    'area'                     :   object,
    'grupo1'                   :  'Int64',
    'grupo2'                   :  'Int64',
    'grupo3'                   :  'Int64',
    'clas_opc1'                :  'Int64',
    'clas_opc2'                :  'Int64',
    'clas_opc3'                :  'Int64',
    'clacar'                   :  'Int64',
    'nf_f2_opc1'               :'float64',
    'nf_f2_opc2'               :'float64',
    'pres_f2_d4'               :   object,
    'nota_enem'                :'float64',
    'notpad_lc_ve'             :'float64',
    'notpad_mat_ve'            :'float64',
    'notpad_cn_ve'             :'float64',
    'notpad_ch_ve'             :'float64',
    'notpad_red_ve'            :'float64',
    'not_red_ve'               :'float64',
    'notpad_he_ve'             :'float64',
    'not_he_ve'                :'float64',
    'npo1_ve'                  :'float64',
    'npo2_ve'                  :'float64',
    'grupo1_ve'                :  'Int64',
    'grupo2_ve'                :  'Int64',
    'clas_opc1_ve'             :  'Int64',
    'clas_opc2_ve'             :  'Int64',
    'questoes_vi'              :'float64',
    'pontuacao_vi'             :'float64',
    'not_red_vi'               :'float64',
    'not_musica_vi'            :'float64',
    'nf_opc1_vi'               :'float64',
    'nf_opc2_vi'               :'float64',
    'grupo1_vi'                :  'Int64',
    'grupo2_vi'                :  'Int64',
    'clas_opc1_vi'             :  'Int64',
    'clas_opc2_vi'             :  'Int64',
    'presente_vi'              :   object,
    'olimpiada1_vo'            :   object,
    'participacao1_vo'         :   object,
    'olimpiada2_vo'            :   object,
    'participacao2_vo'         :   object,
    'npo1_vo'                  :'float64',
    'npo2_vo'                  :'float64',
    'grupo1_vo'                :  'Int64',
    'grupo2_vo'                :  'Int64',
    'clas_opc1_vo'             :  'Int64',
    'clas_opc2_vo'             :  'Int64',
}