import pandas as pd
from pandas import DataFrame
import os

"""
Este script define os dicionários com as colunas a serem extraídas de cada planilha
dos dados de ingresso (2011 a 2022). As listas de colunas foram extraídas dos prints
enviados, excluindo as colunas de questões (colunas iniciadas com "q").
"""

# Dicionário com as colunas para cada ano (em "força bruta")
columns = {}

# Planilha 2011
columns["2011"] = [
    'AnoIng', 'insc2', 'nome', 'cpf', 'sexo', 'email', 'municipio_nasc',
    'est_nasc', 'dia', 'mes', 'ano', 'nacionalidade', 'est_civil',
    'nome_pai', 'nome_mae', 'rua', 'complemento', 'bairro', 'municipio',
    'estado', 'cep', 'ddd', 'telefone', 'ddd_cel', 'celular', 'cod_escola',
    'escola', 'NHUM', 'NNAT', 'NLIN', 'NMAT', 'NRED', 'matriculado'
]

# Planilha 2012
columns["2012"] = [
    'AnoIng', 'insc', 'nome', 'cpf', 'sexo', 'email', 'municipio_nasc',
    'est_nasc', 'dia', 'mes', 'ano', 'nacionalidade', 'est_civil',
    'nome_pai', 'nome_mae', 'RUA', 'bairro', 'municipio', 'estado', 'cep',
    'ddd', 'telefone', 'ddd_cel', 'celular', 'cod_escola', 'escola',
    'Renda1', 'Renda', 'ncnt', 'ncht', 'nlct', 'nmt', 'nred', 'nf', 'matrfim'
]

# Planilha 2013
columns["2013"] = [
    'AnoIng', 'insc2', 'nome', 'cpf', 'sexo', 'email', 'municipio_nasc',
    'est_nasc', 'dia', 'mes', 'ano', 'nacionalidade', 'est_civil',
    'nome_pai', 'nome_mae', 'RUA', 'bairro', 'municipio', 'estado', 'cep',
    'ddd', 'telefone', 'ddd_cel', 'celular', 'cod_escola', 'nome_escola',
    'ncnt', 'ncht', 'nlct', 'nmt', 'nred', 'NF', 'Matriculado'
]

# Planilha 2014
columns["2014"] = [
    'AnoIng', 'insc', 'nome', 'cpf', 'sexo', 'email', 'municipio_nasc',
    'est_nasc', 'dia', 'mes', 'ano', 'nacionalidade', 'est_civil',
    'nome_pai', 'nome_mae', 'RUA', 'bairro', 'municipio', 'estado', 'cep',
    'ddd', 'telefone', 'ddd_cel', 'celular', 'cod_escola', 'nome_escola',
    'ncnt', 'ncht', 'nlct', 'nmt', 'nred', 'NF', 'Matriculado'
]

# Planilha 2015 e 2016 (mesma estrutura)
columns["2015"] = [
    'AnoIng', 'insc', 'nome', 'cpf', 'sexo', 'email', 'municipio_nasc',
    'est_nasc', 'dia', 'mes', 'ano', 'nacionalidade', 'est_civil',
    'nome_pai', 'nome_mae', 'tipo_logradouro', 'logradouro', 'numero',
    'complemento', 'bairro', 'municipio', 'estado', 'cep', 'ddd', 'telefone',
    'ddd_cel', 'celular', 'cod_escola', 'nome_escola',
    'ncnt', 'ncht', 'nlct', 'nmt', 'nred', 'NF', 'Matriculado'
]

# Planilha 2017
columns["2017"] = [
    'AnoIng', 'insc2', 'nome', 'cpf', 'sexo', 'email', 'municipio_nasc',
    'est_nasc', 'dia', 'mes', 'ano', 'nacionalidade', 'est_civil',
    'nome_pai', 'nome_mae', 'tipo_logradouro', 'logradouro', 'numero',
    'complemento', 'bairro', 'municipio', 'estado', 'cep', 'ddd', 'telefone',
    'ddd_cel', 'celular', 'cod_escola', 'nome_escola',
    'ncnt', 'ncht', 'nlct', 'nmt', 'nred', 'NF', 'Matriculado'
]

