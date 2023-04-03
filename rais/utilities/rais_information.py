from rais.verification import verification_functions
from rais.extract import cleaning_functions


# Return extension of original rais files from specified year
def get_extension(year):
    if year <= 2010:
        return 'TXT'
    else:
        return 'txt'


# Return a list with all columns from clean rais files
def get_all_columns_rais():
    columns = get_columns_info_rais()
    column_list = [column for column in columns.keys()]
    return column_list


# Return name of some column in specified year
def get_column(column_name, year):
    columns_info = get_columns_info_rais()
    periods = columns_info[column_name]['campo']
    return get_info_period(year, periods)


def get_info_period(year, periods):
    for period in periods:
        (ini, end) = period
        if year >= ini and year <= end:
            return periods[period]
    return None


# Get information of columns from rais
def get_columns_info_rais():
    return {
        'id': {
            'tipo': 'int64',
            'tipo_limpo': 'Int64',
            'campo': {},
            'clean_function': {},
            'check_function': verification_functions.dummy
        },
        'ano_base': {
            'tipo': 'int64',
            'tipo_limpo': 'Int64',
            'campo': {},
            'clean_function': {},
            'check_function': verification_functions.dummy
        },
        'ano_nasc_r': {
            'tipo': 'int64',
            'tipo_limpo': 'Int64',
            'campo': {},
            'clean_function': {},
            'check_function': verification_functions.dummy
        },
        'mun_estbl': {
            'tipo': 'object',
            'tipo_limpo': "string",
            'campo': {
                (2002, 2010): 'MUNICIPIO',
                (2011, 2018): 'Município'
            },
            'clean_function': {},
            'check_function': verification_functions.check_mun_estbl
        },
        'cnae95': {
            'tipo': 'object',
            'tipo_limpo': "string",
            'campo': {
                (2002, 2009): 'CLAS CNAE 95',
                (2011, 2018): 'CNAE 95 Classe'
            },
            'clean_function': {},
            'check_function': verification_functions.check_cnae95
        },
        'vinculo_ativo': {
            'tipo': 'int64',
            'tipo_limpo': 'Int64',
            'campo': {
                (2002, 2010): 'EMP EM 31/12',
                (2011, 2018): 'Vínculo Ativo 31/12'
            },
            'clean_function': {},
            'check_function': verification_functions.check_zero_or_one
        },
        'vinculo_tipo': {
            'tipo': 'object',
            'tipo_limpo': 'Int64',
            'campo': {
                (2002, 2002): 'TP VINCL',
                (2003, 2010): 'TP VINCULO',
                (2011, 2018): 'Tipo Vínculo'
            },
            'clean_function': {
                (2002, 2002): cleaning_functions.get_vinculo_tipo
            },
            'check_function': verification_functions.check_vinculo_tipo
        },
        'deslig_motivo': {
            'tipo': 'int64',
            'tipo_limpo': 'Int64',
            'campo': {
                (2002, 2010): 'CAUSA DESLI',
                (2011, 2018): 'Motivo Desligamento'
            },
            'clean_function': {},
            'check_function': verification_functions.dummy
        },
        'deslig_mes': {
            'tipo': 'int64',
            'tipo_limpo': 'Int64',
            'campo': {
                (2002, 2010): 'MES DESLIG',
                (2011, 2018): 'Mês Desligamento'
            },
            'clean_function': {},
            'check_function': verification_functions.dummy
        },
        'admissao_tipo': {
            'tipo': 'int64',
            'tipo_limpo': 'Int64',
            'campo': {
                (2003, 2010): 'TIPO ADM',
                (2011, 2018): 'Tipo Admissão'
            },
            'clean_function': {},
            'check_function': verification_functions.check_admissao_tipo
        },
        'salario_tipo': {
            'tipo': 'int64',
            'tipo_limpo': 'Int64',
            'campo': {
                (2002, 2010): 'TIPO SAL',
                (2011, 2018): 'Tipo Salário'
            },
            'clean_function': {},
            'check_function': verification_functions.check_salario_tipo
        },
        'cbo94': {
            'tipo': 'object',
            'tipo_limpo': "string",
            'campo': {
                (2002, 2002): 'OCUPACAO',
                (2003, 2009): 'OCUPACAO 94',
                (2011, 2018): 'CBO 94 Ocupação'
            },
            'clean_function': {
                (2002, 2009): cleaning_functions.get_cbo_number,
                (2011, 2018): cleaning_functions.get_cbo
            },
            'check_function': verification_functions.check_cbo94
        },
        'escolaridade': {
            'tipo': 'int64',
            'tipo_limpo': 'Int64',
            'campo': {
                (2002, 2006): 'GRAU INSTR',
                (2007, 2010): 'GR INSTRUCAO',
                (2011, 2018): 'Escolaridade após 2005'
            },
            'clean_function': {},
            'check_function': verification_functions.check_escolaridade
        },
        'sexo_r': {
            'tipo': 'object',
            'tipo_limpo': 'Int64',
            'campo': {
                (2002, 2004): 'SEXO',
                (2005, 2010): 'GENERO',
                (2011, 2018): 'Sexo Trabalhador'
            },
            'clean_function': {
                (2005, 2010): cleaning_functions.get_sexo_word,
                (2011, 2018): cleaning_functions.get_sexo
            },
            'check_function': verification_functions.check_sexo
        },
        'pais_nacionalidade_r': {
            'tipo': 'int64',
            'tipo_limpo': 'Int64',
            'campo': {
                (2002, 2010): 'NACIONALIDAD',
                (2011, 2018): 'Nacionalidade'
            },
            'clean_function': {},
            'check_function': verification_functions.check_pais_nacionalidade
        },
        'raca_r': {
            'tipo': 'int64',
            'tipo_limpo': 'Int64',
            'campo': {
                (2003, 2010): 'RACA_COR',
                (2011, 2018): 'Raça Cor'
            },
            'clean_function': {
                (2003, 2018): cleaning_functions.get_raca
            },
            'check_function': verification_functions.check_raca
        },
        'ind_def': {
            'tipo': {
                (2002, 2006): 'int64',
                (2007, 2007): 'object',
                (2008, 2018): 'int64'
            },
            'tipo_limpo': 'Int64',
            'campo': {
                (2003, 2010): 'PORT DEFIC',
                (2011, 2018): 'Ind Portador Defic'
            },
            'clean_function': {},
            'check_function': verification_functions.check_zero_or_one
        },
        'estbl_tamanho': {
            'tipo': 'int64',
            'tipo_limpo': 'Int64',
            'campo': {
                (2002, 2010): 'TAMESTAB',
                (2011, 2018): 'Tamanho Estabelecimento'
            },
            'clean_function': {
                (2002, 2010): cleaning_functions.get_estbl_tamanho
            },
            'check_function': verification_functions.check_estbl_tamanho
        },
        'nat_juridica': {
            'tipo': 'object',
            'tipo_limpo': 'object',
            'campo': {
                (2002, 2007): 'NATUR JUR',
                (2008, 2010): 'NAT JURIDICA',
                (2011, 2018): 'Natureza Jurídica'
            },
            'clean_function': {},
            'check_function': verification_functions.check_nat_juridica
        },
        'ind_cei_vinc': {
            'tipo': 'object',
            'tipo_limpo': 'Int64',
            'campo': {
                (2002, 2010): 'IND CEI VINC',
                (2011, 2018): 'Ind CEI Vinculado'
            },
            'clean_function': {},
            'check_function': verification_functions.check_zero_or_one
        },
        'estbl_tipo': {
            'tipo': {
                (2002, 2006): 'int64',
                (2007, 2007): 'object',
                (2008, 2018): 'int64'
            },
            'tipo_limpo': 'Int64',
            'campo': {
                (2002, 2010): 'TIPO ESTBL',
                (2011, 2018): 'Tipo Estab'
            },
            'clean_function': {
                (2007, 2007): cleaning_functions.get_estbl_tipo
            },
            'check_function': verification_functions.check_estbl_tipo
        },
        'ind_estbl_pat': {
            'tipo': {
                (2002, 2006): 'int64',
                (2007, 2007): 'object',
                (2008, 2018): 'int64'
            },
            'tipo_limpo': 'Int64',
            'campo': {
                (2002, 2010): 'IND PAT',
                (2011, 2018): 'Ind Estab Participa PAT'
            },
            'clean_function': {},
            'check_function': verification_functions.check_zero_or_one
        },
        'estbl_simples': {
            'tipo': 'object',
            'tipo_limpo': 'Int64',
            'campo': {
                (2002, 2010): 'IND SIMPLES',
                (2011, 2018): 'Ind Simples'
            },
            'clean_function': {},
            'check_function': verification_functions.check_zero_or_one
        },
        'dta_admissao': {
            'tipo': 'object',
            'tipo_limpo': "string",
            'campo': {
                (2002, 2010): 'DT ADMISSAO',
                (2011, 2018): 'Data Admissão Declarada'
            },
            'clean_function': {
                (2002, 2010): cleaning_functions.get_dta_admissao,
                (2011, 2011): cleaning_functions.get_dta_admissao_valid
            },
            'check_function': verification_functions.check_date
        },
        'rem_media': {
            'tipo': 'object',
            'tipo_limpo': 'float64',
            'campo': {
                (2002, 2010): 'REM MED (R$)',
                (2011, 2018): 'Vl Remun Média Nom'
            },
            'clean_function': {
                (2002, 2018): cleaning_functions.get_float
            },
            'check_function': verification_functions.dummy
        },
        'rem_media_sm': {
            'tipo': 'object',
            'tipo_limpo': 'float64',
            'campo': {
                (2002, 2010): 'REM MEDIA',
                (2011, 2018): 'Vl Remun Média (SM)'
            },
            'clean_function': {
                (2002, 2018): cleaning_functions.get_float
            },
            'check_function': verification_functions.dummy
        },
        'rem_dez': {
            'tipo': 'object',
            'tipo_limpo': 'float64',
            'campo': {
                (2002, 2010): 'REM DEZ (R$)',
                (2011, 2018): 'Vl Remun Dezembro Nom'
            },
            'clean_function': {
                (2002, 2018): cleaning_functions.get_float
            },
            'check_function': verification_functions.dummy
        },
        'rem_dez_sm': {
            'tipo': 'object',
            'tipo_limpo': 'float64',
            'campo': {
                (2002, 2010): 'REM DEZEMBRO',
                (2011, 2018): 'Vl Remun Dezembro (SM)'
            },
            'clean_function': {
                (2002, 2018): cleaning_functions.get_float
            },
            'check_function': verification_functions.dummy
        },
        'vinculo_tempo': {
            'tipo': 'object',
            'tipo_limpo': 'float64',
            'campo': {
                (2002, 2010): 'TEMP EMPR',
                (2011, 2018): 'Tempo Emprego'
            },
            'clean_function': {
                (2002, 2018): cleaning_functions.get_float
            },
            'check_function': verification_functions.dummy
        },
        'horas_contr': {
            'tipo': {
                (2002, 2006): 'int64',
                (2007, 2007): 'object',
                (2008, 2018): 'int64'
            },
            'tipo_limpo': 'Int64',
            'campo': {
                (2002, 2010): 'HORAS CONTR',
                (2011, 2018): 'Qtd Hora Contr'
            },
            'clean_function': {
                (2007, 2007): cleaning_functions.get_horas_contr
            },
            'check_function': verification_functions.check_horas_contr
        },
        'rem_ultima': {
            'tipo': 'object',
            'tipo_limpo': 'float64',
            'campo': {
                (2002, 2010): 'ULT REM',
                (2011, 2018): 'Vl Última Remuneração Ano'
            },
            'clean_function': {
                (2002, 2018): cleaning_functions.get_float
            },
            'check_function': verification_functions.dummy
        },
        'sal_contr': {
            'tipo': 'object',
            'tipo_limpo': 'float64',
            'campo': {
                (2002, 2010): 'SAL CONTR',
                (2011, 2018): 'Vl Salário Contratual'
            },
            'clean_function': {
                (2002, 2018): cleaning_functions.get_float
            },
            'check_function': verification_functions.dummy
        },
        'pispasep': {
            'tipo': 'object',
            'tipo_limpo': 'object',
            'campo': {
                (2002, 2018): 'PIS'
            },
            'clean_function': {
                (2002, 2005): cleaning_functions.get_pispasep
            },
            'check_function': verification_functions.dummy #verification_functions.check_pispasep
        },
        'dta_nasc_r': {
            'tipo': 'object',
            'tipo_limpo': 'object',
            'campo': {
                (2002, 2010): 'DT NASCIMENT',
                (2014, 2018): 'Data de Nascimento',
            },
            'clean_function': {},
            'check_function': verification_functions.dummy#verification_functions.check_date
        },
        'ctps': {
            'tipo': 'object',
            'tipo_limpo': 'object',
            'campo': {
                (2002, 2002): 'NUM CTPS',
                (2003, 2010): 'NUME CTPS',
                (2011, 2018): 'Número CTPS'
            },
            'clean_function': {
                (2002, 2010): cleaning_functions.get_ctps,
                (2011, 2018): cleaning_functions.get_ctps_valid
            },
            'check_function': verification_functions.dummy#verification_functions.check_ctps
        },
        'cpf_r': {
            'tipo': 'object',
            'tipo_limpo': 'object',
            'campo': {
                (2002, 2018): 'CPF'
            },
            'clean_function': {},
            'check_function': verification_functions.dummy#verification_functions.check_cpf
        },
        'cei_vinc': {
            'tipo': 'object',
            'tipo_limpo': "string",
            'campo': {
                (2002, 2010): 'CEI VINC',
                (2011, 2018): 'CEI Vinculado'
            },
            'clean_function': {
                (2002, 2010): cleaning_functions.get_cei_vinc,
                (2011, 2013): cleaning_functions.get_cei_vinc_longer,
                (2014, 2018): cleaning_functions.get_cei_vinc_valid
            },
            'check_function': verification_functions.check_cei_vinc
        },
        'cnpj': {
            'tipo': 'object',
            'tipo_limpo': 'object',
            'campo': {
                (2002, 2010): 'IDENTIFICAD',
                (2011, 2018): 'CNPJ / CEI'
            },
            'clean_function': {
                (2002, 2010): cleaning_functions.get_cnpj
            },
            'check_function': verification_functions.check_cnpj
        },
        'cnpj_raiz': {
            'tipo': 'object',
            'tipo_limpo': 'object',
            'campo': {
                (2002, 2010): 'RADIC CNPJ',
                (2011, 2018): 'CNPJ Raiz'
            },
            'clean_function': {
                (2002, 2010): cleaning_functions.get_cnpj_raiz
            },
            'check_function': verification_functions.dummy
        },
        'cbo02': {
            'tipo': 'object',
            'tipo_limpo': "string",
            'campo': {
                (2003, 2010): 'OCUP 2002',
                (2011, 2018): 'CBO Ocupação 2002'
            },
            'clean_function': {
                (2003, 2010): cleaning_functions.get_cbo_number,
                (2011, 2018): cleaning_functions.get_cbo_valid
            },
            'check_function': verification_functions.check_cbo02
        },
        'cnae_20_classe': {
            'tipo': 'object',
            'tipo_limpo': "string",
            'campo': {
                (2006, 2009): 'CLAS CNAE 20',
                (2011, 2018): 'CNAE 2.0 Classe'
            },
            'clean_function': {
                (2006, 2008): cleaning_functions.get_cnae_20_classe
            },
            'check_function': verification_functions.check_cnae_20_classe
        },
        'cnae_20_subclasse': {
            'tipo': 'object',
            'tipo_limpo': "string",
            'campo': {
                (2006, 2010): 'SB CLAS 20',
                (2011, 2018): 'CNAE 2.0 Subclasse'
            },
            'clean_function': {
                (2006, 2008): cleaning_functions.get_cnae_20_subclasse
            },
            'check_function': verification_functions.check_cnae_20_subclasse
        },
        'afast1_causa': {
            'tipo': {
                (2002, 2006): 'int64',
                (2007, 2007): 'object',
                (2008, 2018): 'int64'
            },
            'tipo_limpo': 'Int64',
            'campo': {
                (2007, 2010): 'CAUS AFAST 1',
                (2011, 2018): 'Causa Afastamento 1'
            },
            'clean_function': {
                (2007, 2007): cleaning_functions.get_afast_causa_string,
                (2011, 2018): cleaning_functions.get_afast_causa
            },
            'check_function': verification_functions.check_afast_causa
        },
        'afast1_inic_dia': {
            'tipo': 'object',
            'tipo_limpo': 'Int64',
            'campo': {
                (2007, 2010): 'DIA INI AF 1',
                (2011, 2018): 'Dia Ini AF1'
            },
            'clean_function': {
                (2007, 2018): cleaning_functions.get_afast_dia
            },
            'check_function': verification_functions.check_dia
        },
        'afast1_inic_mes': {
            'tipo': {
                (2002, 2006): 'int64',
                (2007, 2007): 'object',
                (2008, 2018): 'int64'
            },
            'tipo_limpo': 'Int64',
            'campo': {
                (2007, 2010): 'MES INI AF 1',
                (2011, 2018): 'Mês Ini AF1'
            },
            'clean_function': {
                (2007, 2007): cleaning_functions.get_afast_mes_string,
                (2008, 2018): cleaning_functions.get_afast_mes
            },
            'check_function': verification_functions.check_mes
        },
        'afast1_fim_dia': {
            'tipo': 'object',
            'tipo_limpo': 'Int64',
            'campo': {
                (2007, 2010): 'DIA FIM AF 1',
                (2011, 2018): 'Dia Fim AF1'
            },
            'clean_function': {
                (2007, 2018): cleaning_functions.get_afast_dia
            },
            'check_function': verification_functions.check_dia
        },
        'afast1_fim_mes': {
            'tipo': {
                (2002, 2006): 'int64',
                (2007, 2007): 'object',
                (2008, 2018): 'Int64'
            },
            'tipo_limpo': 'Int64',
            'campo': {
                (2007, 2010): 'MES FIM AF 1',
                (2011, 2018): 'Mês Fim AF1'
            },
            'clean_function': {
                (2007, 2007): cleaning_functions.get_afast_mes_string,
                (2008, 2018): cleaning_functions.get_afast_mes
            },
            'check_function': verification_functions.check_mes
        },
        'afast2_causa': {
            'tipo': {
                (2002, 2006): 'int64',
                (2007, 2007): 'object',
                (2008, 2018): 'int64'
            },
            'tipo_limpo': 'Int64',
            'campo': {
                (2007, 2010): 'CAUS AFAST 2',
                (2011, 2018): 'Causa Afastamento 2'
            },
            'clean_function': {
                (2007, 2007): cleaning_functions.get_afast_causa_string,
                (2011, 2018): cleaning_functions.get_afast_causa
            },
            'check_function': verification_functions.check_afast_causa
        },
        'afast2_inic_dia': {
            'tipo': 'object',
            'tipo_limpo': 'Int64',
            'campo': {
                (2007, 2010): 'DIA INI AF 2',
                (2011, 2018): 'Dia Ini AF2'
            },
            'clean_function': {
                (2007, 2018): cleaning_functions.get_afast_dia
            },
            'check_function': verification_functions.check_dia
        },
        'afast2_inic_mes': {
            'tipo': {
                (2002, 2006): 'int64',
                (2007, 2007): 'object',
                (2008, 2018): 'int64'
            },
            'tipo_limpo': 'Int64',
            'campo': {
                (2007, 2010): 'MES INI AF 2',
                (2011, 2018): 'Mês Ini AF2'
            },
            'clean_function': {
                (2007, 2007): cleaning_functions.get_afast_mes_string,
                (2008, 2018): cleaning_functions.get_afast_mes
            },
            'check_function': verification_functions.check_mes
        },
        'afast2_fim_dia': {
            'tipo': 'object',
            'tipo_limpo': 'Int64',
            'campo': {
                (2007, 2010): 'DIA FIM AF 2',
                (2011, 2018): 'Dia Fim AF2'
            },
            'clean_function': {
                (2007, 2018): cleaning_functions.get_afast_dia
            },
            'check_function': verification_functions.check_dia
        },
        'afast2_fim_mes': {
            'tipo': {
                (2002, 2006): 'int64',
                (2007, 2007): 'object',
                (2008, 2018): 'int64'
            },
            'tipo_limpo': 'Int64',
            'campo': {
                (2007, 2010): 'MES FIM AF 2',
                (2011, 2018): 'Mês Fim AF2'
            },
            'clean_function': {
                (2007, 2007): cleaning_functions.get_afast_mes_string,
                (2008, 2018): cleaning_functions.get_afast_mes
            },
            'check_function': verification_functions.check_mes
        },
        'afast3_causa': {
            'tipo': {
                (2002, 2006): 'int64',
                (2007, 2007): 'object',
                (2008, 2018): 'int64'
            },
            'tipo_limpo': 'Int64',
            'campo': {
                (2007, 2010): 'CAUS AFAST 3',
                (2011, 2018): 'Causa Afastamento 3'
            },
            'clean_function': {
                (2007, 2007): cleaning_functions.get_afast_causa_string,
                (2011, 2018): cleaning_functions.get_afast_causa
            },
            'check_function': verification_functions.check_afast_causa
        },
        'afast3_inic_dia': {
            'tipo': 'object',
            'tipo_limpo': 'Int64',
            'campo': {
                (2007, 2010): 'DIA INI AF 3',
                (2011, 2018): 'Dia Ini AF3'
            },
            'clean_function': {
                (2007, 2018): cleaning_functions.get_afast_dia
            },
            'check_function': verification_functions.check_dia
        },
        'afast3_inic_mes': {
            'tipo': {
                (2002, 2006): 'int64',
                (2007, 2007): 'object',
                (2008, 2018): 'int64'
            },
            'tipo_limpo': 'Int64',
            'campo': {
                (2007, 2010): 'MES INI AF 3',
                (2011, 2018): 'Mês Ini AF3'
            },
            'clean_function': {
                (2007, 2007): cleaning_functions.get_afast_mes_string,
                (2008, 2018): cleaning_functions.get_afast_mes
            },
            'check_function': verification_functions.check_mes
        },
        'afast3_fim_dia': {
            'tipo': 'object',
            'tipo_limpo': 'Int64',
            'campo': {
                (2007, 2010): 'DIA FIM AF 3',
                (2011, 2018): 'Dia Fim AF3'
            },
            'clean_function': {
                (2007, 2018): cleaning_functions.get_afast_dia
            },
            'check_function': verification_functions.check_dia
        },
        'afast3_fim_mes': {
            'tipo': {
                (2002, 2006): 'int64',
                (2007, 2007): 'object',
                (2008, 2018): 'int64'
            },
            'tipo_limpo': 'Int64',
            'campo': {
                (2007, 2010): 'MES FIM AF 3',
                (2011, 2018): 'Mês Fim AF3'
            },
            'clean_function': {
                (2007, 2007): cleaning_functions.get_afast_mes_string,
                (2008, 2018): cleaning_functions.get_afast_mes
            },
            'check_function': verification_functions.check_mes
        },
        'afast_dias_total': {
            'tipo': {
                (2002, 2006): 'int64',
                (2007, 2007): 'object',
                (2008, 2018): 'int64'
            },
            'tipo_limpo': 'Int64',
            'campo': {
                (2007, 2010): 'QT DIAS AFAS',
                (2011, 2018): 'Qtd Dias Afastamento'
            },
            'clean_function': {
                (2007, 2007): cleaning_functions.get_afast_dias_total,
                (2011, 2011): cleaning_functions.get_afast_dias_total_valid
            },
            'check_function': verification_functions.check_afast_dias_total
        },
        'idade': {
            'tipo': 'int64',
            'tipo_limpo': 'Int64',
            'campo': {
                (2011, 2018): 'Idade'
            },
            'clean_function': {
                (2011, 2011): cleaning_functions.get_idade
            },
            'check_function': verification_functions.check_idade
        },
        'deslig_dia': {
            'tipo': 'object',
            'tipo_limpo': 'Int64',
            'campo': {
                (2003, 2010): 'DIA DESL',
                (2014, 2018): 'Dia de Desligamento'
            },
            'clean_function': {
                (2004, 2010): cleaning_functions.get_deslig_dia,
                (2014, 2018): cleaning_functions.get_deslig_dia
            },
            'check_function': verification_functions.dummy
        },
        'ibge_subsetor': {
            'tipo': 'int64',
            'tipo_limpo': 'Int64',
            'campo': {
                (2015, 2018): 'IBGE Subsetor'
            },
            'clean_function': {},
            'check_function': verification_functions.check_ibge_subsetor
        },
        'estbl_cep': {
            'tipo': 'object',
            'tipo_limpo': "string",
            'campo': {
                (2015, 2018): 'CEP Estab'
            },
            'clean_function': {},
            'check_function': verification_functions.check_estbl_cep
        },
        'mun_trab': {
            'tipo': 'object',
            'tipo_limpo': "string",
            'campo': {
                (2015, 2018): 'Mun Trab'
            },
            'clean_function': {
                (2017, 2018): cleaning_functions.get_mun
            },
            'check_function': verification_functions.check_mun_estbl
        },
        'razao_social': {
            'tipo': 'object',
            'tipo_limpo': 'object',
            'campo': {
                (2015, 2018): 'Razão Social'
            },
            'clean_function': {
                (2015, 2018): cleaning_functions.get_razao_social
            },
            'check_function': verification_functions.check_razao_social
        },
        'rem_jan': {
            'tipo': 'object',
            'tipo_limpo': 'float64',
            'campo': {
                (2015, 2018): 'Vl Rem Janeiro CC'
            },
            'clean_function': {
                (2015, 2018): cleaning_functions.get_float
            },
            'check_function': verification_functions.dummy
        },
        'rem_fev': {
            'tipo': 'object',
            'tipo_limpo': 'float64',
            'campo': {
                (2015, 2018): 'Vl Rem Fevereiro CC'
            },
            'clean_function': {
                (2015, 2018): cleaning_functions.get_float
            },
            'check_function': verification_functions.dummy
        },
        'rem_mar': {
            'tipo': 'object',
            'tipo_limpo': 'float64',
            'campo': {
                (2015, 2018): 'Vl Rem Março CC'
            },
            'clean_function': {
                (2015, 2018): cleaning_functions.get_float
            },
            'check_function': verification_functions.dummy
        },
        'rem_abr': {
            'tipo': 'object',
            'tipo_limpo': 'float64',
            'campo': {
                (2015, 2018): 'Vl Rem Abril CC'
            },
            'clean_function': {
                (2015, 2018): cleaning_functions.get_float
            },
            'check_function': verification_functions.dummy
        },
        'rem_mai': {
            'tipo': 'object',
            'tipo_limpo': 'float64',
            'campo': {
                (2015, 2018): 'Vl Rem Maio CC'
            },
            'clean_function': {
                (2015, 2018): cleaning_functions.get_float
            },
            'check_function': verification_functions.dummy
        },
        'rem_jun': {
            'tipo': 'object',
            'tipo_limpo': 'float64',
            'campo': {
                (2015, 2018): 'Vl Rem Junho CC'
            },
            'clean_function': {
                (2015, 2018): cleaning_functions.get_float
            },
            'check_function': verification_functions.dummy
        },
        'rem_jul': {
            'tipo': 'object',
            'tipo_limpo': 'float64',
            'campo': {
                (2015, 2018): 'Vl Rem Julho CC'
            },
            'clean_function': {
                (2015, 2018): cleaning_functions.get_float
            },
            'check_function': verification_functions.dummy
        },
        'rem_ago': {
            'tipo': 'object',
            'tipo_limpo': 'float64',
            'campo': {
                (2015, 2018): 'Vl Rem Agosto CC'
            },
            'clean_function': {
                (2015, 2018): cleaning_functions.get_float
            },
            'check_function': verification_functions.dummy
        },
        'rem_set': {
            'tipo': 'object',
            'tipo_limpo': 'float64',
            'campo': {
                (2015, 2018): 'Vl Rem Setembro CC'
            },
            'clean_function': {
                (2015, 2018): cleaning_functions.get_float
            },
            'check_function': verification_functions.dummy
        },
        'rem_out': {
            'tipo': 'object',
            'tipo_limpo': 'float64',
            'campo': {
                (2015, 2018): 'Vl Rem Outubro CC'
            },
            'clean_function': {
                (2015, 2018): cleaning_functions.get_float
            },
            'check_function': verification_functions.dummy
        },
        'rem_nov': {
            'tipo': 'object',
            'tipo_limpo': 'float64',
            'campo': {
                (2015, 2018): 'Vl Rem Novembro CC'
            },
            'clean_function': {
                (2015, 2018): cleaning_functions.get_float
            },
            'check_function': verification_functions.dummy
        },
        'trab_interm': {
            'tipo': 'int64',
            'tipo_limpo': 'Int64',
            'campo': {
                (2017, 2018): 'Ind Trab Intermitente'
            },
            'clean_function': {},
            'check_function': verification_functions.check_zero_or_one
        },
        'trab_parcial': {
            'tipo': 'int64',
            'tipo_limpo': 'Int64',
            'campo': {
                (2017, 2018): 'Ind Trab Parcial'
            },
            'clean_function': {},
            'check_function': verification_functions.check_zero_or_one
        },
        'ind_sindical': {
            'tipo': 'int64',
            'tipo_limpo': 'Int64',
            'campo': {
                (2017, 2017): 'Ind Sindical'
            },
            'clean_function': {},
            'check_function': verification_functions.check_zero_or_one
        },
        'nome_r': {
            'tipo': 'object',
            'tipo_limpo': 'object',
            'campo': {
                (2002, 2010): 'NOME',
                (2011, 2018): 'Nome Trabalhador',
            },
            'clean_function': {},
            'check_function': verification_functions.dummy#verification_functions.check_name
        }
    }
