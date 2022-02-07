import pandas as pd
from comvest.utilities.io import files, read_from_db, write_result
from comvest.utilities.logging import progresslog, resultlog


def cleandata(df,date,keepcolumns=['ano_vest','cod_curso','desc_curso','he','mod_isencao']):
	df.insert(loc=0, column='ano_vest', value=date)
	
	df.drop(columns=['area'], errors='ignore', inplace=True)
	
	df.rename(columns={df.columns[1]:'cod_curso', df.columns[2]:'desc_curso'}, inplace=True)

	df['desc_curso'] = df['desc_curso'].map(
		lambda desc: desc.replace('\r','').replace('\n','').replace('_x000D_','')
	)

	return df.reindex(columns=keepcolumns)


def extraction():
	courses_frames = []

	for path, date in files.items():
		courses = read_from_db(path, sheet_name='cursos')
		progresslog('cursos', date)

		courses = cleandata(courses, date)
		courses_frames.append(courses)

	# Export CSV
	all_courses = pd.concat(courses_frames)
	all_courses.sort_values(by='ano_vest', ascending=False, inplace=True)

	FILE_NAME = 'cursos_comvest.csv'
	write_result(all_courses, FILE_NAME)
	resultlog(FILE_NAME)