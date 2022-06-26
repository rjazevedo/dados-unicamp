import pandas as pd
dados_cadastrais = pd.read_csv('dados_cadastrais.csv')
historico_escolar = pd.read_csv('historico_escolar.csv')
resumo = pd.read_csv('resumo_por_periodo.csv')
vida_academica = pd.read_csv('vida_academica.csv')
vida_academica_habilitacao = pd.read_csv('vida_academica_habilitacao.csv')

dados_cadastrais = dados_cadastrais.drop('id', 1)

historico_escolar = historico_escolar.drop('id',1)
resumo = resumo.drop('id',1)
vida_academica = vida_academica.drop('id',1)
vida_academica_habilitacao = vida_academica_habilitacao.drop('id',1)

print(dados_cadastrais.columns)
print(historico_escolar.columns)
print(resumo.columns)
print(vida_academica.columns)
print(vida_academica_habilitacao.columns)

dados_cadastrais.to_csv('dados_cadastrais.csv')
historico_escolar.to_csv('historico_escolar.csv')
resumo.to_csv('resumo_por_periodo.csv')
vida_academica.to_csv('vida_academica.csv')
vida_academica_habilitacao.to_csv('vida_academica_habilitacao.csv')