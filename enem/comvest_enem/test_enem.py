import os
import pandas as pd
from pandas import DataFrame
import sys
from openpyxl import load_workbook


columns = {
        "PRE2012" : ['NU_INSCRICAO', 'NU_NT_CN', 'NU_NT_CH', 'NU_NT_LC', 'NU_NT_MT', 'NU_NOTA_REDACAO'],
        "PRE2014" : ['NU_INSCRICAO', 'NOTA_CN', 'NOTA_CH', 'NOTA_LC', 'NOTA_MT', 'NU_NOTA_REDACAO'],
        "POS2015" : ['NU_INSCRICAO', 'NU_NOTA_CN', 'NU_NOTA_CH', 'NU_NOTA_LC', 'NU_NOTA_MT', 'NU_NOTA_REDACAO'],
}
reading_parameters = {
    2012 : {
        "columns" : columns["PRE2012"],
        "separator" : ','
    },
    2013 : {
        "columns" : columns["PRE2014"],
        "separator" : ';'
    },
    2014 : {
        "columns" : columns["PRE2014"],
        "separator" : ','
    },

    2015 : {
        "columns" : columns["POS2015"],
        "separator" : ','
    },

    2016 : {
        "columns" : columns["POS2015"],
        "separator" : ';'
    },
    2017 :{
        "columns" : columns["POS2015"],
        "separator" : ';'
    },
    2018 :{
        "columns" : columns["POS2015"],
        "separator" : ';'
    },
    2019 :{
        "columns" : columns["POS2015"],
        "separator" : ';'
    },
    2020 : {
        "columns" : columns["POS2015"],
        "separator" : ';'
    }
}

# Diz quais anos do enem devem ser completados pelas informações de cada ano do fin
enem_fin_correspondece = {
    2019: [2018],
    2020: [2018, 2019],
    2022: [2020, 2021],
    2023: [2022]  
}

# Diz quais colunas do enem devem ser mantidas para cada ano
columns_enem_years = {
    2019: ["insc", "ENEM2018", "NOME", "CPF", "ncnt18", "ncht18", "nlct18", "nmt18", "nred18"],
    2020: ["insc", "enem2018", "enem2019", "nome_cand", "cpf", "ncnt18", "ncht18", "nlct18", "nmt18", "nred18", "ncnt19", "ncht19", "nlct19", "nmt19", "nred19"],
    2022: ["insc", "enem2020", "enem2021", "nome", "cpf", "ncnt20", "ncht20", "nlct20", "nmt20", "nred20", "ncnt21", "ncht21", "nlct21", "nmt21", "nred21"],
    2023: ["insc", 'enem2022', 'cpf', 'nome', 'ncnt22', 'ncht22', 'nlct22', 'nmt22', 'nred22']
}


def read_csv_files(years, parameters):
    """
    Lê arquivos CSV para os anos especificados usando os parâmetros fornecidos.

    Parâmetros:
        years (list): Lista de anos para os quais os arquivos CSV serão lidos.
        parameters (dict): Dicionário contendo os parâmetros de formatação.

    Retorna:
        dict: Um dicionário contendo os DataFrames lidos.
    """
    data = {}
    for year in years:
        file_path = f'/home/gsiqueira/dados-unicamp/input/enem/enem/MICRODADOS_ENEM_{year}.csv'
        if os.path.exists(file_path):
            separator = parameters[year]['separator']
            print(f'Lendo arquivo CSV para o ano {year} com separador "{separator}"')
            data[year] = pd.read_csv(file_path, encoding='latin-1', sep=separator)
        else:
            print(f'Arquivo CSV para o ano {year} não encontrado.')
    return data


