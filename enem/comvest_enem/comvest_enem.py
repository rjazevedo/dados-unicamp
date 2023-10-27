import pandas as pd
from tqdm import tqdm
from enem.utilities.io import read_result, read_comvest_grades, write_result

def main():
    merge()

def merge():
    COMVEST_FILE = 'dados_comvest.csv'
    GRADES_FILE = 'enem_comvest_todos.csv'
    
    comvest = read_result(COMVEST_FILE)
    grades = read_comvest_grades()

    print('Standardizing Enem grades')
    for year, grade in tqdm(grades.items()):
        grade.drop(columns=['NOME', 'CPF'], inplace=True)
        grade = grade.rename(columns={
                        f'comvest_{year}'  : 'insc_vest',
                        f'enem{year - 1}' : 'enem_1',
                        f'ncnt{year - 1}' : 'ncnt_enem_1',
                        f'ncht{year - 1}' : 'ncht_enem_1',
                        f'nlct{year - 1}' : 'nlct_enem_1',
                        f'nred{year - 1}' : 'nred_enem_1',
                        f'nmt{year - 1}'  : 'nmt_enem_1',
                        f'enem{year - 2}' : 'enem_2',
                        f'ncnt{year - 2}' : 'ncnt_enem_2',
                        f'ncht{year - 2}' : 'ncht_enem_2',
                        f'nlct{year - 2}' : 'nlct_enem_2',
                        f'nred{year - 2}' : 'nred_enem_2',
                        f'nmt{year - 2}'  : 'nmt_enem_2'
                    })
        grade['ano_vest'] = year
        grades[year] = grade.loc[:, ['insc_vest', 'ano_vest', 
                                      'enem_1', 'ncnt_enem_1', 'ncht_enem_1', 'nlct_enem_1', 'nmt_enem_1', 'nred_enem_1',
                                      'enem_2', 'ncnt_enem_2', 'ncht_enem_2', 'nlct_enem_2', 'nmt_enem_2', 'nred_enem_2']]

    print('Concating years')
    grades_comvest = pd.concat(grades)

    print("Merging with Comvest")
    comvest_enem_aggregated = comvest.merge(grades_comvest, how='left', on=['ano_vest', 'insc_vest'])
    write_result(comvest_enem_aggregated, COMVEST_FILE)
    write_result(grades_comvest, GRADES_FILE)

if __name__ == '__main__':
    main()

