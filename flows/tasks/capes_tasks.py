"""Tasks do Prefect para CAPES."""

from prefect import task

from capes.cleaning import clean as clean_capes
from capes.extract import merge as merge_capes


@task
def capes_clean_task():
    clean_capes.clean_capes()


@task
def capes_merge_task():
    merge_capes.extract_ids()
