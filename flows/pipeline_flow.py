"""Flow raiz: orquestra os 4 subflows na ordem real do pipeline.

academico_flow -> rais_ids_flow -> fanout_flow -> finalizacao_flow

Nota: a extração da RAIS e sempre "completa" -- a distincao "limitada"/
"completa" (e o prompt interativo que perguntava isso) foi removida do
projeto inteiro por decisao do usuario (2026-09-10): so "completa" e usada,
em __main__.py, rais/__main__.py, rais/extract/__main__.py,
debug_stages.py, run_pipeline.sh e aqui.

Executavel isoladamente: uv run -m flows.pipeline_flow
"""

from prefect import flow

from flows.academico_flow import academico_flow
from flows.rais_ids_flow import rais_ids_flow
from flows.fanout_flow import fanout_flow
from flows.finalizacao_flow import finalizacao_flow


@flow(name="pipeline")
def pipeline_flow():
    academico_flow()
    rais_ids_flow()
    fanout_flow()
    finalizacao_flow()


if __name__ == "__main__":
    pipeline_flow()
