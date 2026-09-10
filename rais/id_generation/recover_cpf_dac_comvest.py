import pandas as pd
import numpy as np
import os
import math
import gc
from difflib import SequenceMatcher

from rais.utilities.df_operations import subtract
from rais.utilities.df_operations import remove_duplicated_rows
from rais.utilities.read import read_dac_comvest_valid
from rais.utilities.read import read_rais_identification_parquet
from rais.utilities.write import write_dac_comvest_recovered
from rais.utilities.file import get_all_pre_processed_files

from rais.utilities.logging import log_recover_cpf_exact_match
from rais.utilities.logging import log_recover_cpf_probabilistic_match
from rais.utilities.logging import log_recover_from_year
from rais.utilities.logging import log_filter_results
from rais.utilities.logging import log_recover_batch
from rais.utilities.logging import log_recover_file
from rais.utilities.logging import log_excluded_no_birthdate
from rais.utilities.logging import log_recover_active_batches
from unidecode import unidecode
from config.settings import get_config

config = get_config("rais")

# ------------------------------------------------------------------------------------------------

UNICO = 3
HOMONIMO = 4
HIGH_SIMILARITY = 5
MEDIUM_SIMILARITY = 6

MIN_MEDIUM_SIMILARITY = 0.8
MIN_HIGH_SIMILARITY = 0.85

# Tier B: tamanho do lote do lado DAC/COMVEST (quem precisa de CPF) casado
# de cada vez, por arquivo do RAIS. O merge probabilistico (nome+data de
# nascimento, chave nao-unica) pode explodir combinatorialmente pra grupos de
# nome/data comuns -- quanto maior o lado esquerdo do merge, maior o pior
# caso por grupo.
#
# Desenho (2 passos, ver recover_cpf_matches_batched): cada arquivo do RAIS
# e lido **uma unica vez** (igual a versao sem blocagem -- blocar o lado
# DAC/COMVEST nao exige reler o RAIS por lote, so repetir o merge, que ja
# esta em memoria). Passo 1: pra cada arquivo [lido 1x], o merge roda por
# lote de candidatos, e o resultado BRUTO (antes do dedup por
# prioridade/similaridade, que precisa ver os matches de TODOS os anos de
# uma vez) vai incrementalmente pra 1 arquivo parquet por lote (parquet, nao
# csv, pra preservar dtype dos campos usados no dedup -- ano_base/similaridade/
# mun_estbl). Passo 2: por lote (bem menor que a populacao inteira), le de
# volta so os matches brutos DAQUELE lote e aplica o mesmo dedup final de
# sempre (fix_duplicated_rows_*, inalterado), escrevendo o resultado final
# incrementalmente. Nao muda nenhum resultado -- cada linha e casada de forma
# independente por merge_id (unico por linha do lado DAC/COMVEST), sem
# interacao entre candidatos de lotes diferentes; so muda quantas linhas
# passam por um merge/dedup de cada vez. Validado por teste de equivalencia
# com dado real (ver scratchpad/test_tier_b_equivalence.py).
BATCH_SIZE = 5000
RAW_MATCHES_DIR = config["path_output_data"] + "tmp/cpf_recover_raw_batches/"
CPF_RECOVERED_BATCHES_FILE = (
    config["path_output_data"] + "tmp/cpf_recovered_batches.csv"
)

# Idade minima de trabalho no Brasil usada pra descartar anos do RAIS
# implausiveis por candidato (aprendiz, valor conservador -- confirmado com
# o usuario 2026-09-07). Candidatos sem data de nascimento valida (sentinela
# "00000000"/ausente) sao excluidos da busca inteiramente, nao so deste
# calculo -- sem idade real, a busca vira so por nome, que e exatamente o
# cenario de explosao combinatoria em nomes comuns (achado real: homonimos
# tipo "ANTONIO CARLOS DA SILVA NETO" casando com 20+ CPFs distintos so
# porque ambos os lados tem a mesma data sentinela). So 1,7% da populacao
# tem data ausente, mas o resultado quando "casa" e HOMONIMO de confianca
# minima mesmo assim -- nao vale o risco de memoria pra um resultado ja
# sabidamente pouco confiavel.
MIN_WORKING_AGE = 14


