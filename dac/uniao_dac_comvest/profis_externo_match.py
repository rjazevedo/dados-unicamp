import pandas as pd

from dac.uniao_dac_comvest.closest_name import get_the_closest_matche

CUTOFF = 0.85

# ProFis tem curso preparatorio entre a candidatura (ano registrado na
# planilha externa, Profis11a22.xlsx) e o ingresso efetivo no curso de
# graduacao (ano_ingresso_curso na DAC) -- medido nos dados reais (606/607
# alunos, cutoff=0.9, sem restricao de ano): offset +2 em 77% dos casos, +3
# em 19%, +4/+6 no residual, 0 raro. Por isso o casamento NAO restringe por
# ano igual (isso derrubava o match rate pra 8/607) -- casa por nome no pool
# inteiro e so DEPOIS valida que o offset (ano DAC - ano planilha) esta
# numa janela plausivel, descartando match fora dela (provavel coincidencia
# de nome comum em ano implausivel, ex.: ano da planilha DEPOIS do ano DAC).
MIN_YEAR_OFFSET = 0
MAX_YEAR_OFFSET = 6
TYPICAL_YEAR_OFFSET = 2

# tipo_ingresso_comvest usado pelas linhas vindas da planilha externa do
# ProFis (comvest/clear_dados/limpeza_profis_externo.py) -- import tardio
# pra evitar ciclo de import entre os pacotes comvest/dac.
def _tipo_ingresso_profis_externo():
    from comvest.clear_dados.limpeza_profis_externo import TIPO_INGRESSO_PROFIS_EXTERNO
    return TIPO_INGRESSO_PROFIS_EXTERNO


def setup_profis_pool(dados_comvest):
    tipo = str(_tipo_ingresso_profis_externo())
    pool = dados_comvest[dados_comvest["tipo_ingresso_comvest"] == tipo].copy()
    return pool


# Casa alunos da DAC (ja identificados como ProFis matriculado, sem match nas
# etapas padrao de uniao_dac_comvest.py -- sem insc_vest/dta_nasc/doc em
# comum) contra os candidatos do ProFis vindos da planilha externa
# (Profis11a22.xlsx), por nome (fuzzy, difflib.get_close_matches via
# get_the_closest_matche ja existente em closest_name.py) + janela de offset
# de ano plausivel (ver constantes acima) -- get_the_closest_matche(...,
# first_name=0) EXIGE que o primeiro nome bata exatamente, alem do cutoff de
# similaridade geral, pra reduzir risco de falso positivo em nomes comuns.
#
# Retorna (matched, unmatched): matched ja vem com colunas *_comvest
# preenchidas (cpf_comvest, dta_nasc_comvest, etc, incl. sexo_comvest/
# email_comvest/matriculado_comvest); unmatched segue sem enriquecimento,
# igual ao comportamento anterior (create_colums_for_concat(df, False)).
def match_unmatched_profis(df, comvest_pool, cutoff=CUTOFF):
    if df.empty or comvest_pool.empty:
        return df.iloc[0:0].copy(), df

    df = df.reset_index(drop=True).copy()
    # Chave de desambiguacao por LINHA de entrada, nao por identif -- uma
    # mesma pessoa (identif) pode ter mais de uma entrada ProFis na DAC
    # (ex.: candidatou-se em 2013, saiu, voltou em 2017), cada uma com seu
    # proprio ano_ingresso_curso e candidato correto na planilha externa.
    # Usar identif como chave de dedup colapsaria as duas em 1 so linha.
    df["_row_id"] = df.index
    nomes_pool = comvest_pool["nome"]
    df["new_name"] = df["nome"].map(
        lambda nome: get_the_closest_matche(nome, nomes_pool, cutoff, first_name=0)
    )

    matched_mask = df["new_name"] != ""
    unmatched = df[~matched_mask].drop(columns=["new_name", "_row_id"]).copy()

    if not matched_mask.any():
        return df.iloc[0:0].drop(columns=["new_name", "_row_id"]), unmatched

    matched = df[matched_mask].copy()
    matched["nome_dac"] = matched["nome"]
    matched["nome"] = matched["new_name"]
    matched = matched.drop(columns=["new_name"])

    merged = pd.merge(
        matched,
        comvest_pool,
        how="left",
        on="nome",
        suffixes=("", "_comvest"),
    )

    # Filtra por janela de offset plausivel (ver comentario no topo do
    # arquivo) -- rejeita candidaturas registradas DEPOIS do ingresso na
    # DAC (offset negativo) ou distantes demais (> MAX_YEAR_OFFSET anos),
    # provavel coincidencia de nome comum casando com a pessoa errada.
    dac_ano = pd.to_numeric(merged["ano_ingresso_curso"], errors="coerce")
    pool_ano = pd.to_numeric(merged["ano_ingresso_curso_comvest"], errors="coerce")
    offset = dac_ano - pool_ano
    plausible = offset.between(MIN_YEAR_OFFSET, MAX_YEAR_OFFSET)

    # Uma linha (_row_id) pode ter mais de um candidato no pool com o mesmo
    # nome casado (em anos diferentes) -- so vira "sem match" se NENHUM dos
    # candidatos dela cair na janela plausivel; se pelo menos 1 cair, a
    # linha segue pro passo de desempate abaixo mesmo que outros candidatos
    # dela tenham sido rejeitados.
    rows_with_plausible = set(merged.loc[plausible, "_row_id"])
    rejected = merged[~plausible & ~merged["_row_id"].isin(rows_with_plausible)]
    rejected = rejected.drop_duplicates(subset="_row_id")
    if not rejected.empty:
        comvest_cols = [c for c in rejected.columns if c.endswith("_comvest") or c == "merge_id"]
        newly_unmatched = rejected.drop(columns=["nome", "_row_id"] + comvest_cols)
        newly_unmatched = newly_unmatched.rename(columns={"nome_dac": "nome"})
        unmatched = pd.concat([unmatched, newly_unmatched], ignore_index=True)

    merged = merged[plausible].copy()
    if merged.empty:
        return merged.drop(columns=["_row_id"]).rename(columns={"nome": "nome_comvest", "nome_dac": "nome"}), unmatched

    # Salvaguarda: se o nome casado existir mais de uma vez no pool dentro
    # da janela de anos plausivel (nome comum, mais de um candidato, ou a
    # mesma pessoa com 2 candidaturas em anos diferentes ambas plausiveis),
    # o merge acima multiplicaria a linha -- desambigua por LINHA de entrada
    # (_row_id, nao identif: uma mesma pessoa pode ter mais de uma entrada
    # ProFis legitima na DAC), mantendo o candidato com offset mais proximo
    # do tipico (TYPICAL_YEAR_OFFSET).
    merged["_offset_dist"] = (
        dac_ano[plausible] - pool_ano[plausible] - TYPICAL_YEAR_OFFSET
    ).abs()
    merged = merged.sort_values("_offset_dist").drop_duplicates(subset="_row_id", keep="first")
    merged = merged.drop(columns=["_offset_dist", "_row_id"])
    merged = merged.rename(columns={"nome": "nome_comvest", "nome_dac": "nome"})

    return merged, unmatched
