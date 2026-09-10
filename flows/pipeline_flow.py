"""Flow raiz: orquestra os 4 subflows na ordem real do pipeline.

academico_flow -> rais_ids_flow -> fanout_flow -> finalizacao_flow

Nota: __main__.py hoje so tem UM prompt interativo (tipo_extracao_rais,
"limitada"/"completa") -- nao existe mais um segundo prompt equivalente
pra socios (o diagnostico original do plan.md mencionava 2 prompts, mas
isso ja nao reflete o __main__.py atual; confirmado por busca no repo que
nao ha nenhum uso de "tipo_extracao_socios"). Por isso pipeline_flow so
expõe tipo_extracao_rais, pra nao introduzir um parametro sem efeito real.

Executavel isoladamente: uv run -m flows.pipeline_flow
"""

from typing import Literal

from prefect import flow

from flows.academico_flow import academico_flow
from flows.rais_ids_flow import rais_ids_flow
from flows.fanout_flow import fanout_flow
from flows.finalizacao_flow import finalizacao_flow


@flow(name="pipeline")
def pipeline_flow(tipo_extracao_rais: Literal["limitada", "completa"] = "completa"):
    academico_flow()
    rais_ids_flow()
    fanout_flow(tipo_extracao_rais=tipo_extracao_rais)
    finalizacao_flow()


if __name__ == "__main__":
    pipeline_flow()