def has_valid_birthdate(dta_nasc):
    return dta_nasc.notna() & (dta_nasc != "00000000") & (dta_nasc != "")


# Ano minimo do RAIS em que cada candidato poderia plausivelmente ja estar
# empregado (nascimento + idade minima de trabalho, nunca antes do primeiro
# ano coberto pelo RAIS). Usado pra pular coortes inteiras de candidatos
# jovens demais em anos antigos do RAIS -- ver stream_raw_matches_year.
def get_min_rais_year(dta_nasc, intervalo_rais_start):
    birth_year = pd.to_numeric(dta_nasc.str[-4:], errors="coerce")
    min_year = (birth_year + MIN_WORKING_AGE).fillna(intervalo_rais_start).astype(int)
    return min_year.clip(lower=intervalo_rais_start)


# Lote = coorte de ano minimo de elegibilidade, subdividido em pedacos de
# batch_size dentro de cada coorte (uma coorte grande sozinha ainda pode
# passar de batch_size). Diferente do lote anterior (posicao arbitraria):
# isso permite pular a coorte INTEIRA pra anos do RAIS anteriores ao ano
# minimo dela, sem nem tentar o merge (ver stream_raw_matches_year) --
# blocagem por ano, nao so por tamanho.
def _assign_batch_ids(df, batch_size):
    sub_idx = df.groupby("_min_rais_year").cumcount() // batch_size
    return df["_min_rais_year"].astype(str) + "_" + sub_idx.astype(str)


# Uses initial union dac/comvest to recover missing
# cpfs in rais and generate a new file with cpfs recovered
def recover_cpf_dac_comvest(batch_size=BATCH_SIZE):
    df_dac_comvest = read_dac_comvest_valid()
    df_cpf_missing = get_cpf_missing_dac_comvest(df_dac_comvest)

    recover_cpf_matches_batched(df_cpf_missing, batch_size)

    finalize_and_write(df_dac_comvest)


# Le CPF_RECOVERED_BATCHES_FILE (ja escrito, seja pelo caminho sequencial
# acima ou pelo Passo 2 rodado externamente por rais_recover_finalize.py
# apos workers paralelos -- ver rais_recover_worker.py) e produz o arquivo
# final. Extraido de recover_cpf_dac_comvest() pra ser reaproveitado pelos
# dois caminhos sem duplicar logica.
def finalize_and_write(df_dac_comvest):
    df_cpf_recovered = pd.read_csv(CPF_RECOVERED_BATCHES_FILE, dtype=str)
    df_cpf_recovered["merge_id"] = df_cpf_recovered["merge_id"].astype(
        df_dac_comvest["merge_id"].dtype
    )
    df_cpf_recovered["origem_cpf"] = df_cpf_recovered["origem_cpf"].astype(int)

    df_final = update_cpf_dac_comvest(df_cpf_recovered, df_dac_comvest)
    write_dac_comvest_recovered(df_final)


