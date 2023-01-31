import socio.cleaning.cleaning_functions as cleaning_functions
import socio.verification.verification_functions as verification_functions


def get_columns_info_estabelecimento():
    return {
        "cnpj_basico": {
            "type": str,
            "cleaning_function": None

        },
        "cnpj_ordem": {
            "type": str,
            "cleaning_function": None

        },
        "cnpj_dv": {
            "type": str,
            "cleaning_function": None

        },
        "identificador_matriz_filial": {
            "type": 'Int64',
            "cleaning_function": None

        },
        "nome_fantasia": {
            "type": str,
            "cleaning_function": cleaning_functions.clear_nome

        },
        "situacao_cadastral": {
            "type": 'Int64',
            "cleaning_function": None

        },
        "data_situacao_cadastral": {
            "type": str,
            "cleaning_function": None

        },
        "motivo_situacao_cadastral": {
            "type": 'Int64',
            "cleaning_function": None

        },
        "nome_cidade_exterior": {
            "type": str,
            "cleaning_function": None

        },
        "pais": {
            "type": str,
            "cleaning_function": None

        },
        "data_inicio_atividade": {
            "type": str,
            "cleaning_function": None

        },
        "cnae_fiscal": {
            "type": str,
            "cleaning_function": None

        },
        "cnae_fiscal_secundaria": {
            "type": str,
            "cleaning_function": None

        },
        "descricao_tipo_logradouro": {
            "type": str,
            "cleaning_function": cleaning_functions.clear_nome

        },
        "logradouro": {
            "type": str,
            "cleaning_function": cleaning_functions.clear_nome

        },
        "numero": {
            "type": str,
            "cleaning_function": None

        },
        "complemento": {
            "type": str,
            "cleaning_function": cleaning_functions.clear_nome

        },
        "bairro": {
            "type": str,
            "cleaning_function": cleaning_functions.clear_nome

        },
        "cep": {
            "type": str,
            "cleaning_function": None

        },
        "uf": {
            "type": str,
            "cleaning_function": None

        },
        "codigo_municipio": {
            "type": 'Int64',
            "cleaning_function": None

        },
        "ddd_telefone_1": {
            "type": str,
            "cleaning_function": None

        },
        "num_telefone_1": {
            "type": str,
            "cleaning_function": None

        },
        "ddd_telefone_2": {
            "type": str,
            "cleaning_function": None

        },
        "num_telefone_2": {
            "type": str,
            "cleaning_function": None

        },
        "ddd_fax": {
            "type": str,
            "cleaning_function": None

        },
        "num_fax": {
            "type": str,
            "cleaning_function": None

        },
        "correio_eletronico": {
            "type": str,
            "cleaning_function": None

        },
        "situacao_especial": {
            "type": str,
            "cleaning_function": None

        },
        "data_situacao_especial": {
            "type": str,
            "cleaning_function": None

        }
    }