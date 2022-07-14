import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
import seaborn as sns
from dac.utilities.format import fill_doc
from dac.utilities.io import write_result
from dac.utilities.io import read_result as read_result_dac, write_output
from comvest.utilities.io import read_result as read_result_comvest

from dac.uniao_dac_comvest import testes

def validar_CPF(cpf_dac, cpf_comvest):
    if cpf_dac != '-':
        filled_cpf = str(cpf_dac).zfill(11)
    else:
        filled_cpf = str(cpf_comvest).zfill(11)

    cpf = [int(char) for char in filled_cpf if char.isdigit()]

    if len(cpf) != 11:
        return '-'
    if all(cpf[i] == cpf[i+1] for i in range (0, len(cpf)-1)):
        return '-'

    #  Valida os dois dígitos verificadores
    for i in range(9, 11):
        valor = sum((cpf[num] * (i+1-num) for num in range(0, i)))
        digito = ((valor * 10) % 11) % 10
        if digito != cpf[i]:
            return '-'

    cpf_valido = [str(d) for d in cpf]
    
    return ''.join(cpf_valido)

def set_origemCPF(cpf_dac, cpf_comvest):
    '''
    Coluna Origem CPF:
        2 se veio da DAC
        1 se veio da Comvest
        0 se não temos CPF nem na DAC nem na Comvest
    '''

    if cpf_dac == '-' and cpf_comvest == '-':
        return 0
    if cpf_dac == '-' and cpf_comvest != '-':
        return 1
    if cpf_dac != '-':
        return 2

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

    #-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # testes.encontrar_vestibular_dos_alunos_109_110(wrong_and_right[1], dados_dac)

    # Apenas tratamento pre 99
    wrong = wrong_and_right[1]
    filt = (wrong.origem == 'pre')
    wrong = wrong[filt]

    wrong_and_right = merge_faltantes_pre_99(wrong, dados_comvest, correct_merge_list)

    return 
    final_df = concat_wrong_and_right(wrong_and_right[1], correct_merge_list)
    final_df.drop_duplicates(subset=['insc_vest','ano_ingresso_curso'], inplace=True)
    write_result(final_df, 'uniao_dac_comvest.csv')

def concat_wrong_and_right(wrong, right):
    wrong = create_colums_for_concat(wrong)
    right = pd.concat(right)

    wrong_and_right = pd.concat([right, wrong])

    final_df = padronize_colums(wrong_and_right)
    return final_df

# Completa as colunas que faltam de um df
def create_colums_for_concat(df):
    if 'insc_vest_comvest' not in df.columns:
        df['insc_vest_comvest'] = df['insc_vest']
    if 'dta_nasc_comvest' not in df.columns:
        df['dta_nasc_comvest'] = df['dta_nasc']
    if 'doc_comvest' not in df.columns:
        df['doc_comvest'] = df['doc']
    if 'nome_comvest' not in df.columns:
        df['nome_comvest'] = df['nome']
    df = df.reindex(columns=['identif', 'nome', 'cpf', 'doc', 'dta_nasc', 'insc_vest',
       'ano_ingresso_curso', 'origem', 'motivo_saida', 'curso',
       'tipo_ingresso', 'nome_comvest', 'cpf_comvest', 'doc_comvest',
       'dta_nasc_comvest', 'insc_vest_comvest']) 
    return df

# Remove colunas inúteis após o merge 
def remove_discartable_columns(df):
    for column in df.columns:
        if '_comvest' in column:
            df = df.drop(columns=[column])
    return df

# Separa os registros que deram match dos que não deram
def get_wrong_and_right(df, correct_merge_list):
    filt = pd.Series(dtype=str)
    if "doc_comvest" in df.columns:
        filt = df.doc_comvest.isnull()
    elif "dta_nasc_comvest" in df.columns:
        filt = df.dta_nasc_comvest.isnull()
    else:
        filt = df.nome_comvest.isnull()

    wrong_merge = df[filt]
    wrong_merge = remove_discartable_columns(wrong_merge)
    right_merge = df[~filt].copy()
    right_merge = create_colums_for_concat(right_merge)

    correct_merge_list.append(right_merge)
    return (right_merge, wrong_merge)

# Carrega e padroniza os dados da COMVEST
def setup_comvest():
    df = read_result_comvest('dados_comvest.csv', dtype=str).loc[:, ['nome_c','cpf','doc_c','dta_nasc_c','insc_vest','ano_vest', 'opc1']]
    df.columns = ['nome','cpf','doc','dta_nasc','insc_vest','ano_ingresso_curso', 'curso']
    write_result(df, "comvest.csv")

    #df = read_result_comvest('dados_comvest.csv', dtype=str).loc[:, ['nome_c','cpf','doc_c','dta_nasc_c','insc_vest','ano_vest', 'opc1', 'opc2', 'opc3', 'tipo_ingresso_comvest']]
    #df.columns = ['nome','cpf','doc','dta_nasc','insc_vest','ano_ingresso_curso', 'opc1', 'opc2', 'opc3', 'tipo_ingresso_comvest']
    #write_result(df, "comvest_to_test.csv")

    df.dta_nasc = df.dta_nasc.astype(str).str.replace('.0', '', regex=False)    
    df.insc_vest = df.insc_vest.astype('float64')
    df.doc = df.doc.astype(str)
    df.doc = df.doc.map(lambda x: re.sub("[^0-9]", "", x))
    df.doc = fill_doc(df.doc, 15)
    df.dta_nasc = df.dta_nasc.astype(str).str.zfill(8)
    return df

# Carrega e padroniza os dados da DAC
def setup_dac():
    df = read_result_dac('dados_ingressante.csv', dtype=str).loc[:, ['identif', 'nome','cpf','doc','dta_nasc','insc_vest','ano_ingresso_curso', "origem", 'motivo_saida','curso', 'tipo_ingresso']]
    df.insc_vest.replace("", np.nan, inplace=True)
    df.insc_vest = df.insc_vest.astype('float64')
    df.doc = fill_doc(df.doc, 15)
    df.dta_nasc = df.dta_nasc.astype(str).str.zfill(8)
    return df

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

    #df.drop(columns=['cpf_dac','cpf_comvest','doc_dac','doc_comvest','nome_dac','nome_comvest','dta_nasc_dac','dta_nasc_comvest'], inplace=True)
    df.drop(columns=['cpf_comvest','doc_comvest','nome_comvest','dta_nasc_comvest'], inplace=True)
    df = df.reindex(columns=['insc_vest','nome','cpf','origem_cpf','dta_nasc','doc','ano_ingresso_curso'])
    return df

# Da merge dos casos que não deram match usando apenas u pedaço do doc
def merge_faltantes_pre_99(wrong_pre, dados_comvest, correct_merge_list):
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

    return 

# Função que cria coluna com apenas alguns valores do doc
def create_doc_key(df, doc_size):
    df_temp = df.copy()
    df_temp['doc_key'] = df['doc'].map(lambda x: re.sub('0', '', x))
    df_temp['doc_key'] = df_temp['doc_key'].map(lambda x: x[:doc_size])
    return df_temp

def plot_graphs(wrong):
    ano_ingresso_curso = wrong['ano_ingresso_curso'].astype(str)
    picture = sns.displot(ano_ingresso_curso, color='red')

    plt.title('Wrong Merge', fontsize=18)
    plt.xlabel('Year', fontsize=16)
    plt.ylabel('Frequency', fontsize=16)

    picture.figure.set_size_inches(10,8)
    picture.savefig("curso-histogram.png")