def read_excel_files(years):
    """
    Lê arquivos Excel para os anos especificados.

    Parâmetros:
        years (list): Lista de anos para os quais os arquivos Excel serão lidos.

    Retorna:
        dict: Um dicionário contendo os DataFrames lidos.
    """
    data = {}
    for year in years:
        file_path_enem = f'/home/input/Enem_Unicamp/Enem{year}.xlsx'
        file_path_fin = f'/home/input/Enem_Unicamp/fin{str(year)[-2:]}.xlsx'
        file_path_vu = f'/home/input/Enem_Unicamp/NotasEnem_VU{str(year + 1)[-2:]}.xlsx'
        
        data[year] = {}
        
        if os.path.exists(file_path_enem):
            print(f'Lendo arquivo Enem para o ano {year}')
            data[year]['Enem'] = pd.read_excel(file_path_enem)
        else:
            print(f'Arquivo Enem para o ano {year} não encontrado.')
        
        if os.path.exists(file_path_fin):
            print(f'Lendo arquivo Fin para o ano {year}')
            data[year]['Fin'] = pd.read_excel(file_path_fin)
        else:
            print(f'Arquivo Fin para o ano {year} não encontrado.')
        
        if os.path.exists(file_path_vu):
            print(f'Lendo arquivo VU para o ano {year}')
            data[year]['VU'] = pd.read_excel(file_path_vu)
        else:
            print(f'Arquivo VU para o ano {year} não encontrado.')
        
        # Remover anos que não têm nenhum arquivo lido
        if not data[year]:
            del data[year]
    
    print(data.keys())
    return data


def compare_columns(columns_enem, columns_fin):
    """
    Compara as colunas dos arquivos Enem e Fin.

    Parâmetros:
        columns_enem (list): Lista de nomes das colunas do arquivo Enem.
        columns_fin (list): Lista de nomes das colunas do arquivo Fin.

    Retorna:
        tuple: Tupla contendo as listas de colunas faltantes e extras.
    """
    columns_enem_set = set(columns_enem)
    columns_fin_set = set(columns_fin)
    
    only_in_enem = columns_enem_set - columns_fin_set
    only_in_fin = columns_fin_set - columns_enem_set
    
    print(f"Comparison results - Only in Enem: {only_in_enem}, Only in Fin: {only_in_fin}")
    return list(only_in_enem), list(only_in_fin)


def extract_columns(df: DataFrame):
    """
    Extrai as colunas que existem nos arquivos CSV do enem lidos

    Parâmetros:
        df (DataFrame): O DataFrame lido do arquivo CSV.
        
    Retorna:
        list: Lista de colunas do DataFrame.
    """
    return df.columns.tolist()


def columns_enem(csv_data):
    """
    Salva as colunas dos arquivos CSV do ENEM em um único DataFrame, onde cada coluna 
    representa um ano e as linhas são os nomes das colunas desse arquivo.
    
    Parâmetros:
        csv_data (dict): Um dicionário contendo os DataFrames do ENEM lidos, onde a chave é o ano.
    """
    # Criar um dicionário para armazenar os nomes das colunas de cada ano
    columns_dict = {}
    
    for year, df in csv_data.items():
        columns = extract_columns(df)  # Extrai as colunas do DataFrame específico
        columns_dict[year] = columns        # Adiciona ao dicionário com o ano como chave
    
    # Converter o dicionário em um DataFrame, com anos como colunas e nomes de colunas do ENEM como linhas
    combined_df = pd.DataFrame(dict([(year, pd.Series(cols)) for year, cols in columns_dict.items()]))
    
    # Salvar o DataFrame em um arquivo Excel
    excel_filename = os.path.join("/home/giovani/testes/enem", f"columns_enems.xlsx")
    combined_df.to_excel(excel_filename, index=False)
    
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
    print(f"Discrepancies saved to {excel_filename}")


def discrepancies_enem_fin(year, only_in_enem, only_in_fin):
    """
    Imprime as discrepâncias entre as colunas dos arquivos Enem e Fin.

    Parâmetros:
        year (int): O ano do arquivo.
        file_enem (str): O nome do arquivo Enem.
        file_fin (str): O nome do arquivo Fin.
        only_in_enem (list): A lista de colunas que estão presentes em Enem mas faltando em Fin.
        only_in_fin (list): A lista de colunas que estão presentes em Fin mas faltando em Enem.
    """
    rows = []
    max_length = max(len(only_in_enem), len(only_in_fin))
    
    for i in range(max_length):
        row = {
            "Somente em Enem": only_in_enem[i] if i < len(only_in_enem) else '',
            "Somente em Fin": only_in_fin[i] if i < len(only_in_fin) else ''
        }
        rows.append(row)
    
    # Criar o DataFrame a partir das linhas
    df = pd.DataFrame(rows)
    
    # Diretório para salvar os arquivos
    os.makedirs("/home/giovani/testes", exist_ok=True)
    
    # Salvar o DataFrame em um arquivo Excel
    excel_filename = os.path.join("/home/giovani/testes/enem", f"dif_enem_vs_fin_{year}.xlsx")
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
    print(f"Discrepancies saved to {excel_filename}")


