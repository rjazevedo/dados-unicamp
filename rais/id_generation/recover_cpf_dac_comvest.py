import pandas as pd
import numpy as np
from difflib import SequenceMatcher

from rais.utilities.df_operations import subtract
from rais.utilities.df_operations import remove_duplicated_rows
from rais.utilities.read import read_dac_comvest_valid
from rais.utilities.read import read_rais_identification
from rais.utilities.write import write_dac_comvest_recovered
from rais.utilities.file import get_all_tmp_files

from rais.utilities.logging import log_recover_cpf_exact_match
from rais.utilities.logging import log_recover_cpf_probabilistic_match
from rais.utilities.logging import log_recover_from_year
from rais.utilities.logging import log_filter_results
from unidecode import unidecode

# ------------------------------------------------------------------------------------------------

UNICO = 3
HOMONIMO = 4
HIGH_SIMILARITY = 5
MEDIUM_SIMILARITY = 6

MIN_MEDIUM_SIMILARITY = 0.8
MIN_HIGH_SIMILARITY = 0.85


# Uses initial union dac/comvest to recover missing
# cpfs in rais and generate a new file with cpfs recovered
def recover_cpf_dac_comvest():
    df_dac_comvest = read_dac_comvest_valid()
    df_cpf_missing = get_cpf_missing_dac_comvest(df_dac_comvest)

    log_recover_cpf_exact_match()
    df_cpf_recovered_exact_match = recover_cpf_exact_match(df_cpf_missing)

    df_cpf_missing = update_cpf_missing(df_cpf_missing, df_cpf_recovered_exact_match)

    log_recover_cpf_probabilistic_match()
    df_cpf_recovered_probabilistic_match = recover_cpf_probabilistic_match(
        df_cpf_missing
    )

    df_final = join_cpf_recovered(
        df_dac_comvest,
        df_cpf_recovered_exact_match,
        df_cpf_recovered_probabilistic_match,
    )
    write_dac_comvest_recovered(df_final)


# ------------------------------------------------------------------------------------------------
# Return df with only the lines with cpf missing or cpf from parents
def get_cpf_missing_dac_comvest(df):
    cpf_missing = df[df.cpf == "-"]
    cpf_missing = cpf_missing.drop_duplicates()
    return cpf_missing


# Return df with matches made with name and birthdate equal
def recover_cpf_exact_match(df):
    prepare_df_dac_comvest_exact_match(df)
    df_recovered = merge_with_rais(df, False)
    log_filter_results()
    df_recovered = remove_invalid_cpf(df_recovered)
    df_recovered = fix_duplicated_rows_exact_match(df_recovered)
    return df_recovered


# Return df with missing cpfs after first recover
def update_cpf_missing(df_cpf_missing, df_cpf_recovered):
    columns = ["merge_id"]
    updated_cpf_missing = subtract(df_cpf_missing, df_cpf_recovered, columns)
    return updated_cpf_missing


# Return df with matches made with first name, birthdate equal and high similarity between names
def recover_cpf_probabilistic_match(df):
    prepare_df_dac_comvest_probabilistic_match(df)
    df_merged = merge_with_rais(df, True)
    log_filter_results()
    df_recovered = remove_invalid_cpf(df_merged)
    df_recovered = fix_duplicated_rows_probabilistic_match(df_recovered)
    return df_recovered


# Return df with initial dataframe replaced with all cpfs recovered
def join_cpf_recovered(
    df_dac_comvest, df_cpf_recovered_exact_match, df_cpf_recovered_probabilistic_match
):
    dfs = [df_cpf_recovered_exact_match, df_cpf_recovered_probabilistic_match]
    df_cpf_recovered = pd.concat(dfs)
    result = update_cpf_dac_comvest(df_cpf_recovered, df_dac_comvest)
    return result


# ------------------------------------------------------------------------------------------------
# Rename columns to use in merge
def prepare_df_dac_comvest_exact_match(df):
    df.nome = df.nome.apply(clean_name)
    del df["cpf"]


# Rename columns to use in merge
def prepare_df_rais_exact_match(df):
    df.rename(columns={"cpf_r": "cpf"}, inplace=True)
    df.rename(columns={"dta_nasc_r": "dta_nasc"}, inplace=True)
    df.rename(columns={"nome_r": "nome"}, inplace=True)
    df.nome = df.nome.apply(clean_name)


# Rename columns and get first name to use in merge
def prepare_df_dac_comvest_probabilistic_match(df):
    df["primeiro_nome"] = get_first_name(df["nome"])


# Rename columns and get first name to use in merge
def prepare_df_rais_probabilistic_match(df):
    df.rename(columns={"cpf_r": "cpf"}, inplace=True)
    df.rename(columns={"dta_nasc_r": "dta_nasc"}, inplace=True)
    df.nome_r = df.nome_r.apply(clean_name)
    df["primeiro_nome"] = get_first_name(df["nome_r"])


