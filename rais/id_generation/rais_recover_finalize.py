"""
Passo 2 (dedup final) + escrita do resultado -- roda depois que TODOS os
workers paralelos do Passo 1 (rais_recover_worker.py) ja terminaram. Le os
parquets brutos particionados por ano/lote que os workers escreveram
(RAW_MATCHES_DIR), aplica o dedup final por lote (fix_duplicated_rows_*,
inalterado), escreve o resultado final (uniao_dac_comvest_recovered.csv).

Uso: uv run python3 -m rais.id_generation.rais_recover_finalize
"""

import argparse
import logging
import os
import sys

import pandas as pd

from rais.utilities.read import read_dac_comvest_valid
from rais.utilities.logging import log_recover_batch
from rais.id_generation.recover_cpf_dac_comvest import (
    get_cpf_missing_dac_comvest,
    prepare_candidate_batches,
    finalize_batch,
    finalize_and_write,
    _cleanup_raw_matches_dir,
    CPF_RECOVERED_BATCHES_FILE,
    BATCH_SIZE,
)


def main():
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s [finalize] %(message)s", stream=sys.stdout
    )
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--batch-size", type=int, default=BATCH_SIZE)
    args = parser.parse_args()

    df_dac_comvest = read_dac_comvest_valid()
    df_cpf_missing = get_cpf_missing_dac_comvest(df_dac_comvest)
    _, _, _, all_batch_ids = prepare_candidate_batches(df_cpf_missing, args.batch_size)
    n_batches = len(all_batch_ids)

    if os.path.exists(CPF_RECOVERED_BATCHES_FILE):
        os.remove(CPF_RECOVERED_BATCHES_FILE)

    for i, batch_id in enumerate(all_batch_ids, start=1):
        log_recover_batch(i, n_batches, args.batch_size)
        finalize_batch(batch_id)

    _cleanup_raw_matches_dir()

    finalize_and_write(df_dac_comvest)


if __name__ == "__main__":
    main()
