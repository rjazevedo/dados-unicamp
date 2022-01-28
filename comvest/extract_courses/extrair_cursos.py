import glob
import re
import pandas as pd


def cleandata(df,date,keepcolumns=['ano_vest','cod_curso','desc_curso','he','mod_isencao']):
	df.insert(loc=0, column='ano_vest', value=date)
	
	df.drop(columns=['area'], errors='ignore', inplace=True)
	
	df.rename(columns={df.columns[1]:'cod_curso', df.columns[2]:'desc_curso'}, inplace=True)

	df['desc_curso'] = df['desc_curso'].map(
		lambda desc: desc.replace('\r','').replace('\n','').replace('_x000D_','')
	)

	return df.reindex(columns=keepcolumns)

# Gets all the file names and makes a dictionary with 
# file path as key and the respective date of the file as its value
files_path = glob.glob("input/comvest/*")
files = { path: int(re.sub('[^0-9]','',path)) for path in files_path }


def extraction():
	courses_frames = []

	for path, date in files.items():
		courses = pd.read_excel(path, sheet_name='cursos')

		courses = cleandata(courses, date)
		courses_frames.append(courses)

	# Export CSV
	all_courses = pd.concat(courses_frames)
	all_courses.sort_values(by='ano_vest', ascending=False, inplace=True)

	file_name = 'cursos_comvest'
	all_courses.to_csv("output/{}.csv".format(file_name), index=False)