"""Subflow rais_ids: pre-processamento do RAIS -> geracao dos ids ->
dac_comvest_ids.csv (o artefato-pivo consumido em fan-out por rais, socio,
capes, enem, unesp, fuvest, comvest.assign_ids e dac.create_ids).

Depende de academico_flow ja ter rodado (precisa de uniao_dac_comvest.csv).

Mesma ordem do grupo rais_ids_pivot de debug_stages.py.

Nota (achado desta sessao, nao corrigido aqui -- fora do escopo de mapear
1:1 o comportamento atual): identification.get_identification_from_all_years()
gera cache em pkl que nenhum consumidor le mais hoje -- cpf_verification,
recover_cpf_dac_comvest, recover_cpf_rais e merge ja foram totalmente
reconciliados pra ler o cache parquet (pre_process_parquet). Mantido aqui
pra nao mudar comportamento de producao sem confirmacao do usuario; ver
plan.md.

random_index_task() e recover_cpf_dac_comvest_task() dependem do conjunto
completo de dados -- NAO decompor em tasks parciais (cache tudo-ou-nada).

Executavel isoladamente: uv run -m flows.rais_ids_flow
"""

from prefect import flow

from flows.tasks.rais_tasks import (
    pre_process_parquet_task,
    identification_task,
    cpf_verification_task,
    recover_cpf_dac_comvest_task,
    random_index_task,
)


@flow(name="rais_ids")
def rais_ids_flow():
    pre_process_parquet_task()
    identification_task()
    cpf_verification_task()
    recover_cpf_dac_comvest_task()
    random_index_task()


if __name__ == "__main__":
    rais_ids_flow()