# Returns only the first name of the person for the whole column (vectorized).
# Non-string entries (incl. NaN) stay NaN; "" stays "" (matches the original
# row-wise behavior exactly, incl. its edge cases -- see test_vectorize_equivalence.py)
def get_first_name(names):
    first = names.str.split().str[0]
    is_empty = names == ""
    return first.where(~is_empty.fillna(False), "")


# ------------------------------------------------------------------------------------------------
# Merge dataframe with all files from rais to recover missing cpfs
def merge_with_rais(df_dac_comvest, is_probabilistic):
    dfs = []
    for year in range(2002, 2019):
        log_recover_from_year(year)
        df_recovered = merge_with_rais_year(df_dac_comvest, year, is_probabilistic)
        dfs.append(df_recovered)

    df = pd.concat(dfs, sort=True)
    df = df.drop_duplicates()
    return df


# Merge dataframe with all files from some year to recover missing cpfs
def merge_with_rais_year(df_dac_comvest, year, is_probabilistic):
    files_rais = get_all_tmp_files(year, "identification_data", "pkl")

    dfs = []
    for file in files_rais:
        df_rais = read_rais_identification(file)
        # Data from year 2011-2013 has the wrong dtype on column 'dta_nasc_r',
        # it's float64 when it should be object
        if year == 2011 or year == 2012 or year == 2013:
            df_rais = df_rais.astype({"dta_nasc_r": "object"})
        del df_rais["pispasep"]
        df_rais = df_rais.drop_duplicates()
        if is_probabilistic:
            df_recovered = find_cpf_probabilistic_match(df_dac_comvest, df_rais)
        else:
            df_recovered = find_cpf_exact_match(df_dac_comvest, df_rais)
        dfs.append(df_recovered)

    df = pd.concat(dfs)
    df = df.drop_duplicates()
    return df


# ------------------------------------------------------------------------------------------------
# Drop rows from df_right whose join key doesn't occur at all in df_left, so the
# actual merge doesn't have to hold/hash irrelevant rows in memory
def filter_matching_keys(df_left, df_right, columns):
    left_keys = pd.MultiIndex.from_frame(df_left[columns])
    right_keys = pd.MultiIndex.from_frame(df_right[columns])
    return df_right[right_keys.isin(left_keys)]


# Merge dataframes in name and birthdate, and return all matches
def find_cpf_exact_match(df_dac_comvest, df_rais):
    prepare_df_rais_exact_match(df_rais)
    df_rais = filter_matching_keys(df_dac_comvest, df_rais, ["nome", "dta_nasc"])
    result = pd.merge(df_dac_comvest, df_rais, on=["nome", "dta_nasc"])
    if result.empty:
        return result

    # cpf vem de df_rais.cpf_r, que é sempre dtype "str" (nunca outro tipo
    # não-nulo) -- ver test_vectorize_equivalence.py / achado documentado no
    # commit. type(x) == str linha a linha é portanto equivalente a notna().
    result = result[result["cpf"].notna()]
    return result


# Merge dataframes in first name and birthdate, and return matches with high similarity
def find_cpf_probabilistic_match(df_dac_comvest, df_rais):
    prepare_df_rais_probabilistic_match(df_rais)
    df_rais = filter_matching_keys(
        df_dac_comvest, df_rais, ["primeiro_nome", "dta_nasc"]
    )
    result = pd.merge(df_dac_comvest, df_rais, on=["primeiro_nome", "dta_nasc"])
    if result.empty:
        return result

    # get_similarity usa SequenceMatcher, sem equivalente vetorizado direto;
    # zip evita o boxing de linha inteira do DataFrame.apply(axis=1).
    result["similaridade"] = [
        get_similarity(a, b) for a, b in zip(result["nome_r"], result["nome"])
    ]
    result = result[
        result["cpf"].notna() & (result["similaridade"] >= MIN_MEDIUM_SIMILARITY)
    ]
    return result


# Calculate similarity of names a and b
def get_similarity(a, b):
    if (type(a) != str) or (type(b) != str):
        return 0.0
    nomes_a = a.split()
    nomes_b = b.split()
    sobrenome_a = " ".join(nomes_a[1:])
    sobrenome_b = " ".join(nomes_b[1:])

    similar_rate = SequenceMatcher(None, sobrenome_a, sobrenome_b).ratio()
    return similar_rate


def remove_invalid_cpf(df):
    return df[is_valid_cpf(df["cpf"]).to_numpy()]


# Vectorized CPF check-digit validation over a whole column. Same algorithm
# as the original row-wise version (zfill to 11, reject non-11-digit and
# palindrome CPFs, validate both check digits), just done with array ops
# instead of a Python loop per row. Validated against the original with a
# 9-case + 5000-case randomized equivalence test before applying (see
# test_vectorize_equivalence.py).
def is_valid_cpf(cpf_column):
    filled = cpf_column.str.zfill(11)
    digits_df = filled.str.extract(r"^(\d)(\d)(\d)(\d)(\d)(\d)(\d)(\d)(\d)(\d)(\d)$")
    valid_format = digits_df.notna().all(axis=1)
    digits = digits_df.fillna(0).astype(int).to_numpy()

    not_palindrome = ~(digits == digits[:, ::-1]).all(axis=1)

    def check_digit(pos):
        weights = np.arange(pos + 1, 1, -1)
        valor = (digits[:, :pos] * weights).sum(axis=1)
        digito = ((valor * 10) % 11) % 10
        return digito == digits[:, pos]

    return valid_format & not_palindrome & check_digit(9) & check_digit(10)


