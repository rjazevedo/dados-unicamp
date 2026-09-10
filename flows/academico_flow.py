"""Subflow academico: COMVEST pre-proc -> DAC pre-proc -> ENEM pre-proc ->
base da COMVEST -> merge Enem -> base da DAC -> uniao_dac_comvest.csv.

Ordem identica a __main__.py (linhas 80-123) e aos grupos comvest_preproc /
dac_preproc / enem_preproc / comvest_base / enem_merge / dac_base de
debug_stages.py -- cadeia real de dependencia por arquivo, mantida
sequencial (nao decomposta em concorrencia; isso fica pra Fase 2).

Executavel isoladamente: uv run -m flows.academico_flow
"""

from prefect import flow

from flows.tasks.comvest_tasks import (
    extrair_cidades_task,
    extrair_cursos_task,
    dict_cursos_task,
    extrair_matriculados_task,
    extrair_convocados_task,
    limpeza_dados_comvest_task,
    cod_ibge_task,
    validacao_esc_task,
    cod_inep_task,
    ids_nomes_task,
    limpeza_perfil_task,
    limpeza_notas_task,
    presenca_task,
)
from flows.tasks.dac_tasks import (
    setup_dados_task,
    ufs_codes_task,
    create_ids_task,
    limpeza_dados_dac_task,
    uf_codes_task,
    school_codes_task,
    historico_escolar_task,
    resumo_por_periodo_task,
    resumo_periodo_cr_task,
    vida_academica_task,
    dados_ingressantes_task,
    habilitacao_task,
    uniao_dac_comvest_task,
)
from flows.tasks.enem_tasks import (
    clear_comvest_task,
    divide_comvest_task,
    comvest_enem_merge_task,
)


@flow(name="academico")
def academico_flow():
    # COMVEST pre-processamento
    extrair_cidades_task()
    extrair_cursos_task()
    dict_cursos_task()
    extrair_matriculados_task()
    extrair_convocados_task()
    limpeza_dados_comvest_task()

    # DAC pre-processamento
    setup_dados_task()
    ufs_codes_task()
    create_ids_task()
    limpeza_dados_dac_task()
    uf_codes_task()

    # ENEM pre-processamento
    clear_comvest_task()
    divide_comvest_task()

    # Base da COMVEST
    cod_ibge_task()
    validacao_esc_task()
    school_codes_task()
    cod_inep_task()
    ids_nomes_task()
    limpeza_perfil_task()
    limpeza_notas_task()
    presenca_task()

    # Merge Enem
    comvest_enem_merge_task()

    # Base da DAC -> uniao_dac_comvest.csv
    historico_escolar_task()
    resumo_por_periodo_task()
    resumo_periodo_cr_task()
    vida_academica_task()
    dados_ingressantes_task()
    habilitacao_task()
    uniao_dac_comvest_task()


if __name__ == "__main__":
    academico_flow()