def compare_enem_fin(data):
    """
    Compara os arquivos Excel lidos e salva as discrepâncias em arquivos Excel.

    Parâmetros:
        data (dict): Um dicionário contendo os DataFrames lidos.
    """
    for year, dfs in data.items():
        df_enem = dfs['Enem']
        df_fin = dfs['Fin']
        
        # Listar colunas dos DataFrames
        columns_enem = df_enem.columns.tolist()
        columns_fin = df_fin.columns.tolist()
        
        # Comparar colunas
        only_in_enem, only_in_fin = compare_columns(columns_enem, columns_fin)
        
        # Imprimir e salvar as discrepâncias
        discrepancies_enem_fin(year, only_in_enem, only_in_fin)


def discrepancies_fin_vu(year, only_in_fin, only_in_vu, excel_filename):
    """
    Imprime as discrepâncias entre as colunas dos arquivos Fin e VU.

    Parâmetros:
        year (int): O ano do arquivo.
        only_in_fin (list): A lista de colunas que estão presentes em Fin mas faltando em VU.
        only_in_vu (list): A lista de colunas que estão presentes em VU mas faltando em Fin.
        excel_filename (str): O nome do arquivo Excel onde as discrepâncias serão salvas.
    """
    rows = []
    max_length = max(len(only_in_fin), len(only_in_vu))
    
    for i in range(max_length):
        row = {
            "Somente em Fin": only_in_fin[i] if i < len(only_in_fin) else '',
            "Somente em VU": only_in_vu[i] if i < len(only_in_vu) else ''
        }
        rows.append(row)
    
    # Criar o DataFrame a partir das linhas
    df = pd.DataFrame(rows)
    
    # Diretório para salvar os arquivos
    os.makedirs("/home/giovani/testes", exist_ok=True)
    
    # Salvar o DataFrame em um arquivo Excel
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
    print(f"Discrepancies saved to {excel_filename}")


def compare_columns_fin_vu(data: dict):
    """
    Compara os arquivos Excel lidos e salva as discrepâncias em arquivos Excel.

    Parâmetros:
        data (dict): Um dicionário contendo os DataFrames lidos.
    """
    for year, dfs in data.items():
        df_fin = dfs['Fin']
        df_vu = dfs['VU']
        
        # Listar colunas dos DataFrames
        columns_fin = df_fin.columns.tolist()
        columns_vu = df_vu.columns.tolist()
        
        # Comparar colunas
        only_in_fin, only_in_vu = compare_columns(columns_fin, columns_vu)
        
        # Imprimir e salvar as discrepâncias
        excel_filename = os.path.join("/home/giovani/testes/enem", f"dif_fin_vs_vu_columns_{year}.xlsx")
        discrepancies_fin_vu(year, only_in_fin, only_in_vu, excel_filename)


def compare_rows_fin_vu(data: dict):
    """
    Compara as linhas dos arquivos Excel lidos e salva as discrepâncias em arquivos Excel.
    
    As colunas desse arquivo são only_in_fin e only_in_vu.
    
    Cada coluna tem como valor o nome da coluna que está presente em um arquivo mas não no outro.

    Parâmetros:
        data (dict): Um dicionário contendo os DataFrames lidos.
    """
    for year, dfs in data.items():
        df_fin = dfs['Fin']
        df_vu = dfs['VU']
        
        # Comparar linhas
        only_in_fin = df_fin[~df_fin.isin(df_vu)].dropna()
        only_in_vu = df_vu[~df_vu.isin(df_fin)].dropna()
        
        # Imprimir e salvar as discrepâncias
        excel_filename = os.path.join("/home/giovani/testes/enem", f"dif_fin_vs_vu_rows_{year}.xlsx")
        discrepancies_fin_vu(year, only_in_fin, only_in_vu, excel_filename)


