"""Task do Prefect para FUVEST (depende so do pivo dac_comvest_ids.csv)."""

from flows.memory_log import task_with_memory_log as task

from fuvest.extract.extract import extract_fuvest


@task
def fuvest_task():
    extract_fuvest()
