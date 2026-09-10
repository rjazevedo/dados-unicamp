"""Tasks do Prefect para o pre-processamento e merge do ENEM."""

from flows.memory_log import task_with_memory_log as task

from enem.comvest_enem import clear_comvest
from enem.comvest_enem import divide_comvest
from enem.comvest_enem import comvest_enem
from enem.comvest_enem import comvest_vest_ids
from enem.comvest_enem import comvest_enem_ids


@task
def clear_comvest_task():
    clear_comvest.clean_all()


@task
def divide_comvest_task():
    divide_comvest.split_all()


@task
def comvest_enem_merge_task():
    comvest_enem.merge()


@task
def comvest_vest_ids_task():
    comvest_vest_ids.retrieve()


@task
def comvest_enem_ids_task():
    comvest_enem_ids.merge()