def compare_enem_fin_rows(excel_data: dict):
    """Verifica se há instâncias duplicadas entre os arquivos Enem e Fin.
    
    Checa para os anos em que fin existe (2018 a 2022, mas sem 2021)
    """
    years = [2018, 2019, 2020, 2021, 2022]
    for year in years:
        if year == 2020:
            next_year = 2022
        else:  
            next_year = year + 1
            
        if next_year in excel_data:
            df_enem = excel_data[next_year]['Enem']
            df_fin = excel_data[year]['Fin']
            
            # Verificar se as colunas 'CPF' e 'cpf' estão presentes
            if next_year >= 2020:
                cpf_column_enem = 'cpf'
            else:
                cpf_column_enem = 'CPF'
            
            cpf_enem = df_enem[cpf_column_enem].dropna()
            cpf_fin = df_fin['cpf'].dropna()
            
            # Encontrar CPFs duplicados e ordenar a lista
            duplicate_cpfs = sorted(list(set(cpf_enem).intersection(set(cpf_fin))))
            
            # Filtrar os DataFrames para manter apenas os CPFs duplicados
            df_enem_filtered = df_enem[df_enem[cpf_column_enem].isin(duplicate_cpfs)]
            df_fin_filtered = df_fin[df_fin['cpf'].isin(duplicate_cpfs)]
            
            # Ordenar os DataFrames por CPF
            df_enem_sorted = df_enem_filtered.sort_values(by=cpf_column_enem).reset_index(drop=True)
            df_fin_sorted = df_fin_filtered.sort_values(by='cpf').reset_index(drop=True)
            
            comparison_results = []
            for cpf in duplicate_cpfs:
                # Acessar as linhas correspondentes
                enem_row = df_enem_sorted[df_enem_sorted[cpf_column_enem] == cpf].iloc[0]
                fin_row = df_fin_sorted[df_fin_sorted['cpf'] == cpf].iloc[0]

                # Obter os dois últimos dígitos do ano menos 1
                year_suffix = str(year)[-2:]
                
                # Comparar valores de interesse
                ncht_enem = enem_row.get(f'ncht{year_suffix}', None)
                ncht_fin = fin_row.get('ncht', None)
                ncnt_enem = enem_row.get(f'ncnt{year_suffix}', None)
                ncnt_fin = fin_row.get('ncnt', None)
                
                if ncht_enem != ncht_fin or ncnt_enem != ncnt_fin:
                    print(f"Discrepância para CPF {cpf}:")
                    print(f"ncht{year_suffix}_enem: {ncht_enem}, ncht_fin: {ncht_fin}")
                    print(f"ncnt{year_suffix}_enem: {ncnt_enem}, ncnt_fin: {ncnt_fin}")
                    comparison_results.append({
                        'CPF': cpf,
                        f'ncht{year_suffix}_enem': ncht_enem,
                        f'ncnt{year_suffix}_enem': ncnt_enem,
                        'ncht_fin': ncht_fin,
                        'ncnt_fin': ncnt_fin,
                    })

            
            # Criar DataFrame com os resultados da comparação
            df_comparison = pd.DataFrame(comparison_results)
            
            # Criar o diretório se não existir
            output_dir = "/home/giovani/testes/enem"
            os.makedirs(output_dir, exist_ok=True)
            
            # Salvar o DataFrame em um arquivo Excel
            excel_filename = os.path.join("/home/giovani/testes/enem", f"comparison_enem_fin_{year}.xlsx")
            df_comparison.to_excel(excel_filename, index=False)
            
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
            print(f"Comparison results saved to {excel_filename}")


