from dac.utilities.io import write_output
from dac.utilities.io import read_result
from dac.utilities.io import write_result
from dac.utilities.io import Bases
import pandas as pd
import numpy as np

def create_ids():
    nomes_comvest = read_result('dados_comvest.csv', base=Bases.RESULT_COMVEST, dtype=str).loc[:, ["nome_c", "nome_pai_c", "nome_mae_c"]]
    nomes_dac = read_result("dados_cadastrais_intermediario.csv").loc[:,['nome', 'nome_mae', 'nome_pai']]
    
    nome_c = nomes_comvest.loc[:, ["nome_c"]].rename(columns={'nome_c': 'nome'})
    nome_mae_c = nomes_comvest.loc[:, ["nome_mae_c"]].rename(columns={'nome_mae_c': 'nome'})
    nome_pai_c = nomes_comvest.loc[:, ["nome_pai_c"]].rename(columns={'nome_pai_c': 'nome'})
    nome_aluno = nomes_dac.loc[:, ["nome"]]
    nome_mae = nomes_dac.loc[:, ["nome_mae"]].rename(columns={'nome_mae': 'nome'})
    nome_pai = nomes_dac.loc[:, ["nome_pai"]].rename(columns={'nome_pai': 'nome'})

    nomes = pd.concat([nome_c, nome_mae_c, nome_pai_c, nome_aluno, nome_mae, nome_pai])
    nomes = nomes.drop_duplicates()
    nomes["id"] = np.arange(len(nomes))
    write_result(nomes, "ids_of_names.csv")