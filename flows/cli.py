"""Entrypoint de linha de comando pro pipeline_flow.

Preserva a UX de quem ja usa `uv run __main__.py`: rodado num TTY sem
argumentos, faz a mesma pergunta interativa de sempre (limitada/completa
pra RAIS). Aceita --tipo-extracao-rais pra uso nao-interativo (ex. via tsp
ou cron).

Uso:
  uv run -m flows.cli
  uv run -m flows.cli --tipo-extracao-rais limitada
"""

import argparse
import sys

from flows.pipeline_flow import pipeline_flow


def _prompt_tipo_extracao_rais() -> str:
    d = {1: "limitada", 2: "completa"}
    while True:
        rais_in = int(
            input(
                "Digite 1 para realizar a extração limitada da base RAIS ou 2 para a extração completa:"
            )
        )
        if rais_in != 1 and rais_in != 2:
            print("Entrada inválida, digite novamente.")
        else:
            return d[rais_in]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--tipo-extracao-rais",
        choices=["limitada", "completa"],
        default=None,
        help="Sem essa flag, num TTY, pergunta interativamente (like __main__.py).",
    )
    args = parser.parse_args()

    tipo_extracao_rais = args.tipo_extracao_rais
    if tipo_extracao_rais is None:
        if sys.stdin.isatty():
            tipo_extracao_rais = _prompt_tipo_extracao_rais()
        else:
            tipo_extracao_rais = "completa"

    pipeline_flow(tipo_extracao_rais=tipo_extracao_rais)


if __name__ == "__main__":
    main()