def compare_grades_enem_consecutives_years(excel_data: dict):
    '''
    Compara as notas ncht e ncnt dos arquivos enem de anos consecutivos
    
    CPFs duplicados (ou seja, presente em ambos os anos são considerados)
    Para o ano de 2020, o arquivo enem de 2022 é que deve ser considerado (já que ele tem informações de 2020 e 2021)
    Após isso, salva em um arquivo excel as informações de CPF, ncht e ncnt de ambos os anos
    '''
    years = [2018, 2019, 2020, 2022]
    for year in years:
        if year == 2020:
            next_year = 2022
        else:  
            next_year = year + 1
            
        if next_year in excel_data:
            df_enem = excel_data[year]['Enem']
            df_enem_prox = excel_data[next_year]['Enem']
            
            # Verificar se as colunas 'CPF' e 'cpf' estão presentes
            if year >= 2020:
                cpf_column_enem = 'cpf'
            else:
                cpf_column_enem = 'CPF'
                
            if next_year >= 2020:
                cpf_column_enem_prox = 'cpf'
            else:
                cpf_column_enem_prox = 'CPF'
            
            cpf_enem = df_enem[cpf_column_enem].dropna()
            cpf_enem_prox = df_enem_prox[cpf_column_enem_prox].dropna()
            
            # Encontrar CPFs duplicados e ordenar a lista
            duplicate_cpfs = sorted(list(set(cpf_enem).intersection(set(cpf_enem_prox))))
            
            # Filtrar os DataFrames para manter apenas os CPFs duplicados
            df_enem_filtered = df_enem[df_enem[cpf_column_enem].isin(duplicate_cpfs)]
            df_enem_prox_filtered = df_enem_prox[df_enem_prox[cpf_column_enem_prox].isin(duplicate_cpfs)]
            
            # Ordenar os DataFrames por CPF
            df_enem_sorted = df_enem_filtered.sort_values(by=cpf_column_enem).reset_index(drop=True)
            df_enem_prox_sorted = df_enem_prox_filtered.sort_values(by=cpf_column_enem_prox).reset_index(drop=True)
            
            comparison_results = []
            for cpf in duplicate_cpfs:
                # Acessar as linhas correspondentes
                enem_row = df_enem_sorted[df_enem_sorted[cpf_column_enem] == cpf].iloc[0]
                enem_prox_row = df_enem_prox_sorted[df_enem_prox_sorted[cpf_column_enem_prox] == cpf].iloc[0]

                # Obter os dois últimos dígitos do ano menos 1
                year_suffix = str(year - 1)[-2:]
                
                # Comparar valores de interesse
                ncht_enem = enem_row.get(f'ncht{year_suffix}', None)
                ncht_enem_prox = enem_prox_row.get(f'ncht{year_suffix}', None)
                ncnt_enem = enem_row.get(f'ncnt{year_suffix}', None)
                ncnt_enem_prox = enem_prox_row.get(f'ncnt{year_suffix}', None)
                
                if ncht_enem != ncht_enem_prox or ncnt_enem != ncnt_enem_prox:
                    print(f"Discrepância para CPF {cpf}:")
                    print(f"ncht{year_suffix}_enem: {ncht_enem}, ncht{year_suffix}_enem_prox: {ncht_enem_prox}")
                    print(f"ncnt{year_suffix}_enem: {ncnt_enem}, ncnt{year_suffix}_enem_prox: {ncnt_enem_prox}")
                    comparison_results.append({
                        'CPF': cpf,
                        f'ncht{year_suffix}_enem_{year}': ncht_enem,
                        f'ncnt{year_suffix}_enem{year}': ncnt_enem,
                        f'ncht{year_suffix}_enem{next_year}': ncht_enem_prox,
                        f'ncnt{year_suffix}_enem{next_year}': ncnt_enem_prox,
                    })

            
            # Criar DataFrame com os resultados da comparação
            df_comparison = pd.DataFrame(comparison_results)
            
            # Criar o diretório se não existir
            output_dir = "/home/giovani/testes/enem"
            os.makedirs(output_dir, exist_ok=True)
            
            # Salvar o DataFrame em um arquivo Excel
            excel_filename = os.path.join("/home/giovani/testes/enem", f"comparison_enem_consec_years_{year}.xlsx")
            df_comparison.to_excel(excel_filename, index=False)
            
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
            print(f"Comparison results saved to {excel_filename}")


