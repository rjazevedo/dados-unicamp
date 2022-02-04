from functools import reduce
from comvest.utilities.io import read_result, write_output
import pandas as pd

def merge(dropcolumns=['nome_c','doc_c','cpf','dta_nasc_c','nome_pai_c','nome_mae_c']):
    dados = read_result('dados_comvest.csv')
    perfil = read_result('perfil_comvest.csv')
    notas = read_result('notas_comvest.csv')
    matriculados = read_result('matriculados_comvest.csv')

    dfs = [dados, perfil, matriculados, notas]

    base_comvest = reduce(lambda left,right: pd.merge(left, right, on=['ano_vest','insc_vest'], how='left'), dfs)

    # Retira variáveis que não serão disponibilizadas na base final
    base_comvest.drop(columns=dropcolumns, inplace=True)

    FILE_NAME = 'comvest_amostra.csv'
    write_output(base_comvest, FILE_NAME)