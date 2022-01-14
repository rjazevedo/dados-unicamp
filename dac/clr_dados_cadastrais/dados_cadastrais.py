from utilities.io import read_from_database
from utilities.io import write_result
from utilities.columns import dados_cadastrais_cols
from utilities.format import str_to_upper_ascii
from utilities.format import padronize_sex
from utilities.format import padronize_race
from utilities.format import padronize_dates
from utilities.format import padronize_marstat
from utilities.format import fill_doc
from utilities.format import dates_to_year

dic = ['identif', 'cpf', 'nome', 'dta_nasc', 'doc','sexo', 'raca', 'est_civil', 'uf_nasc', 'mun_atual', 'mun_resid', 
        'mun_esc_form_em', 'uf_esc_form_em', 'sigla_pais_esc_form_em', 'ano_conclu_em', 'tipo_esc_form_em']

FILE_NAME = 'DadosCadastraisAluno.xlsx'
RESULT_NAME = 'dados_cadastrais.csv'

def generate_clean_data():
    dados_cadastrais = read_from_database(FILE_NAME)
    dados_cadastrais.columns = dados_cadastrais_cols
    dados_cadastrais = dados_cadastrais.loc[:, dic]
    unicode_cols = ['nome', 'mun_atual', 'mun_resid', 'mun_esc_form_em', 'tipo_esc_form_em']
    
    dados_cadastrais.cpf = fill_doc(dados_cadastrais.cpf, 11)
    dados_cadastrais.doc = fill_doc(dados_cadastrais.doc, 15)
    str_to_upper_ascii(dados_cadastrais, unicode_cols)
    padronize_sex(dados_cadastrais)
    padronize_race(dados_cadastrais)
    padronize_marstat(dados_cadastrais)
    padronize_dates(dados_cadastrais, ['dta_nasc'])
    dates_to_year(dados_cadastrais, 'ano_conclu_em')
    dados_cadastrais.tipo_esc_form_em = dados_cadastrais.tipo_esc_form_em.str[7:]
    

    write_result(dados_cadastrais, RESULT_NAME)
    return dados_cadastrais
