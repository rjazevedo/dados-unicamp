import pandas as pd 

dados_cadastrais = pd.read_csv('dados_cadastrais.csv')
print(dados_cadastrais.columns)
print(dados_cadastrais.shape)

historico_escolar = pd.read_csv('historico_escolar.csv')
print(historico_escolar.columns)
print(historico_escolar.shape)

resumo_por_periodo = pd.read_csv('resumo_por_periodo.csv')
print(resumo_por_periodo.columns)
print(resumo_por_periodo.shape)

vida_academica = pd.read_csv('vida_academica.csv')
vida_academica.columns = ['id', 'curso', 'curso_nivel', 'curso_atual_nome', 'ano_ingresso',
       'periodo_ingresso', 'tipo_periodo_ingresso', 'cod_tipo_ingresso',
       'tipo_ingresso', 'ano_saida', 'periodo_saida', 'tipo_periodo_saida',
       'cod_motivo_saida', 'motivo_saida', 'cr', 'cr_padrao', 'cr_medio_turma',
       'opcao_vest', 'chamada_vest', 'aa', 'cota_d', 'cota_tipo',
       'cota_descricao']

print(vida_academica.columns)
print(vida_academica.shape)

vida_academica_habilitacao = pd.read_csv('vida_academica_habilitacao.csv')
print(vida_academica_habilitacao.columns)
print(vida_academica_habilitacao.shape)


merge = pd.merge(vida_academica_habilitacao, vida_academica, on=['id', 'ano_ingresso'])
print(merge.shape)