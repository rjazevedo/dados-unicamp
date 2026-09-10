"""Log de RSS (memoria residente) antes/depois de cada task do Prefect, sem
infraestrutura nova -- so stdlib (le /proc/self/status) + o logger do
proprio Prefect (aparece no log local de cada task run, sem precisar de
OTel/Prometheus/Grafana).

Motivacao (ver plan.md, "Nota de capacidade de maquina" e "Cores vs.
memoria ao planejar paralelizacao"): esta maquina ja teve OOM real em
producao (RAIS chegando a ~119-129GB de RSS num processo unico), e rodar
via Prefect nao substitui saber quanto de memoria cada etapa consome --
isso da visibilidade automatica, por task, sem precisar acompanhar
`ps`/`top` na mao durante a execucao.

Uso: troque "from prefect import task" por
"from flows.memory_log import task_with_memory_log as task" -- os
decorators @task e @task(cache_key_fn=...) ja existentes continuam
funcionando sem nenhuma outra mudanca.

Limitacao conhecida: mede RSS do PROCESSO Python inteiro (via
/proc/self/status), nao so da task -- com o task runner default do
Prefect (tasks rodam na mesma thread/processo por padrao), tasks
sequenciais no mesmo processo compartilham esse numero. Pra RAIS/tasks
pesadas, cada uma roda isolada via `uv run -m` (processo proprio,
ver debug_stages.py), entao o numero reflete so aquela task. Quando
tasks leves rodam no mesmo processo (.submit() com ConcurrentTaskRunner),
o "antes"/"depois" ainda e util pra ver o delta que aquela task
especifica causou, mesmo que o valor absoluto inclua overhead de outras
tasks do mesmo processo.
"""

import functools

from prefect import task as _prefect_task
from prefect.logging import get_run_logger


def _current_rss_mb() -> float:
    try:
        with open("/proc/self/status") as f:
            for line in f:
                if line.startswith("VmRSS:"):
                    return int(line.split()[1]) / 1024
    except (FileNotFoundError, ValueError):
        pass
    return -1.0


def _with_memory_log(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        rss_before = _current_rss_mb()
        try:
            return fn(*args, **kwargs)
        finally:
            rss_after = _current_rss_mb()
            msg = (
                f"[memoria] {fn.__name__}: RSS antes={rss_before:.0f}MB "
                f"depois={rss_after:.0f}MB delta={rss_after - rss_before:+.0f}MB"
            )
            try:
                get_run_logger().info(msg)
            except Exception:
                print(msg)

    return wrapper


def task_with_memory_log(__fn=None, **task_kwargs):
    """Mesma assinatura de @task do Prefect (aceita uso com ou sem
    parenteses/kwargs), mas registra RSS antes/depois de cada execucao."""

    def decorator(fn):
        return _prefect_task(**task_kwargs)(_with_memory_log(fn))

    if __fn is not None:
        return decorator(__fn)
    return decorator
