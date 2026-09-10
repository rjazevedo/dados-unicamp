"""Task do Prefect para simples (independente, roda a qualquer momento)."""

from flows.memory_log import task_with_memory_log as task

from simples.extract import extract_simples_amostra


@task
def simples_task():
    extract_simples_amostra()
