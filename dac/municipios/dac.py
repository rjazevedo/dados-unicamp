from dac.utilities.columns import dados_cadastrais_cols
from dac.utilities.io import read_from_database
from dac.utilities.io import write_output
from dac.municipios.utility_mun import concat_and_drop_duplicates
from dac.municipios.utility_mun import extract_mun_and_uf
from dac.municipios.utility_mun import create_key_for_merge
from dac.municipios.utility_mun import create_concat_key_for_merge
from dac.municipios.utility_mun import CODE_UF_EQUIV
from dac.municipios.utility_mun import create_dictonary_ufs
import pandas as pd

def generate_mun_dac():
    dados_cadastrais = read_from_database('DadosCadastraisAluno.xlsx')
    dados_cadastrais.columns = dados_cadastrais_cols
    
    mun_nasc = extract_mun_and_uf(dados_cadastrais, ['mun_nasc_d', 'uf_nasc_d', 'cod_pais_nascimento'])
    mun_esc_form_em = extract_mun_and_uf(dados_cadastrais, ['mun_esc_form_em', 'uf_esc_form_em', 'sigla_pais_esc_form_em'])
    result = concat_and_drop_duplicates([mun_nasc, mun_esc_form_em])
    
    create_key_for_merge(result)
    dict = create_dictonary_ufs(result)
    return dict