import re
from rais.verification.aux_files import (
    municipios,
    cnae95,
    cbo94,
    cbo02,
    nat_juridica,
    cnae20classe,
    cnae20subclasse,
)

# Checks nothing
def dummy(value):
    return True


# Checks if value is one of municipios codes
def check_mun_estbl(value):
    if type(value) != str:
        return True
    return value in municipios.values


# Checks if value is one of cnae95 codes
def check_cnae95(value):
    if type(value) != str:
        return True
    return value in cnae95.values


# Checks if it's zero (not) or one (yes)
def check_zero_or_one(value):
    if value == -1:
        return True
    return value == 0 or value == 1


# Checks if value is one of vinculo_tipo codes
def check_vinculo_tipo(value):
    values = [
        10,
        15,
        20,
        25,
        30,
        31,
        35,
        40,
        50,
        55,
        60,
        65,
        70,
        75,
        80,
        90,
        95,
        96,
        97,
    ]
    return value in values


# Checks if motivo, mes and dia are all zero or are all valid
def check_deslig(motivo, mes, dia):
    if (motivo == 0) and (mes == 0) and (dia == 0 or dia == -1):
        return True
    return check_deslig_motivo(motivo) and check_mes(mes) and check_dia(dia)


# Checks if value is one of deslig_motivo codes
def check_deslig_motivo(value):
    values = [
        10,
        11,
        12,
        20,
        21,
        22,
        30,
        31,
        32,
        33,
        34,
        40,
        50,
        60,
        62,
        63,
        64,
        70,
        71,
        72,
        73,
        74,
        75,
        76,
        78,
        79,
        80,
        90,
    ]
    return value in values


# Checks if value is one of admissao_tipo codes
def check_admissao_tipo(value):
    if value == -1:
        return True
    return value >= 0 and value <= 10


# Checks if value is one of salario_tipo codes
def check_salario_tipo(value):
    return value >= 1 and value <= 7


# Checks if value is one of cbo94 codes
def check_cbo94(value):
    if type(value) != str:
        return True
    return value in cbo94.values


# Checks if value is one of escolaridade codes
def check_escolaridade(value):
    if value == -1:
        return True
    return value >= 1 and value <= 11


# Checks if value is 1 (male) or 2 (female)
def check_sexo(value):
    return value == 1 or value == 2


# Checks if value is one of nacionalidades codes
def check_pais_nacionalidade(value):
    values = [
        10,
        20,
        21,
        22,
        23,
        24,
        25,
        26,
        27,
        28,
        29,
        30,
        31,
        32,
        34,
        35,
        36,
        37,
        38,
        39,
        40,
        41,
        42,
        43,
        44,
        45,
        46,
        47,
        48,
        49,
        50,
        51,
        59,
        60,
        61,
        62,
        63,
        64,
        70,
        80,
    ]
    return value in values


# Checks if value is one of raca codes
def check_raca(value):
    if value == -1:
        return True
    values = [0, 1, 2, 3, 4, 5, 6]
    return value in values


# Checks if value is one of estbl_tamanho codes
def check_estbl_tamanho(value):
    return value >= 1 and value <= 10


# Checks if value is one of nat_juridica codes
def check_nat_juridica(value):
    return value in nat_juridica.values


# Checks if value is one of estbl_tipo codes
def check_estbl_tipo(value):
    values = [1, 3, 5, 9]
    return value in values


# Checks if value is a valid date
def check_date(value):
    if type(value) != str:
        return True

    day = int(value[:2])
    month = int(value[2:4])
    year = int(value[4:])

    is_day_valid = day >= 1 and day <= 31
    is_month_valid = month >= 1 and month <= 12
    is_year_valid = year >= 1900 and year <= 2018

    return is_day_valid and is_month_valid and is_year_valid


# Checks if value is between 0 and 44
def check_horas_contr(value):
    return value >= 0 and value <= 44


# Checks if value has 11 digits and is not zero
def check_pispasep(value):
    if type(value) != str:
        return True
    if int(value) == 0:
        return False
    return len(value) == 11


# Checks if value has 8 digits and is not zero
def check_ctps(value):
    if type(value) != str:
        return True
    if int(value) == 0:
        return False
    return len(value) == 8


# Checks if value has 11 digits, is numeric and is not zero
def check_cpf(value):
    if int(value) == 0:
        return False
    return (len(value) == 11) and value.isnumeric()


# Checks if value has 12 digits and is not zero
def check_cei_vinc(value):
    if type(value) != str:
        return True
    if int(value) == 0:
        return False
    return len(value) == 12


# Checks if value has 14 digits and is not zero
def check_cnpj(value):
    if int(value) == 0:
        return False
    return len(value) == 14


# Checks if cnpj_raiz is equal the first 8 digits of cnpj
def check_cnpj_raiz(cnpj, cnpj_raiz):
    return cnpj_raiz == cnpj[:8]


# Checks if value doesn't have spaces in the end of string
def check_name(value):
    return value[-1] != " "


# Checks if value is one of cbo02 codes
def check_cbo02(value):
    if type(value) != str:
        return True
    return value in cbo02.values


# Checks if value is one of cnae20_classe codes
def check_cnae_20_classe(value):
    if type(value) != str:
        return True
    return value in cnae20classe.values


# Checks if value is one of cnae20_subclasse codes
def check_cnae_20_subclasse(value):
    if type(value) != str:
        return True
    return value in cnae20subclasse.values


# Checks if value is one of afast_causa codes
def check_afast_causa(value):
    if value == -1:
        return True
    values = [10, 20, 30, 40, 50, 60, 70]
    return value in values


# Checks if value is between 1 and 31
def check_dia(value):
    if value == -1:
        return True
    return value >= 1 and value <= 31


# Checks if value is between 1 and 12
def check_mes(value):
    if value == -1:
        return True
    return value >= 1 and value <= 12


# Checks if value is between 0 and 366
def check_afast_dias_total(value):
    if value == -1:
        return True
    return value >= 0 and value <= 366


# Checks if value is between 13 and 100
def check_idade(value):
    if value == -1:
        return True
    return value >= 13 and value <= 100


# Checks if value is one of ibge_subsetor codes
def check_ibge_subsetor(value):
    if value == -1:
        return True
    values = [
        1,
        2,
        3,
        4,
        5,
        6,
        7,
        8,
        9,
        10,
        11,
        12,
        13,
        14,
        15,
        16,
        17,
        18,
        19,
        20,
        21,
        22,
        23,
        24,
        25,
    ]
    return value in values


# Checks if value has 8 digits
def check_estbl_cep(value):
    if type(value) != str:
        return True
    return len(value) == 8


# Checks if value has not special characters and has not extra spaces
def check_razao_social(value):
    if type(value) != str:
        return True

    if not re.match("^[A-Za-z0-9 ]*$", value):
        return False

    espaco = False
    for char in value:
        if espaco and (char == " "):
            return False
        if char == " ":
            espaco = True
        else:
            espaco = False
    return True
