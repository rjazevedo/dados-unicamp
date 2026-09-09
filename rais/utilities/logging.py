import logging


def log_reading_file(file):
    logging.debug(f"Reading file {file}")


def log_pre_process(year):
    logging.info(f"Pre-processing year {year}\nThis might take a while\n")


def log_writing_file(file):
    logging.debug(f"Writing file {file}")


def log_remove_invalid_cpf():
    logging.info(
        "Removing invalid CPF from DAC Comvest Union\nThis might take a while\n"
    )


def log_recover_cpf_exact_match():
    logging.info(
        "Recovering CPF from DAC Comvest Union by exact match\nThis might take a while\n"
    )


def log_recover_cpf_probabilistic_match():
    logging.info(
        "Recovering CPF from DAC Comvest Union by probabilistic match\nThis might take a while\n"
    )


def log_recover_from_year(year):
    logging.info(f"Recovering from year {year} of RAIS\nThis might take a while\n")


def log_filter_results():
    logging.info("Filtering recovery results\nThis might take a while\n")


def log_recover_batch(batch_num, n_batches, batch_size):
    logging.info(
        f"Recovering CPF batch {batch_num}/{n_batches} (batch_size={batch_size})\n"
    )


def log_recover_file(year, file_num, n_files, file, n_rais_rows, n_exact, n_prob):
    logging.info(
        f"[{year}] arquivo {file_num}/{n_files} ({file}): "
        f"{n_rais_rows} linhas RAIS, {n_exact} match exato, {n_prob} match probabilistico"
    )


def log_excluded_no_birthdate(n_excluded, n_total):
    logging.info(
        f"Excluidos {n_excluded}/{n_total} candidatos sem data de nascimento valida "
        f"(sentinela/ausente) -- busca por nome sozinho e pouco confiavel e cara em memoria\n"
    )


def log_recover_active_batches(year, n_active, n_total_batches):
    logging.info(
        f"[{year}] {n_active}/{n_total_batches} coortes elegiveis pra este ano\n"
    )


def log_create_index():
    logging.info("Generating index to individuals from DAC Comvest Union\n")


def log_merge_rais_dac_comvest(year):
    logging.info(f"Merging year {year} of RAIS with IDs\nThis might take a while\n")


def log_recover_cpf_rais(year):
    logging.info(
        f"Recovering CPF from year {year} of RAIS based on PIS\nThis might take a while\n"
    )


def log_cleaning_year(year):
    logging.info(f"Cleaning year {year} from RAIS\nThis might take a while\n")


def log_cleaning_file(file):
    logging.debug(f"Cleaning file: {file}")


def log_verifying_database():
    logging.info("Verifying RAIS Sample\n")


def log_verifying_column(column):
    logging.info(f"Verifying column: {column}")


def log_show_result(df, columns):
    if df.empty:
        logging.info("All entries are OK\n")
    else:
        num_fail = df.shape[0]
        df = df.loc[:, columns]
        logging.info(f"Failed in {num_fail} entries\nHead:\n{df.head()}\n")
