import pandas as pd
import re
from dac.uniao_dac_comvest.utilities import get_wrong_and_right

# Da merge dos casos que não deram match usando apenas um pedaço do doc
def merge_by_doc_part(wrong_pre, dados_comvest, correct_merge_list):
    wrong_pre_temp = create_doc_key(wrong_pre.copy(), 5)
    comvest_temp = create_doc_key(dados_comvest.copy(), 5)
    merge = pd.merge(wrong_pre_temp, comvest_temp, how ='left', on=['doc_key', 'dta_nasc', 'curso', 'ano_ingresso_curso'], suffixes=('','_comvest'))
    merge = merge.drop(columns = ["doc_key"])
    wrong_and_right = get_wrong_and_right(merge, correct_merge_list)
    wrong = wrong_and_right[1]

    wrong_pre_temp = create_doc_key(wrong.copy(), 7)
    comvest_temp = create_doc_key(dados_comvest.copy(), 7)
    merge = pd.merge(wrong_pre_temp, comvest_temp, how ='left', on=['doc_key', 'curso', 'ano_ingresso_curso'], suffixes=('','_comvest'))
    merge = merge.drop(columns = ["doc_key"])
    wrong_and_right = get_wrong_and_right(merge, correct_merge_list)
    wrong = wrong_and_right[1]

    # nome identico
    wrong_pre_temp = create_doc_key(wrong.copy(), 3)
    comvest_temp = create_doc_key(dados_comvest.copy(), 3)
    merge = pd.merge(wrong_pre_temp, comvest_temp, how ='left', on=['nome', 'doc_key', 'curso', 'ano_ingresso_curso'], suffixes=('','_comvest'))
    merge = merge.drop(columns = ["doc_key"])
    wrong_and_right = get_wrong_and_right(merge, correct_merge_list)
    wrong = wrong_and_right[1]

    wrong_pre_temp = create_doc_key(wrong.copy(), 7)
    comvest_temp = create_doc_key(dados_comvest.copy(), 7)
    wrong_pre_temp = create_nome_key(wrong_pre_temp.copy(), 10)
    comvest_temp = create_nome_key(comvest_temp.copy(), 10)
    merge = pd.merge(wrong_pre_temp, comvest_temp, how ='left', on=['nome_key', 'doc_key', 'ano_ingresso_curso'], suffixes=('','_comvest'))
    merge = merge.drop(columns = ["doc_key", 'nome_key'])
    wrong_and_right = get_wrong_and_right(merge, correct_merge_list)
    wrong = wrong_and_right[1]

    return wrong


# Função que cria coluna com apenas alguns valores do nome
def create_nome_key(df, name_size):
    df_temp = df.copy()
    df_temp['nome_key'] = df['nome'].map(lambda x: x.replace(" ", ""))
    df_temp['nome_key'] = df_temp['nome_key'].map(lambda x: x[:name_size])
    return df_temp


# Função que cria coluna com apenas alguns valores do doc
def create_doc_key(df, doc_size):
    df_temp = df.copy()
    df_temp['doc_key'] = df['doc'].map(lambda x: re.sub('0', '', x))
    df_temp['doc_key'] = df_temp['doc_key'].map(lambda x: x[:doc_size])
    return df_temp