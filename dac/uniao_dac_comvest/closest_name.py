import pandas as pd
import difflib as dff
from dac.utilities.io import write_result
from dac.uniao_dac_comvest.utilities import get_wrong_and_right
from dac.uniao_dac_comvest.utilities import create_colums_for_concat


def get_closest_name(wrong, comvest, correct_merge_list):
    wrong = setup_wrong(wrong)
    comvest = setup_comvest(comvest)
    
    wrong_and_right = closest_name(wrong, comvest, 'turma', 0.65)
    right1 = closest_name(wrong_and_right[1], comvest, 'ano_ingresso_curso', 0.8)
    right2 = closest_name(right1[1], comvest, 'ano_ingresso_curso', 0.9, first_name=1)
    
    no_match = deal_with_last_students(right2[1])
    correct_merge_list.append(no_match)
    final_df = pd.concat([wrong_and_right[0], right1[0], right2[0]])

    merge = merge_by_name(final_df, comvest)
    wrong = get_wrong_and_right(merge, correct_merge_list)


def deal_with_last_students(df):
    # planilha de alunos sem merge
    no_match = df.iloc[:, 0:11]
    write_result(no_match, "uniao_dac_comvest_alunos_sem_match.csv")

    # adicionar alunos na união
    df = df.drop(columns=['new_name', 'turma'])
    return create_empty_colums_for_concat(df)


def create_empty_colums_for_concat(df):
    new_df = df.copy()

    if 'insc_vest_comvest' not in df.columns:
        new_df['insc_vest_comvest'] = ""
    if 'dta_nasc_comvest' not in df.columns:
        new_df['dta_nasc_comvest'] = ""
    if 'doc_comvest' not in df.columns:
        new_df['doc_comvest'] = ""
    if 'nome_comvest' not in df.columns:
        new_df['nome_comvest'] = ""
    
    new_df = new_df.reindex(columns=['identif', 'nome', 'cpf', 'doc', 'dta_nasc', 'insc_vest', 'ano_ingresso_curso',
                             'origem', 'curso', 'nome_comvest', 'cpf_comvest', 'doc_comvest','dta_nasc_comvest',
                             'insc_vest_comvest', 'curso_comvest', 'merge_id', 'tipo_ingresso']) 

    return new_df


def merge_by_name(df, comvest):
    df['nome_dac'] = df['nome']
    df['nome'] = df['new_name']
    df = df.drop(columns=['new_name', 'turma'])
    final_df = pd.merge(df, comvest, how='left',  on=['nome', 'ano_ingresso_curso'], suffixes=('','_comvest'))
    final_df.rename(columns = {'nome': 'nome_comvest', 'nome_dac':'nome'}, inplace=True)
    return final_df


def closest_name(wrong, comvest, column, cutoff, first_name=0):
    wrong = wrong.copy()
    comvest = comvest.copy()

    dict = {}
    turmas_wrong = wrong[column].unique()

    for turma in turmas_wrong:
        filt = (comvest[column] == turma)
        dict[turma] = comvest[filt]
    
    for index, row in wrong.iterrows():
        df = dict[row[column]]
        nome = get_the_closest_matche(row['nome'], df['nome'], cutoff, first_name)
        wrong.loc[index, 'new_name'] = nome

    return divide_wrong_and_right(wrong)


def divide_wrong_and_right(df):
    filt = (df.new_name == '')
    right = df[~filt]
    wrong = df[filt]
    return (right, wrong)


def get_the_closest_matche(name, name_serie, cutoff, first_name):
    values = dff.get_close_matches(name, name_serie, cutoff=cutoff)

    if len(values) > 0:
        if first_name == 1:
            return values[0]
        else:
            split_name = name.split()
            first_name = split_name[0]

            possible_name = values[0]
            split_possible_name = possible_name.split()
            first_possible_name = split_possible_name[0]

            if first_name == first_possible_name:
                return values[0]
            else: 
                return ''

    else:
        return ''    


def setup_comvest(comvest):
    comvest = comvest[(comvest['ano_ingresso_curso'] < '1999')]

    # Padoniza cursos da Musica
    filt = comvest['curso'].isin(['93', '92', '91', '90'])
    comvest.loc[filt,['curso']] = '22'

    filt = comvest['curso'].isin(['1', '4', '28'])
    comvest.loc[filt,['curso']] = '51'

    comvest['turma'] = comvest['curso'] + comvest['ano_ingresso_curso']
    return comvest


def setup_wrong(wrong):
    # Padroniza cursos de Portugues
    filt = wrong['curso'].isin(['7', '18'])
    wrong.loc[filt,['curso']] = '24'
    
    # Padroniza cursos do Cursão
    filt = wrong['curso'].isin(['1', '4', '28'])
    wrong.loc[filt,['curso']] = '51'

    wrong['turma'] = wrong['curso'] + wrong['ano_ingresso_curso']
    return wrong