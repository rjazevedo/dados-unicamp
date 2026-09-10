"""Subflow fanout: todos os ramos abaixo dependem so do pivo
(dac_comvest_ids.csv, gerado por rais_ids_flow) e sao independentes ENTRE
si -- rodam de fato em paralelo via Task.submit()/wait_for (Prefect local,
processos/threads do task runner default).

Dentro de cada ramo a ordem e sequencial (real dependencia por arquivo):
  diplomas: scrapper -> merge
  enem:     comvest_vest_ids.retrieve() -> comvest_enem_ids.merge()
  rais:     merge (por ano) -> build_lookup -> recover_cpf (por ano) ->
            clear (por ano) -> finalize (uniao dos anos)
  socio:    clear -> merge
  capes:    clean -> merge
  unesp, fuvest: cada um e uma unica task independente

RAIS decomposto por ano via .map() (reaproveitando os workers de 1 ano so
ja validados em producao via tsp, ver run_pipeline.sh e
flows/tasks/rais_tasks.py) -- as fases (merge/build_lookup/recover_cpf/
clear) continuam gated em bloco (TODOS os anos de uma fase terminam antes
da proxima comecar), mesmo desenho coarse-grained que ja rodava via tsp em
producao, so trocando o orquestrador de concorrencia.

Mesmo agrupamento e mesma ordem interna de debug_stages.py, ja validado em
producao.

Executavel isoladamente: uv run -m flows.fanout_flow
"""

from prefect import flow

from flows.tasks.diplomas_tasks import diplomas_scrapper_task, diplomas_merge_task
from flows.tasks.enem_tasks import comvest_vest_ids_task, comvest_enem_ids_task
from flows.tasks.rais_tasks import (
    rais_years,
    rais_merge_year_task,
    rais_recover_cpf_build_lookup_task,
    rais_recover_cpf_year_task,
    rais_clear_year_task,
    rais_clear_finalize_task,
)
from flows.tasks.socio_tasks import socio_clear_task, socio_merge_task
from flows.tasks.capes_tasks import capes_clean_task, capes_merge_task
from flows.tasks.unesp_tasks import unesp_task
from flows.tasks.fuvest_tasks import fuvest_task


@flow(name="fanout")
def fanout_flow():
    diplomas_1 = diplomas_scrapper_task.submit()
    diplomas_2 = diplomas_merge_task.submit(wait_for=[diplomas_1])

    enem_1 = comvest_vest_ids_task.submit()
    enem_2 = comvest_enem_ids_task.submit(wait_for=[enem_1])

    years = rais_years()
    rais_merge_futures = rais_merge_year_task.map(years)
    rais_build_lookup_fut = rais_recover_cpf_build_lookup_task.submit(
        wait_for=rais_merge_futures
    )
    rais_recover_futures = rais_recover_cpf_year_task.map(
        years, wait_for=[rais_build_lookup_fut]
    )
    rais_clear_futures = rais_clear_year_task.map(years, wait_for=rais_recover_futures)
    rais_finalize_fut = rais_clear_finalize_task.submit(wait_for=rais_clear_futures)

    socio_1 = socio_clear_task.submit()
    socio_2 = socio_merge_task.submit(wait_for=[socio_1])

    capes_1 = capes_clean_task.submit()
    capes_2 = capes_merge_task.submit(wait_for=[capes_1])

    unesp_fut = unesp_task.submit()
    fuvest_fut = fuvest_task.submit()

    branch_futures = [
        diplomas_2, enem_2, rais_finalize_fut, socio_2, capes_2, unesp_fut, fuvest_fut,
    ]
    for fut in branch_futures:
        fut.result()

    # socio_2 (socio_merge) produz socio_amostra.csv, consumido por
    # empresa/estabelecimento/simples em finalizacao_flow -- devolvido pra
    # quem chamar este subflow poder aguardar so essa dependencia especifica
    # se quiser encadear sem esperar os outros ramos (ja aguardados acima).
    return socio_2.result()


if __name__ == "__main__":
    fanout_flow()
