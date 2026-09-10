"""Subflow rais_ids: pre-processamento do RAIS -> geracao dos ids ->
dac_comvest_ids.csv (o artefato-pivo consumido em fan-out por rais, socio,
capes, enem, unesp, fuvest, comvest.assign_ids e dac.create_ids).

Depende de academico_flow ja ter rodado (precisa de uniao_dac_comvest.csv).

Decomposto por ano via .map() (reaproveitando as funcoes worker-de-1-ano-so
ja validadas em producao via tsp, ver flows/tasks/rais_tasks.py) pra
pre_process_parquet, identification e o Passo 1 (busca por candidato) de
recover_cpf_dac_comvest. cpf_verification e random_index continuam
monoliticos (population-wide, sem passo parcial por ano). O Passo 2 de
recover_cpf_dac_comvest (dedup final entre TODOS os anos) so roda depois
que TODOS os workers do Passo 1 terminarem.

Nota (achado desta sessao, nao corrigido aqui -- fora do escopo de mapear
1:1 o comportamento atual): identification.get_identification_from_year()
gera cache em pkl que nenhum consumidor le mais hoje -- cpf_verification,
recover_cpf_dac_comvest, recover_cpf_rais e merge ja foram totalmente
reconciliados pra ler o cache parquet (pre_process_parquet). Mantido aqui
pra nao mudar comportamento de producao sem confirmacao do usuario; ver
plan.md.

Executavel isoladamente: uv run -m flows.rais_ids_flow
"""

from prefect import flow

from flows.tasks.rais_tasks import (
    rais_years,
    pre_process_parquet_setup_task,
    pre_process_parquet_year_task,
    identification_setup_task,
    identification_year_task,
    cpf_verification_task,
    recover_cpf_reset_task,
    recover_cpf_worker_year_task,
    recover_cpf_finalize_task,
    random_index_task,
)


@flow(name="rais_ids")
def rais_ids_flow():
    years = rais_years()

    pre_process_parquet_setup_task()
    parquet_futures = pre_process_parquet_year_task.map(years)

    identification_setup_task()
    identification_futures = identification_year_task.map(years)

    for fut in [*parquet_futures, *identification_futures]:
        fut.result()

    cpf_verification_task()

    recover_cpf_reset_task()
    worker_futures = recover_cpf_worker_year_task.map(years)
    for fut in worker_futures:
        fut.result()
    recover_cpf_finalize_task()

    random_index_task()


if __name__ == "__main__":
    rais_ids_flow()
