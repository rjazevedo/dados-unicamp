from dac.utilities.io import read_result
from dac.utilities.io import write_output
from dac.utilities.io import write_result
from dac.utilities.io import Bases
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

ID_NAMES = "ids_of_names.csv"
RESULT_NAME = 'dados_cadastrais.csv'
DADOS_CADASTRAIS = "dados_cadastrais_intermediario.csv"

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
    #dados_with_code = generate_uf_code(dados_cadastrais)
    #dados_with_school_code = generate_school_codes(dados_with_code)
    write_result(dados_cadastrais, RESULT_NAME)


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