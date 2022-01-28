import pandas as pd
import numpy as np


def validar_CPF(cpf_dac, cpf_comvest):
    if cpf_dac != '-':
        filled_cpf = str(cpf_dac).zfill(11)
    else:
        filled_cpf = str(cpf_comvest).zfill(11)

    cpf = [int(char) for char in filled_cpf if char.isdigit()]

    if len(cpf) != 11:
        return '-'
    if all(cpf[i] == cpf[i+1] for i in range (0, len(cpf)-1)):
        return '-'

    #  Valida os dois dígitos verificadores
    for i in range(9, 11):
        valor = sum((cpf[num] * (i+1-num) for num in range(0, i)))
        digito = ((valor * 10) % 11) % 10
        if digito != cpf[i]:
            return '-'

    cpf_valido = [str(d) for d in cpf]
    
    return ''.join(cpf_valido)

def set_origemCPF(cpf_dac, cpf_comvest):
    '''
    Coluna Origem CPF:
        2 se veio da DAC
        1 se veio da Comvest
        0 se não temos CPF nem na DAC nem na Comvest
    '''

    if cpf_dac == '-' and cpf_comvest == '-':
        return 0
    if cpf_dac == '-' and cpf_comvest != '-':
        return 1
    if cpf_dac != '-':
        return 2


dados_comvest = pd.read_csv('resultados/dados_comvest.csv', dtype=str).loc[:, ['nome_c','cpf','doc_c','dta_nasc_c','insc_vest','ano_vest']]
dados_comvest.columns = ['nome','cpf','doc','dta_nasc','insc_vest','ano_ingresso_curso']

dados_dac = pd.read_csv('resultados/dados_ingressante.csv', dtype=str).loc[:, ['nome','cpf','doc','dta_nasc','insc_vest','ano_ingresso_curso']]

uniao_dac_comvest = dados_dac.merge(dados_comvest, how='outer', on=['insc_vest','ano_ingresso_curso'], suffixes=('_dac','_comvest'))

uniao_dac_comvest['cpf_dac'].fillna('-', inplace=True)
uniao_dac_comvest['cpf_comvest'].fillna('-', inplace=True)

valida_cpf = np.vectorize(validar_CPF)
uniao_dac_comvest['cpf'] = valida_cpf(uniao_dac_comvest['cpf_dac'], uniao_dac_comvest['cpf_comvest'])
#uniao_dac_comvest['cpf'] = uniao_dac_comvest.apply(lambda idx: validar_CPF(idx), axis=1)

origem_cpf = np.vectorize(set_origemCPF)
uniao_dac_comvest['origem_cpf'] = origem_cpf(uniao_dac_comvest['cpf_dac'], uniao_dac_comvest['cpf_comvest'])

uniao_dac_comvest['nome'] = uniao_dac_comvest['nome_dac'].fillna(uniao_dac_comvest['nome_comvest'])
uniao_dac_comvest['dta_nasc'] = uniao_dac_comvest['dta_nasc_dac'].fillna(uniao_dac_comvest['dta_nasc_comvest'])
uniao_dac_comvest['doc'] = uniao_dac_comvest['doc_dac'].fillna(uniao_dac_comvest['doc_comvest'])

uniao_dac_comvest.drop(columns=['cpf_dac','cpf_comvest','doc_dac','doc_comvest','nome_dac','nome_comvest','dta_nasc_dac','dta_nasc_comvest'], inplace=True)

uniao_dac_comvest = uniao_dac_comvest.reindex(columns=['insc_vest','nome','cpf','origem_cpf','dta_nasc','doc','ano_ingresso_curso'])


uniao_sem_cpf = uniao_dac_comvest[uniao_dac_comvest['cpf'] == '-'].drop(['cpf','origem_cpf','doc'], axis=1)
uniao_com_cpf = uniao_dac_comvest[uniao_dac_comvest['cpf'] != '-']

uniao = uniao_sem_cpf.merge(uniao_com_cpf[['nome','dta_nasc','cpf','origem_cpf','doc']], on=['nome','dta_nasc'])
uniao = uniao.loc[:, ['insc_vest','nome','cpf','origem_cpf','doc','dta_nasc','ano_ingresso_curso']]

uniao_dac_comvest = pd.concat([uniao, uniao_dac_comvest])
uniao_dac_comvest.drop_duplicates(subset=['insc_vest','ano_ingresso_curso'], inplace=True)


uniao_dac_comvest[uniao_dac_comvest['cpf'] == '-'].to_csv('uniao_dac_comvest_sem_cpf.csv', index=False)
uniao_dac_comvest.to_csv('uniao_dac_comvest.csv', index=False)
