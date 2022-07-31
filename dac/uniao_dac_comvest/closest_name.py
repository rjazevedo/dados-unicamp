import pandas as pd
import difflib as dff
from dac.utilities.io import write_result


def get_closest_name(wrong, comvest):
    wrong = setup_wrong(wrong)
    comvest = setup_comvest(comvest)
    
    wrong_and_right = closest_name(wrong, comvest, 'turma', 0.65)
    write_result(wrong_and_right[0], "uniao_frist_name.csv")
    right = closest_name(wrong_and_right[1], comvest, 'ano_ingresso_curso', 0.8)
    write_result(right[0], "uniao_not_frist_name.csv")

    final_df = pd.concat([wrong_and_right[0], right[0]])

    final_df['nome'] = final_df['new_name']
    final_df = final_df.drop(columns=['new_name', 'turma'])
    return final_df


def closest_name(wrong, comvest, column, cutoff):
    wrong = wrong.copy()
    comvest = comvest.copy()

    dict = {}
    turmas_wrong = wrong[column].unique()

    for turma in turmas_wrong:
        filt = (comvest[column] == turma)
        dict[turma] = comvest[filt]
    
    for index, row in wrong.iterrows():
        df = dict[row[column]]
        nome = get_the_closest_matche(row['nome'], df['nome'], cutoff)
        wrong.loc[index, 'new_name'] = nome

    return divide_wrong_and_right(wrong)


def divide_wrong_and_right(df):
    filt = (df.new_name == '')
    right = df[~filt]
    wrong = df[filt]
    return (right, wrong)


def get_the_closest_matche(name, name_serie, cutoff):
    values = dff.get_close_matches(name, name_serie, cutoff=cutoff)

    if len(values) > 0:
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
    filt = comvest['curso'].isin(['93, 92, 91, 90'])
    comvest.loc[filt,['curso']] = '22'

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