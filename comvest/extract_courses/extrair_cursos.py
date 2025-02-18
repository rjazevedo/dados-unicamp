"""
Módulo para extração de dados dos cursos Comvest.

Este módulo contém funções para extrair e processar dados dos cursos oferecidos nos exames Comvest.

Funções:
- cleandata(df, date, keepcolumns=['ano_vest', 'cod_curso', 'desc_curso', 'he', 'mod_isencao']): Realiza a limpeza dos dados dos cursos.
- extraction(): Executa a extração e processamento dos dados dos cursos Comvest.

Como usar:
Implemente e execute as funções para realizar a extração e processamento dos dados dos cursos Comvest.
"""


import pandas as pd
from comvest.utilities.io import files, read_from_db, write_result
from comvest.utilities.logging import progresslog, resultlog


def cleandata(df,date,keepcolumns=['ano_vest','cod_curso','desc_curso','he','mod_isencao']):
	"""
    Realiza a limpeza dos dados dos cursos.

    Parâmetros:
    ----------
    df : DataFrame
        O DataFrame contendo os dados dos cursos.
    date : int
        O ano do exame Comvest.
    keepcolumns : list, opcional
        Lista de colunas a serem mantidas no DataFrame final (o padrão é ['ano_vest', 'cod_curso', 'desc_curso', 'he', 'mod_isencao']).

    Retorna:
    -------
    DataFrame
        O DataFrame contendo os dados dos cursos limpos.
    """
	df.insert(loc=0, column='ano_vest', value=date)
	
	df.drop(columns=['area'], errors='ignore', inplace=True)
	
	df.rename(columns={df.columns[1]:'cod_curso', df.columns[2]:'desc_curso'}, inplace=True)

	df['desc_curso'] = df['desc_curso'].map(
		lambda desc: desc.replace('\r','').replace('\n','').replace('_x000D_','')
	)

	return df.reindex(columns=keepcolumns)


def extraction():
	"""
	Executa a extração e processamento dos dados dos cursos Comvest.

	Esta função lê os dados dos cursos de diferentes anos, realiza a limpeza dos dados e os concatena em um único DataFrame.

	Retorna:
	-------
	None
	"""
	courses_frames = []

	for path, date in files.items():
		if "Profis" in path:
			continue

		courses = read_from_db(path, sheet_name='cursos')
		courses = cleandata(courses, date)

		try:
			courses_vi = read_from_db(path, sheet_name='vi_cursos')
			courses_vi = cleandata(courses_vi, date)
		except:
			print(f'{date} doesn\'t have a "vi_cursos" sheet')
			courses_vi = None
		
		progresslog('cursos', date)

		courses_frames.append(courses)
		courses_frames.append(courses_vi)

	# Export CSV
	all_courses = pd.concat(courses_frames)
	all_courses.sort_values(by='ano_vest', ascending=False, inplace=True)
	all_courses.drop_duplicates(subset=['ano_vest','cod_curso'], inplace=True)

	FILE_NAME = 'cursos_comvest.csv'
	write_result(all_courses, FILE_NAME)
	resultlog(FILE_NAME)
