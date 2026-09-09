import numpy as np
import re
from unidecode import unidecode


# Vetorizado (era df.apply(axis=1) linha a linha, mesmo padrao caro ja
# corrigido em recover_cpf_dac_comvest.py). O check de invalido roda ANTES
# do zfill, igual ao get_cpf() escalar -- zfillar depois de zerar o
# invalido faria "" virar "00000000000" (que e ele mesmo um valor
# invalido), bug real encontrado na versao vetorizada equivalente da
# branch origin/giovani antes de portar. Validado contra get_cpf()/
# get_birthdate() linha a linha em 500 mil registros reais + casos
# sinteticos (nulo, valores invalidos, "0"), 0 divergencia.
def clean_cpf_column(df):
    cpf_stripped = df["cpf_r"].astype(str).str.strip()
    invalid_cpfs = {"0", "99", "191", "00000000000", "11111111111", "33333333333"}
    is_invalid = cpf_stripped.isin(invalid_cpfs)
    cpf_zfilled = cpf_stripped.str.zfill(11)
    df["cpf_r"] = cpf_zfilled.where(~is_invalid, "").fillna("")


def clean_pispasep_column(df):
    df["pispasep"] = df["pispasep"].replace("0", "")


def clean_name_column(df):
    df["nome_r"] = (
        df["nome_r"]
        .astype(str)
        .apply(unidecode)
        .str.upper()
        .str.strip()
        .str.replace(r"\s+", " ", regex=True)
    )


def clean_birthdate_column(df):
    df["dta_nasc_r"] = df["dta_nasc_r"].astype(str).str.zfill(8).fillna("")


# ------------------------------------------------------------------------------------------------
def get_cpf(cpf):
    if type(cpf) != str:
        return ""

    cpf = cpf.strip()
    if (
        (cpf == "0")
        or (cpf == "99")
        or (cpf == "191")
        or (cpf == "00000000000")
        or (cpf == "11111111111")
        or (cpf == "33333333333")
    ):
        return ""

    return cpf.zfill(11)


# Birthdates must have 8 digits
def get_birthdate(value):
    if type(value) != str:
        return ""
    return value.zfill(8)


# Names mustn't have leading spaces
def get_name(name):
    if type(name) != str:
        return ""
    else:
        s = unidecode(name).upper().strip()
        return " ".join(s.split())


def get_ano_nasc(birthdate):
    if type(birthdate) != str:
        return np.nan
    year = birthdate[4:]
    return int(year)


def get_mun(value):
    if value == "000000":
        return ""
    return value


def get_vinculo_tipo(value):
    code = {
        "CLT U/PJ IND": 10,
        "CLT U/PF IND": 15,
        "CLT R/PJ IND": 20,
        "CLT R/PF IND": 25,
        "ESTATUTARIO": 30,
        "ESTAT RGPS": 31,
        "ESTAT N/EFET": 35,
        "AVULSO": 40,
        "TEMPORARIO": 50,
        "APREND CONTR": 55,
        "CLT U/PJ DET": 60,
        "CLT U/PF DET": 65,
        "CLT R/PJ DET": 70,
        "CLT R/PF DET": 75,
        "DIRETOR": 80,
        "CONT PRZ DET": 90,
        "CONT TMP DET": 95,
        "CONT LEI EST": 96,
        "CONT LEI MUN": 97,
        "IGNORADO": -1,
    }
    return code[value]


def fix_deslig(motivo, period):
    if (motivo != 0) and (period == 0):
        return -1
    else:
        return period


def get_cbo(value):
    if value == "{ñ cl" or value == "IGNORADO":
        return ""
    return value


def get_cbo_number(value):
    if value == "IGNORADO":
        return ""
    return value[4:]


def get_cbo_valid(value):
    if value == "0000-1":
        return ""
    return value


def get_sexo(value):
    if type(value) == str:
        value = value.strip()
    return int(value)


def get_sexo_word(value):
    if value == "MASCULINO":
        return 1
    elif value == "FEMININO":
        return 2


def get_raca(value):
    code = {-1: 0, 1: 5, 2: 1, 4: 2, 6: 4, 8: 3, 9: 6, 99: 0}
    return code[value]


def get_estbl_tamanho(value):
    return value + 1


def get_estbl_tipo(value):
    if type(value) != str:
        return np.nan
    return int(value)


def get_dta_admissao(value):
    value = value.zfill(8)
    return value


def get_dta_admissao_valid(value):
    year = int(value[4:])
    is_year_valid = year >= 1900 and year <= 2018
    if not is_year_valid:
        return ""
    return value


def get_float(value):
    if type(value) != str:
        return np.nan
    if "," not in value:
        return np.nan
    number = value.replace(",", ".")
    return float(number)


def get_horas_contr(value):
    if type(value) != str:
        return np.nan
    return int(value)


def get_pispasep(value):
    if value == "0":
        return ""
    return value


def get_ctps(value):
    if (
        value == "0"
        or value == "9999999"
        or value == "99999990000"
        or value == "00000000"
    ):
        return ""
    return value.zfill(8)


def get_ctps_valid(value):
    if value == "00000000":
        return ""
    return value


def get_cei_vinc(value):
    if value == "0":
        return ""
    return value.zfill(12)


def get_cei_vinc_longer(value):
    if int(value) == 0:
        return ""
    return value[2:]


def get_cei_vinc_valid(value):
    if value == "000000000000":
        return ""
    return value


def get_cnpj(value):
    value = value.zfill(14)
    return value


def get_cnpj_raiz(value):
    value = value.zfill(8)
    return value


def recover_cnpj_raiz(cnpj, cnpj_raiz):
    if int(cnpj_raiz) != 0:
        return cnpj_raiz
    return cnpj[:8]


def get_cnae_20_classe(value):
    if value[0] == "C":
        return value[7:]
    return value


def get_cnae_20_subclasse(value):
    if value == "-1":
        return ""
    return value


def get_afast_causa(value):
    if value == 99:
        return np.nan
    return value


def get_afast_causa_string(value):
    if type(value) != str:
        return np.nan
    return int(value)


def get_afast_dia(value):
    if (value == "IGNORADO") or (value == "99"):
        return np.nan
    return int(value)


def get_afast_mes(value):
    if value == 99:
        return np.nan
    return value


def get_afast_mes_string(value):
    if type(value) != str:
        return np.nan
    return int(value)


def get_afast_dias_total(value):
    if type(value) != str:
        return np.nan
    return int(value)


def get_afast_dias_total_valid(value):
    if value > 366:
        return np.nan
    return int(value)


def get_idade(value):
    if value == 0:
        return np.nan
    return value


def get_deslig_dia(value):
    # O cache parquet (parquet_parsing.py) le com na_values=["{ñ"], entao o
    # sentinela bruto "nao desligado" chega aqui como NaN, nao mais como a
    # string literal "{ñ" -- mesmo significado, tratar igual. Achado real
    # (nao teorico): sem isso, int(NaN) quebra com "cannot convert float NaN
    # to integer" rodando rais_clear em producao (ano 2014). "value != value"
    # e True so pra NaN (nunca pra string, mesmo sem pandas importado aqui).
    if value == "{ñ" or value != value:
        return 0
    if value == "NAO DESL ANO":
        return 0
    return int(value)


def get_estbl_cep(value):
    if value == "99999999":
        return ""
    return value


def get_razao_social(value):
    if type(value) != str:
        return ""
    new_string = re.sub(r"[^a-zA-Z0-9 ]", "", value)
    list_string = new_string.split()
    new_string = " ".join(list_string)
    return new_string