# Planilha 2018
columns["2018"] = [
    'AnoIng', 'insc', 'nome', 'cpf', 'sexo', 'email', 'municipio_nasc',
    'est_nasc', 'dia', 'mes', 'ano', 'nacionalidade', 'est_civil',
    'nome_pai', 'nome_mae', 'tipo_logradouro', 'logradouro', 'numero',
    'complemento', 'bairro', 'municipio', 'estado', 'cep', 'ddd', 'telefone',
    'ddd_cel', 'celular', 'cod_escola', 'nome_escola',
    'ncnt', 'ncht', 'nlct', 'nmt', 'nred', 'NF', 'Matriculado'
]

# Planilha 2019
columns["2019"] = [
    'AnoIng', 'insc2', 'nome', 'cpf', 'sexo', 'email', 'municipio_nasc',
    'est_nasc', 'dia', 'mes', 'ano', 'nacionalidade', 'est_civil',
    'nome_pai', 'nome_mae', 'tipo_logradouro', 'logradouro', 'numero',
    'complemento', 'bairro', 'municipio', 'estado', 'cep', 'ddd', 'telefone',
    'ddd_cel', 'celular', 'cod_escola', 'nome_escola',
    'ncnt', 'ncht', 'nlct', 'nmt', 'nred', 'NF', 'Matrfim'
]

# Planilha 2020
columns["2020"] = [
    'AnoIng', 'insc2', 'nome', 'cpf', 'sexo', 'email', 'municipio_nasc',
    'est_nasc', 'dia', 'mes', 'ano', 'nacionalidade', 'est_civil',
    'nome_pai', 'nome_mae', 'tipo_logradouro', 'logradouro', 'numero',
    'complemento', 'bairro', 'municipio', 'estado', 'cep', 'ddd', 'telefone',
    'ddd_cel', 'celular', 'cod_escola', 'escola',
    'ncnt', 'ncht', 'nlct', 'nmt', 'nred', 'NF', 'Matrfim'
]

# Planilha 2021
columns["2021"] = [
    'AnoIng', 'insc', 'nome', 'cpf', 'sexo', 'email', 'municipio_nasc',
    'est_nasc', 'dia', 'mes', 'ano', 'nacionalidade', 'est_civil',
    'nome_pai', 'nome_mae', 'tipo_logradouro', 'logradouro', 'numero',
    'complemento', 'bairro', 'municipio', 'estado', 'cep', 'ddd', 'telefone',
    'ddd_cel', 'celular', 'cod_escola', 'nome_escola',
    'ncnt', 'ncht', 'nlct', 'nmt', 'nred', 'NF', 'matriculado'
]

# Planilha 2022
columns["2022"] = [
    'AnoIng', 'insc', 'nome', 'cpf', 'sexo', 'email', 'municipio_nasc',
    'est_nasc', 'dia', 'mes', 'ano', 'nacionalidade', 'est_civil',
    'nome_pai', 'nome_mae', 'tipo_logradouro', 'logradouro', 'numero',
    'complemento', 'bairro', 'municipio', 'estado', 'cep', 'ddd', 'telefone',
    'ddd_cel', 'celular', 'cod_escola', 'nome_escola',
    'ncnt', 'ncht', 'nlct', 'nmt', 'nred', 'NF', 'matriculado'
]

# Dicionário de parâmetros de leitura para cada ano
reading_parameters = {
    2011: {"columns": columns["2011"]},
    2012: {"columns": columns["2012"]},
    2013: {"columns": columns["2013"]},
    2014: {"columns": columns["2014"]},
    2015: {"columns": columns["2015"]},
    2016: {"columns": columns["2015"]},
    2017: {"columns": columns["2017"]},
    2018: {"columns": columns["2018"]},
    2019: {"columns": columns["2019"]},
    2020: {"columns": columns["2020"]},
    2021: {"columns": columns["2021"]},
    2022: {"columns": columns["2022"]},
}