def separate_enem(excel_data: dict) -> dict:
    """
    Separa os dados do Enem em diferentes DataFrames para cada ano e escreve em arquivos Excel.

    Parâmetros:
        excel_data (dict): Um dicionário contendo os DataFrames lidos.

    Retorna:
        dict: Um dicionário com as chaves "enem2019", "enem2020", "enem2021", "enem2022" e "enem2023",
              onde o valor de cada chave é um DataFrame com as colunas especificadas no dicionário columns_enem_years,
              ajustadas para o formato e ordem desejados.
    """
    separated_data = {}

    for year, dfs in excel_data.items():
        if year in columns_enem_years and 'Enem' in dfs:
            df_enem = dfs['Enem']
            columns = columns_enem_years[year]
            df_enem = df_enem[columns]
            
            if year == 2019:
                continue

            elif year == 2020:
                # Separar os dados em dois anos distintos
                year1 = str(year - 2)[-2:]
                year2 = str(year - 1)[-2:]
                df_year1 = df_enem[["insc", f"enem{year - 2}", "nome_cand", "cpf", f"ncnt{year1}", f"ncht{year1}", f"nlct{year1}", f"nmt{year1}", f"nred{year1}"]]
                df_year2 = df_enem[["insc", f"enem{year - 1}", "nome_cand", "cpf", f"ncnt{year2}", f"ncht{year2}", f"nlct{year2}", f"nmt{year2}", f"nred{year2}"]]

                df_year1 = df_year1.rename(columns={
                    f"enem{year - 2}": "enem",
                    "nome_cand": "nome",
                    f"ncnt{year1}": "ncnt",
                    f"ncht{year1}": "ncht",
                    f"nlct{year1}": "nlct",
                    f"nmt{year1}": "nmt",
                    f"nred{year1}": "nred"
                })

                df_year2 = df_year2.rename(columns={
                    f"enem{year - 1}": "enem",
                    "nome_cand": "nome",
                    f"ncnt{year2}": "ncnt",
                    f"ncht{year2}": "ncht",
                    f"nlct{year2}": "nlct",
                    f"nmt{year2}": "nmt",
                    f"nred{year2}": "nred"
                })

                separated_data[f"enem20{year1}"] = df_year1
                separated_data[f"enem20{year2}"] = df_year2

            elif year == 2022:
                # Separar os dados em dois anos distintos
                year1 = str(year - 2)[-2:]
                year2 = str(year - 1)[-2:]
                df_year1 = df_enem[["insc", f"enem{year - 2}", "nome", "cpf", f"ncnt{year1}", f"ncht{year1}", f"nlct{year1}", f"nmt{year1}", f"nred{year1}"]]
                df_year2 = df_enem[["insc", f"enem{year - 1}", "nome", "cpf", f"ncnt{year2}", f"ncht{year2}", f"nlct{year2}", f"nmt{year2}", f"nred{year2}"]]

                df_year1 = df_year1.rename(columns={
                    f"enem{year - 2}": "enem",
                    "nome": "nome",
                    f"ncnt{year1}": "ncnt",
                    f"ncht{year1}": "ncht",
                    f"nlct{year1}": "nlct",
                    f"nmt{year1}": "nmt",
                    f"nred{year1}": "nred"
                })

                df_year2 = df_year2.rename(columns={
                    f"enem{year - 1}": "enem",
                    "nome": "nome",
                    f"ncnt{year2}": "ncnt",
                    f"ncht{year2}": "ncht",
                    f"nlct{year2}": "nlct",
                    f"nmt{year2}": "nmt",
                    f"nred{year2}": "nred"
                })

                separated_data[f"enem20{year1}"] = df_year1
                separated_data[f"enem20{year2}"] = df_year2

            elif year == 2023:
                # Ajustar a ordem das colunas para 2023
                df_enem = df_enem[["insc", 'enem2022', 'nome', 'cpf', 'ncnt22', 'ncht22', 'nlct22', 'nmt22', 'nred22']]
                # Ajustar as colunas para o formato e ordem desejados
                df_enem = df_enem.rename(columns={
                    "insc": "insc",
                    'enem2022': "enem",
                    'nome': "nome",
                    'cpf': "cpf",
                    'ncnt22': "ncnt",
                    'ncht22': "ncht",
                    'nlct22': "nlct",
                    'nmt22': "nmt",
                    'nred22': "nred"
                })

                # Selecionar apenas as colunas ajustadas
                df_enem = df_enem[["insc", "enem", "nome", "cpf", "ncnt", "ncht", "nlct", "nmt", "nred"]]

                separated_data[f"enem{year - 1}"] = df_enem


    # Escrever cada DataFrame em um arquivo Excel separado
    output_dir = "/home/giovani/testes/enem/"
    os.makedirs(output_dir, exist_ok=True)
    for year, df in separated_data.items():
        output_file = os.path.join(output_dir, f"{year}.xlsx")
        df.to_excel(output_file, index=False)
        print(f"DataFrame for {year} written to {output_file}")

    return separated_data


