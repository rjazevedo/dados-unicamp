import pandas as pd
from pandas import DataFrame
from pandas import Series
import numpy as np
import os

def replace_N_with_nan(profis: DataFrame) -> DataFrame:
    """
    Preenche valores com 'N' na coluna "matriculado" por nan, seguindo o padrão na COMVEST.
    
    Parâmetros
    ----------
    profis : DataFrame
        DataFrame a ser processado.
    
    Retorna
    -------
    DataFrame
        DataFrame com valores nulos na coluna 'matriculado' preenchidos com 'N'.
    """
    for col in profis.columns:
        if col in ["matriculado", "matrfim", "Matriculado", "Matrfim"]:
            profis[col] = profis[col].replace("N", np.nan)
        
    return profis


def calculate_age_at_year(df: DataFrame, exam_year: int) -> Series: 
    """
    Calcula a idade dos candidatos no ano `exam_year`, com base na data de
    nascimento (dia, mês, ano). Considera que quem nasceu em outubro (mês 10)
    ou antes já fez aniversário; quem nasceu em novembro/dezembro ainda não.
    
    Parâmetros
    ----------
    df : DataFrame
        DataFrame com as informações do Profis.
    exam_year : int
        Ano do exame (ex: 2022).
        
    Retorna
    -------
    Series
        Série com as idades dos candidatos no ano do exame.
    """
    birth_year = df["ano"].astype(int)
    birth_month = df["mes"].astype(int)
    age = exam_year - birth_year
    # subtrai 1 para nascidos após maio (época de inscrição)
    return age - (birth_month > 5).astype(int)


def get_questions(df: DataFrame) -> DataFrame:
    """
    Extrai as colunas de questões do DataFrame, renomeando-as para o padrão da COMVEST.
    
    Colunas de questões são identificadas por nomes que começam com 'q' seguidos de números.
    
    Parâmetros
    ----------
    df : DataFrame
        DataFrame com as informações do ProFIS.
        
    Retorna
    -------
    set
        Conjunto com os nomes das colunas de questões, renomeadas para o padrão da
        
    """
    questions = df.filter(regex=r'^q\d+[A-Za-z]?$')
    questions = questions.rename(columns=lambda x: x.replace('q', 'q'))
    
    return set(questions)


def stand_2011_questions(profis: DataFrame, perfil_comvest: DataFrame) -> DataFrame:
    """
    Padroniza as questões do ProFIS de 2011 para o formato presente no dicionário da COMVEST.
    
    Parâmetros
    ----------
    profis : DataFrame
        DataFrame com as informações do ProFIS.
    perfil_comvest : DataFrame
        DataFrame de perfil da Comvest (modelo).
        
    Retorna
    -------
    DataFrame
        DataFrame com as questões padronizadas.
    """
    # 1) Remapeia as questões do ProFIS para o sua equivalente na COMVEST
    rename_map = {
        "q1": "q1",
        "q2": "q2",
        "q3": "q5",
        "q4": "q6",
        "q5": "q7",
        "q6": "q8",
        "q7": "q9",
        "q8": "q11",
        "q9": "q13",
        "q10": "q14",
        "q11": "q15",
        "q12": "q16",
        "q13": "q17",
        "q14": "q18",
        "q15": "q19",
        "q16": "q20",
        "q17": "q21",
        "q18": "q22",
        "q19": "q23",
        "q20": "q24",
        "q21": "q25",
        "q22": "q30",
        "q23a": "q28a",
        "q23b": "q28b",
        "q23c": "q28c",
        "q23d": "q28d",
        "q24a": "q32a",
        "q24b": "q32b",
        "q24c": "q32c",
        "q24d": "q32d",
        "q24e": "q32e",
        "q25a": "q33a",
        "q25b": "q33b",
        "q25c": "q33c",
        "q25d": "q33d",
        "q25e": "q33e",
    }
    
    # 2) Renomeia as colunas do ProFIS de acordo com o mapeamento
    profis = profis.rename(columns=rename_map)
    
    # 3) Faz com que todas os valores 0 na coluna 'q13' virem 'N'
    if "q13" in profis.columns:
        profis["q13"] = profis["q13"].replace(0, "N")
    
    # 4) Extrai todas as colunas de questões da COMVEST (como modelo)
    comvest_questions = get_questions(perfil_comvest)
    profis_questions = get_questions(profis)
    
    # 5) Encontra a diferença nos dois questionários (questões que estão na COMVEST, mas não estão no ProFIS)
    questions_diff = comvest_questions - profis_questions
    
    # 6) Adiciona as questões que estão na COMVEST, mas não estão no ProFIS, após o remapeamento
    for question in questions_diff:
        profis[question] = 0        
    
    return profis


