import pandas as pd
import re
import numpy as np
from dac.utilities.format import fill_doc
from dac.utilities.io import read_result as read_result_dac
from comvest.utilities.io import read_result as read_result_comvest
from dac.uniao_dac_comvest import uniao_dac_comvest
from dac.utilities.io import write_result
from dac.utilities.io import read_result as read_result_dac, write_output

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


def setup_comvest():
    curso = read_result_comvest('matriculados_comvest.csv', dtype=str).loc[:, ['ano_vest','insc_vest','curso_matric']]
    curso.columns = ['ano_ingresso_curso', 'insc_vest', 'curso']

    comvest = read_result_comvest('dados_comvest.csv', dtype=str).loc[:, ['nome_c','cpf','doc_c','dta_nasc_c','insc_vest','ano_vest']]
    comvest.columns = ['nome','cpf','doc','dta_nasc','insc_vest','ano_ingresso_curso']

    df = pd.merge(comvest, curso, how='left', on=['ano_ingresso_curso', 'insc_vest'])

    df.dta_nasc = df.dta_nasc.astype(str).str.replace('.0', '', regex=False)    
    df.insc_vest = df.insc_vest.astype('float64')
    df.doc = df.doc.astype(str)
    df.doc = df.doc.map(lambda x: re.sub("[^0-9]", "", x))
    df.doc = fill_doc(df.doc, 15)
    df.dta_nasc = df.dta_nasc.astype(str).str.zfill(8)

    df['merge_id'] = range(0, len(df))
    return df


def setup_dac():
    df = read_result_dac('dados_ingressante.csv', dtype=str).loc[:, ['identif', 'nome','cpf','doc','dta_nasc','insc_vest','ano_ingresso_curso', "origem", 'curso', 'tipo_ingresso']]
    df.insc_vest.replace("", np.nan, inplace=True)
    df.insc_vest = df.insc_vest.astype('float64')
    df.doc = fill_doc(df.doc, 15)
    df.dta_nasc = df.dta_nasc.astype(str).str.zfill(8)
    return df


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


def create_colums_for_concat(df):
    new_df = df.copy()

    if 'insc_vest_comvest' not in df.columns:
        new_df['insc_vest_comvest'] = df['insc_vest']
    if 'dta_nasc_comvest' not in df.columns:
        new_df['dta_nasc_comvest'] = df['dta_nasc']
    if 'doc_comvest' not in df.columns:
        new_df['doc_comvest'] = df['doc']
    if 'nome_comvest' not in df.columns:
        new_df['nome_comvest'] = df['nome']
    
    new_df = new_df.reindex(columns=['identif', 'nome', 'cpf', 'doc', 'dta_nasc', 'insc_vest', 'ano_ingresso_curso',
                             'origem', 'curso', 'nome_comvest', 'cpf_comvest', 'doc_comvest','dta_nasc_comvest',
                             'insc_vest_comvest', 'curso_comvest', 'merge_id', 'tipo_ingresso']) 

    return new_df


def remove_discartable_columns(df):
    for column in df.columns:
        if '_comvest' in column:
            df = df.drop(columns=[column])
    df = df.drop(columns=['merge_id'])
    return df


def concat_dac_comvest(correct_merge_list, comvest):
    dac_df = pd.concat(correct_merge_list)
    
    merge_ids = dac_df['merge_id'].unique()
    comvest_filt = comvest['merge_id'].isin(merge_ids)
    comvest = comvest[~comvest_filt]
    comvest = create_colums_for_concat(comvest)

    uniao_dac_comvest = pd.concat([dac_df, comvest])
    uniao_dac_comvest = uniao_dac_comvest.drop_duplicates(subset=["merge_id"])
    return uniao_dac_comvest