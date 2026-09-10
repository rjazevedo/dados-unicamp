"""Task do Prefect para estabelecimento (depende de socio_amostra.csv)."""

from flows.memory_log import task_with_memory_log as task

from estabelecimento.extract import extract_estabelecimento_amostra


@task
def estabelecimento_task():
    extract_estabelecimento_amostra()
