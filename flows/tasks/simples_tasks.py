"""Task do Prefect para simples (independente, roda a qualquer momento)."""

from prefect import task

from simples.extract import extract_simples_amostra


@task
def simples_task():
    extract_simples_amostra()
