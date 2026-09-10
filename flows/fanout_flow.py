"""Subflow fanout: todos os ramos abaixo dependem so do pivo
(dac_comvest_ids.csv, gerado por rais_ids_flow) e sao independentes ENTRE
si -- rodam de fato em paralelo via Task.submit()/wait_for (Prefect local,
processos/threads do task runner default).

Dentro de cada ramo a ordem e sequencial (real dependencia por arquivo):
  diplomas: scrapper -> merge
  enem:     comvest_vest_ids.retrieve() -> comvest_enem_ids.merge()
  rais:     merge -> recover_cpf -> clear (parametrizado por tipo_extracao_rais)
  socio:    clear -> merge
  capes:    clean -> merge
  unesp, fuvest: cada um e uma unica task independente

Mesmo agrupamento (grupo "fanout") e mesma ordem interna de
debug_stages.py, ja validado em producao.

Executavel isoladamente: uv run -m flows.fanout_flow
"""

from prefect import flow

from flows.tasks.diplomas_tasks import diplomas_scrapper_task, diplomas_merge_task
from flows.tasks.enem_tasks import comvest_vest_ids_task, comvest_enem_ids_task
from flows.tasks.rais_tasks import rais_merge_task, rais_recover_cpf_task, rais_clear_task
from flows.tasks.socio_tasks import socio_clear_task, socio_merge_task
from flows.tasks.capes_tasks import capes_clean_task, capes_merge_task
from flows.tasks.unesp_tasks import unesp_task
from flows.tasks.fuvest_tasks import fuvest_task


@flow(name="fanout")
def fanout_flow(tipo_extracao_rais: str = "completa"):
    diplomas_1 = diplomas_scrapper_task.submit()
    diplomas_2 = diplomas_merge_task.submit(wait_for=[diplomas_1])

    enem_1 = comvest_vest_ids_task.submit()
    enem_2 = comvest_enem_ids_task.submit(wait_for=[enem_1])

    rais_1 = rais_merge_task.submit()
    rais_2 = rais_recover_cpf_task.submit(wait_for=[rais_1])
    rais_3 = rais_clear_task.submit(tipo_extracao_rais, wait_for=[rais_2])

    socio_1 = socio_clear_task.submit()
    socio_2 = socio_merge_task.submit(wait_for=[socio_1])

    capes_1 = capes_clean_task.submit()
    capes_2 = capes_merge_task.submit(wait_for=[capes_1])

    unesp_fut = unesp_task.submit()
    fuvest_fut = fuvest_task.submit()

    branch_futures = [diplomas_2, enem_2, rais_3, socio_2, capes_2, unesp_fut, fuvest_fut]
    for fut in branch_futures:
        fut.result()

    # socio_2 (socio_merge) produz socio_amostra.csv, consumido por
    # empresa/estabelecimento/simples em finalizacao_flow -- devolvido pra
    # quem chamar este subflow poder aguardar so essa dependencia especifica
    # se quiser encadear sem esperar os outros ramos (ja aguardados acima).
    return socio_2.result()


if __name__ == "__main__":
    fanout_flow()
