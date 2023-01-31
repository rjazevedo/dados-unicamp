from rais.utilities.rais_information import get_columns_info_rais
from rais.utilities.rais_information import get_column
from rais.utilities.rais_information import get_info_period


# Return dtype for dac files
def get_dtype_dac_comvest():
    return {
        "ano_ingresso_curso": "int64",
        "cpf": str,
        "cpf_comvest": str,
        "cpf_dac": str,
        "curso_comvest": "Int32",
        "curso_dac": "Int32",
        "doc": str,
        "doc_comvest": str,
        "doc_dac": str,
        "dta_nasc": str,
        "dta_nasc_comvest": str,
        "dta_nasc_dac": str,
        "identif": "Int64",
        "insc_vest": "Int64",
        "insc_vest_comvest": "Int64",
        "insc_vest_dac": "Int64",
        "nome": str,
        "nome_comvest": str,
        "nome_dac": str,
        "origem": str,
        "tipo_ingresso": str,
        "tipo_ingresso_comvest": "Int32",
        "origem_cpf": "int64",
    }


# Return dtype for original rais files from specified year
def get_dtype_rais_original(year):
    columns_info = get_columns_info_rais()
    dtype = {}
    for column in columns_info:
        name_column = get_column(column, year)
        if name_column != None:
            type_column = columns_info[column]["tipo"]
            if type(type_column) == str:
                dtype[name_column] = type_column
            else:
                dtype[name_column] = get_info_period(year, type_column)
    return dtype


# Return dtype for clean rais files
def get_dtype_rais_clean():
    columns_info = get_columns_info_rais()
    dtype = {}
    for column in columns_info:
        dtype[column] = columns_info[column]["tipo_limpo"]
    return dtype
