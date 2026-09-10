"""Subflow finalizacao: empresa/estabelecimento/simples (dependem so de
socio_amostra.csv, produzido por fanout_flow) + atribuicao final de ids
(COMVEST, DAC).

empresa/estabelecimento rodam em paralelo entre si (so leem socio_amostra.csv
e seu proprio input, escrevem em arquivos de saida distintos). simples e
totalmente independente (nao depende de socio_amostra.csv), roda junto.
merge_sheets/comvest_ids/identificadores sao sequenciais (mesma cadeia de
dependencia por arquivo do grupo "finalizacao" de debug_stages.py).

Executavel isoladamente: uv run -m flows.finalizacao_flow
"""

from prefect import flow

from flows.tasks.empresa_tasks import empresa_task
from flows.tasks.estabelecimento_tasks import estabelecimento_task
from flows.tasks.simples_tasks import simples_task
from flows.tasks.comvest_tasks import merge_sheets_task, comvest_ids_task
from flows.tasks.dac_tasks import identificadores_task


@flow(name="finalizacao")
def finalizacao_flow():
    empresa_fut = empresa_task.submit()
    estabelecimento_fut = estabelecimento_task.submit()
    simples_fut = simples_task.submit()
    for fut in [empresa_fut, estabelecimento_fut, simples_fut]:
        fut.result()

    merge_sheets_task()
    comvest_ids_task()
    identificadores_task()


if __name__ == "__main__":
    finalizacao_flow()
