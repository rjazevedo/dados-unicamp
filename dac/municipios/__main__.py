from dac.clr_vida_academica_habilitacao import cursos_habilitacoes
from dac.clr_vida_academica_habilitacao import vida_academica_habilitacao
from dac.municipios.dac import generate_mun_dac
from dac.municipios.dados_ibge import generate_ibge_data
from dac.municipios.comvest import generate_mun_comvest
from dac.utilities.io import write_output
import pandas as pd

def main():
    dac_data = generate_mun_dac() 
    # comvest_data = generate_mun_comvest()
    # concat = pd.concat(dfs, ignore_index = True)
    # concat = concat.drop_duplicates(keep=False)
    # write_output(concat, 'municipios.csv')

    # ibge_data = generate_ibge_data()
    # result = dados_cadastrais.reset_index().merge(ibge_data)
    # merge probabilístico entre od dois agora em josé ?

def is_same_person(name_a, name_b):
    first_name_a = name_a.split()[0]
    first_name_b = name_b.split()[0]
    similar_rate = SequenceMatcher(None, first_name_a, first_name_b).ratio()
    return similar_rate > 0.7

if __name__ == '__main__':
    main()