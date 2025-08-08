"""
Módulo para validação de dados das escolas Comvest.

Este módulo contém funções para validar e processar os dados das escolas dos candidatos.

Funções:
- validation(): Executa a validação dos dados das escolas.
- get_closest_schools(esc_dict, inep): Obtém as escolas mais próximas com base na similaridade dos nomes.
- create_escs_dict(esc, inep): Cria um dicionário de escolas com base nos códigos dos municípios.

Como usar:
Implemente e execute as funções para validar e processar os dados das escolas dos candidatos.
"""


import pandas as pd
from comvest.utilities.io import write_result
from comvest.escolas.inep_base import load_inep_base
from comvest.escolas.escolas_base import load_esc_bases
from comvest.escolas.utility import get_tokens
import textdistance # Para sorensen
from fuzzywuzzy import fuzz # Para token_sort_ratio e ratio

ESTADOS = {
    "RO", "AC", "AM", "RR", "PA", "AP", "TO", "MA", "PI", "CE", "RN", "PB",
    "PE", "AL", "SE", "BA", "MG", "ES", "RJ", "SP", "PR", "SC", "RS", "MS",
    "MT", "GO", "DF",
}


def validation():
    """
    Executa a validação dos dados das escolas.

    Retorna
    -------
    None
    """
    print("Carregando a base de escolas...")
    escs = load_esc_bases()
    print("Carregando a base do INEP...")
    inep = load_inep_base()

    escs_matched = match_schools(
        base_escolas=inep,
        escolas=escs,
    )

    write_result(result, "escola_codigo_inep.csv")


def match_schools(base_escolas, escolas, min_overall_cutoff=70):
    """
    Realiza o matching de escolas utilizando um ensemble de estratégias de similaridade.
    Bloqueia por UF e calcula uma média ponderada dos scores de diferentes métricas.

    Parâmetros
    ----------
    base_escolas : pd.DataFrame
        DataFrame contendo as escolas de referência (INEP).
    escolas : pd.DataFrame
        DataFrame contendo as escolas do Comvest a serem validadas.    
    min_overall_cutoff : int
        Score médio mínimo (0-100) para considerar um match válido.

    Retorna
    -------
    pd.DataFrame
        DataFrame do Comvest com as colunas 'matched_chave_seq' (chave da escola na base)
        e 'match_score' (score médio do match).
    """
    # Prepara a base de escolas para bloqueio por UF
    escolas_por_uf = {
        uf: base_escolas[base_escolas["UF"] == uf].copy()
        for uf in ESTADOS
    }

    # DataFrame para armazenar os resultados do match
    # Inicializa com NaN para que possamos preencher apenas os matches encontrados
    escolas['matched_chave_seq'] = pd.NA
    escolas['match_score'] = 0.0

    # Itera sobre cada UF para aplicar o bloqueio
    for uf in ESTADOS:
        escolas_subset = escolas[escolas["UF"] == uf]
        base_subset = escolas_por_uf.get(uf)

        if base_subset is None or escolas_subset.empty:
            continue # Pula se não houver dados para esta UF em uma das bases

        # Itera sobre cada escola do Comvest no subset da UF
        for escola_idx, escola_row in escolas_subset.iterrows():
            best_avg_score = 0.0
            best_match_key = pd.NA

            # Garante que as chaves não são NaN antes de tentar o matching
            if pd.isna(escola_row['chave_seq']) or pd.isna(escola_row['chave_tok']):
                continue

            # Prepara tokens para Sorensen, se necessário
            escola_tokens = get_tokens(escola_row['chave_seq'])

            # Itera sobre cada escola na base de referência para a mesma UF
            for base_idx, base_row in base_subset.iterrows():
                # Garante que as chaves não são NaN antes de tentar o matching
                if pd.isna(base_row['chave_seq']) or pd.isna(base_row['chave_tok']):
                    continue

                # --- Cálculo dos Scores de Similaridade ---
                
                # 1. fuzzywuzzy.fuzz.token_sort_ratio (para chave_seq, robusto à reordenação)
                score1 = fuzz.token_sort_ratio(escola_row['chave_seq'], base_row['chave_seq'])

                # 2. textdistance.sorensen (para chave_seq, similaridade de conjunto de tokens)
                # Multiplica por 100 para escalar para 0-100 como fuzzywuzzy
                base_tokens = get_tokens(base_row['chave_seq'])
                score2 = textdistance.sorensen(escola_tokens, base_tokens) * 100 if escola_tokens and base_tokens else 0

                # 3. fuzzywuzzy.fuzz.ratio (para chave_seq, similaridade de caracteres direta)
                score3 = fuzz.ratio(escola_row['chave_seq'], base_row['chave_seq'])

                # --- Cálculo da Média Simples dos Scores ---
                avg_score = (score1 + score2 + score3) / 3.0

                # --- Atualiza o Melhor Match ---
                if avg_score > best_avg_score:
                    best_avg_score = avg_score
                    best_match_key = base_row['chave_seq'] # Retorna a chave_seq da base_escolas
            
            escolas 

            # Armazena o melhor match encontrado para a escola do Comvest, se o score for suficiente
            if best_avg_score >= min_overall_cutoff:
                escolas.loc[escola_idx, 'matched_chave_seq'] = best_match_key
                escolas.loc[escola_idx, 'match_score'] = best_avg_score



    return escolas