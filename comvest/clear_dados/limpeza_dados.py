import glob
import re
import pandas as pd
from unidecode import unidecode
pd.options.mode.chained_assignment = None  # default='warn'


# Função para concatenar dia, mês e ano
def data_nasc(row, df):
  if ('DATA_NASC' in df.columns) or ('DAT_NASC' in df.columns) or ('DTNASC' in df.columns):
    if 'DATA_NASC' in df.columns:
      data = row['DATA_NASC']
    elif 'DAT_NASC' in df.columns:
      data = row['DAT_NASC']
    else:
      data = row['DTNASC']

    data = str(data)

    if data == 'nan': return ('-')

    if len(data) <= 6:
      data = data[:-2] + '19' + data[-2:]

    ano = data[-4:]
    mes = data[-6:-4]
    dia = data.replace(data[-6:], '')

    if len(data) < 8:
      dia = '0' + dia

    res = dia + mes + ano

  elif all(x in df.columns for x in ('DIA','MES','ANO')):
    dia = row['DIA'].zfill(2)
    mes = row['MES'].zfill(2)
    ano = row['ANO']

    if len(ano) < 4:
      ano = '19' + ano

    res = "{0}{1}{2}".format(dia, mes, ano)
  
  else:
    # Documento sem coluna(s) com data de nascimento
    res = '-'

  return res

def tratar_inscricao(df):
  # Checa Número de Inscrição de acordo com as diferentes variações no nome da coluna e retira o '\.0' da string
  if 'INSC' in df.columns:
    df['INSC'] = df['INSC'].astype(str).replace('\.0', '', regex=True)
  elif 'INSC_CAND' in df.columns:
    df['INSC'] = df['INSC_CAND'].astype(str).replace('\.0', '', regex=True)
  elif 'INSC_cand' in df.columns:
    df['INSC'] = df['INSC_cand'].astype(str).replace('\.0', '', regex=True)
  elif 'INSCRICAO' in df.columns:
    df['INSC'] = df['INSCRICAO'].astype(str).replace('\.0', '', regex=True)
  
  return df

def tratar_CPF(df):
  # Checa se existe a coluna de CPF
  if 'CPF' in df.columns:
    df['CPF'] = df['CPF'].map(lambda cpf: cpf if len(cpf) == 11 else cpf.zfill(11))
  else:
    df.insert(loc=1, column='CPF', value='-')

  return df

def tratar_doc(df):
  if 'RG' in df.columns:
    df.rename({'RG': 'DOC'}, axis=1, inplace=True)
  elif 'DOC3' in df.columns:
    df.rename({'DOC3': 'DOC'}, axis=1, inplace=True)

  return df

def tratar_nome(df):
  # Se o nome é dado por NOME_CAND ou NOMEOFIC, entao renomeia a coluna para NOME
  if 'NOME_CAND' in df.columns:
    df.rename({'NOME_CAND': 'NOME'}, axis=1, inplace=True)
  elif 'NOMEOFIC' in df.columns:
    df.rename({'NOMEOFIC': 'NOME'}, axis=1, inplace=True)
  elif 'NOME_cand' in df.columns:
    df.rename({'NOME_cand': 'NOME'}, axis=1, inplace=True)

  return df

def tratar_nome_pai(df):
  if 'PAI' in df.columns:
    df.rename({'PAI': 'NOME_PAI'}, axis=1, inplace=True)    

  return df

def tratar_nome_mae(df):
  if 'MAE' in df.columns:
    df.rename({'MAE': 'NOME_MAE'}, axis=1, inplace=True)

  return df

def tratar_nacionalidade(df):
  for col in df.columns:
    if col in {'NACIONALID','NACION','NACIONALIDADE'}:
      df.rename({col: 'NACIONALIDADE'}, axis=1, inplace=True)

      return df

  return df

def tratar_mun_nasc(df):
  for col in df.columns:
    if col in {'MUNICIPIO_NASC','MU_NASC','MUNIC_NASC','CIDNASC','CIDNAS'}:
      df.rename({col: 'MUN_NASC'}, axis=1, inplace=True)
      df['MUN_NASC'] = df['MUN_NASC'].map(lambda mun: unidecode(str(mun)).upper())

      return df

  return df

def tratar_uf_nasc(df):
  for col in df.columns:
    if col in {'UFNASC','EST_NASC','UFNAS'}:
      df.rename({col: 'UF_NASC'}, axis=1, inplace=True)

      return df

  return df