def build_perfil_profis(profis: DataFrame, perfil_comvest: DataFrame, year: int) -> DataFrame:
    """
    Cria o DataFrame de perfil do Profis para o ano especificado.
    
    Parâmetros
    ----------
    profis : DataFrame
        DataFrame com as informações do ProFIS.
    perfil_comvest : DataFrame
        DataFrame de perfil da Comvest (modelo).
    year : int
        Ano correspondente ao DataFrame.
    
    Retorna
    -------
    DataFrame
        DataFrame com o perfil do Profis, padronizado de acordo com a Comvest.
    """
    # Se o ano for 2011, aplica o remapeamento das questões
    if year == 2011:
        profis = stand_2011_questions(profis, perfil_comvest)
    
    # 1) Identifica dinamicamente qual coluna usar como inscrição
    rename_map = {}
    for col in ("insc", "insc2"):
        if col in profis.columns:
            rename_map[col] = "insc_cand"
            break

    # 2) Idem para município de inscrição (se for o caso)
    if "municipio" in profis.columns:
        rename_map["municipio"] = "cid_inscricao"

    # 3) Aplica só as renomeações que existem
    perfil = profis.rename(columns=rename_map)
    perfil["idade"] = calculate_age_at_year(perfil, year)
    
    # 4) Encontra quais as colunas que estão na Comvest e não estão no Profis
    cols_comvest = perfil_comvest.columns
    cols_profis = perfil.columns
    cols_diff = set(cols_comvest) - set(cols_profis)
    
    # 5) Adiciona as colunas que estão na Comvest e não estão no Profis
    for col in cols_diff:
        if col == "curpas":
            if year < 2020:
                perfil[col] = np.nan
            else:
                perfil[col] = 0
        elif col == "universidade":
            perfil[col] = 1
        elif col == "vestibular":
            perfil[col] = year
        elif col == "aprovf2":
            matriculado_col = None
            for col2 in ["matriculado", "matrfim", "Matriculado", "Matrfim"]:
                if col2 in perfil.columns:
                    matriculado_col = col2
                    break
            if matriculado_col is not None:
                if year < 2018:
                    # Para anos abaixo de 2018, mapeia "S" para 1 e "N" para 0
                    perfil["aprovf2"] = np.where(perfil[matriculado_col].str.upper() == "S", 1, 0)
                else:
                    # A partir de 2018, mantém "S" ou "N"
                    perfil["aprovf2"] = np.where(perfil[matriculado_col].str.upper() == "S", "S", "N")
        elif col == "processo":
            perfil[col] = "ProFIS"
        elif col == "opcao1" or col == "opcao2":
            perfil[col] = 200      
        else:
            perfil[col] = 0
    
    # 6) Para este ano, a questão 13, relacionada à renda, veio na coluna "renda"
    if year == 2012:
        perfil['q13'] = perfil['renda']
    
    # 7) Seleciona do df do profis (perfil) somente as colunas que estão na Comvest
    perfil = perfil[cols_comvest]
    
    # 8) Na coluna "sexo", para manter o padrão da Comvest, converte "M" para 1 e "F" para 2
    if "sexo" in perfil.columns:
        perfil["sexo"] = perfil["sexo"].str.upper().replace({"M": 1, "F": 2})
    
    return perfil


def build_dados_profis(profis: DataFrame, dados_profis_comvest: DataFrame) -> DataFrame:
    """
    Cria o DataFrame de dados do Profis para o ano especificado, baseando-se no padrão de 2022.
    
    Parâmetros
    ----------
    profis : DataFrame
        DataFrame com as informações do ProFIS.
    perfil_comvest : DataFrame
        DataFrame de dados do profis da Comvest (modelo de 2022).
    
    Retorna
    -------
    DataFrame
        DataFrame com os dados do Profis, padronizado de acordo com a Comvest.
    """
    profis.columns = profis.columns.str.upper()
    # 1) Renomeia as colunas para padronizar
    rename_map = {}
    for col in ("INSC", "INSC2"):
        if col in profis.columns:
            rename_map[col] = "INSC_CAND"
            break
    
    if "NOME" in profis.columns:
        rename_map["NOME"] = "NOME_CAND"
        
    if "ESCOLA" in profis.columns:
        rename_map["ESCOLA"] = "NOME_ESCOLA"
    
    # 2) Aplica só as renomeações que existem
    dados = profis.rename(columns=rename_map)

    # 3) Encontra quais as colunas que estão na Comvest e não estão no Profis
    cols_comvest = dados_profis_comvest.columns
    cols_profis = dados.columns
    cols_diff = set(cols_comvest) - set(cols_profis)
    
    for col in cols_diff:
        if col == "TIPODOC":
            dados[col] = "CPF"
        elif col == "DOC":
            dados[col] = profis["CPF"]
        else:
            dados[col] = np.nan
    
    # 4) Seleciona do df do profis (perfil) somente as colunas que estão na Comvest
    dados = dados[cols_comvest]
    dados["MUNICIPIO_NASC"] = dados["MUNICIPIO_NASC"].str.upper()
    
    # 5) Corrige o tipo das colunas "PAIS_NASC" e "DOC" para ser object, assim como na Comvest
    if "PAIS_NASC" in dados.columns:
        dados["PAIS_NASC"] = dados["PAIS_NASC"].astype("object")
    if "DOC" in dados.columns:
        dados["DOC"] = dados["DOC"].astype("object")
    
    return dados
    

