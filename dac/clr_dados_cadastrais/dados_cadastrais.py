from dac.utilities.io import read_from_database
from dac.utilities.io import read_result
from dac.utilities.io import write_output
from dac.utilities.io import write_result
from dac.utilities.io import read_from_external
from dac.utilities.io import read_csv_from_database
from dac.utilities.columns import dados_cadastrais_cols
from dac.utilities.columns import dados_cadastrais_final_cols
from dac.utilities.format import str_to_upper_ascii
from dac.utilities.format import padronize_sex
from dac.utilities.format import padronize_race
from dac.utilities.format import padronize_dates
from dac.utilities.format import padronize_marstat
from dac.utilities.format import fill_doc
from dac.utilities.format import dates_to_year
from dac.utilities.format import padronize_string_miss
from dac.utilities.format import padronize_int_miss
from dac.utilities.dtypes import dtypes_dados_cadastrais
import pandas as pd
import numpy as np

drop_cols = ['nome_mae', 'nome_pai', 'idade_atual', 
        'tipo_doc', 'dt_emissao_doc', 'orgao_emissor_doc', 'uf_emissor_doc', 'doc_tratado']

PRE_99_BASE_NAME = 'Rodolfo_Complementacao.xlsx'
POS_99_BASE_NAME = 'DadosCadastraisAluno.xlsx'
DADOS_SHEET_NAME = 'Dados Cadastrais'

RESULT_NAME = 'dados_cadastrais.csv'
UF_CODE_NAME = 'final_counties.csv'
SCHOOL_CODES = "escola_codigo_inep.csv"

def generate_clean_data():
    dados_cadastrais = load_dados_cadastais()
    
    dados_cadastrais.drop(drop_cols, axis=1, inplace=True)
    unicode_cols = ['nome', 'mun_atual', 'mun_resid_d', 'mun_esc_form_em', 'tipo_esc_form_em', 
    'raca_descricao', 'mun_nasc_d', 'pais_nasc_d', 'nacionalidade_d', 'pais_nac_d', 'naturalizado',
    'escola_em_d','pais_esc_form_em'] 
    
    dados_cadastrais.cpf = fill_doc(dados_cadastrais.cpf, 11)
    dados_cadastrais.doc = fill_doc(dados_cadastrais.doc, 15)
    
    for column in dados_cadastrais.columns:
        if 'cep' in column:
                dados_cadastrais[column] = fill_doc(dados_cadastrais[column], 8)
    
    str_to_upper_ascii(dados_cadastrais, unicode_cols)
    padronize_sex(dados_cadastrais, 'sexo_d')
    padronize_race(dados_cadastrais, 'raca_d')
    padronize_marstat(dados_cadastrais, 'est_civil_d')
    padronize_dates(dados_cadastrais, ['dta_nasc'])
    dates_to_year(dados_cadastrais, 'ano_conclu_em')

    dados_cadastrais.tipo_esc_form_em = dados_cadastrais.tipo_esc_form_em.str[7:]
    dados_cadastrais.insert(
            loc=dados_cadastrais.columns.get_loc('dta_nasc')+1, 
            column='ano_nasc_d', 
            value=dados_cadastrais['dta_nasc'].map(lambda date: date[-4:])
            )
    
    padronize_string_miss(dados_cadastrais, ['cpf', 'cep_nasc', 'cep_escola_em', 'cep_atual', 'cep_resid_d', 'tipo_esc_form_em'], '-')
    padronize_int_miss(dados_cadastrais, ['ano_conclu_em'], 0)

    dados_cadastrais.drop_duplicates(subset=['identif'], keep='last', inplace=True)
    dados_with_code = generate_uf_code(dados_cadastrais)
    dados_with_school_code = generate_school_codes(dados_with_code)
    write_result(dados_with_school_code, RESULT_NAME)


def load_dados_cadastais():
    dados_cadastrais_pre_99 = read_from_database(PRE_99_BASE_NAME, sheet_name=DADOS_SHEET_NAME, names=dados_cadastrais_cols)
    dados_cadastrais_pos_99 = read_from_database(POS_99_BASE_NAME, names=dados_cadastrais_cols)

    dados_cadastrais = pd.concat([dados_cadastrais_pre_99, dados_cadastrais_pos_99])
    dados_cadastrais = clear_dados_cadastrais_pre_99(dados_cadastrais)
    return dados_cadastrais


# Limpa erros na tabela pré 99 vistos empiricamente
def clear_dados_cadastrais_pre_99(df):
    ceps_colums = ['cep_nasc', 'cep_resid_d', 'cep_escola_em', 'cep_atual']
    null_colums = ['uf_nasc_d', 'escola_em_d', 'uf_esc_form_em', 'mun_esc_form_em', 'sigla_pais_esc_form_em', 'pais_esc_form_em', 'naturalizado', 'mun_atual', 'mun_resid_d','cep_nasc', 'cep_resid_d', 'cep_escola_em', 'cep_atual']
    padronize_string_miss(df, [null_colums], '<null>')
    df[ceps_colums] = df[ceps_colums].replace('',np.nan).astype(float)

    df['dta_nasc'] = df['dta_nasc'].astype(str)
    df['dta_nasc'] = pd.to_datetime(df['dta_nasc'], errors='coerce', format= '%Y-%m-%d')
    df['ano_conclu_em'] = df['ano_conclu_em'].astype(str)
    df['ano_conclu_em'] = pd.to_datetime(df['ano_conclu_em'], errors='coerce', format= '%Y-%m-%d')
    return df


# Atribui os códigos das ufs presentes na tabela
def generate_uf_code(dados_cadastrais):
    final_counties = read_result(UF_CODE_NAME)

    final_counties = final_counties[['municipio', 'uf', 'codigo_municipio', 'confianca', 'municipio_ibge', 'uf_ibge']]
    final_counties = final_counties.drop_duplicates(['municipio', 'uf'])

    final_counties.columns = ['mun_nasc_d', 'uf_nasc_d', 'cod_mun_nasc_d', 'origem_cod_mun_nasc_d', 'mun_nasc_ibge', 'uf_nasc_ibge']
    mun_nasc_d_merge = pd.merge(dados_cadastrais, final_counties, how='left')

    final_counties.columns = ['mun_esc_form_em', 'uf_esc_form_em', 'cod_mun_form_em', 'origem_cod_mun_form_em', 'mun_esc_form_em_ibge', 'uf_esc_form_em_ibge']
    mun_nasc_d_merge = pd.merge(mun_nasc_d_merge, final_counties, how='left')
    
    mun_nasc_d_merge = mun_nasc_d_merge.reindex(columns= dados_cadastrais_final_cols)
    return mun_nasc_d_merge


# Atribui códigos das escolas 
def generate_school_codes(dados_cadastrais):
    code_schools = read_csv_from_database(SCHOOL_CODES).loc[:, ["escola_base", "Código INEP", "escola_inep", "codigo_municipio"]]
    code_schools = code_schools.drop_duplicates(subset=["escola_base", "codigo_municipio"])

    code_schools.columns = ["escola_em_d", "cod_escola_em_inep", "escola_em_inep", "cod_mun_form_em"]
    result = pd.merge(dados_cadastrais, code_schools, how="left", on=["escola_em_d", "cod_mun_form_em"])
    return result