# Prepara os lotes de candidatos (exclusao por data invalida + coorte por
# ano minimo de elegibilidade + sub-lote por tamanho) -- determinístico:
# chamado de novo com os mesmos df_cpf_missing/batch_size sempre reproduz os
# mesmos lotes, propriedade usada pelos workers paralelos (cada processo
# reconstroi os lotes de forma independente, sem precisar compartilhar
# estado entre processos -- ver rais_recover_worker.py).
def prepare_candidate_batches(df_cpf_missing, batch_size=BATCH_SIZE):
    n_before = len(df_cpf_missing)
    df_cpf_missing = df_cpf_missing[
        has_valid_birthdate(df_cpf_missing["dta_nasc"])
    ].copy()
    log_excluded_no_birthdate(n_before - len(df_cpf_missing), n_before)

    intervalo = config["intervalo_rais"]
    min_rais_year = get_min_rais_year(df_cpf_missing["dta_nasc"], intervalo[0])

    df_dac_comvest_exact = df_cpf_missing.copy(deep=True)
    df_dac_comvest_exact.nome = clean_name_column(df_dac_comvest_exact.nome)
    del df_dac_comvest_exact["cpf"]
    df_dac_comvest_exact["_min_rais_year"] = min_rais_year.values
    df_dac_comvest_exact["_batch_id"] = _assign_batch_ids(df_dac_comvest_exact, batch_size)

    df_dac_comvest_prob = df_cpf_missing.copy(deep=True)
    df_dac_comvest_prob.nome = clean_name_column(df_dac_comvest_prob.nome)
    del df_dac_comvest_prob["cpf"]
    df_dac_comvest_prob["primeiro_nome"] = get_first_name(df_dac_comvest_prob["nome"])
    df_dac_comvest_prob["_min_rais_year"] = min_rais_year.values
    df_dac_comvest_prob["_batch_id"] = _assign_batch_ids(df_dac_comvest_prob, batch_size)

    all_batch_ids = sorted(df_dac_comvest_exact["_batch_id"].unique())
    batch_min_year = (
        df_dac_comvest_exact.groupby("_batch_id")["_min_rais_year"].first().to_dict()
    )

    exact_batches = dict(list(df_dac_comvest_exact.groupby("_batch_id")))
    prob_batches = dict(list(df_dac_comvest_prob.groupby("_batch_id")))
    return exact_batches, prob_batches, batch_min_year, all_batch_ids


def recover_cpf_matches_batched(df_cpf_missing, batch_size=BATCH_SIZE):
    _reset_scratch_files()

    exact_batches, prob_batches, batch_min_year, all_batch_ids = (
        prepare_candidate_batches(df_cpf_missing, batch_size)
    )
    n_batches = len(all_batch_ids)

    log_recover_cpf_exact_match()
    log_recover_cpf_probabilistic_match()

    # Passo 1: 1 leitura por arquivo do RAIS; o merge desse arquivo roda por
    # LOTE de candidatos (nao contra os ~950 mil de uma vez) -- lotes ja
    # preparados por prepare_candidate_batches. Cada lote e uma coorte de
    # ano minimo de elegibilidade -- permite pular coortes inteiras em anos
    # do RAIS anteriores ao ano minimo delas (ver stream_raw_matches_year),
    # sem nem tentar o merge. Necessario porque o merge de 1 unico arquivo
    # grande do RAIS contra a populacao inteira de candidatos ainda pode
    # explodir sozinho (achado real: OOM em producao mesmo com escrita
    # incremental por arquivo -- ver historico/plan.md).
    stream_raw_matches(exact_batches, prob_batches, batch_min_year)
    del exact_batches, prob_batches
    gc.collect()

    # Passo 2: por lote, dedup final (igual sempre foi) sobre so os matches
    # brutos daquele lote, acrescentado ao resultado final incrementalmente.
    for i, batch_id in enumerate(all_batch_ids, start=1):
        log_recover_batch(i, n_batches, batch_size)
        finalize_batch(batch_id)

    _cleanup_raw_matches_dir()


def _reset_scratch_files():
    if os.path.exists(CPF_RECOVERED_BATCHES_FILE):
        os.remove(CPF_RECOVERED_BATCHES_FILE)
    _cleanup_raw_matches_dir()
    os.makedirs(RAW_MATCHES_DIR, exist_ok=True)


def _cleanup_raw_matches_dir():
    if not os.path.isdir(RAW_MATCHES_DIR):
        return
    for f in os.listdir(RAW_MATCHES_DIR):
        os.remove(RAW_MATCHES_DIR + f)


# Particionado por ANO (nao so por lote/tipo) de proposito: permite rodar
# anos diferentes em processos paralelos separados sem os workers colidirem
# escrevendo no mesmo arquivo (ver rais_recover_worker.py) -- cada worker
# so escreve nos arquivos dos anos que ele mesmo processa, nunca nos de
# outro worker. Sequencial (1 processo so) tambem funciona igual, so produz
# mais arquivos pequenos em vez de poucos grandes.
def _raw_batch_path(kind, batch_id, year):
    return f"{RAW_MATCHES_DIR}{kind}_batch_{batch_id}_year{year}.parquet"


