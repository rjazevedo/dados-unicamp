from utilities.io import read_result, write_result

def extract(mask):
    indices = read_result('indices.csv', dtype=str)
    indices_masked = indices[mask(indices)]
    
    dc_key = indices_masked.loc[:, ['identif']].drop_duplicates()
    va_key = indices_masked.loc[:, ['insc_vest', 'ano_ingresso']].drop_duplicates()
    rp_key = indices_masked.loc[:, ['identif','ano_ingresso', 'curso']].drop_duplicates()

    dados_cadastrais = read_result('dados_cadastrais.csv', dtype=str)
    dados_cadastrais_extracted = dc_key.merge(dados_cadastrais)
    vida_academica = read_result('vida_academica.csv', dtype=str)
    vida_academica_extracted = va_key.merge(vida_academica)
    resumo_periodo = read_result('resumo_por_periodo.csv', dtype=str)
    resumo_periodo_extracted = rp_key.merge(resumo_periodo)

    write_result(dados_cadastrais_extracted, 'extraction/dados_cadastrais_extracted.csv')
    write_result(vida_academica_extracted, 'extraction/vida_academica_extracted.csv')
    write_result(resumo_periodo_extracted, 'extraction/resumo_periodo_extracted.csv')