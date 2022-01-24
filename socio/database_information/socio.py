import socio.cleaning.cleaning_functions as cleaning_functions
import socio.verification.verification_functions as verification_functions

def get_columns_info_socio():
    return {
        'cnpj': {
            'type': 'object',
            'cleaning_function': None,
            'verification_function': verification_functions.check_cnpj
        },
        'identificador_de_socio': {
            'type': 'int64',
            'cleaning_function': None,
            'verification_function': verification_functions.check_identificador_de_socio
        },
        'nome_socio': {
            'type': 'object',
            'cleaning_function': cleaning_functions.clear_nome,
            'verification_function': None
        },
        'cnpj_cpf_do_socio': {
            'type': 'object',
            'cleaning_function': cleaning_functions.clear_cnpj_cpf,
            'verification_function': verification_functions.check_cnpj_cpf_do_socio
        },
        'codigo_qualificacao_socio': {
            'type': 'int64',
            'cleaning_function': cleaning_functions.clear_codigo_qualificacao,
            'verification_function': verification_functions.check_codigo_qualificacao
        },
        'data_entrada_sociedade': {
            'type': 'object',
            'cleaning_function': cleaning_functions.clear_data,
            'verification_function': verification_functions.check_data
        },
        'ano_entrada_sociedade': {
            'type': 'int64',
            'cleaning_function': None,
            'verification_function': None
        },
        'cpf_representante_legal': {
            'type': 'object',
            'cleaning_function': cleaning_functions.clear_cpf,
            'verification_function': verification_functions.check_cpf
        },
        'nome_representante_legal': {
            'type': 'object',
            'cleaning_function': None,
            'verification_function': verification_functions.check_name
        },
        'codigo_qual_representante_legal': {
            'type': 'int64',
            'has_null_value': True,
            'cleaning_function': cleaning_functions.clear_codigo_qualificacao,
            'verification_function': verification_functions.check_codigo_qualificacao
        }
    }