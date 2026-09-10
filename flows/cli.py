"""Entrypoint de linha de comando pro pipeline_flow.

Uso:
  uv run -m flows.cli
"""

from flows.pipeline_flow import pipeline_flow


def main():
    pipeline_flow()


if __name__ == "__main__":
    main()
