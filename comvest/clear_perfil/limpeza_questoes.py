from utilities.read import read_from_db


def filtrar_perguntas(desc):
  descricao = desc.lower()
  if 'sexo' in descricao:
    return 'sexo'
  elif 'isenção' in descricao:
    return 'isento'
  elif 'paais' in descricao:
    return 'paais'
  elif 'estado civil' in descricao:
    return 'est_civil'
  elif 'língua estrangeira' in descricao:
    return 'lestrangeira'
  elif all(txt in descricao for txt in ['local','residência']):
    return 'local_residencia'
  elif 'você lê jornal?' in descricao:
    return 'jornal_le'
  elif 'além dos livros escolares, quantos livros há em sua casa?' in descricao:
    return 'livros_qtos'
  elif 'existe em sua casa um lugar calmo para você estudar?' in descricao:
    return 'lugar_calmo_casa'
  elif 'a sua família faz assinatura de um jornal diário?' in descricao:
    return 'jornal_assina'
  elif any(txt in descricao for txt in ['a sua família faz assinatura de revistas semanais','a sua família faz assinatura de revistas de informação geral']):
    return 'revistas_assina'
  elif 'enciclopédia' in descricao:
    return 'enciclopedia'
  elif 'atlas' in descricao:
    return 'atlas'
  elif 'dicionário' in descricao:
    return 'dicionario'
  elif 'calculadora' in descricao:
    return 'calculadora'
  elif 'em sua residência trabalha alguma empregada doméstica' in descricao:
    return 'empr_domest_qtas'
  elif 'você tem acesso à internet' in descricao:
    return 'internet'
  elif 'onde você acessa a internet com maior frequencia?' in descricao:
    return 'internet_onde'
  elif 'cozinha' in descricao:
    return 'cozinha_qtas'
  elif 'sala' in descricao:
    return 'sala_qtas'
  elif 'quarto' in descricao:
    return 'quarto_qts'
  elif 'banheiro' in descricao:
    return 'banheiro_qts'
  elif 'rádio' in descricao:
    return 'radio_qts'
  elif any(txt in descricao for txt in ['existe microcomputador em sua casa?']):
    return 'computador'
  elif any(txt in descricao for txt in ['em caso positivo, você usa o microcomputador?','mesmo não existindo microcomputador em sua casa, você usa microcomputador?','você sabe usar um computador, mesmo que de forma elementar?']):
    return 'computador_uso'
  elif any(txt in descricao for txt in ['quantas horas por semana você dedica em média ao uso do micro?','quantas horas por semana você dedica em média ao uso do microcomputador?']):
    return 'computador_freq'
  elif any(txt in descricao for txt in ['em caso positivo, você usa microcomputador para']):
    return 'computador_finalidade'
  elif any(txt in descricao for txt in ['você usa algum tipo de sistema de janelas']):
    return 'computador_sj'
  elif any(txt in descricao for txt in ['você usa microcomputador para jogos?']):
    return 'computador_jogos'
  elif any(txt in descricao for txt in ['você usa microcomputador para processador de texto?','você usa processadores de texto']):
    return 'processadores_txt'
  elif any(txt in descricao for txt in ['você usa micro. para montagem de tabelas, através de planilhas eletrônicas?','você usa micro. para montagem de tabelas, através de plan. eletrônicas?','você usa microcomputador para montagem de tabelas, através de planilhas eletrônicas?','você usa planilhas eletrônicas']):
    return 'planilhas'
  elif any(txt in descricao for txt in ['você usa microcomputador para montagem de banco de dados?','você usa algum sistema de banco de dados']):
    return 'sistema_bd'
  elif any(txt in descricao for txt in ['você usa programas de apresentação']):
    return 'programas_slides'
  elif any(txt in descricao for txt in ['você usa micro.p/ des.seus próprios prog.e aplic.em basic, fortran, logo ou outra?','você usa micro.p/ des seus próprios prog.e aplic.em basic, fortran, logo ou outra?','você usa micro.p/ des.seus próprios prog. e aplic. em basic, fortran, logo ou outra?','você usa micro. p/ des. seus próprios prog. e aplic. em basic, fortran, logo ou outra?','você usa software desenvolvido por você mesmo?']):
    return 'software_proprio'
  elif any(txt in descricao for txt in ['você tem kit multimídia e usa-o']):
    return 'kit_multimidia'
  elif any(txt in descricao for txt in ['você tem placa de fax/modem e usa-a:']):
    return 'placas_fax_modem'
  elif any(txt in descricao for txt in ['você aprendeu a usar o microcomputador']):
    return 'computador_aprendizado'
  elif all(txt in descricao for txt in ['quanto','computador']):
    return 'computador_qtos'
  elif 'aspirador' in descricao:
    return 'aspirador'
  elif 'freezer' in descricao:
    return 'freezer'
  elif 'geladeira' in descricao:
    return 'geladeira'
  elif all(txt in descricao for txt in ['máquina','roupa']):
    return 'maq_roupa'
  elif all(txt in descricao for txt in ['máquina','louça']):
    return 'maq_louca'
  elif any(txt in descricao for txt in ['quantos automóveis há em sua residência?','quanto automóvel há em sua residência?']):
    return 'carro_qtos'
  elif any(txt in descricao for txt in ['televisão','televisões']):
    return 'tv_qts'
  elif any(txt in descricao for txt in ['quantos vídeocassetes/dvd há em sua residência?']):
    return 'dvd_vhs_qts'
  elif all(txt in descricao for txt in ['cor','raça']):
    return 'raca'
  elif any(txt in descricao for txt in ['ensino fundamental','ens. fundamental','1º grau']):
    if 'ensino fundamental 1' in descricao:
      return 'tipo_esc_ef_1'
    elif 'ensino fundamental 2' in descricao:
      return 'tipo_esc_ef_2'
    else:
      return 'tipo_esc_ef'
  elif any(txt in descricao for txt in ['em que estabelecimento você cursou o ensino médio?','onde você cursou o ensino médio?','em que tipo de estabelecimento você cursou o ensino médio','em que tipo de estabelecimento você cursou o 2º grau?','em que tipo de estabelecimento de ensino você cursou o 2º grau?']):
    return 'tipo_esc_em'
  elif any(txt in descricao for txt in ['caso tenha estudado em colégio técnico, assinale de que tipo era seu colégio:']):
    return 'coltec_tipo'
  elif any(txt in descricao for txt in ['você interrompeu seus estudos em algum momento, durante o ens.fund.ou médio?']):
    return 'interromp_estudos'
  elif any(txt in descricao for txt in ['caso tenha parado de estudar o ens. fund. ou médio, resp.: qual o motivo?']):
    return 'interromp_estudos_motivo'
  elif any(txt in descricao for txt in ['caso tenha parado de estudar, resp: quanto tempo?']):
    return 'interromp_estudos_tempo'
  elif all(txt in descricao for txt in ['concluiu','concluirá','curso']):
    return 'tipo_curso_em'
  elif ('ensino médio' in descricao or '2º grau' in descricao) and any(txt in descricao for txt in ['turno','período']):
    return 'periodo_em'
  elif any(txt in descricao for txt in ['você frequenta ou frequentou cursinho pré-vestibular?','você freqüentou algum curso pré-vestibular?','você realizou curso pré-vestibular?','você realizou cursinho pré-vestibular?']):
    return 'cursinho'
  elif any(txt in descricao for txt in ['que motivo que o(a) levou a freqüentar curso pré-vestibular?','qual o principal motivo que o(a) levou a fazer cursinho?','qual o principal motivo que o(a) levou a fazer curso pré-vestibular?','qual o principal motivo que o levou a fazer curso pré-vestibular?']):
    return 'cursinho_motivo'
  elif any(txt in descricao for txt in ['se você não fez cursinho, qual o motivo principal de não fazê-lo?','se você não fez curso pré-vestibular, qual o motivo principal de não fazê-lo?']):
    return 'cursinho_nao_motivo'
  elif any(txt in descricao for txt in ['durante quanto tempo você freqüentou curso pré-vestibular?','durante quanto tempo você fez cursinho?','durante quanto tempo você fez curso pré-vestibular?']):
    return 'cursinho_tempo'
  elif any(txt in descricao for txt in ['que tipo de cursinho você freqüentou?','que tipo de curso pré-vestibular você freqüentou?','que tipo de curso pré-vestibular você frequentou?']):
    return 'cursinho_tipo'
  elif any(txt in descricao for txt in ['você recebeu algum tipo de bolsa de estudos no cursinho?']):
    return 'cursinho_bolsa'
  elif any(txt in descricao for txt in ['em que período você freqüentou o cursinho?']):
    return 'cursinho_periodo'
  elif any(txt in descricao for txt in ['relação ao domínio de líng.estrang., em que situação você se enquadra melhor?','relação ao domínio de línguas estrang., em que situação você se enquadra melhor?','relação ao domínio de líng. estrang., em que situação você se enquadra melhor?','relação ao domínio de línguas estrangeiras, em que situação você se enquadra melhor?','relação ao domínio de línguas estrang, em que situação você se enquadra melhor?']):
    return 'idiomas'
  elif any(txt in descricao for txt in ['na sua família fala-se']):
    return 'idiomas_fam'
  elif any(txt in descricao for txt in ['no caso de falar outro idioma em casa, qual  é ele?']):
    return 'idiomas_fam_quais'
  elif any(txt in descricao for txt in ['onde você estudou ou estuda francês?']):
    return 'escola_frances'
  elif any(txt in descricao for txt in ['por quanto tempo?']):
    return 'escola_frances_tempo'
  elif any(txt in descricao for txt in ['você acha que saber francês é relevante para a sua área de interesse?']):
    return 'frances_relevancia'
  elif any(txt in descricao for txt in ['você já fez ou está fazendo algum curso superior?','você já iniciou ou está cursando algum curso superior?','você já fez ou vem fazendo algum curso superior?']):
    return 'univ_outra'
  elif all(txt in descricao for txt in ['motivo','unicamp']):
    return 'unicamp_motivo'
  elif 'motivo' in descricao and any(txt in descricao for txt in ['1ª opção','primeira opção']):
    return 'opc1_motivo'
  elif all(txt in descricao for txt in ['renda','total','família']):
    return 'renda_sm'
  elif all(txt in descricao for txt in ['vivem','renda']):
    return 'renda_qtas'
  elif all(txt in descricao for txt in ['contribuem','renda']):
    return 'renda_contrib_qtas'
  elif any(txt in descricao for txt in ['qual a situação da moradia em que você reside?']):
    return 'moradia_situacao'
  elif any(txt in descricao for txt in ['como você mora?']):
    return 'moradia_como'
  elif any(txt in descricao for txt in ['se aprovado neste vestibular, qual será sua mais provável situação de moradia?']):
    return 'moradia_pos_aprov'
  elif all(txt in descricao for txt in ['ocupação','pai']):
    return 'ocup_pai'
  elif any(txt in descricao for txt in ['qual é ou era a situação do resp. p/ você (ex: pai, padrasto, tio avô) no trabalho?','qual é ou era a situação do seu pai no trabalho?','qual é ou era a situação de seu pai no trabalho?']):
    return 'trabalha_pai'
  elif any(txt in descricao for txt in ['há ou havia outras pessoas trabalhando para ele ou sob suas ordens?']):
    return 'subordinados_pai'
  elif any(txt in descricao for txt in ['qual das seguintes altern. melhor expressa a atual situação de seu pai no trabalho?','qual das seguintes alterna.melhor expressa a atual situação de seu pai no trabalho?','qual das seguintes alterna. melhor expressa a atual situação de seu pai no trabalho?','qual das seguintes alternativas melhor expressa a atual situação de seu pai no trabalho?']):
    return 'situacao_pai'
  elif all(txt in descricao for txt in ['ocupação','mãe']):
    return 'ocup_mae'
  elif any(txt in descricao for txt in ['qual é ou era a situação do resp. p/ você (ex: mãe, madrasta, tia, avó)?','qual é ou era a situação da sua mãe no trabalho?','qual é ou era a situação de sua mãe no trabalho?','qual é ou era a situação de sua mãe?']):
    return 'trabalha_mae'
  elif any(txt in descricao for txt in ['há ou havia outras pessoas trabalhando para ela ou sob suas ordens?']):
    return 'subordinados_mae'
  elif any(txt in descricao for txt in ['qual das seguintes altern. melhor expressa a atual situação de sua mãe no trabalho?','qual das seguintes alterna.melhor expressa a atual situação de sua mãe no trabalho?','qual das seguintes alterna. melhor expressa a atual situação de sua mãe no trabalho?']):
    return 'situacao_mae'
  elif 'instrução' in descricao and any(txt in descricao for txt in ['do','pai']):
    return 'educ_pai'
  elif 'instrução' in descricao and any(txt in descricao for txt in ['da','mãe']):
    return 'educ_mae'
  elif all(txt in descricao for txt in ['exerce','atividade remunerada']):
    return 'trabalha'
  elif all(txt in descricao for txt in ['participação','família']):
    return 'contribui_renda_fam'
  elif any(txt in descricao for txt in ['você foi reprovado em alguma série do 2º grau?','você foi reprovado em alguma série do ensino médio (2º grau)?']):
    return 'reprovacao_em'
  elif any(txt in descricao for txt in ['em que ano você fez ou fará o vestibular pela primeira vez?']):
    return 'primeiro_vest'
  elif any(txt in descricao for txt in ['sem levar em consid. exper. c/ treineiro, você já prestou algum vest. anterior.? quantos?','você já prestou algum ex.vest.anteriormente (treineiro não conta)? quantos?','você já prestou algum exame vest. anteriormente (treineiro não conta)? quantos?','você já prestou algum exame vestibular anteriormente (treineiro não conta)? quantos?','em quantas instituições (universidades, faculdades) você já prestou vestibular?','em quantas instituições (universidades, faculdades ) você já prestou vestibular?']):
    return 'vest_qts'
  elif any(txt in descricao for txt in ['se você já prestou outro(s) vestibular(es), indique em qual(is) instituição(ões)','se você já prestou outro(s) vestibular(es), em qual(is) instituição(ões)?','se você já prestou outro(s) vestibular(es) em qual(is) instituição(ões)?']):
    return 'vest_quais'
  elif any(txt in descricao for txt in ['você prestará vestibular, no ano']):
    return 'vest_outro'
  elif any(txt in descricao for txt in ['se já fez ou está faz. curso sup., qual das seguintes altern. melhor expres.sua situação?','se já fez ou vem fazendo algum curso superior, qual das seguintes alternativas melhor expressa sua situação no referido curso?','se já fez ou está fazendo curso sup., qual das seg.altern.melhor expres.sua situação?','se já fez ou está faz. curso sup., qual das seguintes altern. melhor expres. sua situação?','se já fez ou está fazendo curso sup., qual das seg. altern. melhor expres. sua situação?','se já fez ou está faz.curso sup., qual das seguintes altern. melhor expres.sua situação?','se já fez ou está faz.curso sup., qual das seguintes altern.melhor expres.sua situação?','se já fez ou está faz.curso sup., qual das seguintes altern. melhor expres. sua situação?','se já fez ou está faz.curso sup., qual das seguintes altern.melhor expres. sua situação?']):
    return 'other_univreas'
  elif any(txt in descricao for txt in ['qual a instituição em que você já está ou esteve matriculado?','qual a instituição em que já está ou esteve matriculado?']):
    return 'univ_outra_inst'
  elif any(txt in descricao for txt in ['da relação abaixo, qual a disciplina que você mais gostaria de continuar estudando?']):
    return 'disciplina_favorita'
  elif any(txt in descricao for txt in ['o que você espera, em primeiro lugar, de um curso universitário?']):
    return 'expectativa_curso'
  elif any(txt in descricao for txt in ['como você se posiciona frente às carreiras ou cursos oferecidos pela universidade?']):
    return 'interesse_curso'
  elif any(txt in descricao for txt in ['qual a opinião de seus pais sobre a sua escolha profissional?']):
    return 'opiniao_pais'
  elif any(txt in descricao for txt in ['quanto à sua primeira opção, você se considera', 'quanto à sua primeira opção, você considera']):
    return 'career_decis'
  elif any(txt in descricao for txt in ['você escolheu a carreira ou curso no qual está se inscrevendo em 1ª opção baseando-se','você escolheu a carreira ou curso para no qual está inscrevendo em 1ª opção baseando-se']):
    return 'career_decishow'
  elif any(txt in descricao for txt in ['se você abando.ou pretende abandonar o curso superior já iniciado, qual seria o motivo?','se você abandonou ou pretende abandonar o curso superior já iniciado, qual seria o motivo?','se você abandonou ou pretende abandonar o curso superior já iniciado, qual o principal motivo que o levou ou levará a esta decisão?','se você abandonou ou pretende abandonar o curso superior já iniciado, qual o motivo?']):
    return 'other_univdropreas'
  elif any(txt in descricao for txt in ['quais as atividades extraclasse de que você mais participa?']):
    return 'extra_activ'
  elif any(txt in descricao for txt in ['com qual das atividades abaixo citadas você ocupa mais tempo?']):
    return 'other_activ'
  elif any(txt in descricao for txt in ['qual o meio que você mais utiliza para se manter informado sobre os acontec. atuais?','qual o meio que você mais utiliza p/ manter informado sobre os acontecimentos atuais?','qual o meio que você mais utiliza p/ manter informado(a) sobre os acontecim.atuais?','qual o meio que mais utiliza para se manter informado(a) sobre os acontec. atuais?','qual o meio que você mais utiliza p/ manter informado(a) sobre os acontec.atuais?','qual o meio que você mais utiliza para se manter informado(a) sobre os acontec.atuais?','qual o meio que você mais utiliza p/ manter informado(a) sobre os acontec. atuais?']):
    return 'news_media'
  elif any(txt in descricao for txt in ['dos tipos de revistas abaixo citados, qual você mais lê?','dos tipos de revistas e/ou jornais de lazer abaixo citados, qual você mais lê?','dos tipos de revistas e/ou jornais abaixo citados, qual você mais lê?']):
    return 'magazine_type'
  elif any(txt in descricao for txt in ['além dos textos didáticos e informativos, o que você mais lê?']):
    return 'read_type'
  elif any(txt in descricao for txt in ['muitos hj. estão deix.os cigarros p/ acharem que são prejs. à saúde. você estaria entre','muitos hj. estão deix. os cigarros p/ acharem que são prejs. à saúde. você estaria entre']):
    return 'cigarro_uso'
  elif any(txt in descricao for txt in ['com qual frequência você lê notícias e reportagens (impresso/internet)?']):
    return 'noticias_freq'
  elif any(txt in descricao for txt in ['com qual frequência você lê gibis, mangá (impresso/internet)?']):
    return 'gibis_freq'
  elif any(txt in descricao for txt in ['com qual frequência você lê livros (não escolares)?']):
    return 'livros_freq'
  elif any(txt in descricao for txt in ['com qual frequência você lê blogs, sites?']):
    return 'blogs_freq'
  elif any(txt in descricao for txt in ['com qual frequência você lê textos religiosos?']):
    return 'religiosos_freq'
  elif any(txt in descricao for txt in ['quantas motocicletas há em sua residência?']):
    return 'motos_qts'
  elif any(txt in descricao for txt in ['quantos micro-ondas há em sua residência?']):
    return 'microondas_qts'
  elif any(txt in descricao for txt in ['quantas secadoras de roupa há em sua residência?']):
    return 'secadora_qts'
  elif any(txt in descricao for txt in ['há água encanada em sua residência?']):
    return 'agua_encanada'
  elif any(txt in descricao for txt in ['há rua pavimentada em sua residência?']):
    return 'rua_pavimentada'
  elif any(txt in descricao for txt in ['quantos aparelhos de som há em sua residência?']):
    return 'som_qts'
  elif any(txt in descricao for txt in ['quantos dvds há em sua residência?']):
    return 'dvd_qts'
  elif any(txt in descricao for txt in ['quanto videocassete há em sua residência?','quantos vídeocassetes há em sua residência?']):
    return 'vhs_qts'
  
  
  return 'TODO'

def get_questions(path):
  df = read_from_db(path, sheet_name='questoes')

  # Filtra as linhas do questionário com a descrição da pergunta
  df_questoes = df[df['resposta'] == 99]
  # Filtra as linhas do questionário com as respostas para a pergunta
  df_respostas = df[df['resposta'] != 99]


  df_questoes['descricao'] = df_questoes['descricao'].map(filtrar_perguntas)
  # df_questoes = df_questoes[df_questoes['descricao'] != 'TODO']
  df_questoes = df_questoes.reindex(columns=['questao','descricao'])

  questoes_dict = df_questoes.set_index(['questao']).to_dict()['descricao']
  
  df_respostas['questao'] = df_respostas['questao'].map(questoes_dict)
  df_respostas = df_respostas.dropna()
  df_respostas = df_respostas.reindex(columns=['questao','resposta','descricao'])
  
  '''
    df_respostas é um DataFrame auxiliar criado para verificar as possíveis respostas
    para cada pergunta de cada ano
  '''

  return df_questoes, df_respostas