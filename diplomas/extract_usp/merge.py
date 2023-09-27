import pandas as pd

FILE_PATH = '/home/output/intermediario/'
FILENAME = 'usp-diplomados.csv'

tables = []

for i in range(1, 7):
    FILENAME = f'table{i}.csv'
    print(f"Reading {FILENAME}")
    table = pd.read_csv(FILENAME)
    tables.append(table)

diplomados = pd.concat(tables)
diplomados.drop_duplicates(inplace=True)

diplomados.to_csv(FILENAME, index=False)