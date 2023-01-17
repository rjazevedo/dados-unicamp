from dac.utilities.io import read_result
from dac.utilities.io import write_output
from dac.utilities.io import write_result
from dac.utilities.io import Bases
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

DADOS_CADASTRAIS = "dados_cadastrais_intermediario.csv"
UF_CODE_NAME = 'final_counties.csv'
SCHOOL_CODES = "escola_codigo_inep.csv"
ID_NAMES = "ids_of_names.csv"
RESULT_NAME = 'dados_cadastrais.csv'

def generate_clean_data():
    dados_cadastrais = read_result("dados_cadastrais_intermediario.csv")
    dados_cadastrais = generate_id_names(dados_cadastrais)
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
    code_schools = read_result(SCHOOL_CODES).loc[:, ["escola_base", "Código INEP", "escola_inep", "codigo_municipio"]]
    code_schools.columns = ["escola_em_d", "cod_escola_em_inep", "escola_em_inep", "cod_mun_form_em"]
    result = pd.merge(dados_cadastrais, code_schools, how="left", on=["escola_em_d", "cod_mun_form_em"])
    return result


# Atribui ids dos nomes  
def generate_id_names(dados_cadastrais):
    id_names = read_result(ID_NAMES)

    dados_cadastrais = pd.merge(dados_cadastrais, id_names, how="left", on = ["nome"])
    dados_cadastrais.rename(columns = {"id": "nome_id"}, inplace=True)
    id_names.rename(columns = {"nome": "nome_pai"}, inplace = True)

    dados_cadastrais = pd.merge(dados_cadastrais, id_names, how="left", on = ["nome_pai"])
    dados_cadastrais.rename(columns = {"id": "nome_pai_id"}, inplace=True)
    id_names.rename(columns = {"nome_pai": "nome_mae"}, inplace = True)

    dados_cadastrais = pd.merge(dados_cadastrais, id_names, how="left", on = ["nome_mae"])
    dados_cadastrais.rename(columns = {"id": "nome_mae_id"}, inplace=True)

    return dados_cadastrais