# dados-unicamp

## Overview
Processamento de dados educacionais da Unicamp

## Dependências
|        |          |                            |
|--------|----------|----------------------------|
| python | >=3.8    | https://www.python.org/    |
| pandas | >=0.25.3 | https://pandas.pydata.org/ |
| numpy  | >=1.17.4 | https://numpy.org/         |

## Execução
Para rodar a limpeza completa de todas as bases rode na pasta onde está seu repositório:
``` 
python3 -m dados-unicamp

``` 
Caso queira apenas limpar uma base específica:
- DAC
``` 
cd dados-unicamp/dac
python3 -m extract_dac
```