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
    log_recover_cpf_probabilistic_match()
    df_cpf_recovered_exact_match, df_cpf_recovered_probabilistic_match = (
        recover_cpf_matches(df_cpf_missing)
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


# Computes exact match and probabilistic match together, reading and
# preparing (clean_name/primeiro_nome) each RAIS file only ONCE for both --
# previously each ran as a fully separate pass over all 17 anos x ~500
# arquivos (merge_with_rais chamado 2x), lendo+descomprimindo+limpando o
# mesmo dado duas vezes (~68% do tempo total, ver achado de profiling no
# commit). Diferenca de comportamento: a busca probabilistica aqui roda
# sobre a populacao COMPLETA de faltantes (nao exclui previamente quem ja
# foi recuperado pelo exact match, como a versao anterior fazia antes do
# merge) e so exclui esses casos DEPOIS, no resultado -- equivalente,
# porque o merge eh independente por linha (o resultado calculado pra um
# candidato nao muda dependendo de quais OUTROS candidatos estao no lote) e
# a deduplicacao por merge_id em fix_duplicated_rows_probabilistic_match
# tambem age por grupo de merge_id, sem interacao entre candidatos
# diferentes. Validado por teste de equivalencia (ver commit) comparando
# contra a versao anterior em dado real.
def recover_cpf_matches(df_cpf_missing):
    df_dac_comvest_exact = df_cpf_missing.copy(deep=True)
    df_dac_comvest_exact.nome = clean_name_column(df_dac_comvest_exact.nome)
    del df_dac_comvest_exact["cpf"]

    df_dac_comvest_prob = df_cpf_missing.copy(deep=True)
    df_dac_comvest_prob.nome = clean_name_column(df_dac_comvest_prob.nome)
    del df_dac_comvest_prob["cpf"]
    df_dac_comvest_prob["primeiro_nome"] = get_first_name(df_dac_comvest_prob["nome"])

    df_merged_exact, df_merged_prob = merge_with_rais(
        df_dac_comvest_exact, df_dac_comvest_prob
    )

    log_filter_results()
    df_recovered_exact = remove_invalid_cpf(df_merged_exact)
    df_recovered_exact = fix_duplicated_rows_exact_match(df_recovered_exact)

    df_recovered_prob_all = remove_invalid_cpf(df_merged_prob)
    df_recovered_prob_all = fix_duplicated_rows_probabilistic_match(
        df_recovered_prob_all
    )
    df_recovered_prob = update_cpf_missing(df_recovered_prob_all, df_recovered_exact)

    return df_recovered_exact, df_recovered_prob


# Return df with rows from df1 whose merge_id doesn't appear in df2 -- usado
# tanto pra excluir do resultado probabilistico quem ja foi recuperado pelo
# exact match (ver recover_cpf_matches) quanto, no fluxo geral do pipeline,
# pra achar quem ainda ficou sem CPF depois de tudo.
def update_cpf_missing(df_cpf_missing, df_cpf_recovered):
    columns = ["merge_id"]
    updated_cpf_missing = subtract(df_cpf_missing, df_cpf_recovered, columns)
    return updated_cpf_missing


# Return df with initial dataframe replaced with all cpfs recovered
def join_cpf_recovered(
    df_dac_comvest, df_cpf_recovered_exact_match, df_cpf_recovered_probabilistic_match
):
    dfs = [df_cpf_recovered_exact_match, df_cpf_recovered_probabilistic_match]
    df_cpf_recovered = pd.concat(dfs)
    result = update_cpf_dac_comvest(df_cpf_recovered, df_dac_comvest)
    return result


# ------------------------------------------------------------------------------------------------
# Renomeia colunas e limpa o nome UMA vez (nome_r), derivando tanto "nome"
# (chave do exact match) quanto "primeiro_nome" (chave do probabilistic
# match) do mesmo valor limpo -- antes, cada modo de busca limpava o
# mesmo nome_r de novo, do zero, numa passada separada pelo arquivo.
def prepare_df_rais(df):
    df.rename(columns={"cpf_r": "cpf"}, inplace=True)
    df.rename(columns={"dta_nasc_r": "dta_nasc"}, inplace=True)
    df["nome_r"] = clean_name_column(df["nome_r"])
    df["nome"] = df["nome_r"]
    df["primeiro_nome"] = get_first_name(df["nome_r"])
    return df


# Returns only the first name of the person for the whole column (vectorized).
# Non-string entries (incl. NaN) stay NaN; "" stays "" (matches the original
# row-wise behavior exactly, incl. its edge cases -- see test_vectorize_equivalence.py)
def get_first_name(names):
    first = names.str.split().str[0]
    is_empty = names == ""
    return first.where(~is_empty.fillna(False), "")


# ------------------------------------------------------------------------------------------------
# Merge dataframes with all files from rais to recover missing cpfs -- exact
# match e probabilistic match juntos, ver recover_cpf_matches.
def merge_with_rais(df_dac_comvest_exact, df_dac_comvest_prob):
    dfs_exact = []
    dfs_prob = []
    for year in range(2002, 2019):
        log_recover_from_year(year)
        df_exact_year, df_prob_year = merge_with_rais_year(
            df_dac_comvest_exact, df_dac_comvest_prob, year
        )
        dfs_exact.append(df_exact_year)
        dfs_prob.append(df_prob_year)

    df_exact = pd.concat(dfs_exact, sort=True).drop_duplicates()
    df_prob = pd.concat(dfs_prob, sort=True).drop_duplicates()
    return df_exact, df_prob


# Merge dataframes with all files from some year to recover missing cpfs
def merge_with_rais_year(df_dac_comvest_exact, df_dac_comvest_prob, year):
    files_rais = get_all_tmp_files(year, "identification_data", "pkl")

    dfs_exact = []
    dfs_prob = []
    for file in files_rais:
        df_rais = read_rais_identification(file)
        # Data from year 2011-2013 has the wrong dtype on column 'dta_nasc_r',
        # it's float64 when it should be object
        if year == 2011 or year == 2012 or year == 2013:
            df_rais = df_rais.astype({"dta_nasc_r": "object"})
        del df_rais["pispasep"]
        df_rais = df_rais.drop_duplicates()
        df_rais = prepare_df_rais(df_rais)

        dfs_exact.append(find_cpf_exact_match(df_dac_comvest_exact, df_rais))
        dfs_prob.append(find_cpf_probabilistic_match(df_dac_comvest_prob, df_rais))

    df_exact = pd.concat(dfs_exact).drop_duplicates()
    df_prob = pd.concat(dfs_prob).drop_duplicates()
    return df_exact, df_prob


# ------------------------------------------------------------------------------------------------
# Drop rows from df_right whose join key doesn't occur at all in df_left, so the
# actual merge doesn't have to hold/hash irrelevant rows in memory
def filter_matching_keys(df_left, df_right, columns):
    left_keys = pd.MultiIndex.from_frame(df_left[columns])
    right_keys = pd.MultiIndex.from_frame(df_right[columns])
    return df_right[right_keys.isin(left_keys)]


# Merge dataframes in name and birthdate, and return all matches. Seleciona
# de df_rais (ja preparado por prepare_df_rais) so as colunas que o exact
# match original usava, pra nao levar adiante nome_r/primeiro_nome (que
# so interessam ao probabilistic match) sem necessidade.
def find_cpf_exact_match(df_dac_comvest, df_rais):
    df_rais_exact = df_rais[["ano_base", "nome", "cpf", "dta_nasc", "mun_estbl"]]
    df_rais_exact = filter_matching_keys(
        df_dac_comvest, df_rais_exact, ["nome", "dta_nasc"]
    )
    result = pd.merge(df_dac_comvest, df_rais_exact, on=["nome", "dta_nasc"])
    if result.empty:
        return result

    # cpf vem de df_rais.cpf_r, que é sempre dtype "str" (nunca outro tipo
    # não-nulo) -- ver test_vectorize_equivalence.py / achado documentado no
    # commit. type(x) == str linha a linha é portanto equivalente a notna().
    result = result[result["cpf"].notna()]
    return result


# Merge dataframes in first name and birthdate, and return matches with high
# similarity. Mesma ideia de find_cpf_exact_match: seleciona so as colunas
# que o probabilistic match original usava.
def find_cpf_probabilistic_match(df_dac_comvest, df_rais):
    df_rais_prob = df_rais[
        ["ano_base", "nome_r", "cpf", "dta_nasc", "mun_estbl", "primeiro_nome"]
    ]
    df_rais_prob = filter_matching_keys(
        df_dac_comvest, df_rais_prob, ["primeiro_nome", "dta_nasc"]
    )
    result = pd.merge(df_dac_comvest, df_rais_prob, on=["primeiro_nome", "dta_nasc"])
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


# Applies clean_name() to a whole column, but calls it only once per unique
# value instead of once per row -- clean_name is pure (unidecode + string
# ops), and ~74-76% dos nomes no RAIS sao unicos, entao a memoizacao corta
# uma fatia real das chamadas caras sem mudar nenhum resultado. Validado
# contra clean_name(row-a-row) em ~50000 nomes reais (0 divergencia) e
# casos sinteticos (None/NaN/"", duplicatas exatas) -- ver
# test_clean_name_dedup.py.
def clean_name_column(names):
    is_null = names.isna()
    non_null = names[~is_null]
    unique_names = non_null.unique()
    cleaned_by_name = {n: clean_name(n) for n in unique_names}
    result = non_null.map(cleaned_by_name)
    result = result.reindex(names.index)
    result = result.where(~is_null, "")
    return result
