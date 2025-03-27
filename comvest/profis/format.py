"""
Este script define os parâmetros de leitura e as colunas para os dados do Profis em diferentes anos.

Dicionários:
- columns: Define as colunas a serem lidas para diferentes períodos.
- reading_parameters: Define os parâmetros de leitura, incluindo as colunas e o separador, para cada ano específico.

Como usar:
Importe os dicionários `columns` e `reading_parameters` para acessar as colunas e os parâmetros de leitura para os dados do Enem.
"""

columns = {
        "2011" : ['Anolng', 'insc2', 'nome', 'cpf', 'sexo', 'municipio nasc', 'est_nas', 'dia', 'mes', 'ano', 'nacionalidade',
                  'nome_pai', 'nome_mae', 'municipio', 'estado', 'cep', 'escola'],
        "PRE2014" : ['NU_INSCRICAO', 'NOTA_CN', 'NOTA_CH', 'NOTA_LC', 'NOTA_MT', 'NU_NOTA_REDACAO'],
        "POS2015" : ['NU_INSCRICAO', 'NU_NOTA_CN', 'NU_NOTA_CH', 'NU_NOTA_LC', 'NU_NOTA_MT', 'NU_NOTA_REDACAO'],
}

reading_parameters = {
    2012 : {
        "columns" : columns["PRE2012"],
        "separator" : ','
    },
    2013 : {
        "columns" : columns["PRE2014"],
        "separator" : ';'
    },
    2014 : {
        "columns" : columns["PRE2014"],
        "separator" : ','
    },

    2015 : {
        "columns" : columns["POS2015"],
        "separator" : ','
    },

    2016 : {
        "columns" : columns["POS2015"],
        "separator" : ';'
    },
    2017 :{
        "columns" : columns["POS2015"],
        "separator" : ';'
    },
    2018 :{
        "columns" : columns["POS2015"],
        "separator" : ';'
    },
    2019 :{
        "columns" : columns["POS2015"],
        "separator" : ';'
    },
    2020 : {
        "columns" : columns["POS2015"],
        "separator" : ';'
    },
    2021 : {
        "columns" : columns["POS2015"],
        "separator" : ';'
    }
}