# Escreve o resultado bruto (pre-dedup) de 1 (arquivo, lote, ano),
# acrescentando ao parquet desse lote/tipo/ano ja existente (append) --
# append so entre arquivos do MESMO ano (varios estados por ano), nunca
# entre anos diferentes (arquivos separados, ver _raw_batch_path).
def _append_raw_matches(kind, batch_id, year, df):
    if df.empty:
        return
    path = _raw_batch_path(kind, batch_id, year)
    append = os.path.exists(path)
    df.to_parquet(path, engine="fastparquet", compression="lz4", append=append)


# Le e concatena os parquets de TODOS os anos pra 1 lote/tipo -- cada ano
# pode ter sido escrito por um worker paralelo diferente, arquivo separado.
def _read_raw_batch(kind, batch_id):
    import glob

    pattern = f"{RAW_MATCHES_DIR}{kind}_batch_{batch_id}_year*.parquet"
    files = glob.glob(pattern)
    if not files:
        return pd.DataFrame()
    dfs = [pd.read_parquet(f, engine="fastparquet") for f in files]
    return pd.concat(dfs, ignore_index=True).drop_duplicates()


# Passo 1: percorre o RAIS 1 unica vez (mesma ordem/leitura de sempre --
# nenhum arquivo e relido). Pra CADA arquivo [lido 1x], o merge roda por
# lote de candidatos (exact_batches/prob_batches, ja agrupados fora deste
# loop) em vez de contra a populacao inteira de uma vez -- bounded worst
# case por (1 arquivo x 1 lote), nao (1 arquivo x populacao inteira).
def stream_raw_matches(exact_batches, prob_batches, batch_min_year, year_start=None, year_end=None):
    intervalo = config["intervalo_rais"]
    year_start = intervalo[0] if year_start is None else year_start
    year_end = intervalo[1] if year_end is None else year_end
    for year in range(year_start, year_end + 1):
        log_recover_from_year(year)
        stream_raw_matches_year(exact_batches, prob_batches, batch_min_year, year)


def stream_raw_matches_year(exact_batches, prob_batches, batch_min_year, year):
    # So processa lotes cuja coorte ja seria elegivel pra trabalhar neste
    # ano do RAIS (ver get_min_rais_year/_assign_batch_ids) -- calculado uma
    # vez por ano, nao por arquivo. Anos antigos do RAIS acabam so buscando
    # candidatos mais velhos; anos recentes buscam praticamente todo mundo.
    active_exact = {
        bid: df for bid, df in exact_batches.items() if batch_min_year[bid] <= year
    }
    active_prob = {
        bid: df for bid, df in prob_batches.items() if batch_min_year[bid] <= year
    }
    log_recover_active_batches(year, len(active_exact), len(exact_batches))

    files_rais = get_all_pre_processed_files(year, "parquet")
    n_files = len(files_rais)
    for i, file in enumerate(files_rais, start=1):
        df_rais = read_rais_identification_parquet(file)
        # Data from year 2011-2013 has the wrong dtype on column 'dta_nasc_r',
        # it's float64 when it should be object
        if year == 2011 or year == 2012 or year == 2013:
            df_rais = df_rais.astype({"dta_nasc_r": "object"})
        del df_rais["pispasep"]
        df_rais = df_rais.drop_duplicates()
        n_rais_rows = len(df_rais)
        df_rais = prepare_df_rais(df_rais)

        n_exact_total = 0
        n_prob_total = 0
        for batch_id, batch_exact in active_exact.items():
            df_exact_file = find_cpf_exact_match(batch_exact, df_rais)
            _append_raw_matches("exact", batch_id, year, df_exact_file)
            n_exact_total += len(df_exact_file)
            del df_exact_file
        for batch_id, batch_prob in active_prob.items():
            df_prob_file = find_cpf_probabilistic_match(batch_prob, df_rais)
            _append_raw_matches("prob", batch_id, year, df_prob_file)
            n_prob_total += len(df_prob_file)
            del df_prob_file
        del df_rais

        log_recover_file(year, i, n_files, file, n_rais_rows, n_exact_total, n_prob_total)


