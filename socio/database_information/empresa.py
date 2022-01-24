import socio.cleaning.cleaning_functions as cleaning_functions
import socio.verification.verification_functions as verification_functions

def get_columns_info_empresa():
    return {
        'cnpj': {
            'type': 'object',
            'cleaning_function': None,
            'verification_function': verification_functions.check_cnpj
        },
        'identificador_matriz_filial': {
            'type': 'int64',
            'cleaning_function': None,
            'verification_function': verification_functions.check_identificador_matriz_filial
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
            'verification_function': verification_functions.check_situacao_cadastral
        },
        'data_situacao_cadastral': {
            'type': 'object',
            'cleaning_function': cleaning_functions.clear_data,
            'verification_function': verification_functions.check_data
        },
        'motivo_situacao_cadastral': {
            'type': 'int64',
            'cleaning_function': cleaning_functions.clear_motivo_situacao_cadastral,
            'verification_function': verification_functions.check_motivo_situacao_cadastral
        },
        'codigo_natureza_juridica': {
            'type': 'object',
            'cleaning_function': cleaning_functions.clear_codigo_natureza_juridica,
            'verification_function': None,
            'codes_file': 'socio/verification/codes/nat_juridica.csv'
        },
        'data_inicio_atividade': {
            'type': 'object',
            'cleaning_function': cleaning_functions.clear_data,
            'verification_function': verification_functions.check_data
        },
        'cnae_fiscal': {
            'type': 'object',
            'cleaning_function': cleaning_functions.clear_cnae_fiscal,
            'verification_function': None,
            'codes_file': 'socio/verification/codes/cnae_fiscal.csv'
        },
        'cep': {
            'type': 'object',
            'cleaning_function': cleaning_functions.clear_cep,
            'verification_function': verification_functions.check_cep
        },
        'id_municipio_rf': {
            'type': 'object',
            'cleaning_function': cleaning_functions.clear_id_municipio_rf,
            'verification_function': None,
            'codes_file': 'socio/verification/codes/municipios_rf.csv'
        },
        'id_municipio': {
            'type': 'object',
            'cleaning_function': None,
            'verification_function': None,
            'codes_file': 'socio/verification/codes/municipios.csv'
        },
        'qualificacao_do_responsavel': {
            'type': 'int64',
            'has_null_value': True,
            'cleaning_function': cleaning_functions.clear_codigo_qualificacao,
            'verification_function': verification_functions.check_codigo_qualificacao
        },
        'capital_social': {
            'type': 'float64',
            'has_null_value': True,
            'cleaning_function': None,
            'verification_function': verification_functions.check_capital_social
        },
        'porte': {
            'type': 'int64',
            'has_null_value': True,
            'cleaning_function': None,
            'verification_function': verification_functions.check_porte
        },
        'opcao_pelo_simples': {
            'type': 'int64',
            'has_null_value': True,
            'cleaning_function': None,
            'verification_function': verification_functions.check_true_or_false
        },
        'data_opcao_pelo_simples': {
            'type': 'object',
            'cleaning_function': cleaning_functions.clear_data,
            'verification_function': verification_functions.check_data
        },
        'data_exclusao_do_simples': {
            'type': 'object',
            'cleaning_function': cleaning_functions.clear_data,
            'verification_function': verification_functions.check_data
        },
        'opcao_pelo_mei': {
            'type': 'int64',
            'has_null_value': True,
            'cleaning_function': None,
            'verification_function': verification_functions.check_true_or_false
        },
        'sigla_uf': {
            'type': 'object',
            'cleaning_function': None,
            'verification_function': verification_functions.check_sigla_uf
        },
    }