def build_notas_enem_profis(profis: DataFrame, year: int) -> DataFrame:
    """
    Cria o DataFrame de notas do ENEM do Profis para o ano especificado, baseando-se no padrão dos arquivos fin.
    
    O arquivo fin foi escolhido como padrão, uma vez que seu formato é o mais compatível com o que vem no ProFIS. 
    Isso se deve ao fato de ele ter as notas do ENEM para um único ano, sendo este um anterior ao que consta no nome do arquivo.
    
    Parâmetros
    ----------
    profis : DataFrame
        DataFrame com as informações do ProFIS.
    year : int
        Ano correspondente ao DataFrame.
        
    Retorna
    -------
    DataFrame
        DataFrame com as notas do ENEM do Profis, padronizado de acordo com o padrão dos arquivos fin.
    """
    # Renomeia as colunas para padronizar
    # 1) Identifica dinamicamente qual coluna usar como inscrição
    profis.columns = profis.columns.str.lower()
    rename_map = {}
    for col in ("insc", "insc2"):
        if col in profis.columns:
            rename_map[col] = f"comvest_{year}"
            break

    # 2) Idem para nome e para o cpf do candidato
    if "nome" in profis.columns:
        rename_map["nome"] = "NOME"
        
    if "cpf" in profis.columns:
        rename_map["cpf"] = "CPF"
        
    # 3) Faz a renomeação para as colunas de notas do ENEM no ProFIS
    if year == 2011:
        rename_map["nhum"] = f"ncnt{year - 1}"
        rename_map["nnat"] = f"ncht{year - 1}"
        rename_map["nlin"] = f"nlct{year - 1}"
        rename_map["nmat"] = f"nmt{year - 1}"
        rename_map["nred"] = f"nred{year - 1}"
        
    else:
        rename_map["ncnt"] = f"ncnt{year - 1}"
        rename_map["ncht"] = f"ncht{year - 1}"
        rename_map["nlct"] = f"nlct{year - 1}"
        rename_map["nmt"] = f"nmt{year - 1}"
        rename_map["nred"] = f"nred{year - 1}"
        
    # 4) Aplica só as renomeações que existem
    notas_enem = profis.rename(columns=rename_map)
    
    # 5) Seleciona apenas as colunas que estão no padrão do ENEM
    notas_enem = notas_enem.loc[:,[f"comvest_{year}", "NOME", "CPF",
                        f"ncnt{year - 1}", f"ncht{year - 1}", f"nlct{year - 1}", f"nmt{year - 1}", f"nred{year - 1}"]]
    
    # 6) Especifica as colunas que devem ser adicionadas para deixar o arquivo no padrão do ENEM
    cols_to_add = [f'enem{year - 1}', f'enem{year - 2}' ,f'ncnt{year - 2}', f'ncht{year - 2}', f'nlct{year - 2}', 
                    f'nmt{year - 2}', f'nred{year - 2}']
    
    # 7) Preenche as novas colunas com valores nulos
    for col in cols_to_add:
        notas_enem[col] = np.nan
    
    # 8) Ajusta a ordem das colunas do fin para que seja a mesma do df do enem
    notas_enem = notas_enem[[f'comvest_{year}', f'enem{year - 2}', f'enem{year - 1}', 'NOME', 'CPF',
             f'ncnt{year - 2}', f'ncht{year - 2}', f'nlct{year - 2}', f'nmt{year - 2}', f'nred{year - 2}',
             f'ncnt{year - 1}', f'ncht{year - 1}', f'nlct{year - 1}', f'nmt{year - 1}', f'nred{year - 1}']]
    
    # 9) Corrige o tipo das colunas "CPF" para int64, enem{year - 1} e enem{year} para object e nred{year - 1} e nred{year} para float64
    if "CPF" in notas_enem.columns:
        notas_enem["CPF"] = notas_enem["CPF"].astype("Int64")
    if f'enem{year - 2}' in notas_enem.columns:
        notas_enem[f'enem{year - 2}'] = notas_enem[f'enem{year - 2}'].astype("object")
    if f'enem{year - 1}' in notas_enem.columns:
        notas_enem[f'enem{year - 1}'] = notas_enem[f'enem{year - 1}'].astype("object")
    if f'nred{year - 2}' in notas_enem.columns:
        notas_enem[f'nred{year - 2}'] = notas_enem[f'nred{year - 2}'].astype("float64")
    if f'nred{year - 1}' in notas_enem.columns:
        notas_enem[f'nred{year - 1}'] = notas_enem[f'nred{year - 1}'].astype("float64")
    
    return notas_enem
    

