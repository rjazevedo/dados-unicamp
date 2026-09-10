"""Task do Prefect para estabelecimento (depende de socio_amostra.csv)."""

from prefect import task

from estabelecimento.extract import extract_estabelecimento_amostra


@task
def estabelecimento_task():
    extract_estabelecimento_amostra()
