from dac.utilities.io import read_result
from dac.utilities.io import write_result
from dac.utilities.format import calc_cr_periodo
RESUMO_FILE = 'resumo_por_periodo.csv'
HIST_FILE = 'historico_creditos.csv'
RESULT_FILE = 'resumo_periodo_cr.csv'
exclui_cr = {
    0 : 'FALTA INFORMACAO',
    2 : 'PROFICIENCIA',
    3 : 'APROVADO POR FREQUENCIA',
    6 : 'REPROVADO POR FREQUENCIA',
    7 : 'APROVEITAMENTO DE ESTUDOS',
    8 : 'DESISTENCIA',
    11 : 'DISPENSA POR IDADE',
}

def generate_cr():
    historico_com_creditos = read_result(HIST_FILE)
    resumo_semestre = read_result(RESUMO_FILE)

    for m in exclui_cr.keys():
        historico_com_creditos.drop(historico_com_creditos[historico_com_creditos.cod_situacao == m].index, inplace=True)

    cr_obr_periodo = calc_cr_periodo(historico_com_creditos, 'cr_obr_periodo')
    resumo_semestre_cr = resumo_semestre.merge(cr_obr_periodo, how='left')
    
    cols = list(resumo_semestre_cr.columns)
    new_col = cols.pop()
    cols.insert(cols.index('cr_periodo') + 1, new_col)
    resumo_semestre_cr = resumo_semestre_cr.loc[:, cols]

    write_result(resumo_semestre_cr, RESULT_FILE)