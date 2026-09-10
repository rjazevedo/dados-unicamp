"""Cache baseado em existencia de arquivo, generalizando
check_if_need_result_file() (hoje restrito a ~15 chamadas em COMVEST/DAC)
para qualquer task do Prefect.

Uso:
    from flows.cache import file_exists_cache_key

    @task(cache_key_fn=file_exists_cache_key(lambda: get_config("comvest")["result"] + "dados_comvest.csv"))
    def cod_ibge_task():
        cod_ibge.merge()

Se o arquivo existir no momento em que a task for chamada, o cache_key_fn
retorna uma chave estavel (baseada so no caminho) -- o Prefect reaproveita o
resultado cacheado em vez de rodar a task de novo. Se o arquivo nao existir,
retorna None (Prefect trata como "sem chave de cache", forcando execucao).

Sem expiracao automatica -- so invalidado apagando o arquivo de output ou
trocando o caminho. Nao usar em tasks cujo cache deve ser tudo-ou-nada por
motivo de corretude (ver rais.id_generation.random_index.generate_index() e
dac.uniao_dac_comvest.uniao_dac_comvest.generate() no plan.md): usar
file_exists_cache_key nelas tambem, mas nunca decompor em tasks parciais por
ano/registro.
"""

from pathlib import Path
from typing import Callable, Union


def file_exists_cache_key(path_or_getter: Union[str, Callable[[], str]]):
    """Cria um cache_key_fn do Prefect a partir de um caminho de arquivo fixo
    ou de uma funcao sem argumentos que retorna esse caminho (use uma funcao
    quando o caminho depender de config/settings.get_config(), resolvida em
    tempo de execucao, nao de import)."""

    def _cache_key_fn(context, parameters):
        path = path_or_getter() if callable(path_or_getter) else path_or_getter
        if Path(path).exists():
            return f"file-exists:{path}"
        return None

    return _cache_key_fn