def tratar_cep(df):
  for col in df.columns:
    if col in {'CEP','CEPEND','CEP_END','CEP3'}:
      df.rename({col: 'CEP_RESID'}, axis=1, inplace=True)

      df['CEP_RESID'] = df['CEP_RESID'].map(lambda cep: re.sub(r'[^0-9]','',str(cep)))
      # df['CEP_RESID'] = df['CEP_RESID'].map(lambda cep: '{:<08s}'.format(cep) if cep != '' else cep)

      return df

  return df

def tratar_mun_resid(df):
  for col in df.columns:
    if col in {'MUEND','MUNIC_END','MUNICIPIO','CID','CIDEND'}:
      df.rename({col: 'MUN_RESID'}, axis=1, inplace=True)
      df['MUN_RESID'] = df['MUN_RESID'].map(lambda mun: unidecode(str(mun)).upper())

      return df

  return df

def tratar_uf_resid(df):
  # Se a UF de Residência é dado por UFEND, UF_END ou ESTADO, entao renomeia a coluna para UF_RESID
  if 'UFEND' in df.columns:
    df.rename({'UFEND': 'UF_RESID'}, axis=1, inplace=True)
  elif 'UF_END' in df.columns:
    df.rename({'UF_END': 'UF_RESID'}, axis=1, inplace=True)
  elif 'ESTADO' in df.columns:
    df.rename({'ESTADO': 'UF_RESID'}, axis=1, inplace=True)
  elif 'EST' in df.columns:
    df.rename({'EST': 'UF_RESID'}, axis=1, inplace=True)
  
  return df

def tratar_opvest(df,date,path):
  # Checa colunas de opção de curso no vestibular
  for col in df.columns:
    if any(opc in col for opc in {'OPCAO1','OP1','OPCAO1OR'}):
      df.rename({col: 'OPCAO1'}, axis=1, inplace=True)
      df['OPCAO1'] = pd.to_numeric(df['OPCAO1'], errors='coerce')
    if any(opc in col for opc in {'OPCAO2','OP2','OPCAO2OR'}):
      df.rename({col: 'OPCAO2'}, axis=1, inplace=True)
      df['OPCAO2'] = pd.to_numeric(df['OPCAO2'], errors='coerce')
    if any(opc in col for opc in {'OPCAO3','OP3'}):
      df.rename({col: 'OPCAO3'}, axis=1, inplace=True)
      df['OPCAO3'] = pd.to_numeric(df['OPCAO3'], errors='coerce')
    
  # Opcao 1 = 22 (Musica) - deve-se remapear para o codigo referente a enfase, obtida no perfil
  if (date == 2001) or (date == 2002) or (date == 2003):
    emphasis = pd.read_excel(path, sheet_name='perfil', usecols=['insc_cand','opcao1'], dtype=str)
  
    df.drop(columns='OPCAO1', errors='ignore', inplace=True)

    df = df.merge(emphasis, how='inner', left_on=['INSC'], right_on=['insc_cand'])
    df.rename({'opcao1':'OPCAO1'}, axis=1, inplace=True)

  return df

def tratar_escola(df):
  # Checa coluna de escola do ensino médio do candidato
  for col in df.columns:
    if col in {'NOMEESC','NOME_ESC','ESCOLAEM','ESCOLA','ESC2'}:
      df.rename({col: 'ESCOLA_EM'}, axis=1, inplace=True)
      df['ESCOLA_EM'] = df['ESCOLA_EM'].map(lambda esc: unidecode(str(esc)).upper())

      return df

  return df

def tratar_mun_escola(df):
  # Checa coluna do município da escola do ensino médio do candidato
  for col in df.columns:
    if col in {'MUESC','MUN_ESC','MUN_ESCOLA','MUNESC','MUNICIPIO_ESCOLA','CIDESC'}:
      df.rename({col: 'MUN_ESC_EM'}, axis=1, inplace=True)
      df['MUN_ESC_EM'] = df['MUN_ESC_EM'].map(lambda mun: unidecode(str(mun)).upper())

      return df
  
  return df

def tratar_uf_escola(df):
  # Checa coluna da UF onde se localiza a escola do ensino médio do candidato
  for col in df.columns:
    if col in {'UFESC','UF_ESC','ESTADO_ESC','ESTESC','UF_ESCOLA','ESTADO_ESCOLA','EST_ESCOLA'}:
      df.rename({col: 'UF_ESCOLA_EM'}, axis=1, inplace=True)

      return df
    
  return df

def tratar_tipo_escola(df):
  # Checa coluna do tipo da escola do ensino médio do candidato
  for col in df.columns:
    if col in {'TIPOESC','TIPO_ESC','TIPO_ESCOL','TIPO_ESCOLA'}:
      df['TIPO_ESCOLA_EM'] = df.apply(lambda row: int(str(row[col]).split('.')[0]) if (str(row[col]).split('.')[0].isdigit() and 1 <= float(row[col]) <= 2) else '', axis=1)

      return df

  return df

