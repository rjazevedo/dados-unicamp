# Fluxo de dados do pipeline (Fase 1 — Prefect)

Diagrama da árvore de dependência real entre os 4 subflows e os principais
artefatos de arquivo (checkpoints em disco), conforme desenhado em
`plan.md` e implementado em `flows/`.

```mermaid
flowchart TD
    subgraph ACADEMICO["academico_flow (sequencial)"]
        A1[COMVEST pré-proc] --> A2[DAC pré-proc]
        A2 --> A3[ENEM pré-proc]
        A3 --> A4[Base COMVEST]
        A4 --> A5[Merge Enem]
        A5 --> A6[Base DAC]
        A6 --> UDC[("uniao_dac_comvest.csv")]
    end

    subgraph RAISIDS["rais_ids_flow (sequencial)"]
        UDC --> R1["RAIS pré-proc (.map por ano)"]
        R1 --> R2[cpf_verification]
        R2 --> R3["recover_cpf_dac_comvest\n(Passo 1 .map por ano + Passo 2 finalize)"]
        R3 --> R4[random_index]
        R4 --> PIVO[("dac_comvest_ids.csv\n[PIVÔ]")]
    end

    subgraph FANOUT["fanout_flow (paralelo entre ramos)"]
        direction TB
        PIVO --> F1["diplomas\n(scrapper → merge)"]
        DC[("dados_comvest.csv")] --> F1
        PIVO --> F2["enem_ids\n(vest_ids → enem_ids)"]
        PIVO --> F3["RAIS extract\n(merge → build_lookup → recover_cpf → clear,\ntodos .map por ano)"]
        PIVO --> F4["sócio\n(clear → merge)"]
        PIVO --> F5["capes\n(clean → merge)"]
        PIVO --> F6[unesp]
        PIVO --> F7[fuvest]
        F4 --> SAM[("socio_amostra.csv")]
    end

    subgraph FINAL["finalizacao_flow"]
        SAM --> N1[empresa]
        SAM --> N2[estabelecimento]
        N3[simples]
        N1 --> N4["merge_sheets → comvest_ids → identificadores"]
        N2 --> N4
        N3 --> N4
    end

    A4 -.-> DC
```

Legenda:
- Nós retangulares = tasks/etapas do Prefect (`flows/tasks/`).
- Nós em formato de "banco de dados" = artefatos de arquivo (checkpoints reais em disco, não estado do Prefect).
- `dac_comvest_ids.csv` é o pivô — todo o `fanout_flow` depende só dele, exceto `diplomas`, que também precisa de `dados_comvest.csv`.
- Etapas marcadas `.map por ano` são as decompostas em tasks paralelas por ano (RAIS pré-processamento, `recover_cpf_dac_comvest`, e o extract final do RAIS); o resto continua sequencial dentro de cada ramo.
