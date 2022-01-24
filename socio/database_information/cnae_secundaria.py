import socio.verification.verification_functions as verification_functions

def get_columns_info_cnae_secundaria():
    return {
        'cnpj': {
            'type': 'object',
            'cleaning_function': None,
            'verification_function': verification_functions.check_cnpj
        },
        'cnae': {
            'type': 'object',
            'cleaning_function': None,
            'verification_function': None,
            'codes_file': 'socio/verification/codes/cnae.csv'
        }
    }