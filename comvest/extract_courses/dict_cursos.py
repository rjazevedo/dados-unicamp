import pandas as pd
from comvest.utilities.io import read_courses ,read_result, write_result

def get():
    cursos_dac = read_courses(dtype={'ANO':'Int64','CURSO':'Int64'}).loc[:,['ANO','CURSO']]
    cursos_comvest = read_result('cursos_comvest.csv').loc[:, ['ano_vest','cod_curso']]

    cursos_dac.columns = cursos_comvest.columns

    cursos = pd.concat([cursos_dac, cursos_comvest])

    cursos.drop_duplicates(subset=['ano_vest','cod_curso'], inplace=True)
    cursos.sort_values(by='ano_vest', ascending=False, inplace=True)

    write_result(cursos, 'cursos.csv')
    