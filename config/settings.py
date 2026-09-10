"""Config unificada de caminhos para todos os pacotes do pipeline.

Le config/paths.yaml uma vez, resolve os placeholders {INPUT_ROOT} /
{OUTPUT_ROOT} / {PROCESSADOS_ROOT} a partir da env var opcional
DADOS_UNICAMP_ROOT, e expoe get_config(pacote) -> dict.

Sem DADOS_UNICAMP_ROOT setada, os roots sao os mount points de producao
de sempre (/home/input, /home/output, /home/processados) -- zero mudanca
de comportamento pra quem nao usa a env var.
"""

import os
from pathlib import Path

import yaml

_PATHS_FILE = Path(__file__).parent / "paths.yaml"

_DEFAULT_ROOTS = {
    "INPUT_ROOT": "/home/input",
    "OUTPUT_ROOT": "/home/output",
    "PROCESSADOS_ROOT": "/home/processados",
}


def _roots() -> dict:
    dados_root = os.environ.get("DADOS_UNICAMP_ROOT")
    if not dados_root:
        return dict(_DEFAULT_ROOTS)
    dados_root = dados_root.rstrip("/")
    return {
        "INPUT_ROOT": f"{dados_root}/input",
        "OUTPUT_ROOT": f"{dados_root}/output",
        "PROCESSADOS_ROOT": f"{dados_root}/processados",
    }


def _load_raw() -> dict:
    with open(_PATHS_FILE) as f:
        return yaml.safe_load(f)


def _resolve(value, roots):
    if isinstance(value, str):
        return value.format(**roots)
    if isinstance(value, list):
        return [_resolve(v, roots) for v in value]
    return value


def get_config(pacote: str) -> dict:
    raw = _load_raw()
    if pacote not in raw:
        raise KeyError(
            f"Pacote '{pacote}' nao encontrado em config/paths.yaml. "
            f"Pacotes disponiveis: {sorted(raw.keys())}"
        )
    roots = _roots()
    return {key: _resolve(value, roots) for key, value in raw[pacote].items()}
