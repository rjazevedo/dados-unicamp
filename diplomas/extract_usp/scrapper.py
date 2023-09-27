from tqdm import tqdm
import pandas as pd
from bs4 import BeautifulSoup
from diplomas.utilities.io import next_usp_file

def scrap(FILENAME, SAVE_FILE):
    with open(FILENAME, 'rb') as file:
        df = pd.DataFrame(columns=['nome', 'instituicao', 'grau', 'curso', 'ano_conclusao'])
        print("Scrapping " + FILENAME)
        soup = BeautifulSoup(file.read(), 'html.parser')
                
        table = soup.find('table', class_='table_list')
        for row in tqdm(table.tbody.find_all('tr')):    

            columns = row.find_all('td')
        
            if(columns != []):
                nome = columns[0].text.strip()
                instituicao = columns[1].text.strip()
                grau = columns[2].text.strip()
                curso = columns[3].text.strip()
                ano_conclusao = columns[4].text.strip()

                df = df.append({'nome': nome,  'instituicao': instituicao, 
                'grau': grau, 'curso': curso, 'ano_conclusao': ano_conclusao}, ignore_index=True)
                
        df.to_csv(SAVE_FILE, index=False)

def merge(FILE_NAMES, SAVE_FILE):
    files = [pd.read_csv(f) for f in FILE_NAMES]

    diplomados_usp = pd.concat(files)
    diplomados_usp.drop_duplicates(inplace=True)
    diplomados_usp.to_csv(SAVE_FILE, index=False)