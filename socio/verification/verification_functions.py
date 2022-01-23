def check_cnpj(value):
    if value == '99999999999999':
        is_valid = False
    else:
        # Checks if is in pattern NNNNNNNNNNNNNN
        is_valid_len = len(value) == 14
        is_valid_num = all(char.isnumeric() for char in value)
        is_valid = is_valid_len and is_valid_num
    return not is_valid

def check_cpf(value):
    if value == '00000000000':
        is_valid = False
    else:
        # Checks if is in pattern ***NNNNNN** or NNNNNNNNNNN
        is_valid_len = len(value) == 11
        is_valid_num = all((char == '*' or char.isnumeric()) for char in value[:3]) and all(char.isnumeric() for char in value[3:-2]) and all((char == '*' or char.isnumeric()) for char in value[-2:])
        is_valid = is_valid_len and is_valid_num
    return not is_valid

def check_identificador_de_socio(value):
    values = [1, 2, 3]
    is_valid = value in values
    return not is_valid
    
def check_nome_socio(nome, identificador_socio):
    # If it is a juridic person, checks if it is a person name
    if identificador_socio == 2:
        return check_name(nome)
    return False
    
def check_cnpj_cpf_do_socio(value):
    if len(value) == 11:
        return check_cpf(value)
    if len(value) == 14:
        return check_cnpj(value)
    return True
    
def check_codigo_qualificacao(value):
    is_valid = value >= 1 and value <= 79
    return not is_valid
    
def check_data(date):
    day = int(date[:2])
    month = int(date[2:4])
    year = int(date[4:])

    is_day_valid = day >= 1 and day <= 31
    is_month_valid = month >= 1 and month <= 12
    is_year_valid = year > 0

    is_valid = is_day_valid and is_month_valid and is_year_valid
    return not is_valid
    
def check_ano(year, date):
    # Checks if year of 'data_entrada_sociedade' is equal 'ano_entrada_sociedade'
    year_date = int(date[4:])
    is_valid = year == year_date
    return not is_valid
    
def check_name(value):
    # Checks if name has only alphabetic caracters or spaces
    is_valid = all(char.isalpha() or char.isspace() for char in value)
    return not is_valid

def check_identificador_matriz_filial(value):
    values = [1, 2]
    is_valid = value in values
    return not is_valid

def check_situacao_cadastral(value):
    values = [1, 2, 3, 4, 8]
    is_valid = value in values
    return not is_valid

def check_motivo_situacao_cadastral(value):
    values = [60, 61, 62, 63, 64, 66, 67, 70, 71, 72, 73, 74, 80]
    is_valid = (value >= 1 and value <= 55) or (value in values)
    return not is_valid

def check_cep(value):
    is_valid = len(value) == 8
    return not is_valid

def check_capital_social(value):
    is_valid = value >= 0
    return not is_valid

def check_porte(value):
    values = [0, 1, 3, 5]
    is_valid = value in values
    return not is_valid

def check_true_or_false(value):
    values = [0, 1]
    is_valid = value in values
    return not is_valid

def check_sigla_uf(value):
    values = [
        'AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO',
        'MA', 'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI',
        'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO',
        'EX'
    ]
    is_valid = value in values
    return not is_valid
