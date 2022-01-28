from functools import reduce
import pandas as pd

dados = pd.read_csv('dados/dados_comvest.csv', dtype=str)
perfil = pd.read_csv('perfil/perfil_comvest.csv', dtype=str)
notas = pd.read_csv('notas/notas_comvest.csv', dtype=str)
matriculados = pd.read_csv('matriculados/matriculados_comvest.csv', dtype=str)

dfs = [dados, matriculados, perfil, notas]

base_comvest = reduce(lambda left,right: pd.merge(left, right, on=['ano_vest','insc_vest'], how='left'), dfs)

base_comvest = base_comvest[base_comvest['nome_c'].notnull()]

# Nao disponibilizar nome, nomes dos pais, documento, data de nascimento e CPF na base final
base_comvest.drop(columns=['nome_c','doc_c','cpf','dta_nasc_c','nome_pai_c','nome_mae_c'], inplace=True)

base_comvest.to_csv('../output/comvest_amostra.csv', index=False)