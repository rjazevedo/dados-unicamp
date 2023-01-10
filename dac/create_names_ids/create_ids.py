from dac.utilities.io import read_result
from dac.utilities.io import write_result
from dac.utilities.io import Bases
import pandas as pd
import numpy as np

RESULT_NAME = "ids_of_names.csv"
DADOS_COMVEST = 'dados_comvest.csv'
DADOS_DAC = "dados_cadastrais_intermediario.csv"

def create_ids():
    nomes_comvest = read_result(DADOS_COMVEST, base=Bases.RESULT_COMVEST, dtype=str).loc[:, ["nome_c", "nome_pai_c", "nome_mae_c"]]
    nomes_dac = read_result(DADOS_DAC, dtype=str).loc[:,['nome', 'nome_mae', 'nome_pai']]
    
    nome_c = nomes_comvest.loc[:, ["nome_c"]].rename(columns={'nome_c': 'nome'})
    nome_mae_c = nomes_comvest.loc[:, ["nome_mae_c"]].rename(columns={'nome_mae_c': 'nome'})
    nome_pai_c = nomes_comvest.loc[:, ["nome_pai_c"]].rename(columns={'nome_pai_c': 'nome'})
    nome_aluno = nomes_dac.loc[:, ["nome"]]
    nome_mae = nomes_dac.loc[:, ["nome_mae"]].rename(columns={'nome_mae': 'nome'})
    nome_pai = nomes_dac.loc[:, ["nome_pai"]].rename(columns={'nome_pai': 'nome'})

    nomes = pd.concat([nome_c, nome_mae_c, nome_pai_c, nome_aluno, nome_mae, nome_pai])
    nomes = nomes.drop_duplicates()
    nomes["id"] = np.arange(len(nomes))

    write_result(nomes, RESULT_NAME)
    #write_result(nomes, RESULT_NAME, base=Bases.TESTE)
    #teste()

def teste():
    ids_names = read_result(RESULT_NAME, base=Bases.TESTE, dtype=str)
    nomes_comvest = read_result(DADOS_COMVEST, base=Bases.RESULT_COMVEST, dtype=str).loc[:, ["nome_c", "nome_pai_c", "nome_mae_c"]]
    ids_names.rename(columns = {"nome": "nome_c"}, inplace = True)

    nomes_comvest = pd.merge(nomes_comvest, ids_names, how="left", on = ["nome_c"])
    nomes_comvest.rename(columns = {"id": "nome_id"}, inplace=True)
    ids_names.rename(columns = {"nome_c": "nome_pai_c"}, inplace = True)

    nomes_comvest = pd.merge(nomes_comvest, ids_names, how="left", on = ["nome_pai_c"])
    nomes_comvest.rename(columns = {"id": "nome_pai_id"}, inplace=True)
    ids_names.rename(columns = {"nome_pai_c": "nome_mae_c"}, inplace = True)

    nomes_comvest = pd.merge(nomes_comvest, ids_names, how="left", on = ["nome_mae_c"])
    nomes_comvest.rename(columns = {"id": "nome_mae_id"}, inplace=True)
    write_result(nomes_comvest, RESULT_NAME, base=Bases.TESTE)
