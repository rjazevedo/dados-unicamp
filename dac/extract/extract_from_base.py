from pandas.io.parsers import read_csv
from utilities.io import read_result, write_result

def extract(base_path, keys):
    indices = read_result('indices.csv', dtype=str)
    base = read_csv(base_path, dtype=str).loc[:, keys]
    indices_masked = indices.merge(base)
    
    dc_key = indices_masked.loc[:, ['id', 'identif']].drop_duplicates()
    va_key = indices_masked.loc[:, ['id', 'insc_vest', 'ano_vest']].drop_duplicates()
    he_key = indices_masked.loc[:, ['id', 'identif','ano_vest']].drop_duplicates()
    
    dados_cadastrais = read_result('dados_cadastrais.csv', dtype=str)
    dados_cadastrais_extracted = dc_key.merge(dados_cadastrais)
    
    vida_academica = read_result('vida_academica.csv', dtype=str)
    vida_academica_extracted = va_key.merge(vida_academica)
    
    resumo_periodo = read_result('resumo_periodo_cr.csv', dtype=str)
    resumo_periodo_extracted = he_key.merge(resumo_periodo)
    
    historico_escolar = read_result('historico_escolar_aluno.csv', dtype=str)
    historico_escolar_extracted = he_key.merge(historico_escolar)

    write_result(dados_cadastrais_extracted, 'extraction/dados_cadastrais_extracted.csv')
    write_result(vida_academica_extracted, 'extraction/vida_academica_extracted.csv')
    write_result(resumo_periodo_extracted, 'extraction/resumo_periodo_extracted.csv')
    write_result(historico_escolar_extracted, 'extraction/historico_escolar_extracted.csv')