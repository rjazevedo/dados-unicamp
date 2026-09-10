"""Task do Prefect para UNESP (depende so do pivo dac_comvest_ids.csv)."""

from prefect import task

from unesp.extract.extract import extract_unesp


@task
def unesp_task():
    extract_unesp()
