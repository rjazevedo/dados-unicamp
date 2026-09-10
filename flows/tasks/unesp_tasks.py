"""Task do Prefect para UNESP (depende so do pivo dac_comvest_ids.csv)."""

from flows.memory_log import task_with_memory_log as task

from unesp.extract.extract import extract_unesp


@task
def unesp_task():
    extract_unesp()
