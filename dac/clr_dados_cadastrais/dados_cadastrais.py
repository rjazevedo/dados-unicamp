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

drop_cols = ['nome_mae', 'nome_pai', 'idade_atual', 
        'tipo_doc', 'dt_emissao_doc', 'orgao_emissor_doc', 'uf_esmissao_doc', 'doc_tratado']

FILE_NAME = 'DadosCadastraisAluno.xlsx'
RESULT_NAME = 'dados_cadastrais.csv'

def generate_clean_data():
    dados_cadastrais = read_from_database(FILE_NAME)
    dados_cadastrais.columns = dados_cadastrais_cols
    dados_cadastrais.drop(drop_cols, axis=1, inplace=True)
    unicode_cols = ['nome', 'mun_atual', 'mun_resid', 'mun_esc_form_em', 'tipo_esc_form_em', 
    'raca_descricao', 'mun_nasc', 'pais_nascimento', 'nacionalidade', 'pais_nacionalidade', 'naturalizado',
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
    

    write_result(dados_cadastrais, RESULT_NAME)
    return dados_cadastrais