# ------------------------------------------------------------------------------------------------
# Remove duplicated lines according to priority
def fix_duplicated_rows_exact_match(df):
    df = order_by_priority(df)
    get_origem_cpf_column_exact_match(df)
    df = get_dac_information_exact_match(df)
    columns = ["merge_id"]
    df = remove_duplicated_rows(df, columns)
    return df


# Remove duplicated lines according to priority
def fix_duplicated_rows_probabilistic_match(df):
    get_origem_cpf_column_probabilistic_match(df)
    df = order_by_similarity(df)
    df = get_dac_information_probabilistic_match(df)
    columns = ["merge_id"]
    df = remove_duplicated_rows(df, columns)
    return df


# ------------------------------------------------------------------------------------------------
# Priority of a city, by state code (first 2 digits of mun_estbl)
PRIORITY_BY_STATE_CODE = {
    "35": 3,  # SP
    "33": 2,  # RJ
    "31": 2,  # MG
    "32": 2,  # ES
    "53": 1,  # DF
}


# Order dataframe by priority of the year and state
def order_by_priority(df):
    df["prioridade"] = get_priority(df["mun_estbl"], df["ano_base"])
    df = df.sort_values(by="prioridade", ascending=False)
    del df["prioridade"]
    del df["mun_estbl"]
    del df["ano_base"]
    df = df.drop_duplicates()
    return df


# Order dataframe by similarity between names in rais and dac/comvest
def order_by_similarity(df):
    df = df.sort_values(by="similaridade", ascending=False)
    del df["similaridade"]
    return df


# Get the value of priority based on state and year of the register (vectorized)
def get_priority(mun, ano_base):
    is_str = mun.map(lambda x: type(x) == str)
    state_code = mun.where(is_str, other="").astype(str).str.slice(0, 2)
    mun_priority = state_code.map(PRIORITY_BY_STATE_CODE).fillna(0)
    mun_priority = mun_priority.where(is_str, 0)
    return mun_priority * 10000 + ano_base


# ------------------------------------------------------------------------------------------------
# Create origem_cpf column
def get_origem_cpf_column_exact_match(df):
    columns = ["merge_id"]
    df["duplicado"] = df.duplicated(subset=columns, keep=False)
    df["origem_cpf"] = np.where(df["duplicado"], HOMONIMO, UNICO)
    del df["duplicado"]


# Create origem_cpf column
def get_origem_cpf_column_probabilistic_match(df):
    df["origem_cpf"] = np.where(
        df["similaridade"] >= MIN_HIGH_SIMILARITY, HIGH_SIMILARITY, MEDIUM_SIMILARITY
    )


# ------------------------------------------------------------------------------------------------
# Filter and rename columns
def get_dac_information_exact_match(df):
    df.rename(columns={"dtanasc": "dta_nasc"}, inplace=True)
    df = filter_columns_dac_comvest(df)
    return df


# Filter and rename columns
def get_dac_information_probabilistic_match(df):
    df.rename(columns={"dtanasc": "dta_nasc"}, inplace=True)
    df.rename(columns={"nome_dac_comvest": "nome"}, inplace=True)
    df = filter_columns_dac_comvest(df)
    return df


# Filter only columns that appear in dac/comvest
def filter_columns_dac_comvest(df):
    columns = [
        "insc_vest",
        "nome",
        "origem_cpf",
        "dta_nasc",
        "ano_ingresso_curso",
        "cpf",
        "merge_id",
        "invalid",
    ]
    df = df.loc[:, columns]
    df = df.drop_duplicates()
    return df


# ------------------------------------------------------------------------------------------------
# Update initial dataframe with recovered cpfs and return resultant dataframe
def update_cpf_dac_comvest(df_cpf_recovered, df_uniao_dac_comvest):
    df_cpf_recovered = df_cpf_recovered.loc[:, ["cpf", "origem_cpf", "merge_id"]]
    df_cpf_recovered.rename(columns={"cpf": "cpf_recovered"}, inplace=True)
    df_cpf_recovered.rename(
        columns={"origem_cpf": "origem_cpf_recovered"}, inplace=True
    )
    df_cpf_recovered["recovered"] = True

    result = df_uniao_dac_comvest.merge(df_cpf_recovered, on=["merge_id"], how="left")
    was_recovered = result["recovered"] == True
    result["cpf"] = result["cpf"].where(~was_recovered, result["cpf_recovered"])
    result["origem_cpf"] = (
        result["origem_cpf"]
        .where(~was_recovered, result["origem_cpf_recovered"])
        .astype(int)
    )

    del result["cpf_recovered"]
    del result["origem_cpf_recovered"]
    del result["recovered"]

    return result


def clean_name(name):
    if pd.isnull(name):
        return ""
    else:
        s = unidecode(name).upper().strip()
        return " ".join(s.split())