def merge_enem_fin(excel_data: dict, separated_enem: dict):
    '''
    Acrescenta aos arquivos do enem as informações do arquivo fin
    
    Para os anos de 2018 a 2021
    Usa os dfs do enem (já separados corretamente) e os dfs do fin em excel data
    Primeiro, formata as colunas do fin (para ficar com as mesmas do enem)
    Para isso, seleciona as 9 primeiras colunas, renomeia corretamente e troca a ordem das colunas nome e cpf (coloca nome antes de cpf)
    Concatena os dois dfs e elimina as pessoas duplicadas (mantendo a cópia que está no fin)
    Após isso, verifica se há pessoas com, pelo menos, duas notas vazias e as remove do df em caso afirmativo
    Por fim, armazena o resultado final em um arquivo excel
    
    Parâmetros:
        excel_data (dict): Um dicionário contendo os DataFrames lidos.
        separated_enem (dict): Um dicionário com os DataFrames do enem separados por ano
    '''
    years = [2018, 2019, 2020, 2021, 2022]
    for year in years:
        df_fin = excel_data[year]['Fin']
        df_enem = separated_enem[f"enem{year}"]
        
        # Ajustando as colunas do fin para ficar com as mesma do enem
        df_fin = df_fin.iloc[:, :9]
        df_fin = df_fin.rename(columns={
            "INSC": "insc",
            f"enem{year}": "enem"
        })
        df_fin = df_fin[["insc", "enem", "nome", "cpf", "ncnt", "ncht", "nlct", "nmt", "nred"]]
        
        # Concatenando os dois dataframes e eliminando as réplicas
        df_merged = pd.concat([df_enem, df_fin]).drop_duplicates(subset=["cpf"], keep='last').reset_index(drop=True)
        
        # Dropando as colunas "enem", "nome" e "cpf"
        df_merged = df_merged.drop(columns=["enem", "nome", "cpf"])
        
        # Removendo pessoas com, pelo menos, duas notas vazias
        df_merged = df_merged.replace(0, pd.NA)
        df_merged = df_merged.dropna(subset=["ncnt", "ncht", "nlct", "nmt", "nred"], thresh=2)
        df_merged = df_merged.fillna(0)
        
        # Salvando o resultado final em um arquivo Excel
        output_dir = "/home/giovani/testes/enem/"
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, f"merged_enem_fin_{year}.xlsx")
        df_merged.to_excel(output_file, index=False)
        print(f"DataFrame for {year} written to {output_file}")
            

def main():
    # Anos para os arquivos CSV
    #csv_years = list(range(2018, 2020))
    #csv_data = read_csv_files(csv_years, reading_parameters)

    # Exibe as colunas que existem nos arquivos CSV do enem lidos
    #columns_enem(csv_data)

    # Anos para os arquivos Excel
    excel_years = list(range(2018, 2024))
    excel_data = read_excel_files(excel_years)

    # Compara os arquivos Excel
    #compare_enem_fin(excel_data)
    
    # Comparando os arquivos excel VU e fin
    #vu_years = list(range(2019, 2024))
    #vu_data = read_excel_files(vu_years)
    #compare_columns_fin_vu(vu_data)
    #compare_rows_fin_vu(vu_data)
    
    # Verificando se há duplicadas entre enem e fin
    # compare_enem_fin_rows(excel_data)
    # compare_grades_enem_consecutives_years(excel_data)
    separated_enem = separate_enem(excel_data)
    merge_enem_fin(excel_data, separated_enem)


if __name__ == "__main__":
    main()
