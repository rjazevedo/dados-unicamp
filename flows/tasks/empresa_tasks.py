"""Task do Prefect para empresa (depende de socio_amostra.csv)."""

from prefect import task

from empresa.extract import extract_empresa_amostra


@task
def empresa_task():
    extract_empresa_amostra()
