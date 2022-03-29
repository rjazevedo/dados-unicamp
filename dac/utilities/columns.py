dados_cadastrais_cols = [
    'identif', 'nome', 'nome_mae', 'nome_pai', 'dta_nasc', 'idade_atual', 'cpf', 'tipo_doc', 'doc', 'dt_emissao_doc', 'orgao_emissor_doc', 'uf_esmissao_doc', 'doc_tratado', 
    'sexo_d', 'est_civil_d', 'raca_d', 'raca_descricao', 
    'cep_nasc', 'mun_nasc_d', 'uf_nasc_d', 'cod_pais_nascimento', 'pais_nasc_d', 'nacionalidade_d', 'cod_pais_nacionalidade', 'pais_nacionalidade', 'naturalizado',
    'ano_conclu_em', 'escola_em_d', 'tipo_esc_form_em', 'cep_escola_em', 'uf_esc_form_em', 'mun_esc_form_em', 'sigla_pais_esc_form_em', 'pais_esc_form_em', 
    'mun_atual', 'cep_atual', 'mun_resid_d', 'cep_resid_d']

vida_academica_cols = [
    'identif', 'curso', 'curso_nivel', 'curso_nome', 'ano_ingresso_curso', 'periodo_ingresso', 
    'tipo_periodo_ingresso', 'cod_tipo_ingresso', 'tipo_ingresso', 'ano_saida', 
    'periodo_saida', 'tipo_periodo_saida', 'cod_motivo_saida', 'motivo_saida', 
    'cr', 'cr_padrao', 'cr_medio_turma', 'insc_vest', 'opcao_vest', 'chamada_vest', 'aa', 
    'cota_d', 'cota_tipo', 'cota_descricao']

historico_escolar_cols = [
    'identif','periodo','ano','dt_inicio','dt_fim','cod_curricularidade','curricularidade',
    'disc','turma','cod_situacao','situacao','nota','frequencia']

credito_columns = ['periodo', 'ano', 'disc', 'creditos']

resumo_por_periodo_cols = ['identif', 'curso_atual', 'curso_nivel', 'cod_espec_hab', 'ano_ingresso_curso', 'periodo_ingresso', 'tipo_periodo_ingresso', 
            'ano_saida', 'periodo_saida', 'tipo_periodo_saida', 'periodo', 'ano', 'data_inicio','data_fim', 'situacao','motivo', 
            'cr_periodo', 'cp_periodo', 'disc_cursadas', 'disc_aprovadas', 'repr_nota', 'repr_freq', 'aproveitamentos', 
            'aprov_proficiencia', 'disc_aproveitadas', 'desistencias', 'creditos_periodo', 'bolsa_moradia', 'bolsa_auxilio', 'bolsa_transporte', 
            'bolsa_alimentacao', 'bolsa_pesquisa', 'bolsas_outras', 'estag_obrig',	'estagio_opcion']

cursos_habilitacoes_cols = ['curso', 'NIVEL', 'NOME CURSO', 'codigo_habilitacao', 'NOME HABILITACAO', 'total_creditos_curso_hab', 'total_horas_curso_hab', 'tp_integralizacao_sugerido',
            'tp_integralizacao_max', 'ano_ingresso']

vida_academica_habilitacao_cols = ['identif', 'ano_ingresso', 'periodo_ingresso', 'tipo_periodo_ingresso', 'ano_saida', 'periodo_saida', 'tipo_periodo_saida' ,
            'cod_motivo_saida', 'motivo_saida', 'curso', 'nivel_curso', 'codigo_habilitacao', 'nome_habilitacao', 'prioridade_habilitacao', 'situacao_habilitacao',
            'cp', 'cpf', 'cp_esperado', 'ano_limite_integralizacao', 'periodo_limite_integralizacao', 'data_conclusao'] 