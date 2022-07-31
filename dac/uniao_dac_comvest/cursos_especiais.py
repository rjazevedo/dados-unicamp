import pandas as pd
from dac.utilities.io import write_result
from dac.uniao_dac_comvest.utilities import create_colums_for_concat


def deal_special_students(df, correct_merge_list):
    correct_special_list = []

    unknow = tecnology_students(df, correct_special_list)
    pedagogy = pedagogy_students(unknow, correct_special_list)
    profis = profis_students(pedagogy, correct_special_list)
    rest = drop_109_110_students(profis)

    correct_df = pd.concat(correct_special_list)
    correct_merge_list.append(correct_df)
    return rest


def tecnology_students(df, correct_special_list):
    pre_filt = (df['origem'] == 'pre')
    unknow_filt = (df['curso'].isin(['36','35','33','32','31']))
    course_filt = (pre_filt & unknow_filt)

    unknow_students = df[course_filt]
    normal_students = df[~course_filt]

    unknow_students = create_colums_for_concat(unknow_students)
    correct_special_list.append(unknow_students)
    return normal_students


def pedagogy_students(df, correct_special_list):   
    pos_filt = (df['origem'] == 'pos')
    pedagogy_filt = (df['curso'].isin(['65', '59', '66', '67']))
    courses_filt =  (pos_filt & pedagogy_filt)

    pedagogy_students = df[courses_filt]
    normal_students = df[~courses_filt]    

    pedagogy_students = create_colums_for_concat(pedagogy_students)
    correct_special_list.append(pedagogy_students)
    return normal_students


def profis_students(df, correct_special_list):
    pos_filt = (df['origem'] == 'pos')
    ingresso_filt = (df['tipo_ingresso'] == 'INGRESSO POR CONCLUSAO NO PROFIS')
    profis_filt = (df['curso'] == '200')
    courses_filt = (pos_filt & (ingresso_filt | profis_filt))

    profis_students = df[courses_filt]
    normal_students = df[~courses_filt]    

    profis_students = create_colums_for_concat(profis_students)
    correct_special_list.append(profis_students)
    return normal_students


def drop_109_110_students(df):
    pos_filt = (df['origem'] == 'pos')
    adm_filt = (df['curso'].isin(['109', '110']))
    ingresso_filt = (adm_filt & pos_filt)
    
    normal_students = df[~ingresso_filt]
    return normal_students


def find_entry_109_110_students(wrong, dados_dac, dados_comvest):
    wrong_pos = wrong[(wrong['origem'] == 'pos')]
    wrong_pos = remove_pedagogia_and_profis_students(wrong_pos)

    merge = pd.merge(wrong_pos, dados_comvest, how="left", on=['nome', 'dta_nasc'])

    df = merge.loc[:, ['identif', 'nome', 'dta_nasc', 'curso_x', 'insc_vest_y','ano_ingresso_curso_y', 'curso_y']]
    df.columns =  ['identif', 'nome', 'dta_nasc', 'curso', 'insc_vest', 'ano_ingresso_curso_comvest', 'curso_matric']
    df = df[(df['curso_matric'].isin(['103', '104', '105', '106']))]

    dados_dac['insc_vest'] = dados_dac['insc_vest'].astype(str)
    df['insc_vest'] = df['insc_vest'].astype(str)
    merge = pd.merge(df, dados_dac, how="left", on=['insc_vest'])
    merge = merge[~(merge["nome_y"].isnull())]

    merge = merge.loc[:, ['identif_x', 'nome_x', 'dta_nasc_x', 'curso_x', 'ano_ingresso_curso', 'insc_vest', 'curso_matric', 'ano_ingresso_curso_comvest']]
    merge.columns = ['identif', 'nome', 'dta_nasc', 'curso_dac','ano_ingresso_dac', 'insc_vest', 'curso_comvest', 'ano_ingresso_comvest']
    
    final_merge = pd.merge(wrong_pos, merge, how='left', on=['nome', 'dta_nasc'])
    final_merge = final_merge.loc[:, ['identif_x', 'nome', 'cpf', 'dta_nasc', 'curso_dac', 'ano_ingresso_curso', 'insc_vest_y', 'curso_comvest', 'ano_ingresso_comvest']]
    final_merge.columns = ['identif_dac', 'nome', 'cpf', 'dta_nasc', 'curso_dac', 'ano_ingresso_dac', 'insc_vest_comvest','curso_comvest', 'ano_ingresso_comvest']
    final_merge = final_merge[~(final_merge["curso_dac"].isnull())]

    write_result(final_merge, "cursos_109_e_110.csv")


def courses_that_are_different_in_both_bases(right_list):
    dfs = right_list.copy()
    dfs = pd.concat(right_list).loc[:,['origem', 'curso', 'curso_matric']]
    dfs = dfs[(dfs['origem'] == 'pre')]
    dfs['key'] = dfs['curso'] + dfs['curso_matric']
    dfs = dfs.drop_duplicates(subset=['curso', 'curso_matric'])
    dfs = dfs[~(dfs['curso'] == dfs['curso_matric'])]
    dfs = dfs.loc[:, ['curso', 'curso_matric']]
    write_result(dfs, "cursos_que_diferem_nas_bases.csv")