import pandas as pd
import os
from pandas import DataFrame
from openpyxl import load_workbook


def compare_columns(equal_sheets: list[str], sheets_1: dict, sheets_2: dict) -> dict:
    """
    Compara as colunas das planilhas que estão presentes em ambos os arquivos.

    Parâmetros:
    ----------
    equal_sheets : list[str]
        Lista de nomes das planilhas que estão presentes em ambos os arquivos.
    sheets_1 : dict
        Dicionário onde as chaves são os nomes das planilhas e os valores são os DataFrames.
    sheets_2 : dict
        Dicionário onde as chaves são os nomes das planilhas e os valores são os DataFrames.

    Retorna:
    -------
    dict
        Dicionário onde as chaves são os nomes das planilhas e os valores são dicionários contendo listas de colunas.
    """
    comparison = {}
    for sheet in equal_sheets:
        columns_1 = set(sheets_1[sheet].columns)
        columns_2 = set(sheets_2[sheet].columns)
        
        missing_columns = columns_1 - columns_2
        extra_columns = columns_2 - columns_1
        common_columns = columns_1 & columns_2
        
        altered_columns = [col for col in common_columns if list(sheets_1[sheet].columns).index(col) != list(sheets_2[sheet].columns).index(col)]
        
        comparison[sheet] = {
            "common_columns": list(common_columns),
            "missing_columns": list(missing_columns),
            "extra_columns": list(extra_columns),
            "altered_columns": altered_columns
        }
        
    return comparison


def print_columns_discrepancies(year: int, equal_sheets: list[str], sheets_1: dict, sheets_2: dict) -> None:
    """
    Salva em arquivos Excel as diferenças entre as colunas existentes para cada uma das chaves no dicionário comparison para o ano indicado.

    Parâmetros:
    ----------
    year : int
        O ano de referência para a comparação.
    equal_sheets : list[str]
        Lista de nomes das planilhas que estão presentes em ambos os arquivos.
    sheets_1 : dict
        Dicionário onde as chaves são os nomes das planilhas e os valores são os DataFrames.
    sheets_2 : dict
        Dicionário onde as chaves são os nomes das planilhas e os valores são os DataFrames.
    """
    comparison = compare_columns(equal_sheets, sheets_1, sheets_2)
    
    for sheet_name, columns in comparison.items():
        common_columns = columns["common_columns"]
        missing_columns = columns["missing_columns"]
        extra_columns = columns["extra_columns"]
        altered_columns = columns["altered_columns"]
        
        rows = []
        max_length = max(len(common_columns), len(missing_columns), len(extra_columns), len(altered_columns))
        
        for i in range(max_length):
            row = {
                "Colunas Iguais": common_columns[i] if i < len(common_columns) else '',
                "Colunas Faltantes": missing_columns[i] if i < len(missing_columns) else '',
                "Colunas Extras": extra_columns[i] if i < len(extra_columns) else '',
                "Colunas Alteradas": altered_columns[i] if i < len(altered_columns) else ''
            }
            rows.append(row)
        
        # Criar o DataFrame a partir das linhas
        df = pd.DataFrame(rows)
        
        # Diretório para salvar os arquivos
        output_dir = f"/home/giovani/testes/Comvest/{year}"
        os.makedirs(output_dir, exist_ok=True)
        
        # Salvar o DataFrame em um arquivo Excel
        excel_filename = os.path.join(output_dir, f"columns_discrepancies_{sheet_name}_{year}.xlsx")
        df.to_excel(excel_filename, index=False)
        
        # Ajustar a largura das colunas e a altura das linhas
        wb = load_workbook(excel_filename)
        ws = wb.active
        
        for col in ws.columns:
            max_length = 0
            column = col[0].column_letter  # Get the column name
            for cell in col:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(cell.value)
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
        print(f'Discrepâncias salvas em {excel_filename}')


