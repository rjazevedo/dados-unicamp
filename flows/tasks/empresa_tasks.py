"""Task do Prefect para empresa (depende de socio_amostra.csv)."""

from flows.memory_log import task_with_memory_log as task

from empresa.extract import extract_empresa_amostra


@task
def empresa_task():
    extract_empresa_amostra()
