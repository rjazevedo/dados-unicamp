import pandas as pd

from dac.uniao_dac_comvest import uniao_dac_comvest
from dac.utilities.io import write_result
from dac.utilities.io import read_result as read_result_dac, write_output

def encontrar_vestibular_dos_alunos_109_110(wrong, dados_dac):

    print("removendo cursos de pedagogia e profis")
    filt = (wrong['origem'] == 'pos')
    wrong_pos = wrong[filt]
    wrong_pos = remover_alunos_pedagogia_profis(wrong_pos)

    print("sobraram com curso 109 e 110")
    dados_comvest_teste = read_result_dac("comvest_to_test.csv", dtype=str)
    merge = pd.merge(wrong_pos, dados_comvest_teste, how="left", on=['nome', 'dta_nasc', 'doc'])
    print(merge.shape)

    filt_ano = (merge['ano_ingresso_curso_y'] >= '2009')
    merge = merge[filt_ano]
    print(merge.shape)

    df = merge.loc[:, ['identif', 'nome', 'dta_nasc', 'curso',
       'insc_vest_y','ano_ingresso_curso_y', 'opc1', 'opc2', 'opc3']]

    df.columns =  ['identif', 'nome', 'dta_nasc', 'curso',
       'insc_vest', 'ano_ingresso_curso_comvest', 'opc1', 'opc2', 'opc3']

    dados_dac['insc_vest'] = dados_dac['insc_vest'].astype(str)
    df['insc_vest'] = df['insc_vest'].astype(str)
    merge = pd.merge(df, dados_dac, how="left", on=['insc_vest'])

    filt = merge["nome_y"].isnull()
    merge = merge[~filt]

    merge = merge.loc[:, ['identif_x', 'nome_x', 'dta_nasc_x', 'curso_x', 'ano_ingresso_curso', 'insc_vest', 'opc1', 'ano_ingresso_curso_comvest']]
    merge.columns = ['identif', 'nome', 'dta_nasc', 'curso_dac','ano_ingresso_dac', 'insc_vest', 'curso_comvest', 'ano_ingresso_comvest']

    print("aipaipara")
    
    final_merge = pd.merge(wrong_pos, merge, how='left', on=['nome', 'dta_nasc'])
    print(final_merge.columns)
   
    final_merge = final_merge.loc[:, ['identif_x', 'nome', 'cpf', 'dta_nasc', 'curso_dac', 'ano_ingresso_curso', 'identif_y', 'insc_vest_y', 'curso_comvest', 'ano_ingresso_comvest']]
    final_merge.columns = ['identif_dac', 'nome', 'cpf', 'dta_nasc', 'curso_dac', 'ano_ingresso_dac', 'identif_dac', 'insc_vest_comvest','curso_comvest', 'ano_ingresso_comvest']

    filt = final_merge["curso_dac"].isnull()
    final_merge = final_merge[~filt]

    write_result(final_merge, "uniao_serelepe.csv")
    print(final_merge.shape)


def remover_alunos_pedagogia_profis(wrong_pos):
    wrong_pos = wrong_pos.drop_duplicates(subset=['identif'], keep=False)
    print(wrong_pos.shape)

    filt = (wrong_pos['curso'] == '65')
    wrong_pos = wrong_pos[~filt]
    print(wrong_pos.shape)

    filt = (wrong_pos['curso'] == '59')
    wrong_pos = wrong_pos[~filt]
    print(wrong_pos.shape)

    filt = (wrong_pos['curso'] == '66')
    wrong_pos = wrong_pos[~filt]
    print(wrong_pos.shape)

    filt = (wrong_pos['curso'] == '67')
    wrong_pos = wrong_pos[~filt]
    print(wrong_pos.shape)

    filt = (wrong_pos['curso'] == '200')
    wrong_pos = wrong_pos[~filt]
    print(wrong_pos.shape)

    filt = (wrong_pos['tipo_ingresso'] != 'INGRESSO POR CONCLUSAO NO PROFIS')
    wrong_pos = wrong_pos[filt]
    print(wrong_pos.shape)

    return wrong_pos

def comvest_1989(wrong, dados_comvest):
    wrong = wrong_and_right[1]
    print(wrong.shape)
    filt = (wrong['origem'] == 'pre')
    wrong_pre = wrong[filt]

    filt = (wrong_pre['ano_ingresso_curso'] == "1989")
    wrong_pre = wrong_pre[filt]
    print(wrong_pre.shape)

    write_result(wrong_pre, "dac.csv")

    uniao_dac_comvest = pd.merge(wrong_pre, dados_comvest, how='left',  on=['nome', 'ano_ingresso_curso', 'curso'], suffixes=('','_comvest'))

    print(uniao_dac_comvest.shape)
    write_result(uniao_dac_comvest, 'uniao_wrong_pre.csv')