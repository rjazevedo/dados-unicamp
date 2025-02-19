from tqdm import tqdm
import pandas as pd
from bs4 import BeautifulSoup
from diplomas.utilities.io import write_result, read_result, usp_files
from diplomas.utilities.io import Bases
import os

def scrap(FILENAME, SAVE_FILE):
    with open(FILENAME, 'rb') as file:
        data = []
        print("Scrapping " + FILENAME)
        soup = BeautifulSoup(file.read(), 'html.parser', from_encoding='utf-8')
        
        table = soup.find('table', class_='table_list')
        for row in tqdm(table.tbody.find_all('tr')):    

            columns = row.find_all('td')
        
            if(columns != []):
                nome = columns[0].text.strip()
                instituicao = columns[1].text.strip()
                grau = columns[2].text.strip()
                curso = columns[3].text.strip()
                ano_conclusao = columns[4].text.strip()

                data.append({'nome': nome,  'instituicao': instituicao, 
                'grau': grau, 'curso': curso, 'ano_conclusao': ano_conclusao})
        
        df = pd.DataFrame(data)
        write_result(df, SAVE_FILE)

def merge(FILE_NAMES, SAVE_FILE):
    files = [read_result(f) for f in FILE_NAMES]

    diplomados_usp = pd.concat(files)
    diplomados_usp.drop_duplicates(inplace=True)
    write_result(diplomados_usp, SAVE_FILE)

def proccess_usp():
    RESULT_FILES = []
    OUTPUT_FILE = "usp-diplomados.csv"
    for i, f in enumerate(usp_files):
        SAVE_FILE =  f"diplomas/DIPLOMAS{i}" + ".csv"
        RESULT_FILES.append(SAVE_FILE)
        scrap(f, SAVE_FILE)
    
    merge(RESULT_FILES, OUTPUT_FILE)
    
    for f in RESULT_FILES: os.remove(Bases.RESULT.value + f)