from utilities.io import read_result
from utilities.io import write_result
from utilities.io import get_identificadores
import numpy as np

def generate_ids():
    ids = get_identificadores()
    vida_academica = read_result('vida_academica.csv', dtype=str).loc[:, ['identif', 'insc_vest', 'curso', 'ano_ingresso_curso', 'cod_tipo_ingresso']]
    dados_cadastrais = read_result('dados_cadastrais.csv', dtype=str)
    identifs = vida_academica.merge(ids, on=['insc_vest', 'ano_ingresso_curso'], how='left')
    null_identifs = identifs[identifs.id.isna()].loc[:, ['identif', 'insc_vest','curso', 'ano_ingresso_curso', 'cod_tipo_ingresso']]
    identifs = identifs[~identifs.id.isna()]

    # print(null_identifs[null_identifs.cod_tipo_ingresso != '1'].shape)
    # cpf_identifs = null_identifs.merge(dados_cadastrais, on=['identif'], how='left')
    # cpf_identifs = cpf_identifs.loc[:,  ['identif','insc_vest','cod_tipo_ingresso', 'ano_ingresso_curso','cpf']]
    # cpf_identifs = cpf_identifs[cpf_identifs.cpf != '-']
    # found_cpf = cpf_identifs.merge(ids.loc[:, ['id', 'cpf','origem_cpf','doc', 'nome', 'dta_nasc']], on=['cpf'], how ='left')
    # found_cpf.drop_duplicates(subset=['insc_vest', 'ano_ingresso_curso', 'id'], inplace=True)
    # null_identifs = found_cpf[found_cpf.id.isna()].loc[:, ['identif', 'insc_vest', 'ano_ingresso_curso', 'cod_tipo_ingresso']]
    # found_cpf = found_cpf[~found_cpf.id.isna()]
    # found_cpf = found_cpf.loc[:, ['identif','insc_vest','ano_ingresso_curso','cod_tipo_ingresso','nome','cpf','origem_cpf','dta_nasc','doc']]
    # # max_id = np.max(identifs.id)
    
    # non_comvest = null_identifs[null_identifs.cod_tipo_ingresso != '1']
    # non_comvest = non_comvest.merge(dados_cadastrais, how='left', on=['identif'])
    # non_comvest['origem_cpf'] = 1
    # non_comvest['id'] = pd.factorize(non_comvest['cpf'])

    # non_comvest = non_comvest.loc[:, ['identif','insc_vest','ano_ingresso_curso','cod_tipo_ingresso','nome','cpf','origem_cpf','dta_nasc','doc']]
    # print(non_comvest[non_comvest.cpf.isna()].shape)

    # found = null_identifs.merge(identifs.loc[:, ['identif', 'id', 'nome','cpf','origem_cpf','dta_nasc','doc']], on=['identif'])
    # found = found.loc[:, ['identif','insc_vest','ano_ingresso_curso','cod_tipo_ingresso','id','nome','cpf','origem_cpf','dta_nasc','doc']]
    # identifs = identifs.concat(found)
    null_identifs = null_identifs.merge(dados_cadastrais, how='left', on='identif')
    null_identifs = null_identifs.loc[:, ['identif', 'insc_vest', 'ano_ingresso_curso', 'nome','dta_nasc', 'cpf','doc','cod_tipo_ingresso', 'curso',]]
    null_identifs = null_identifs[null_identifs.cod_tipo_ingresso == '1']
    
    write_result(identifs, 'identifs.csv')
    write_result(null_identifs, 'nonidentif.csv')