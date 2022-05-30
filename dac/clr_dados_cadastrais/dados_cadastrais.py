from dac.utilities.io import read_from_database
from dac.utilities.io import read_result
from dac.utilities.io import write_output
from dac.utilities.io import write_result
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
import pandas as pd

drop_cols = ['nome_mae', 'nome_pai', 'idade_atual', 
        'tipo_doc', 'dt_emissao_doc', 'orgao_emissor_doc', 'uf_emissor_doc', 'doc_tratado']

FILE_NAME = 'DadosCadastraisAluno.xlsx'
RESULT_NAME = 'dados_cadastrais.csv'
UF_CODE_NAME = 'counties_code.csv'

def generate_clean_data():
    dados_cadastrais = read_from_database(FILE_NAME)
    
    dados_cadastrais.columns = dados_cadastrais_cols
    dados_cadastrais.drop(drop_cols, axis=1, inplace=True)
    unicode_cols = ['nome', 'mun_atual', 'mun_resid_d', 'mun_esc_form_em', 'tipo_esc_form_em', 
    'raca_descricao', 'mun_nasc_d', 'pais_nasc_d', 'nacionalidade_d', 'pais_nac_d', 'naturalizado',
    'escola_em_d', 'pais_esc_form_em']
    
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
    
    padronize_string_miss(dados_cadastrais, ['cep_nasc', 'cep_escola_em', 'cep_atual', 'cep_resid_d', 'tipo_esc_form_em'], '-')
    padronize_int_miss(dados_cadastrais, ['ano_conclu_em'], 0)
    
    write_result(dados_cadastrais, RESULT_NAME)
    generate_uf_code()

def generate_uf_code():
    final_counties = read_result(UF_CODE_NAME)
    dados_cadastrais = read_result(RESULT_NAME)

    final_counties = final_counties[['municipio_x', 'uf_y', 'codigo_municipio', 'confianca']]
    final_counties = final_counties.drop_duplicates(['municipio_x', 'uf_y'])

    final_counties.columns = ['mun_nasc_d', 'uf_nasc_d', 'cod_mun_nasc_d', 'origem_cod_mun_nasc_d']
    mun_nasc_d_merge = pd.merge(dados_cadastrais, final_counties, how='left')

    final_counties.columns = ['mun_esc_form_em', 'uf_esc_form_em', 'cod_mun_form_em', 'origem_cod_mun_form_em']
    mun_nasc_d_merge = pd.merge(mun_nasc_d_merge, final_counties, how='left')
    
    mun_nasc_d_merge = mun_nasc_d_merge.reindex(columns= dados_cadastrais_final_cols)
    write_result(mun_nasc_d_merge, RESULT_NAME)