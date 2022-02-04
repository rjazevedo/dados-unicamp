from utilities.io import read_result
from utilities.io import write_result
from utilities.io import read_from_external
from utilities.io import write_output

def generate_dac_ids():
    ids = read_from_external('dac_comvest_ids.csv', sep=';', dtype=str)
    comvest_keys = read_result('vida_academica.csv', dtype=str)
    identifs = comvest_keys.merge(ids, on=['insc_vest', 'ano_ingresso_curso'], how='left').loc[:, ['id','identif']]
    identifs.drop_duplicates(subset=['identif'], inplace=True)
    write_result(identifs, 'identifs.csv')

def replicate_ids_dac():
    dados_cadastrais = read_result('dados_cadastrais.csv')
    vida_academica = read_result('vida_academica.csv')
    historico_escolar = read_result('historico_escolar_aluno.csv')
    resumo_por_periodo = read_result('resumo_periodo_cr.csv')

    ids = read_result('identifs.csv')

    dados_cadastrais = ids.merge(dados_cadastrais).drop(['identif', 'cpf', 'doc', 'nome'], axis=1)
    vida_academica = ids.merge(vida_academica).drop('identif', axis=1)
    historico_escolar = ids.merge(historico_escolar).drop('identif', axis=1)
    resumo_por_periodo = ids.merge(resumo_por_periodo).drop('identif', axis=1)

    write_output(dados_cadastrais, 'dados_cadastrais.csv')
    write_output(vida_academica, 'vida_academica.csv')
    write_output(historico_escolar, 'historico_escolar.csv')
    write_output(resumo_por_periodo, 'resumo_por_periodo.csv')