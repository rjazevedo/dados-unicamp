

columns = {
        "PRE2012" : ['NU_INSCRICAO', 'NU_NT_CN', 'NU_NT_CH', 'NU_NT_LC', 'NU_NT_MT', 'NU_NOTA_REDACAO'],
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
    }
}