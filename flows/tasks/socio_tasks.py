"""Tasks do Prefect para socios."""

from prefect import task

from socio.cleaning import clear as clear_socio
from socio.extract import merge as merge_socio


@task
def socio_clear_task():
    clear_socio.clear_socio()


@task
def socio_merge_task():
    merge_socio.merge_socio_dac_comvest()