def organize_comparison_questions(comvest: set[str], profis: set[str], year: int) -> None:
    """
    Organiza e salva as discrepâncias entre as colunas de questões da comvest e do Profis em um arquivo Excel.
    
    Parâmetros
    ----------
    comvest : set[str]
        Conjunto de colunas do DataFrame da comvest.
    profis : set[str]
        Conjunto de colunas do DataFrame do Profis.
    year : int
        O ano de referência para a comparação.
        
    Retorna
    -------
    None
    """
    rows = []
    # Ordena as colunas dos dois DataFrames em ordem alfabética
    questions_comvest = sorted(comvest)
    questions_profis = sorted(profis)
    # Preenche as linhas com os dados
    max_length = max(len(questions_comvest), len(questions_profis))
    for i in range(max_length):
        row = {
            "Questões Comvest": questions_comvest[i] if i < len(questions_comvest) else '',
            "Questões Profis": questions_profis[i] if i < len(questions_profis) else ''
        }
        rows.append(row)
    
    # Criar o DataFrame a partir das linhas
    df = pd.DataFrame(rows)
    
    # Diretório para salvar os arquivos
    output_dir = f"/home/giovani/testes/Profis/{year}"
    os.makedirs(output_dir, exist_ok=True)
    
    # Salvar o DataFrame em um arquivo Excel
    excel_filename = os.path.join(output_dir, f"questions_discrepancies_comvest_profis_{year}.xlsx")
    df.to_excel(excel_filename, index=False)
    
    # Ajustar a largura das colunas e a altura das linhas
    wb = load_workbook(excel_filename)
    ws = wb.active
    
    for col in ws.columns:
        max_length = 0
        column = col[0].column_letter  # Get the column name
        for cell in col:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(cell.value)
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
    print(f'Discrepâncias salvas em {excel_filename}')


def verify_cpfs_Profis(profis_sheets: dict, sheets_2022: dict) -> None:
    """
    Verifica se os CPFs dos candidatos do Profis estão presentes nos arquivos de ingresso do ano indicado.

    Parâmetros:
    ----------
    year : int
        O ano de referência para a comparação.
    profis_sheets : dict
        Dicionário onde as chaves são os nomes das planilhas e os valores são os DataFrames.
    sheets_2022 : dict
        Dicionário onde as chaves são os nomes das planilhas e os valores são os DataFrames.
    """
    profis_cpfs = set(profis_sheets["2022"]["cpf"])
    sheets_2022_cpfs = set(sheets_2022["profis_dados"]["CPF"])
    
    missing_cpfs = profis_cpfs - sheets_2022_cpfs
    
    if len(missing_cpfs) > 0:
        print(f"CPFs faltantes em 2022: {missing_cpfs}")
    else:
        print("Todos os CPFs do Profis estão presentes em 2022")


def get_question_columns(df: pd.DataFrame) -> set[str]:
    """Extracts column names starting with 'q'."""
    if df is None:
        return set()
    return {col for col in df.columns if isinstance(col, str) and col.lower().startswith('q')}


def main() -> None:
    for year in range(2011, 2023):
        print(f"Lendo o perfil da comvest para o ano {year}")
        if year in range(2011, 2019):
            comvest = pd.read_excel(f"/home/input/COMVEST/vest{year}.xlsx", sheet_name="perfil")  
        else:
            comvest = pd.read_excel(f"/home/input/COMVEST/ingresso{year}.xlsx", sheet_name="perfil")
 
        print(f"Lendo o perfil do Profis para o ano {year}")
        profis = pd.read_excel(f"/home/input/COMVEST/Profis11a22.xlsx", sheet_name=f"{year}")
        
        print(f"Pegando as colunas de perguntas do Comvest e do Profis")
        comvest_questions = get_question_columns(comvest)
        profis_questions = get_question_columns(profis)
        
        print(f"Organizando as discrepâncias entre as colunas de questões da Comvest e do Profis")
        organize_comparison_questions(comvest_questions, profis_questions, year)
        print()
 
 
if __name__ == "__main__":
    main()
