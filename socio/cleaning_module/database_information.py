import cleaning.cleaning_functions
import cleaning_module.verification_functions

def get_dtype(columns_info, is_original=False):
    dtype = {}
    for column in columns_info:
        if is_original:
            dtype[column] = get_type_column_original(column, columns_info)
        else:
            dtype[column] = get_type_column_clean(column, columns_info)
    return dtype

def get_type_column_original(column, columns_info):
    if 'has_null_value' in columns_info[column]:
        return 'object'
    else:
       return columns_info[column]['type']

def get_type_column_clean(column, columns_info):
    return columns_info[column]['type']

#------------------------------------------------------------------------------------------------
def get_columns_info_socio():
    return {
        'cnpj': {
            'type': 'object',
            'cleaning_function': None,
            'verification_function': cleaning_module.verification_functions.check_cnpj
        },
        'identificador_de_socio': {
            'type': 'int64',
            'cleaning_function': None,
            'verification_function': cleaning_module.verification_functions.check_identificador_de_socio
        },
        'nome_socio': {
            'type': 'object',
            'cleaning_function': cleaning.cleaning_functions.clear_nome,
            'verification_function': None
        },
        'cnpj_cpf_do_socio': {
            'type': 'object',
            'cleaning_function': cleaning.cleaning_functions.clear_cnpj_cpf,
            'verification_function': cleaning_module.verification_functions.check_cnpj_cpf_do_socio
        },
        'codigo_qualificacao_socio': {
            'type': 'int64',
            'cleaning_function': cleaning.cleaning_functions.clear_codigo_qualificacao,
            'verification_function': cleaning_module.verification_functions.check_codigo_qualificacao
        },
        'data_entrada_sociedade': {
            'type': 'object',
            'cleaning_function': cleaning.cleaning_functions.clear_data,
            'verification_function': cleaning_module.verification_functions.check_data
        },
        'ano_entrada_sociedade': {
            'type': 'int64',
            'cleaning_function': None,
            'verification_function': None
        },
        'cpf_representante_legal': {
            'type': 'object',
            'cleaning_function': cleaning.cleaning_functions.clear_cpf,
            'verification_function': cleaning_module.verification_functions.check_cpf
        },
        'nome_representante_legal': {
            'type': 'object',
            'cleaning_function': None,
            'verification_function': cleaning_module.verification_functions.check_name
        },
        'codigo_qual_representante_legal': {
            'type': 'int64',
            'has_null_value': True,
            'cleaning_function': cleaning.cleaning_functions.clear_codigo_qualificacao,
            'verification_function': cleaning_module.verification_functions.check_codigo_qualificacao
        }
    }

def get_columns_info_empresa():
    return {
        'cnpj': {
            'type': 'object',
            'cleaning_function': None,
            'verification_function': cleaning_module.verification_functions.check_cnpj
        },
        'identificador_matriz_filial': {
            'type': 'int64',
            'cleaning_function': None,
            'verification_function': cleaning_module.verification_functions.check_identificador_matriz_filial
        },
        'razao_social': {
            'type': 'object',
            'cleaning_function': None,
            'verification_function': None
        },
        'nome_fantasia': {
            'type': 'object',
            'cleaning_function': None,
            'verification_function': None
        },
        'situacao_cadastral': {
            'type': 'int64',
            'cleaning_function': None,
            'verification_function': cleaning_module.verification_functions.check_situacao_cadastral
        },
        'data_situacao_cadastral': {
            'type': 'object',
            'cleaning_function': cleaning.cleaning_functions.clear_data,
            'verification_function': cleaning_module.verification_functions.check_data
        },
        'motivo_situacao_cadastral': {
            'type': 'int64',
            'cleaning_function': cleaning.cleaning_functions.clear_motivo_situacao_cadastral,
            'verification_function': cleaning_module.verification_functions.check_motivo_situacao_cadastral
        },
        'codigo_natureza_juridica': {
            'type': 'object',
            'cleaning_function': cleaning.cleaning_functions.clear_codigo_natureza_juridica,
            'verification_function': None,
            'codes_file': 'cleaning_module/codes/nat_juridica.csv'
        },
        'data_inicio_atividade': {
            'type': 'object',
            'cleaning_function': cleaning.cleaning_functions.clear_data,
            'verification_function': cleaning_module.verification_functions.check_data
        },
        'cnae_fiscal': {
            'type': 'object',
            'cleaning_function': cleaning.cleaning_functions.clear_cnae_fiscal,
            'verification_function': None,
            'codes_file': 'cleaning_module/codes/cnae_fiscal.csv'
        },
        'cep': {
            'type': 'object',
            'cleaning_function': cleaning.cleaning_functions.clear_cep,
            'verification_function': cleaning_module.verification_functions.check_cep
        },
        'id_municipio_rf': {
            'type': 'object',
            'cleaning_function': cleaning.cleaning_functions.clear_id_municipio_rf,
            'verification_function': None,
            'codes_file': 'cleaning_module/codes/municipios_rf.csv'
        },
        'id_municipio': {
            'type': 'object',
            'cleaning_function': None,
            'verification_function': None,
            'codes_file': 'cleaning_module/codes/municipios.csv'
        },
        'qualificacao_do_responsavel': {
            'type': 'int64',
            'has_null_value': True,
            'cleaning_function': cleaning.cleaning_functions.clear_codigo_qualificacao,
            'verification_function': cleaning_module.verification_functions.check_codigo_qualificacao
        },
        'capital_social': {
            'type': 'float64',
            'has_null_value': True,
            'cleaning_function': None,
            'verification_function': cleaning_module.verification_functions.check_capital_social
        },
        'porte': {
            'type': 'int64',
            'has_null_value': True,
            'cleaning_function': None,
            'verification_function': cleaning_module.verification_functions.check_porte
        },
        'opcao_pelo_simples': {
            'type': 'int64',
            'has_null_value': True,
            'cleaning_function': None,
            'verification_function': cleaning_module.verification_functions.check_true_or_false
        },
        'data_opcao_pelo_simples': {
            'type': 'object',
            'cleaning_function': cleaning.cleaning_functions.clear_data,
            'verification_function': cleaning_module.verification_functions.check_data
        },
        'data_exclusao_do_simples': {
            'type': 'object',
            'cleaning_function': cleaning.cleaning_functions.clear_data,
            'verification_function': cleaning_module.verification_functions.check_data
        },
        'opcao_pelo_mei': {
            'type': 'int64',
            'has_null_value': True,
            'cleaning_function': None,
            'verification_function': cleaning_module.verification_functions.check_true_or_false
        },
        'sigla_uf': {
            'type': 'object',
            'cleaning_function': None,
            'verification_function': cleaning_module.verification_functions.check_sigla_uf
        },
    }

def get_columns_info_cnae_secundaria():
    return {
        'cnpj': {
            'type': 'object',
            'cleaning_function': None,
            'verification_function': cleaning_module.verification_functions.check_cnpj
        },
        'cnae': {
            'type': 'object',
            'cleaning_function': None,
            'verification_function': None,
            'codes_file': 'cleaning_module/codes/cnae.csv'
        }
    }
