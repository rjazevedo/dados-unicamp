import verification.verification_functions

def get_columns_info_cnae_secundaria():
    return {
        'cnpj': {
            'type': 'object',
            'cleaning_function': None,
            'verification_function': verification.verification_functions.check_cnpj
        },
        'cnae': {
            'type': 'object',
            'cleaning_function': None,
            'verification_function': None,
            'codes_file': 'verification/codes/cnae.csv'
        }
    }