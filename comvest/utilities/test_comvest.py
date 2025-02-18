import pandas as pd
import os
from pandas import DataFrame
from openpyxl import load_workbook


def read_excel_tables(file_path: str) -> dict:
    """
    Lê todas as planilhas de um arquivo Excel.

    Parâmetros:
    ----------
    file_path : str
        O caminho do arquivo Excel.

    Retorna:
    -------
    dict
        Um dicionário onde as chaves são os nomes das planilhas e os valores são os DataFrames.
    """
    # Lê todas as planilhas do arquivo Excel
    all_sheets = pd.read_excel(file_path, sheet_name=None)
    
    return all_sheets


def compare_sits(year: int, sheets: dict) -> None:
    """
    Compara as colunas sit (de presença) presentes nas planilhas de primeira e de segunda fase.
    
    Filtra-se as pessoas que estão em ambas as planilhas e compara-se as colunas sit (para ver se possuem o mesmo valor).
    
    Para se saber quais pessoas estão em ambas, utiliza-se o número de inscrição (coluna insc).
    
    O resultado é salvo em um arquivo excel com as colunas: insc, sit iguais, sit diferentes.
    
    Parâmetros
    ----------
    year : int
        O ano do vestibular.
    sheets : dict
        Um dicionário onde as chaves são os nomes das planilhas e os valores são os DataFrames.
        
    Retorna
    -------
    None
    """
    inscs_f1 = set(sheets["notasf1"]["insc"])
    inscs_f2 = set(sheets["notasf2"]["insc"])
    inscs = inscs_f1.intersection(inscs_f2)
    
    if year == 2023:
        df_f1 = sheets["notasf1"].loc[sheets["notasf1"]["insc"].isin(inscs), ["insc", "sit"]]
        df_f2 = sheets["notasf2"].loc[sheets["notasf2"]["insc"].isin(inscs), ["insc", "sit_f1"]]
        df_f2 = df_f2.rename(columns={"sit_f1": "sit"})
        
    else:
        df_f1 = sheets["notasf1"].loc[sheets["notasf1"]["insc"].isin(inscs), ["insc", "sit"]]
        df_f2 = sheets["notasf2"].loc[sheets["notasf2"]["insc"].isin(inscs), ["insc", "sit"]]
    
    # Merge dos DataFrames para comparação
    df_merged = pd.merge(df_f1, df_f2, on="insc", suffixes=('_f1', '_f2'))
    
    # Filtrar apenas os casos em que há discrepância entre os valores de sit_f1 e sit_f2
    df_discrepancies = df_merged[df_merged["sit_f1"] != df_merged["sit_f2"]]
    
    # Seleção das colunas para o resultado final
    df_result = df_discrepancies[["insc", "sit_f1", "sit_f2"]]
    
    # Diretório para salvar os arquivos
    output_dir = "/home/giovani/testes/Comvest/sit/"
    os.makedirs(output_dir, exist_ok=True)
    
    # Nome do arquivo Excel
    excel_filename = os.path.join(output_dir, f"comparison_sits_{year}.xlsx")
    
    # Salvar o DataFrame em um arquivo Excel
    df_result.to_excel(excel_filename, index=False)
    
    # Ajustar a largura das colunas e a altura das linhas
    wb = load_workbook(excel_filename)
    ws = wb.active
    
    for col in ws.columns:
        max_length = 0
        column = col[0].column_letter  # Get the column name
        for cell in col:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(str(cell.value))
            except:
                pass
        adjusted_width = (max_length + 2)
        ws.column_dimensions[column].width = adjusted_width
    
    for row in ws.iter_rows():
        max_height = 0
        for cell in row:
            if cell.value:
                max_height = max(max_height, len(str(cell.value).split('\n')))
        ws.row_dimensions[row[0].row].height = max_height * 15
    
    wb.save(excel_filename)
    print(f'Comparação de sit entre as fases para o ano {year} salva em {excel_filename}')
        

def main() -> None:
    for year in range(2019, 2024):
        print(f"Lendo arquivo ingresso{year}.xlsx")
        sheets = read_excel_tables(f"/home/input/COMVEST/ingresso{year}.xlsx")

        print(f"Comparando a presença dos candidatos na planilha de primeira fase com a planilha de segunda fase para o ano {year}")
        compare_sits(year, sheets)


if __name__ == "__main__":
    main()
