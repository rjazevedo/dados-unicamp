from utilities.io import read_result
from utilities.io import write_result

def generate_trasnf_int():
    vida_academica = read_result('vida_academica.csv', dtype=str)
    dados_cadastrais = read_result('dados_cadastrais.csv', dtype=str)
    ingressantes = vida_academica.merge(dados_cadastrais, how='left', on='identif')
    remanj_intern = ingressantes[ingressantes.cod_motivo_saida == '3']
    remanj_intern = remanj_intern.loc[:, ['insc_vest', 'ano_ingresso_curso', 'identif','nome','curso', 'cod_motivo_saida']]

    write_result(remanj_intern, 'remanejamento_interno.csv')

    