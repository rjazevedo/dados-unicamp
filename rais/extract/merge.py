from difflib import SequenceMatcher

from rais.utilities.read import read_ids
from rais.utilities.read import read_rais_identification
from rais.utilities.write import write_rais_merge
from rais.utilities.file import create_folder_inside_year
from rais.utilities.file import get_all_tmp_files

from rais.utilities.logging import log_merge_rais_dac_comvest


# Merge all the years from rais with uniao_dac_comvest and save in file rais.csv
def merge_all_years():
    df_dac_comvest = read_ids()
    df_dac_comvest = prepare_dac_comvest(df_dac_comvest)

    for year in range(2002, 2019):
        log_merge_rais_dac_comvest(year)
        create_folder_inside_year(year, "rais_dac_comvest")
        merge_year(df_dac_comvest, year)


# Merge rais from year with df_dac_comvest and save in files in rais_dac_comvest directory
def merge_year(df_dac_comvest, year):
    files = get_all_tmp_files(year, "identification_data", "pkl")

    for file_rais in files:
        print(f"File: {file_rais}")
        df_rais = read_rais_identification(file_rais)
        df = merge_dfs(df_rais, df_dac_comvest)
        write_rais_merge(df, year, file_rais)


# Merge rais df with dac/comvest df and remove invalid cpfs
def merge_dfs(df_rais, df_dac_comvest):
    result = df_rais.reset_index().merge(df_dac_comvest)
    result = check_is_same_person(result)
    result = filter_columns_rais_dac_comvest(result)
    result = result.drop_duplicates().set_index("index")
    return result


# ------------------------------------------------------------------------------------------------
# Read file with dac/comvest union and return dataframe
def prepare_dac_comvest(df):
    df = df[df["cpf"] != "-"]
    df.drop_duplicates(subset=["cpf"], inplace=True)
    df.rename(columns={"cpf": "cpf_r"}, inplace=True)
    return df


# Rename columns after merge
def filter_columns_rais_dac_comvest(df):
    columns = ["ano_base", "nome_r", "cpf_r", "dta_nasc_r", "pispasep", "index", "id"]
    df = df.loc[:, columns]
    return df


# ------------------------------------------------------------------------------------------------
# Remove cases of people with different names and return resultant dataframe
def check_is_same_person(df):
    same_person = df.apply(lambda x: is_same_person(x["nome_r"], x["nome"]), axis=1)
    if same_person.empty:
        return df.drop(df.index)
    return df[same_person]


# Says if person_a is person_b based on the probabilistic match between the two first names
def is_same_person(name_a, name_b):
    first_name_a = name_a.split()[0]
    first_name_b = name_b.split()[0]
    similar_rate = SequenceMatcher(None, first_name_a, first_name_b).ratio()
    return similar_rate > 0.7