def main() -> None:
    # Nome do arquivo com as inforações do Profis
    arquivo_profis = "/home/input/COMVEST/Profis11a22.xlsx"
    # Colunas que não possuem nenhuma correspondência na Comvest
    unused_columns = ["ddd", "telefone", "ddd_cel", "celular", "email", "rua", "bairro", "renda1"]
    # Cria o diretório para armazenar os arquivos de perfil do ProFIS
    os.makedirs(f"/home/output/intermediario/ProfisDivided/perfil", exist_ok=True)
    # Cria o diretório para armazenar os arquivos de dados do ProFIS
    os.makedirs(f"/home/output/intermediario/ProfisDivided/profis_dados", exist_ok=True)
    # Cria o diretório para armazenar os arquivos de notas do ENEM do ProFIS
    os.makedirs(f"/home/output/intermediario/ProfisDivided/notas_enem", exist_ok=True)
    # Padrão dos dados do ProFIS estabelecido na Comvest de 2022 (planilha profis_dados)
    profis_dados_comvest = pd.read_excel("/home/input/COMVEST/ingresso2022.xlsx", sheet_name="profis_dados")
    
    for year in range(2011, 2023):
        print(f"Processando ano {year}")
        # Leitura utilizando somente as colunas definidas para o ano
        print(f"Lendo o arquivo do Profis para o ano {year}")
        profis = pd.read_excel(arquivo_profis, sheet_name=str(year))  
        
        if year in (2021, 2022):
            profis = replace_N_with_nan(profis)
        
        print(f"Lendo o arquivo da Comvest para o ano {year}")
        if year < 2019:
            perfil_comvest = pd.read_excel(f"/home/input/COMVEST/vest{year}.xlsx", sheet_name="perfil")
        else:
            perfil_comvest = pd.read_excel(f"/home/input/COMVEST/ingresso{year}.xlsx", sheet_name="perfil")

        # Utiliza letra minúscula para os nomes das colunas indesejadas
        profis.columns = [col.lower() for col in profis.columns]
        profis_columns = [col for col in profis.columns if col not in unused_columns]
        profis = profis[profis_columns]
        
        # Constrói o perfil do ProFIS utilizando o padrão estabelecido na Comvest
        perfil_profis = build_perfil_profis(profis, perfil_comvest, year)

        # Constrói os dados do ProFIS utilizando o padrão estabelecido na Comvest de 2022
        dados_profis = build_dados_profis(profis, profis_dados_comvest)
        
        # Constrói as notas do ENEM do ProFIS utilizando o padrão estabelecido na base do ENEM
        notas_enem_profis = build_notas_enem_profis(profis, year)
 
        print(f"Salvando o arquivo do perfil do ProFIS para o ano {year}")
        perfil_profis.to_excel(f"/home/output/intermediario/ProfisDivided/perfil/perfil_profis{year}.xlsx", index=False)
        
        print(f"Salvando o arquivo dos dados do ProFIS para o ano {year}")   
        dados_profis.to_excel(f"/home/output/intermediario/ProfisDivided/profis_dados/profis_dados{year}.xlsx", index=False)   
         
        print(f"Salvando o arquivo das notas do ENEM do ProFIS para o ano {year}")
        if year == 2011:
            notas_enem_profis.to_csv(f"/home/output/intermediario/Enem_Comvest/EnemComvest{year}.csv", index=False) 
        else:
            notas_enem_profis.to_csv(f"/home/output/intermediario/ProfisDivided/notas_enem/notas_enem_profis{year}.csv", index=False)

    print("Geração dos arquivos intermediários do ProFIS concluída com sucesso!")    
    
    
if __name__ == '__main__':
    main()
