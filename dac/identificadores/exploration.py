import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import numpy as np
from os import write
from utilities.io import get_identificadores, read_result
from utilities.io import write_result

from difflib import SequenceMatcher

def get_similarity(a, b):
    if (type(a) != str) or (type(b) != str):
        return 0.0
    nomes_a = a.split()
    nomes_b = b.split()
    
    if nomes_a[0].lower() != nomes_b[0].lower() :
        return 0.0
    sobrenome_a = ' '.join(nomes_a[1:])
    sobrenome_b = ' '.join(nomes_b[1:])
    
    similar_rate = SequenceMatcher(None, sobrenome_a, sobrenome_b).ratio()
    return similar_rate



def get_similarity_series(s1, s2):
    similarity = np.vectorize(get_similarity)
    return similarity(s1, s2)

def get_relations():
    comvest_ids = get_identificadores()
    
    non_identif = read_result('explore/non_rescued.csv', dtype=str)
    
    non_identif = non_identif.loc[:,  ['identif','insc_vest','cod_tipo_ingresso', 'ano_ingresso_curso','cpf', 'nome', 'dta_nasc', 'doc', 'curso']]
    comvest_ids = comvest_ids.loc[:, ['id', 'cpf','origem_cpf','doc', 'nome', 'dta_nasc']]

    cpf_identifs = non_identif[non_identif.cpf != '-']
    non_cpf_identifs = non_identif[non_identif.cpf == '-']

    cpf_rescued = cpf_identifs.merge(comvest_ids.loc[:, ['cpf', 'id']], on=['cpf'], how ='left')
    cpf_rescued.drop_duplicates(subset=['insc_vest', 'ano_ingresso_curso'], inplace=True)
    non_rescued = cpf_rescued[cpf_rescued.id.isna()]
    cpf_rescued = cpf_rescued[~cpf_rescued.id.isna()]
    cpf_rescued['rescued'] = 'CPF'

    non_rescued.drop(['id'], axis=1, inplace=True)

    non_rescued = pd.concat([non_cpf_identifs, non_rescued])
    
    doc_identifs = non_rescued[(non_rescued.doc != '-') & (non_rescued.doc != '')]

    doc_rescued = doc_identifs.merge(comvest_ids.loc[:, ['doc', 'id']], on=['doc'], how='left')
    doc_rescued.drop_duplicates(subset=['insc_vest', 'ano_ingresso_curso'], inplace=True)
    doc_rescued = doc_rescued[~doc_rescued.id.isna()]
    doc_rescued['rescued'] = 'DOC'
    
    rescued = pd.concat([cpf_rescued, doc_rescued, non_identif])
    rescued.drop_duplicates(subset=['insc_vest', 'ano_ingresso_curso'], inplace=True, keep='first')

    non_rescued = rescued[rescued.id.isna()]
    rescued = rescued[~rescued.id.isna()]
    non_rescued.drop(['id', 'rescued'], axis=1, inplace=True)
    
    # name_date_rescued = non_rescued.merge(comvest_ids.loc[:, ['nome', 'dta_nasc', 'id']], on=['nome', 'dta_nasc'])
    # name_date_rescued.drop_duplicates(subset=['insc_vest', 'ano_ingresso_curso'], inplace=True)
    # name_date_rescued['rescued'] = 'NOME-DATA'
    # rescued = pd.concat([rescued, name_date_rescued, non_rescued])
    # rescued.drop_duplicates(subset=['insc_vest', 'ano_ingresso_curso'], inplace=True, keep='first')
    
    # non_rescued = rescued[rescued.id.isna()]
    # rescued = rescued[~rescued.id.isna()]

    # non_rescued.drop(['id', 'rescued'], axis=1, inplace=True)

    partial_name_ids = comvest_ids.loc[:, ['id', 'nome', 'dta_nasc']]
    

    partial_name_rescued = non_rescued.merge(partial_name_ids, on=['dta_nasc'])
    partial_name_rescued['similarity'] = get_similarity_series(partial_name_rescued.nome_x, partial_name_rescued.nome_y)
    partial_name_rescued.sort_values(by=['similarity'], ascending=False, inplace=True)
    partial_name_rescued.drop_duplicates(subset=['insc_vest', 'ano_ingresso_curso'], inplace=True, keep='first')
    partial_name_rescued = partial_name_rescued[partial_name_rescued.similarity > 0.7]
    partial_name_rescued.drop(['similarity', 'nome_y'], axis=1, inplace=True)
    partial_name_rescued.rename(columns={'nome_x': 'nome'})
    partial_name_rescued['rescued'] = 'PARTIAL-NAME'

    rescued = pd.concat([rescued, partial_name_rescued, non_rescued])
    rescued.drop_duplicates(subset=['insc_vest', 'ano_ingresso_curso'], inplace=True, keep='first')

    non_rescued = rescued[rescued.id.isna()]
    rescued = rescued[~rescued.id.isna()]
    non_rescued.drop(['id', 'rescued'], axis=1, inplace=True)
    
    
    non_rescued.curso.sort_values().hist()
    plt.savefig('/home/gsiqueira/project/clean_dac/results/explore/nonrescued-curso.png')
    plt.clf()

    non_rescued.ano_ingresso_curso.sort_values().hist()
    plt.savefig('/home/gsiqueira/project/clean_dac/results/explore/nonrescued-ano.png')
    plt.clf()

    rescued.curso.sort_values().hist()
    plt.savefig('/home/gsiqueira/project/clean_dac/results/explore/rescued-curso.png')
    plt.clf()

    rescued.ano_ingresso_curso.sort_values().hist()
    plt.savefig('/home/gsiqueira/project/clean_dac/results/explore/rescued-ano.png')
    plt.clf()

    write_result(rescued, 'explore/rescued_by_comvest.csv')
    write_result(non_rescued, 'explore/non_rescued.csv')