# Dicionário de padronização de colunas para cada ano (renomeia só o necessário)
stand_columns_dict = {
    2011: {
        "AnoIng": "ano",
        "insc2": "insc",
        "NHUM": "ncht",
        "NNAT": "ncnt",
        "NLIN": "nlct",
        "NMAT": "nmt",
        "NRED": "nred",
    },
    2012: {
        "AnoIng": "ano",
        "RUA": "rua",
        "Renda1": "renda1",
        "Renda": "renda",
        "matrfim": "matriculado",
    },
    2013: {
        "AnoIng": "ano",
        "insc2": "insc",
        "RUA": "rua",
        "NF": "nf",
        "Matriculado": "matriculado",
    },
    2014: {
        "AnoIng": "ano",
        "RUA": "rua",
        "NF": "nf",
        "Matriculado": "matriculado",
    },
    2015: {
        "AnoIng": "ano",
        "NF": "nf",
        "Matriculado": "matriculado",
    },
    2016: {
        "AnoIng": "ano",
        "NF": "nf",
        "Matriculado": "matriculado",
    },
    2017: {
        "AnoIng": "ano",
        "insc2": "insc",
        "NF": "nf",
        "Matriculado": "matriculado",
    },
    2018: {
        "AnoIng": "ano",
        "NF": "nf",
        "Matriculado": "matriculado",
    },
    2019: {
        "AnoIng": "ano",
        "insc2": "insc",
        "NF": "nf",
        "Matrfim": "matriculado",
    },
    2020: {
        "AnoIng": "ano",
        "insc2": "insc",
        "NF": "nf",
        "Matrfim": "matriculado",
    },
    2021: {
        "AnoIng": "ano",
        "NF": "nf",
        "matriculado": "matriculado",
    },
    2022: {
        "AnoIng": "ano",
        "NF": "nf",
        "matriculado": "matriculado",
    },
}


def stand_columns(df: DataFrame, ano: int) -> DataFrame:
    """
    Padroniza os nomes das colunas do DataFrame para o ano especificado.
    
    Utiliza o dicionário de padronização de colunas para renomear apenas as colunas
    
    Parâmetros
    ----------
    df : DataFrame
        DataFrame a ser padronizado.
    ano : int
        Ano correspondente ao DataFrame.
    
    Retorna
    -------
    DataFrame
        DataFrame com os nomes das colunas padronizados.
    """
    std_columns = stand_columns_dict[ano]
    for col in std_columns:
        if col in df.columns:
            df = df.rename(columns={col: std_columns[col]})
            
    return df


def fill_matrnull_withN(df: DataFrame) -> DataFrame:
    """
    Preenche valores nulos na coluna 'matriculado' com 'N'.
    
    Parâmetros
    ----------
    df : DataFrame
        DataFrame a ser processado.
    
    Retorna
    -------
    DataFrame
        DataFrame com valores nulos na coluna 'matriculado' preenchidos com 'N'.
    """
    if "matriculado" in df.columns:
        df["matriculado"] = df["matriculado"].fillna("N")
        
    return df


def main():
    nome_arquivo = "/home/input/COMVEST/Profis11a22.xlsx"
    for year in range(2011, 2023):
        print(f"Processando ano {year}")
        # Leitura utilizando somente as colunas definidas para o ano
        df = pd.read_excel(nome_arquivo, sheet_name=str(year), usecols=reading_parameters[year]["columns"])
        df = stand_columns(df, year)
        
        if year not in (2021, 2022):
            df = fill_matrnull_withN(df)
        
        
        os.makedirs("/home/giovani/testes/Profis", exist_ok=True)
        df.to_excel(f"/home/giovani/testes/Profis/profis{year}.xlsx", index=False)
        
         
if __name__ == '__main__':
    main()