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
    DAC_VA_SAMPLE = read_output("vida_academica.csv", "dac")
    DAC_DC_SAMPLE = read_output("dados_cadastrais.csv", "dac")
    DAC_HE_SAMPLE = read_output("historico_escolar_aluno.csv", "dac")
    DAC_RPP_SAMPLE = read_output("resumo_periodo_cr.csv", "dac")
    SOCIO_SAMPLE = pd.read_csv(
        "/home/output/socios/socio_amostra.csv", sep=";", low_memory=False
    )
    RAIS_SAMPLE = pd.read_csv(
        "/home/output/rais/rais_amostra.csv", sep=";", low_memory=False
    )
    CAPES_SAMPLE = pd.read_csv(
        "/home/output/capes/capes_amostra.csv", sep=";", low_memory=False
    )

    # Filtragem de cursos na Comvest
    filteredIDs_comvest = set(
        filter_db.filterby_course(COMVEST_SAMPLE, courses=[3, 42], db="comvest")
    )

    # Filtragem de cursos na DAC
    filteredIDs_dac = set(
        filter_db.filterby_course(DAC_VA_SAMPLE, courses=[3, 42], db="dac")
    )

    ids_union = filteredIDs_comvest.union(filteredIDs_dac)

    COMVEST_FILTERED = COMVEST_SAMPLE[COMVEST_SAMPLE["id"].isin(ids_union)]

    DAC_VA_FILTERED = DAC_VA_SAMPLE[DAC_VA_SAMPLE["id"].isin(ids_union)]
    DAC_DC_FILTERED = DAC_DC_SAMPLE[DAC_DC_SAMPLE["id"].isin(ids_union)]
    DAC_HE_FILTERED = DAC_HE_SAMPLE[DAC_HE_SAMPLE["id"].isin(ids_union)]
    DAC_RPP_FILTERED = DAC_RPP_SAMPLE[DAC_RPP_SAMPLE["id"].isin(ids_union)]

    SOCIO_FILTERED = SOCIO_SAMPLE[SOCIO_SAMPLE["id"].isin(filteredIDs_dac)]
    RAIS_FILTERED = RAIS_SAMPLE[RAIS_SAMPLE["id"].isin(filteredIDs_dac)]
    CAPES_FILTERED = CAPES_SAMPLE[CAPES_SAMPLE["id"].isin(filteredIDs_dac)]

    # Escrita das bases filtradas conforme o pedido especifico
    COMVEST_FILTERED.to_csv("pedido_1/comvest_amostra.csv", index=False)
    DAC_VA_FILTERED.to_csv("pedido_1/vida_academica.csv", index=False)
    DAC_DC_FILTERED.to_csv("pedido_1/dados_cadastrais.csv", index=False)
    DAC_HE_FILTERED.to_csv("pedido_1/historico_escolar.csv", index=False)
    DAC_RPP_FILTERED.to_csv("pedido_1/resumo_por_periodo.csv", index=False)
    SOCIO_FILTERED.to_csv("pedido_1/socio_amostra.csv", index=False)
    RAIS_FILTERED.to_csv("pedido_1/rais_amostra.csv", index=False)
    CAPES_FILTERED.to_csv("pedido_1/capes_amostra.csv", index=False)