def tratar_ano_conclu(df):
  # Checa coluna do ano de conclusão do ensino médio do candidato
  for col in df.columns:
    if col in {'ANO_CONCLU','ANOCONC','ANO_CONC','ANO_CONCLUSAO'}:
      df.rename({col: 'ANO_CONCLU_EM'}, axis=1, inplace=True)
      df['ANO_CONCLU_EM'] = df['ANO_CONCLU_EM'].map(lambda ano: ano if len(str(ano)) == 4 else ('19' + str(ano)))

      return df

  return df

def tratar_dados(df,date,path,ingresso=1):

  # Junção da data de nascimento em 1 única coluna
  df['DATA_NASC'] = df.apply(data_nasc, axis=1, args=(df,))
  df['ANO_NASC'] = df.apply(lambda row: row['DATA_NASC'][-4:] if row['DATA_NASC'] != '-' else row['DATA_NASC'], axis=1)

  # Inserir ano da base no dataframe final
  df.loc[:, 'ANO'] = date

  # Inserir tipo de ingresso na Comvest
  df.loc[:, 'TIPO_INGRESSO_COMVEST'] = ingresso


  df = tratar_inscricao(df)
  df = tratar_CPF(df)
  df = tratar_doc(df)
  df = tratar_nome(df)
  df = tratar_nome_mae(df)
  df = tratar_nome_pai(df)
  df = tratar_opvest(df,date,path)
  df = tratar_nacionalidade(df)
  df = tratar_mun_nasc(df)
  df = tratar_uf_nasc(df)
  df = tratar_cep(df)
  df = tratar_mun_resid(df)
  df = tratar_uf_resid(df)
  df = tratar_escola(df)
  df = tratar_mun_escola(df)
  df = tratar_uf_escola(df)
  df = tratar_tipo_escola(df)
  df = tratar_ano_conclu(df)


  # Rearranja colunas e as renomeia apropriadamente
  df = df.reindex(columns=['ANO','TIPO_INGRESSO_COMVEST','NOME','CPF','DOC','DATA_NASC','ANO_NASC','NOME_PAI','NOME_MAE','INSC','OPCAO1','OPCAO2','OPCAO3','NACIONALIDADE','PAIS_NASC','MUN_NASC','UF_NASC','CEP_RESID','MUN_RESID','UF_RESID','ESCOLA_EM','MUN_ESC_EM','UF_ESCOLA_EM','TIPO_ESCOLA_EM','ANO_CONCLU_EM'])
  df.columns = ['ano_vest','tipo_ingresso_comvest','nome_c','cpf','doc_c','dta_nasc_c','ano_nasc_c','nome_pai_c','nome_mae_c','insc_vest','opc1','opc2','opc3','nacionalidade','pais_nasc','mun_nasc_c','uf_nasc_c','cep_resid_c','mun_resid_c','uf_resid','esc_em','mun_esc_em','uf_esc_em','nat_esc_em','ano_conclu_em_c']

  return df


# Gets all the file names and makes a dictionary with 
# file path as key and the respective date of the file as its value
files_path = glob.glob("input/comvest/*")
files = { path: int(re.sub('[^0-9]','',path)) for path in files_path }


def extraction():
  dados_comvest = []

  for path, date in files.items():
    df = pd.read_excel(path, sheet_name='dados', dtype=str)

    df = tratar_dados(df,date,path)

    if date >= 2019:
      vi_dados = pd.read_excel(path, sheet_name='vi_dados', dtype=str)
      vo_dados = pd.read_excel(path, sheet_name='vo_dados', dtype=str)

      vi_dados = tratar_dados(vi_dados, date, path, ingresso=2)                  # 2 - Vestibular Indigena
      vo_dados = tratar_dados(vo_dados, date, path, ingresso=3)                  # 3 - Vagas Olimpicas

      df = pd.concat([df, vi_dados, vo_dados])

      if date != 2021:
        ve_dados = pd.read_excel(path, sheet_name='ve_dados', dtype=str)

        ve_dados = tratar_dados(ve_dados, date, path, ingresso=4)                # 4 - ENEM-Unicamp

        df = pd.concat([df, ve_dados])
      
    dados_comvest.append(df)


  # Exportar CSV
  dados_comvest = pd.concat(dados_comvest)
  dados_comvest.sort_values(by='ano_vest', ascending=False, inplace=True)
  dados_comvest = dados_comvest[dados_comvest['nome_c'].notnull()]

  file_name = 'dados_comvest'
  dados_comvest.to_csv("output/{}.csv".format(file_name), index=False)