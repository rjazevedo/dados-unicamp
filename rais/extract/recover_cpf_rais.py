import pandas as pd
import yaml

from rais.utilities.file import get_all_tmp_files
from rais.utilities.file import get_all_pre_processed_files
from rais.utilities.read import read_rais_merge
from rais.utilities.read import read_rais_merge_by_identification
from rais.utilities.read import read_rais_identification_parquet
from rais.utilities.write import write_rais_merge
from rais.utilities.logging import log_recover_cpf_rais

stream = open("rais/configuration.yaml")
config = yaml.safe_load(stream)


def recover_cpf_all_years():
    df = join_all_years()
    df_pis_cpf = get_pis_cpf(df)

    intervalo = config["intervalo_rais"]
    for year in range(intervalo[0], intervalo[1] + 1):
        log_recover_cpf_rais(year)
        recover_cpf_year(df_pis_cpf, year)


# ------------------------------------------------------------------------------------------------
# Join rais people that is dac comvest union and save in file "rais.csv"
def join_all_years():
    dfs = []
    intervalo = config["intervalo_rais"]
    for year in range(intervalo[0], intervalo[1] + 1):
        df = join_year(year)
        dfs.append(df)
    df = pd.concat(dfs, sort=True)
    return df


# Join rais people from year that is dac comvest union and return dataframe
def join_year(year):
    files = get_all_tmp_files(year, "rais_dac_comvest", "csv")
    dfs = []
    for file_rais in files:
        df = read_rais_merge(file_rais)
        dfs.append(df)
    df = pd.concat(dfs, sort=True)
    return df


# ------------------------------------------------------------------------------------------------
def get_pis_cpf(df):
    df_cpf_pis = df.loc[:, ["cpf_r", "pispasep", "id", "id_blake2s"]]
    df_cpf_pis = df_cpf_pis.drop_duplicates()
    df_cpf_pis = df_cpf_pis[df_cpf_pis["pispasep"].notna()]
    df_cpf_pis = df_cpf_pis[~df_cpf_pis.duplicated(subset=["pispasep"], keep=False)]
    return df_cpf_pis


# ------------------------------------------------------------------------------------------------
def recover_cpf_year(df_pis_cpf, year):
    files = get_all_pre_processed_files(year, "parquet")
    for file in files:
        recover_cpf_file(df_pis_cpf, file, year)


def recover_cpf_file(df_pis_cpf, file, year):
    df_rais = read_rais_identification_parquet(file)
    df_cpf_recovered = recover_cpf(df_pis_cpf, df_rais)
    df_cpf_known = read_rais_merge_by_identification(file, year)
    df_concat = pd.concat([df_cpf_known, df_cpf_recovered], sort=True)
    write_rais_merge(df_concat, year, file)


# ------------------------------------------------------------------------------------------------
# Paralelizacao (run_pipeline.sh): join_all_years()+get_pis_cpf() precisa ler
# TODOS os anos antes de gerar a tabela pis->cpf->id (nao da pra paralelizar
# esse passo por ano) -- roda 1x, sequencial, e persiste o resultado em disco.
# Cada worker de ano so entao le esse arquivo de volta em vez de recalcular.
PIS_CPF_LOOKUP_FILE = config["path_output_data"] + "tmp/pis_cpf_lookup.csv"


def build_and_save_pis_cpf_lookup():
    df = join_all_years()
    df_pis_cpf = get_pis_cpf(df)
    df_pis_cpf.to_csv(PIS_CPF_LOOKUP_FILE, index=False)


def load_pis_cpf_lookup():
    return pd.read_csv(PIS_CPF_LOOKUP_FILE, dtype=str)


def recover_cpf(df_pis_cpf, df_rais):
    df_cpf_missing = df_rais[df_rais["cpf_r"].isna()]
    del df_cpf_missing["cpf_r"]
    del df_cpf_missing["mun_estbl"]
    df_cpf_missing = df_cpf_missing.reset_index()
    cpf_recovered = pd.merge(df_cpf_missing, df_pis_cpf, on="pispasep")
    cpf_recovered = cpf_recovered.set_index("index")
    return cpf_recovered


# Worker de 1 ano so -- usado pelo orquestrador paralelo (run_pipeline.sh).
# Requer que build_and_save_pis_cpf_lookup() ja tenha rodado (1x, sequencial)
# antes de qualquer worker de ano comecar.
def main():
    import argparse
    import logging
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")

    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--build-lookup", action="store_true")
    group.add_argument("--year", type=int)
    args = parser.parse_args()

    if args.build_lookup:
        build_and_save_pis_cpf_lookup()
    else:
        df_pis_cpf = load_pis_cpf_lookup()
        log_recover_cpf_rais(args.year)
        recover_cpf_year(df_pis_cpf, args.year)


if __name__ == "__main__":
    main()
