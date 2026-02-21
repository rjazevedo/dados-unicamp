import csv
import os
from multiprocessing import Pool

pasta = "/home/input/rais-novo/2011"

def process_file(filename):
    if filename.endswith(".txt"):
        filepath = os.path.join(pasta, filename)
        with open(filepath, newline='', encoding='iso-8859-1') as file:
            reader = csv.reader(file, delimiter=';')  # Usando ; como delimitador
            line_count = 0
            column_histogram = {}
            for row in reader:
                line_count += 1
                column_count = len(row)
                column_histogram[column_count] = column_histogram.get(column_count, 0) + 1

            result = f"File: {filename}, Total lines: {line_count}\n"
            result += "Column count histogram:\n"
            for col_count, freq in sorted(column_histogram.items()):
                result += f"  {col_count} columns: {freq} lines\n"
            return result

def main():
    files = os.listdir(pasta)
    with Pool() as pool:
        results = pool.map(process_file, files)
        for res in results:
            if res:  # Ignorar arquivos que não são .txt
                print(res)

if __name__ == "__main__":
    main()