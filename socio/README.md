# Sócios, Empresas e CNAE Secundária

## Correção dos arquivos originais
Na base original de sócios carregada da internet, o arquivo .csv apresenta um problema onde algumas linhas aparecem com mais campos do que deveriam, impossiblitando a leitura por meio do framework pandas.

Dessa forma, antes de rodar os scripts de limpeza, é necessário rodar o seguinte comando para consertar o arquivo:
```
sed '6252723d' ARQUIVO_SOCIO_ORIGINAL.csv | sed '7543653d' > ARQUIVO_SOCIO_CONSERTADO.csv
```
Explicação do comando:
A linha defeituosa do arquivo é a linha 6252723, que removemos com o comando sed.
Após a remoção dessa linha, uma nova linha defeiturosa aparece na posição 7543653, que removemos também.

## Módulos disponíveis

Aqui se encontram os scripts de limpeza, extração e verificação dos dados das bases de Sócios, Empresas e CNAE Secundário, todas carregadas no site https://basedosdados.org/dataset/br-me-socios.

O projeto está dividido nos seguintes módulos:

- cleaning - Responsável pela limpeza dos dados das três bases
- database_information - Dicionário com informações dos campos de cada uma das bases, como o tipo da variável, função de limpeza correspondente e função de verificação correspondente
- extract - Responsável pela extração da amostra dos sócios presentes também na união_dac_comvest
- utilities - Disponibiliza funções auxiliares para leitura e escrita de arquivos e log de informação.
- verification - Responsável pela verificação dos dados limpos das três bases

## Execução dos scripts
Inicialmente, coloque os arquivos originais das bases de Sócios (tendo já removido as linhas com problema), Empresas e CNAE Secundária no diretório 'input/socio' do projeto.

É necessário também preencher o arquivo configuration.yaml com os caminhos para os arquivos originais das bases, o arquivo com os ids dos indivíduos da uniao_dac_comvest e o diretório onde os arquivos limpos deverão ser criados.

Para executar a limpeza completa das bases execute:
```
python3 -m socio.cleaning
```

Para extrair apenas os dados referentes a indivíduos da uniao_dac_comvest execute:
```
python3 -m socio.extract
```

Para verificar as bases limpas execute:
```
python3 -m socio.verification
```