import pandas as pd
import numpy as np
import yaml

from rais.extract import cleaning_functions

from rais.utilities.rais_information import get_all_columns_rais
from rais.utilities.rais_information import get_column
from rais.utilities.rais_information import get_columns_info_rais
from rais.utilities.rais_information import get_info_period

from rais.utilities.dtypes import get_dtype_rais_clean

from rais.utilities.file import create_folder_inside_year
from rais.utilities.file import get_all_tmp_files

from rais.utilities.read import read_rais_merge
from rais.utilities.read import read_rais_original_pre_processed
from rais.utilities.read import read_rais_clean

from rais.utilities.write import write_rais_clean
from rais.utilities.write import write_rais_sample

from rais.utilities.logging import log_cleaning_year
from rais.utilities.logging import log_cleaning_file

stream = open("rais/configuration.yaml")
config = yaml.safe_load(stream)


def clear_all_years(tipo_extracao):
    intervalo = config["intervalo_rais"]
    for year in range(intervalo[0], intervalo[1] + 1):
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
    df_original = read_rais_original_pre_processed(file, year)
    df_final = get_columns(df_clean, df_original, year, file)
    write_rais_clean(df_final, year, file)


def join_all_years(tipo_extracao):
    dfs = []
    intervalo = config["intervalo_rais"]
    for year in range(intervalo[0], intervalo[1] + 1):
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
        # del result["mun_etbl"]
        # del result["mun_etbl"]
    final_cleaning(result)
    write_rais_sample(result)


# ------------------------------------------------------------------------------------------------
def get_columns(df_clean, df_original, year, file):
    # suffixes=("", "_original"): df_original agora vem do cache parquet
    # pre-processado (read_rais_original_pre_processed), que ja tem
    # nome_r/cpf_r/dta_nasc_r/pispasep/ano_base/mun_estbl renomeados pro nome
    # canonico (parquet_parsing.py roda rename_columns() nessas 5 antes de
    # gravar) -- colide com as mesmas colunas ja presentes em df_clean (vindas
    # de merge.py). Sem suffixes explicito o pandas gera "pispasep_x"/"_y" pros
    # dois lados, quebrando clean_columns() (achado real rodando o teste de
    # integracao, KeyError em 'pispasep'). suffixes=("", "_original") mantem o
    # nome plano pro lado de df_clean (a versao correta) e joga a duplicata
    # redundante de df_original pra "<col>_original" (nunca selecionada depois,
    # fica so como redundancia inofensiva).
    df_merged = pd.merge(
        df_clean, df_original, left_index=True, right_index=True,
        suffixes=("", "_original"),
    )
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
    # mun_estbl: mesma razao das 5 acima -- ja vem renomeado do parquet_parsing.py,
    # NAO remover faria rename_columns() procurar o nome bruto antigo (ex.
    # "Município"), nao achar (a coluna ja se chama "mun_estbl"), e sobrescrever
    # o dado real com um placeholder NaN -- bug real encontrado rodando o teste
    # de integracao (silencioso, sem crash, so viraria NaN). Mesmo bug existe
    # em origin/giovani (nao removeu mun_estbl da lista), corrigido aqui.
    columns.remove("mun_estbl")
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
    df["ano_nasc_r"] = df["ano_nasc_r"].replace(0, np.nan)
    df["deslig_mes"] = df["deslig_mes"].replace(-1, np.nan)
    df["raca_r"] = df["raca_r"].replace(0, np.nan)
    df["afast1_causa"] = df["afast1_causa"].replace(-1, np.nan)
    df["afast1_inic_dia"] = df["afast1_inic_dia"].replace(-1, np.nan)
    df["afast1_inic_mes"] = df["afast1_inic_mes"].replace(-1, np.nan)
    df["afast1_fim_dia"] = df["afast1_fim_dia"].replace(-1, np.nan)
    df["afast1_fim_mes"] = df["afast1_fim_mes"].replace(-1, np.nan)
    df["afast2_causa"] = df["afast2_causa"].replace(-1, np.nan)
    df["afast2_inic_dia"] = df["afast2_inic_dia"].replace(-1, np.nan)
    df["afast2_inic_mes"] = df["afast2_inic_mes"].replace(-1, np.nan)
    df["afast2_fim_dia"] = df["afast2_fim_dia"].replace(-1, np.nan)
    df["afast2_fim_mes"] = df["afast2_fim_mes"].replace(-1, np.nan)
    df["afast3_causa"] = df["afast3_causa"].replace(-1, np.nan)
    df["afast3_inic_dia"] = df["afast3_inic_dia"].replace(-1, np.nan)
    df["afast3_inic_mes"] = df["afast3_inic_mes"].replace(-1, np.nan)
    df["afast3_fim_dia"] = df["afast3_fim_dia"].replace(-1, np.nan)
    df["afast3_fim_mes"] = df["afast3_fim_mes"].replace(-1, np.nan)
    df["afast_dias_total"] = df["afast_dias_total"].replace(-1, np.nan)
    df["deslig_dia"] = df["deslig_dia"].replace(-1, np.nan)


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
    # Limite superior original era 2018 (nunca estendido, nem pelo giovani).
    # fix_deslig() so muda o valor quando deslig_mes==0 E deslig_motivo!=0 --
    # se esse padrao nao existir em 2019-2022, a chamada e um no-op seguro;
    # se existir (igual ao padrao ja visto em 2013-2018), fica corrigido.
    # Nao validado com dado real de 2019-2022 ainda -- ver plan.md.
    elif year >= 2013:
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
