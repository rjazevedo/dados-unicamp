from comvest.utilities.io import read_from_db


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
  elif any(txt in descricao for txt in ['quanto videocassete há em sua residência?','quantos dvds há em sua residência?','quantos vídeocassetes/dvd há em sua residência?']):
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
  elif any(txt in descricao for txt in ['relação ao domínio de líng.estrang., em que situação você se enquadra melhor?','relação ao domínio de línguas estrang., em que situação você se enquadra melhor?','relação ao domínio de líng. estrang., em que situação você se enquadra melhor?','relação ao domínio de línguas estrangeiras, em que situação você se enquadra melhor?','relação ao domínio de línguas estrang, em que situação você se enquadra melhor?']):
    return 'idiomas'
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
  elif all(txt in descricao for txt in ['qual a situação da moradia em que você reside?']):
    return 'moradia_situacao'
  elif all(txt in descricao for txt in ['ocupação','pai']):
    return 'ocup_pai'
  elif any(txt in descricao for txt in ['qual é ou era a situação do seu pai no trabalho?','qual é ou era a situação de seu pai no trabalho?']):
    return 'trabalha_pai'
  elif all(txt in descricao for txt in ['ocupação','mãe']):
    return 'ocup_mae'
  elif any(txt in descricao for txt in ['qual é ou era a situação da sua mãe no trabalho?','qual é ou era a situação de sua mãe no trabalho?']):
    return 'trabalha_mae'
  elif 'instrução' in descricao and any(txt in descricao for txt in ['do','pai']):
    return 'educ_pai'
  elif 'instrução' in descricao and any(txt in descricao for txt in ['da','mãe']):
    return 'educ_mae'
  elif all(txt in descricao for txt in ['exerce','atividade remunerada']):
    return 'trabalha'
  elif all(txt in descricao for txt in ['participação','família']):
    return 'contribui_renda_fam'
  return 'TODO'

def get_questions(path):
  df = read_from_db(path, sheet_name='questoes')

  # Filtra as linhas do questionário com a descrição da pergunta
  df_questoes = df[df['resposta'] == 99]
  # Filtra as linhas do questionário com as respostas para a pergunta
  df_respostas = df[df['resposta'] != 99]


  df_questoes['descricao'] = df_questoes['descricao'].map(filtrar_perguntas)
  df_questoes = df_questoes[df_questoes['descricao'] != 'TODO']
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