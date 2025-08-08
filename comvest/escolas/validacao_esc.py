"""
Módulo para validação e matching de nomes de escolas da base Comvest com a base de referência do INEP.

Este módulo utiliza um ensemble de algoritmos de similaridade de strings para encontrar
as correspondências mais prováveis entre as duas bases, bloqueando a busca por UF
para otimizar o desempenho.

Funções Principais:
- validation(): Orquestra todo o processo: carrega os dados, executa o matching, une os resultados e salva o arquivo final.
- match_schools(): Realiza o matching, comparando cada escola da Comvest com as escolas da base INEP
  dentro da mesma UF e calculando um score de similaridade.

Como usar:
Para executar o processo de validação completo, simplesmente chame a função `validation()`.
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
    Executa a validação dos dados das escolas, incluindo o merge e salvamento.
    """
    print("Carregando a base de escolas...")
    escs = load_esc_bases()
    print("Carregando a base do INEP...")
    inep = load_inep_base()

    # --- PASSO 1: Realiza o matching ---
    print("Iniciando o processo de matching das escolas...")
    escs_matched = match_schools(
        base_escolas=inep,
        escolas=escs,
    )
    print("Matching concluído.")

    # --- PASSO 2: Unir (Merge) as bases de dados ---
    print("Fazendo o merge das bases de escolas e do INEP...")
    result = pd.merge(
        escs_matched,
        inep,
        left_on=['codigo_municipio', 'matched_chave_seq'],
        right_on=['codigo_municipio', 'chave_seq'],
        how='left',
        suffixes=("_comvest", "_inep") # Adiciona sufixos para diferenciar colunas com mesmo nome
    )

    # --- PASSO 3: Calcular e exibir a taxa de sucesso do match ---
    match_rate = escs_matched['matched_chave_seq'].notna().sum() / len(escs_matched)
    print(f"Taxa de match: {match_rate:.2%}")

    # --- PASSO 4: Preparar o DataFrame final para a saída ---
    print("Preparando o arquivo de saída...")
    
    # Renomeia as colunas para o formato de saída desejado
    # A coluna 'chave_seq_inep' já é nomeada corretamente pelo sufixo do merge
    result = result.rename(columns={
        'chave_seq_comvest': 'chave_seq_escs',
        'match_score': 'score' # A coluna de score vem de escs_matched e não recebe sufixo
    })

    # Remove a coluna auxiliar usada para o merge, que não é mais necessária
    result = result.drop(columns=['matched_chave_seq'])

    # Garante que cada escola da base Comvest original apareça apenas uma vez no resultado
    final_result = result.drop_duplicates(subset=["chave_seq_escs", "codigo_municipio"])
    
    # --- PASSO 5: Salvar o resultado ---
    print("Salvando o resultado final...")
    # O DataFrame 'final_result' agora contém o merge completo com as colunas renomeadas
    write_result(final_result, "escola_codigo_inep.csv")
    print("Processo de validação finalizado com sucesso!")


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
    escolas['matched_chave_seq'] = pd.NA
    escolas['match_score'] = 0.0

    # Itera sobre cada UF para aplicar o bloqueio
    for i, uf in enumerate(ESTADOS):
        print(f"Processando UF: {uf} ({i+1}/{len(ESTADOS)})...")
        escolas_subset = escolas[escolas["UF"] == uf]
        base_subset = escolas_por_uf.get(uf)

        if base_subset is None or escolas_subset.empty:
            continue # Pula se não houver dados para esta UF em uma das bases

        # Itera sobre cada escola do Comvest no subset da UF
        for escola_idx, escola_row in escolas_subset.iterrows():
            best_avg_score = 0.0
            best_match_key = pd.NA

            if pd.isna(escola_row['chave_seq']):
                continue

            # Prepara tokens para Sorensen
            escola_tokens = get_tokens(escola_row['chave_seq'])

            # Itera sobre cada escola na base de referência para a mesma UF
            for base_idx, base_row in base_subset.iterrows():
                if pd.isna(base_row['chave_seq']):
                    continue

                # --- Cálculo dos Scores de Similaridade ---
                
                # 1. fuzzywuzzy.fuzz.token_sort_ratio (para chave_seq, robusto à reordenação)
                score1 = fuzz.token_sort_ratio(escola_row['chave_seq'], base_row['chave_seq'])

                # 2. textdistance.sorensen (para tokens, similaridade de conjunto de tokens)
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
                    best_match_key = base_row['chave_seq']
            
            # Armazena o melhor match encontrado para a escola do Comvest, se o score for suficiente
            if best_avg_score >= min_overall_cutoff:
                escolas.loc[escola_idx, 'matched_chave_seq'] = best_match_key
                escolas.loc[escola_idx, 'match_score'] = best_avg_score

    return escolas
