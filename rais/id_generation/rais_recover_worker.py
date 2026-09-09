"""
Worker paralelo do Passo 1 de recover_cpf_dac_comvest -- processa so um
intervalo de anos do RAIS, escrevendo em arquivos particionados por ano
(seguro rodar varios workers ao mesmo tempo, cada um com seu proprio
intervalo, sem colidir escrevendo no mesmo arquivo -- ver
recover_cpf_dac_comvest.py::_raw_batch_path).

Cada worker chama prepare_candidate_batches() de novo, de forma
independente -- e deterministico (mesmos df_cpf_missing/batch_size sempre
produzem os mesmos lotes), entao nao precisa compartilhar estado entre
processos.

Uso (exemplo, 8 workers cobrindo 2002-2022):
  uv run python3 -m rais.id_generation.rais_recover_worker --year-start 2002 --year-end 2004
  uv run python3 -m rais.id_generation.rais_recover_worker --year-start 2005 --year-end 2007
  ...

Depois que TODOS os workers terminarem, rodar rais_recover_finalize.py uma
unica vez (Passo 2 + escrita do resultado final).
"""

import argparse
import logging
import sys

from rais.utilities.read import read_dac_comvest_valid
from rais.id_generation.recover_cpf_dac_comvest import (
    get_cpf_missing_dac_comvest,
    prepare_candidate_batches,
    stream_raw_matches,
    BATCH_SIZE,
)


def main():
    # Sem isso, log_recover_from_year/log_recover_file/log_recover_active_batches
    # (logging.info espalhado por recover_cpf_dac_comvest.py) nao aparece em
    # lugar nenhum -- achado real (nao teorico): rodei 8 workers em producao
    # sem NENHUMA visibilidade de progresso, so RSS por fora, exatamente o
    # mesmo erro ja cometido (e corrigido) em debug_stages.py antes. Prefixo
    # com o intervalo de anos pra distinguir qual worker esta logando o que,
    # ja que os 8 saem misturados no mesmo terminal/log se rodados juntos.
    args_for_prefix = " ".join(sys.argv[1:])
    logging.basicConfig(
        level=logging.INFO,
        format=f"%(asctime)s [worker {args_for_prefix}] %(message)s",
        stream=sys.stdout,
    )
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--year-start", type=int, required=True)
    parser.add_argument("--year-end", type=int, required=True)
    parser.add_argument("--batch-size", type=int, default=BATCH_SIZE)
    args = parser.parse_args()

    df_dac_comvest = read_dac_comvest_valid()
    df_cpf_missing = get_cpf_missing_dac_comvest(df_dac_comvest)
    exact_batches, prob_batches, batch_min_year, _ = prepare_candidate_batches(
        df_cpf_missing, args.batch_size
    )
    stream_raw_matches(
        exact_batches, prob_batches, batch_min_year, args.year_start, args.year_end
    )


if __name__ == "__main__":
    main()
