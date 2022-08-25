import pandas as pd
import numpy as np
import difflib as dff
import matplotlib.pyplot as plt
import seaborn as sns
from dac.utilities.io import write_result
from dac.utilities.io import read_result as read_result_dac, write_output
from dac.utilities.io import read_from_external
from dac.uniao_dac_comvest.cursos_especiais import deal_special_students
from dac.uniao_dac_comvest.doc_part import merge_by_doc_part
from dac.uniao_dac_comvest.utilities import get_wrong_and_right
from dac.uniao_dac_comvest.utilities import concat_dac_comvest
from dac.uniao_dac_comvest.utilities import validar_CPF
from dac.uniao_dac_comvest.utilities import setup_comvest
from dac.uniao_dac_comvest.utilities import setup_dac
from dac.uniao_dac_comvest.utilities import set_origemCPF
from dac.uniao_dac_comvest.closest_name import get_closest_name


def generate():
    dados_comvest = setup_comvest()
    dados_dac = setup_dac()
    correct_merge_list = []

    uniao_dac_comvest = pd.merge(dados_dac, dados_comvest, how='left',  on=['insc_vest', 'ano_ingresso_curso'], suffixes=('','_comvest'))
    wrong_and_right = get_wrong_and_right(uniao_dac_comvest, correct_merge_list)
    
    uniao_dac_comvest = pd.merge(wrong_and_right[1], dados_comvest, how='left',  on=['nome', 'ano_ingresso_curso', 'dta_nasc'], suffixes=('','_comvest'))
    wrong_and_right = get_wrong_and_right(uniao_dac_comvest, correct_merge_list)
    
    uniao_dac_comvest = pd.merge(wrong_and_right[1], dados_comvest, how='left',  on=['ano_ingresso_curso', 'dta_nasc', 'doc'], suffixes=('','_comvest'))
    wrong_and_right = get_wrong_and_right(uniao_dac_comvest, correct_merge_list)

    uniao_dac_comvest = pd.merge(wrong_and_right[1], dados_comvest, how='left',  on=['nome', 'ano_ingresso_curso', 'doc'], suffixes=('','_comvest'))
    wrong_and_right = get_wrong_and_right(uniao_dac_comvest, correct_merge_list)
    
    wrong = deal_special_students(wrong_and_right[1], correct_merge_list)
    wrong = merge_by_doc_part(wrong, dados_comvest, correct_merge_list)
    get_closest_name(wrong, dados_comvest, correct_merge_list)

    generate_planilha_paulo(correct_merge_list)
    concat = concat_dac_comvest(correct_merge_list, dados_comvest)
    final_df = padronize_colums(concat)
    write_result(final_df, "uniao_dac_comvest.csv")


def generate_planilha_paulo(merge_list):
    dac_df = pd.concat(merge_list[1:])
    df_paulo = dac_df.loc[:, ['identif', 'insc_vest', 'insc_vest_comvest', 'ano_ingresso_curso', 'nome', 'nome_comvest', 
                          'dta_nasc', 'dta_nasc_comvest', 'curso', 'curso_comvest', 'doc', 'doc_comvest']]
    write_result(df_paulo, 'planilha_paulo.csv')


def padronize_colums(df):
    df['cpf'].fillna('-', inplace=True)
    df['cpf_comvest'].fillna('-', inplace=True)

    valida_cpf = np.vectorize(validar_CPF)
    df['cpf'] = valida_cpf(df['cpf'], df['cpf_comvest'])

    origem_cpf = np.vectorize(set_origemCPF)
    df['origem_cpf'] = origem_cpf(df['cpf'], df['cpf_comvest'])
 
    df['nome'] = df['nome'].fillna(df['nome_comvest'])
    df['dta_nasc'] = df['dta_nasc'].fillna(df['dta_nasc_comvest'])
    df['doc'] = df['doc'].fillna(df['doc_comvest'])

    df = df.loc[:, ['insc_vest','nome','cpf','origem_cpf','dta_nasc','doc','ano_ingresso_curso']]
    return df