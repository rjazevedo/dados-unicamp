# DAC

Aqui se encontram os scripts de limpeza e extração de dados de bases da DAC (Diretoria Acadêmica da Universidade Estadual de Campias). O projeto está dividido nos seguintes módulos de:

- clr_dados_cadastrais - Para limpeza de dados cadastrais dos alunos
- clr_historico_escolar - Para limpeza do histórico escolar dos alunos
- clr_vida_academica - Para limpeza de dados relativos à vida acadêmica do aluno
- clr_resumo_por_periodo - Para limpeza de dados relativos a vida acadêmica do aluno em cada período cursado
- extract_database - Para limpeza completa da base
- create_ids - Para a geração de identificadores únicos com o fim de manter a unicidade e anonimidade dos alunos
- utilities - Módulo com funções auxiliares utilizadas na limpeza

Além disso temos o arquivo configuration_example.yaml que deve ser renomeado para configuration.yaml e preenchido com os diretórios para as bases.

## Execução
Para executar primeiramente coloque os arquivos .xlsx da base de dados no diretório input do projeto e preencha as configurações em configuration.yaml.


Para executar a limpeza completa da base execute:
```
python3 -m extract_database
```

Similarmente para executar a limpeza de um módulo específico
```
python3 -m <MODULE_NAME>
```