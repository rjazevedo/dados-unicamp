"""flows/__init__.py roda pra qualquer import de flows.* -- usado aqui pra
forcar o Prefect a rodar 100% local antes que qualquer submodulo (tasks,
subflows) tenha chance de "import prefect" primeiro.

Restricao permanente do projeto, nao uma simplificacao "por enquanto" (ver
Contexto em plan.md): os dados processados aqui (PII, RAIS, socios, etc.)
nao podem sair da maquina, entao nenhuma metadata de execucao pode ser
reportada pra fora, mesmo que o Prefect tente por padrao.

Confirmado por teste manual (2026-09-10): sem isso, uma chamada de flow
local ja tenta gravar uma sessao de telemetria no banco sqlite do servidor
efemero (chave "TELEMETRY_SESSION"), gerando inclusive um erro real de
concorrencia ("database is locked") ao rodar tasks em paralelo via
.submit(). Com as env vars abaixo, a gravacao nao acontece.
"""

import os

# PREFECT_API_URL ausente = servidor efemero local (SQLite), nunca
# api.prefect.cloud -- removido explicitamente pra nao herdar um valor de
# ambiente global apontando pra fora.
os.environ.pop("PREFECT_API_URL", None)

os.environ["PREFECT_SERVER_ANALYTICS_ENABLED"] = "false"
os.environ["PREFECT_CLOUD_ENABLE_ORCHESTRATION_TELEMETRY"] = "false"
os.environ["PREFECT_TELEMETRY_ENABLE_RESOURCE_METRICS"] = "false"