# Passo 2: dedup final de 1 lote -- mesma logica que recover_cpf_matches()
# sempre aplicou, so que sobre os matches brutos ja acumulados em disco pra
# esse lote (todos os anos), nao sobre a populacao inteira de uma vez.
EMPTY_RECOVERED = pd.DataFrame(columns=["cpf", "origem_cpf", "merge_id"])


def finalize_batch(batch_id):
    df_merged_exact = _read_raw_batch("exact", batch_id)
    df_merged_prob = _read_raw_batch("prob", batch_id)

    log_filter_results()
    # _read_raw_batch retorna DataFrame vazio SEM colunas quando nenhum
    # arquivo do RAIS, em nenhum ano, deu match nenhum pra esse lote (comum
    # -- a maioria dos lotes nao recupera nada) -- pular remove_invalid_cpf/
    # fix_duplicated_rows_* nesse caso, que esperam o schema completo do
    # merge (mun_estbl/ano_base/etc) e quebram (KeyError) num df sem colunas.
    if not df_merged_exact.empty:
        df_recovered_exact = remove_invalid_cpf(df_merged_exact)
        df_recovered_exact = fix_duplicated_rows_exact_match(df_recovered_exact)
    else:
        df_recovered_exact = EMPTY_RECOVERED

    if not df_merged_prob.empty:
        df_recovered_prob_all = remove_invalid_cpf(df_merged_prob)
        df_recovered_prob_all = fix_duplicated_rows_probabilistic_match(
            df_recovered_prob_all
        )
        df_recovered_prob = update_cpf_missing(df_recovered_prob_all, df_recovered_exact)
    else:
        df_recovered_prob = EMPTY_RECOVERED

    df_recovered_batch = pd.concat([df_recovered_exact, df_recovered_prob])
    if df_recovered_batch.empty:
        return
    df_recovered_batch = df_recovered_batch.loc[:, ["cpf", "origem_cpf", "merge_id"]]

    write_header = not os.path.exists(CPF_RECOVERED_BATCHES_FILE)
    df_recovered_batch.to_csv(
        CPF_RECOVERED_BATCHES_FILE, mode="a", header=write_header, index=False
    )


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
    # Antes hardcoded range(2002, 2019) -- nunca foi atualizado quando o RAIS
    # foi estendido pra 2022 (config["intervalo_rais"]), entao a recuperacao
    # de CPF nunca buscava nos anos novos. Achado real, nao teorico (ver
    # plan.md).
    intervalo = config["intervalo_rais"]
    for year in range(intervalo[0], intervalo[1] + 1):
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
    files_rais = get_all_pre_processed_files(year, "parquet")

    dfs_exact = []
    dfs_prob = []
    for file in files_rais:
        df_rais = read_rais_identification_parquet(file)
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
    # Desempate deterministico por "cpf" quando 2+ candidatos empatam em
    # prioridade (comum em homonimos genuinos -- mesmo nome, dta_nasc
    # desconhecida/sentinela "00000000" do lado DAC casa com varias pessoas
    # reais distintas no RAIS, todas no mesmo ano/faixa de prioridade de
    # estado). Sem isso, sort_values() nao garante ordem estavel em empate,
    # e qual CPF "ganha" fica dependente da ordem de entrada das linhas --
    # mesma classe de bug ja encontrada e corrigida em get_all_files()
    # (glob.glob() sem sorted()). Achado real rodando o teste de
    # equivalencia do Tier B (ver scratchpad/test_tier_b_equivalence.py):
    # 3 merge_id (homonimos) escolhiam um CPF diferente so por causa da
    # ordem diferente em que os arquivos do RAIS eram acumulados.
    df = df.sort_values(by=["prioridade", "cpf"], ascending=[False, True])
    del df["prioridade"]
    del df["mun_estbl"]
    del df["ano_base"]
    df = df.drop_duplicates()
    return df


# Order dataframe by similarity between names in rais and dac/comvest
def order_by_similarity(df):
    # Mesmo desempate deterministico de order_by_priority (ver comentario
    # la) -- 2+ candidatos podem empatar em similaridade exata.
    df = df.sort_values(by=["similaridade", "cpf"], ascending=[False, True])
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
