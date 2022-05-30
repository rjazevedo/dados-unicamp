import numpy as np
from dac.utilities.io import read_result
from dac.utilities.io import write_result

HISTORICO_RESULT = 'historico_escolar_aluno.csv'
CREDITOS_RESULT = 'creditos.csv'
CLEAN_FILE = 'historico_creditos.csv'
def merge():
    historico = read_result(HISTORICO_RESULT, dtype={
        'identif' : str,
        'periodo' : int,
        'ano': int,
        'dt_inicio': str,
        'dt_fim': str,
        'cod_curricularidade': int,
        'curricularidade': str,
        'disc': str,
        'turma': str,
        'cod_situacao_disciplina': int,
        'situacao': str,
        'nota': float,
        'frequencia': int   
    })

    creditos = read_result(CREDITOS_RESULT, dtype={
        'periodo': int, 
        'ano': int, 
        'disc' : str, 
        'creditos': int
    })
    historico = historico.drop(historico[historico.cod_situacao_disciplina == 9].index
                        ).drop(historico[historico.cod_situacao_disciplina == 15].index)

    disc_cursadas = historico.loc[:, ['disc', 'ano', 'periodo']
                            ].merge(creditos, how='left'
                            ).drop_duplicates()

    disc_cursadas = disc_cursadas.sort_values(by=['creditos'], ascending=False,
                                ).sort_values(by=['disc', 'ano'],
                                ).replace(0, np.nan)
    disc_cursadas.creditos = disc_cursadas.groupby('disc')['creditos'].ffill().bfill().astype(int)

    historico_com_creditos = historico.merge(disc_cursadas, how='left')
    write_result(historico_com_creditos, CLEAN_FILE)

