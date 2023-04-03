import pandas as pd
import numpy as np

from rais.extract import cleaning_functions

from rais.utilities.rais_information import get_all_columns_rais
from rais.utilities.rais_information import get_column
from rais.utilities.rais_information import get_columns_info_rais
from rais.utilities.rais_information import get_info_period

from rais.utilities.dtypes import get_dtype_rais_clean

from rais.utilities.file import create_folder_inside_year
from rais.utilities.file import get_all_tmp_files

from rais.utilities.read import read_rais_merge
from rais.utilities.read import read_rais_original_by_merge
from rais.utilities.read import read_rais_clean

from rais.utilities.write import write_rais_clean
from rais.utilities.write import write_rais_sample

from rais.utilities.logging import log_cleaning_year
from rais.utilities.logging import log_cleaning_file


def clear_all_years(tipo_extracao):
    for year in range(2002, 2019):
        log_cleaning_year(year)
        clear_year(year)
    join_all_years(tipo_extracao)


def clear_year(year):
    create_folder_inside_year(year, "clean_data")
    files = get_all_tmp_files(year, "rais_dac_comvest", "csv")
    for file in files:
        clear_file(file, year)


def clear_file(file, year):
    log_cleaning_file(file)
    df_clean = read_rais_merge(file)
    df_original = read_rais_original_by_merge(file, year)
    df_final = get_columns(df_clean, df_original, year, file)
    write_rais_clean(df_final, year, file)


def join_all_years(tipo_extracao):
    dfs = []
    for year in range(2002, 2019):
        files = get_all_tmp_files(year, "clean_data", "csv")
        for file in files:
            df = read_rais_clean(file)
            dfs.append(df)
    result = pd.concat(dfs)
    anonymize_data(result)
    if tipo_extracao == "limitada":
        del result["mun_etbl"]
        del result["cnae95"]
        del result["cnpj"]
        del result["mun_etbl"]
        del result["mun_etbl"]
    final_cleaning(result)
    write_rais_sample(result)


# ------------------------------------------------------------------------------------------------
def get_columns(df_clean, df_original, year, file):
    df_merged = pd.merge(df_clean, df_original, left_index=True, right_index=True)
    df_merged = rename_all_columns(df_merged, year)
    df_clean = clean_columns(df_merged, year)
    columns = get_all_columns_rais()
    valid_cols = list(set(df_clean.columns).intersection(set(columns)))
    df_clean = df_clean.loc[:, valid_cols]
    return df_clean


# ------------------------------------------------------------------------------------------------
def rename_all_columns(df, year):
    columns = get_all_columns_rais()
    columns.remove("id")
    columns.remove("nome_r")
    columns.remove("dta_nasc_r")
    columns.remove("cpf_r")
    columns.remove("pispasep")
    columns.remove("ano_base")
    df = rename_columns(df, year, columns)
    return df


def rename_columns(df, year, new_columns_names):
    clean_dtypes = get_dtype_rais_clean()
    old_column_names = df.columns

    for new_column_name in new_columns_names:
        old_column_name = get_column(new_column_name, year)
        if old_column_name is not None and old_column_name in old_column_names:
            df.rename(columns={old_column_name: new_column_name}, inplace=True)
        else:
            clean_dtype = clean_dtypes[new_column_name]
            if clean_dtype == "object":
                df[new_column_name] = ""
                df = df.astype({new_column_name: "object"})
            elif clean_dtype == "Int64":
                df[new_column_name] = np.nan
            elif clean_dtype == "float64":
                df[new_column_name] = np.nan
    return df


# ------------------------------------------------------------------------------------------------


def final_cleaning(df):
    df["ano_nasc_r"].replace(0, np.nan, inplace=True)
    df["deslig_mes"].replace(-1, np.nan, inplace=True)
    df["raca_r"].replace(0, np.nan, inplace=True)
    df["afast1_causa"].replace(-1, np.nan, inplace=True)
    df["afast1_inic_dia"].replace(-1, np.nan, inplace=True)
    df["afast1_inic_mes"].replace(-1, np.nan, inplace=True)
    df["afast1_fim_dia"].replace(-1, np.nan, inplace=True)
    df["afast1_fim_mes"].replace(-1, np.nan, inplace=True)
    df["afast2_causa"].replace(-1, np.nan, inplace=True)
    df["afast2_inic_dia"].replace(-1, np.nan, inplace=True)
    df["afast2_inic_mes"].replace(-1, np.nan, inplace=True)
    df["afast2_fim_dia"].replace(-1, np.nan, inplace=True)
    df["afast2_fim_mes"].replace(-1, np.nan, inplace=True)
    df["afast3_causa"].replace(-1, np.nan, inplace=True)
    df["afast3_inic_dia"].replace(-1, np.nan, inplace=True)
    df["afast3_inic_mes"].replace(-1, np.nan, inplace=True)
    df["afast3_fim_dia"].replace(-1, np.nan, inplace=True)
    df["afast3_fim_mes"].replace(-1, np.nan, inplace=True)
    df["afast_dias_total"].replace(-1, np.nan, inplace=True)
    df["deslig_dia"].replace(-1, np.nan, inplace=True)


def clean_columns(df, year):
    if df.empty:
        return df
    columns_info = get_columns_info_rais()
    for column in columns_info:
        periods = columns_info[column]["clean_function"]
        function = get_info_period(year, periods)
        if function is not None:
            df[column] = df.apply(lambda x: function(x[column]), axis=1)
    recover_cnpj_raiz(df)
    get_ano_nasc(df)
    fix_deslig_info(df, year)
    return df


def get_ano_nasc(df):
    df["ano_nasc_r"] = df.apply(
        lambda x: cleaning_functions.get_ano_nasc(x["dta_nasc_r"]), axis=1
    )


def recover_cnpj_raiz(df):
    df["cnpj_raiz"] = df.apply(
        lambda x: cleaning_functions.recover_cnpj_raiz(x["cnpj"], x["cnpj_raiz"]),
        axis=1,
    )


def fix_deslig_info(df, year):
    if year == 2010:
        df["deslig_dia"] = df.apply(
            lambda x: cleaning_functions.fix_deslig(
                x["deslig_motivo"], x["deslig_dia"]
            ),
            axis=1,
        )
    elif year >= 2014:
        df["deslig_dia"] = df.apply(
            lambda x: cleaning_functions.fix_deslig(
                x["deslig_motivo"], x["deslig_dia"]
            ),
            axis=1,
        )
    if year >= 2010 and year <= 2011:
        df["deslig_mes"] = df.apply(
            lambda x: cleaning_functions.fix_deslig(
                x["deslig_motivo"], x["deslig_mes"]
            ),
            axis=1,
        )
    elif year >= 2013 and year <= 2018:
        df["deslig_mes"] = df.apply(
            lambda x: cleaning_functions.fix_deslig(
                x["deslig_motivo"], x["deslig_mes"]
            ),
            axis=1,
        )


# ------------------------------------------------------------------------------------------------
def anonymize_data(df):
    del df["nome_r"]
    del df["dta_nasc_r"]
    del df["cpf_r"]
    del df["pispasep"]
    del df["ctps"]
