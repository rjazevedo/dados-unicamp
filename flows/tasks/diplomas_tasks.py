"""Tasks do Prefect para o processamento de diplomados (USP)."""

from flows.memory_log import task_with_memory_log as task

from diplomas.extract_usp import scrapper
from diplomas.extract_usp import comvest_diplomasUSP


@task
def diplomas_scrapper_task():
    scrapper.proccess_usp()


@task
def diplomas_merge_task():
    comvest_diplomasUSP.merge()
