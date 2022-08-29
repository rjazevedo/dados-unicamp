import socio.cleaning.cleaning_functions as cleaning_functions
import socio.verification.verification_functions as verification_functions

def get_columns_info_socio():
    return {
        'cnpj': {
            'type': str,
            'campo': {},
            'available_dates': ['2022-03-12', '2019-08-14', '2019-11-20', '2019-06-10', '2019-04-05', '2018-11-08'],
            'cleaning_function': cleaning_functions.clean_cnpj,
            'verification_function': verification_functions.check_cnpj,
            'has_different_formats': False
        },
        'razao_social': {
            'type': str,
            'campo': {},
            'available_dates': [],
            'cleaning_function' : None,
            'verification_function' : None,
            'has_different_formats': False
        },
        'identificador_de_socio': {
            'type': 'Int64',
            'campo': {},
            'available_dates': ['2022-03-12', '2019-08-14', '2019-11-20', '2019-06-10', '2019-04-05', '2018-11-08'],
            'cleaning_function': None,
            'verification_function': verification_functions.check_identificador_de_socio,
            'ferent_formats': False
        },
        'nome_socio': {
            'type': str,
            'campo': {},
            'available_dates': ['2022-03-12', '2019-08-14', '2019-11-20', '2019-06-10', '2019-04-05', '2018-11-08'],
            'cleaning_function': cleaning_functions.clear_nome,
            'verification_function': None,
            'ferent_formats': False
        },
        'cnpj_cpf_do_socio': {
            'type': str,
            'campo': {},
            'available_dates': ['2022-03-12', '2019-08-14', '2019-11-20', '2019-06-10', '2019-04-05', '2018-11-08'],
            'cleaning_function': cleaning_functions.clear_cnpj_cpf,
            'verification_function': verification_functions.check_cnpj_cpf_do_socio,
            'ferent_formats': False
        },
        'codigo_qualificacao_socio': {
            'type': 'Int64',
            'campo': {},
            'available_dates': ['2022-03-12', '2019-08-14', '2019-11-20', '2019-06-10', '2019-04-05', '2018-11-08'],
            'cleaning_function': cleaning_functions.clear_codigo_qualificacao,
            'verification_function': verification_functions.check_codigo_qualificacao,
            'ferent_formats': False
        },
        'codigo_tipo_socio': {
            'type': 'Int64',
            'campo': {},
            'available_dates': [],
            'cleaning_function' : None,
            'verification_function' : None,
            'ferent_formats': False
        },
        'tipo_socio': {
            'type': str,
            'campo': {},
            'available_dates': [],
            'cleaning_function' : None,
            'verification_function' : None,
            'ferent_formats': False
        },
        'qualificacao_socio': {
            'type': str,
            'campo': {},
            'available_dates': [],
            'cleaning_function' : None,
            'verification_function' : None,
            'ferent_formats': False
        },
        'data_entrada_sociedade': {
            'type': str,
            'campo': {},
            'available_dates': ['2022-03-12', '2019-08-14', '2019-11-20', '2019-06-10', '2019-04-05', '2018-11-08'],
            'cleaning_function': cleaning_functions.clear_data,
            'verification_function': verification_functions.check_data,
            'ferent_formats': True
        },
        'ano_entrada_sociedade': {
            'type': 'Int64',
            'campo': {},
            'available_dates': [],
            'cleaning_function': None,
            'verification_function': None,
            'ferent_formats': False
        },
        'cpf_representante_legal': {
            'type': str,
            'campo': {},
            'available_dates': ['2022-03-12', '2019-08-14', '2019-11-20', '2019-06-10', '2019-04-05', '2018-11-08'],
            'cleaning_function': None, #cleaning_functions.clear_cpf,
            'verification_function': None, #verification_functions.check_cpf,
            'ferent_formats': False
        },
        'nome_representante_legal': {
            'type': str,
            'campo': {},
            'available_dates': ['2022-03-12', '2019-08-14', '2019-11-20', '2019-06-10', '2019-04-05', '2018-11-08'],
            'cleaning_function': None,
            'verification_function': None, #verification_functions.check_name,
            'ferent_formats': False
        },
        'codigo_qualificacao_representante_legal': {
            'type': 'Int64',
            'campo': {},
            'available_dates': ['2022-03-12', '2019-08-14', '2019-11-20', '2019-06-10', '2019-04-05', '2018-11-08'],
            'cleaning_function': None, #cleaning_functions.clear_codigo_qualificacao,
            'verification_function': None, #verification_functions.check_codigo_qualificacao,
            'ferent_formats': False
        },
        'faixa_etaria': {
            'type': 'Int64',
            'campo': {},
            'available_dates': ['2022-03-12'],
            'cleaning_function': None,
            'verification_function': None,
            'ferent_formats': False
        },
        'pais': {
            'type': 'Int64',
            'campo': {},
            'available_dates': ['2022-03-12'],
            'cleaning_function': None,
            'verification_function': None,
            'ferent_formats': False
        },
        'data_coleta': {
            'type': str,
            'campo': {},
            'available_dates': [],
            'cleaning_function': None,
            'verification_function': None,
            'ferent_formats': False

        }

    }