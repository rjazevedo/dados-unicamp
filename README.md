# dados-unicamp

Repositório de processamento, limpeza, integração e amostragem de bases de dados acadêmicas e administrativas relacionadas à Unicamp.

## Objetivo

Este projeto consolida pipelines de múltiplas fontes (ex.: Comvest, DAC, RAIS, Sócios, CAPES, ENEM, FUVEST, UNESP), com foco em:

- extração de dados brutos;
- limpeza e padronização;
- geração de identificadores anonimizados;
- integração entre bases;
- criação de amostras para análise.

## Estrutura geral

Cada fonte de dados possui sua própria pasta com módulos de execução independentes (normalmente com `__main__.py`) e arquivos de configuração (`configuration.yaml` quando aplicável).

Principais diretórios:

- `comvest/`
- `dac/`
- `rais/`
- `socio/`
- `capes/`
- `enem/`
- `fuvest/`
- `unesp/`
- `empresa/`
- `estabelecimento/`
- `simples/`
- `diplomas/`

## Requisitos

- `uv` instalado ([astral.sh/uv](https://astral.sh/uv))
- Python 3.8+

As dependências do projeto agora estão centralizadas em `pyproject.toml`.

### Setup rápido

Na raiz do projeto:

```bash
uv sync
```

Esse comando cria/atualiza o ambiente virtual e instala automaticamente as dependências.

## Como executar

### 1) Pipeline principal (orquestração completa)

Na raiz do projeto:

```bash
uv run __main__.py
```

Esse fluxo executa múltiplas bases em sequência e solicita entradas interativas para definir o tipo de extração em algumas etapas (por exemplo, Sócios e RAIS).

### 2) Execução por módulo

Na raiz do projeto, você também pode executar apenas partes específicas:

```bash
uv run -m comvest.extract
uv run -m dac.extract_database
uv run -m rais
uv run -m socio.cleaning
uv run -m socio.extract
uv run -m capes.cleaning
uv run -m capes.extract
uv run -m fuvest.extract
uv run -m unesp.extract
uv run -m empresa
uv run -m estabelecimento
uv run -m simples
```

## Configuração de dados de entrada

Antes de executar qualquer pipeline:

1. coloque os arquivos brutos nos diretórios esperados por cada base;
2. preencha os arquivos de configuração do módulo correspondente;
3. execute primeiro os passos de pré-processamento quando o módulo exigir.

Cada base define os caminhos e formatos esperados no seu próprio README e/ou `configuration.yaml`.

## Documentação por base

- `comvest/README.md`
- `dac/README.md`
- `rais/README.md`
- `socio/README.md`
- `dac/dac_flowchart.md`
- `rais/flowchart.md`

## Convenções úteis

- módulos com `extract/`, `cleaning/`, `verification/` tendem a representar etapas separadas de pipeline;
- `utilities/` concentra funções auxiliares reutilizáveis;
- arquivos `__main__.py` indicam o ponto de entrada do módulo.

## Próximos passos de documentação (sugerido)

Para facilitar manutenção em um projeto desse porte, vale evoluir para:

1. um índice único dos pipelines (entrada → transformação → saída) por base;
2. um padrão de README por módulo (objetivo, entradas, saídas, comandos, falhas comuns);
3. um catálogo de schemas/colunas principais por dataset processado.