from dac.utilities.io import read_result
from dac.utilities.io import write_result
from dac.utilities.io import read_from_external
from dac.utilities.io import write_output

def generate_dac_ids():
    ids = read_from_external('dac_comvest_ids.csv', sep=';', dtype=str)
    comvest_keys = read_result('vida_academica.csv', dtype=str)
    identifs = comvest_keys.merge(ids, on=['insc_vest', 'ano_ingresso_curso'], how='left').loc[:, ['id','identif']]
    identifs.drop_duplicates(subset=['identif'], inplace=True)
    write_result(identifs, 'identifs.csv')

def replicate_ids_dac():
    dados_cadastrais = read_result('dados_cadastrais.csv')
    vida_academica = read_result('vida_academica.csv')
    vida_academica_habilitacao = read_result('vida_academica_habilitacao.csv')
    historico_escolar = read_result('historico_escolar_aluno.csv')
    resumo_por_periodo = read_result('resumo_periodo_cr.csv')

    ids = read_result('identifs.csv')

    dados_cadastrais = ids.merge(dados_cadastrais).drop(['insc_vest','identif', 'cpf', 'doc', 'nome','dta_nasc', 'origem'], axis=1, errors='ignore')
    vida_academica = ids.merge(vida_academica).drop(['insc_vest','identif', 'origem'], axis=1, errors='ignore')
    vida_academica_habilitacao = ids.merge(vida_academica_habilitacao).drop(['identif'], axis=1, errors='ignore')
    historico_escolar = ids.merge(historico_escolar).drop(['insc_vest','identif'], axis=1, errors='ignore')
    resumo_por_periodo = ids.merge(resumo_por_periodo).drop(['insc_vest','identif'], axis=1, errors='ignore')
    vida_academica_habilitacao = ids.merge(vida_academica_habilitacao).drop(['identif'], axis=1, errors='ignore')

    write_output(dados_cadastrais, 'dados_cadastrais.csv')
    write_output(vida_academica, 'vida_academica.csv')
    write_output(historico_escolar, 'historico_escolar.csv')
    write_output(resumo_por_periodo, 'resumo_por_periodo.csv')
    write_output(vida_academica_habilitacao, 'vida_academica_habilitacao.csv')