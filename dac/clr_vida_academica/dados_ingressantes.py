from dac.utilities.io import read_result, write_result

def generate():                                                                                                 # TODO: Remover origem e curso e tipo_ingresso
    dados_cadastrais = read_result('dados_cadastrais.csv').loc[:, ['identif', 'cpf', 'nome', 'dta_nasc', 'doc']]
    vida_academica = read_result('vida_academica.csv').loc[:, ['identif', 'insc_vest', 'ano_ingresso_curso', 'curso', 'tipo_ingresso', 'motivo_saida', 'origem']]
    dados_ingressante = vida_academica.merge(dados_cadastrais, on=['identif'])
    write_result(dados_ingressante, 'dados_ingressante.csv')