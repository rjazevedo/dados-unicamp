import pandas as pd
from comvest.utilities.io import read_output
from comvest.utilities.dtypes import (
    DTYPES_DADOS,
    DTYPES_PERFIL,
    DTYPES_MATRICULADOS,
    DTYPES_NOTAS,
)
import filters.filters as filter_db


def extract():
    # Leitura das bases
    COMVEST_SAMPLE = read_output(
        "comvest_amostra.csv",
        dtype={**DTYPES_DADOS, **DTYPES_PERFIL, **DTYPES_MATRICULADOS, **DTYPES_NOTAS},
    )
    DAC_VACH_SAMPLE = read_output("vida_academica_habilitacao.csv", 'dac')
    SOCIO_SAMPLE = pd.read_csv("/home/output/socios/socio_amostra.csv", sep=";", low_memory=False)
    RAIS_SAMPLE = pd.read_csv("/home/output/rais/rais_amostra.csv", sep=";", low_memory=False)
    CAPES_SAMPLE = pd.read_csv("/home/output/capes/capes_amostra.csv", sep=";", low_memory=False)

    x = set(filter_db.filterby_joindate(DAC_VACH_SAMPLE, year=2000, how="after"))

    y = set(filter_db.filterby_exitdate(DAC_VACH_SAMPLE, year=2018, how="before"))

    filtered_ids = x.intersection(y)

    dac_cols = [
        "id",
        "ano_ingresso",
        "periodo_ingresso",
        "tipo_periodo_ingresso",
        "ano_saida",
        "periodo_saida",
        "tipo_periodo_saida",
        "cod_motivo_saida",
        "motivo_saida",
        "curso",
        "nivel_curso",
        "codigo_habilitacao",
        "nome_habilitacao",
        "prioridade_habilitacao",
        "situacao_habilitacao",
    ]

    DAC_VACH_FILTERED = DAC_VACH_SAMPLE[DAC_VACH_SAMPLE["id"].isin(filtered_ids)][
        dac_cols
    ]

    comvest_cols = [
        "id",
        "ano_vest",
        "tipo_ingresso_comvest",
        "curso_matric",
        "ano_nasc_c",
        "nacionalidade_c",
        "nat_esc_em_c",
        "ano_conclu_em_c",
        "sexo_c",
        "est_civil_c",
        "isento",
        "paais",
        "raca",
        "tipo_esc_ef",
        "tipo_esc_ef_1",
        "tipo_esc_ef_2",
        "tipo_esc_em",
        "tipo_curso_em",
        "periodo_em",
        "cursinho",
        "cursinho_tempo",
        "renda_sm",
        "renda_sm_a",
        "renda_sm_b",
        "renda_sm_c",
        "renda_sm_d",
        "renda_qtas",
        "renda_contrib_qtas",
        "moradia_situacao",
        "ocup_pai",
        "ocup_mae",
        "educ_pai",
        "educ_mae",
        "trabalha",
        "contribui_renda_fam",
    ]

    COMVEST_FILTERED = COMVEST_SAMPLE[COMVEST_SAMPLE["id"].isin(filtered_ids)][
        comvest_cols
    ]

    COMVEST_FILTERED = COMVEST_FILTERED[~COMVEST_FILTERED['curso_matric'].isna()]

    socio_cols = [
        "id",
        "cnpj",
        "codigo_qualificacao_socio",
        "data_entrada_sociedade",
    ]

    SOCIO_FILTERED = SOCIO_SAMPLE[SOCIO_SAMPLE["id"].isin(filtered_ids)][socio_cols]

    rais_cols = [
        "id",
        "ano_base",
        "mun_estbl",
        "cnae95",
        "vinculo_ativo",
        "vinculo_tipo",
        "deslig_motivo",
        "deslig_mes",
        "admissao_tipo",
        "salario_tipo",
        "cbo94",
        "escolaridade",
        "sexo_r",
        "pais_nacionalidade_r",
        "raca_r",
        "ind_def",
        "estbl_tamanho",
        "nat_juridica",
        "estbl_tipo",
        "dta_admissao",
        "rem_media",
        "rem_media_sm",
        "rem_dez",
        "rem_dez_sm",
        "vinculo_tempo",
        "horas_contr",
        "rem_ultima",
        "sal_contr",
        "cnpj",
        "cbo02",
        "cnae_20_classe",
        "cnae_20_subclasse",
        "afast1_causa",
        "afast_dias_total",
        "idade",
        "ibge_subsetor",
        "mun_trab",
    ]

    RAIS_FILTERED = RAIS_SAMPLE[RAIS_SAMPLE["id"].isin(filtered_ids)][rais_cols]

    CAPES_FILTERED = CAPES_SAMPLE[CAPES_SAMPLE["id"].isin(filtered_ids)]

    """ Escrita das bases filtradas conforme o pedido especifico """
    COMVEST_FILTERED.to_csv("pedido_2/comvest_pedido2.csv", index=False)
    DAC_VACH_FILTERED.to_csv("pedido_2/dac_pedido2.csv", index=False)
    SOCIO_FILTERED.to_csv("pedido_2/socios_pedido2.csv", index=False)
    RAIS_FILTERED.to_csv("pedido_2/rais_pedido2.csv", index=False)
    CAPES_FILTERED.to_csv("pedido_2/capes_amostra2.csv", index=False)
