from functools import reduce
import pandas as pd

def merge(dropcolumns=['nome_c','doc_c','cpf','dta_nasc_c','nome_pai_c','nome_mae_c']):
    dados = pd.read_csv('output/dados_comvest.csv', dtype=str)
    perfil = pd.read_csv('output/perfil_comvest.csv', dtype=str)
    notas = pd.read_csv('output/notas_comvest.csv', dtype=str)
    matriculados = pd.read_csv('output/matriculados_comvest.csv', dtype=str)

    dfs = [dados, perfil, matriculados, notas]

    base_comvest = reduce(lambda left,right: pd.merge(left, right, on=['ano_vest','insc_vest'], how='left'), dfs)

    # Retira variáveis que não serão disponibilizadas na base final
    base_comvest.drop(columns=dropcolumns, inplace=True)

    base_comvest.to_csv('output/comvest_amostra.csv', index=False)