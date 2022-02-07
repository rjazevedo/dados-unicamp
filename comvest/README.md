# Comvest

Neste diretório encontram-se os módulos de limpeza, extração e anonimização de dados da Comvest (Comissão Permanente para os Vestibulares da Unicamp). Como os arquivos originais são planilhas separadas em diferentes páginas (sheet names), os scripts foram desenvolvidos a partir de cada uma delas. Os módulos encontrados no diretório são:

- clear_dados - Extração e limpeza da página de dados.
- clear_notas - Extração e limpeza da(s) página(s) de notas.
- clear_perfil - Extração e limpeza da página de perfil, referente ao Questionário Socioeconômico dos candidatos.
- extract_cities - Extração das cidades que aplicaram as provas Comvest em cada ano.
- extract_courses - Extração dos cursos disponíveis em cada ano.
- extract_enrolled - Extração dos matriculados de cada ano.
- extract - Extração e limpeza completa da base, utilizando-se dos módulos mencionados acima.
- assign_ids - Atribuição de identificadores únicos com o fim de manter a unicidade e anonimidade dos alunos.
- filters - Filtragem do conjunto de dados de acordo com parâmetros específicos.
- utilities - Módulo com funções auxiliares (para leitura/escrita de arquivos, por exemplo).


## Execução
Primeiramente, os arquivos .xlsx da base de dados devem estar contidos no diretório input do projeto e as configurações dos caminhos de arquivos devem ser definidas em configuration.yaml.


Para executar a extração/limpeza completa da base Comvest execute:
```
python3 -m comvest.extract
```

Caso deseje executar a extração/limpeza de um módulo específico:
```
python3 -m comvest.<MODULE_NAME>
```
Ex.: 
```
python3 -m comvest.clear_perfil
```