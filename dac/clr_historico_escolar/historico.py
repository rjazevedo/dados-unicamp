import numpy as np
from utilities.io import read_multiple_from_database
from utilities.io import write_result
from utilities.columns import historico_escolar_cols
from utilities.format import str_to_upper_ascii
from utilities.format import padronize_dates


DATABASE_FILES = ['HistoricoEscolar.xlsx', 'HistoricoEscolar1.xlsx', 'HistoricoEscolar2.xlsx', 'HistoricoEscolar.xlsx']
CLEAN_FILE = 'historico_escolar_aluno.csv'

def generate_clean_data():
    historico_escolar = read_multiple_from_database(DATABASE_FILES)
    historico_escolar.columns = historico_escolar_cols
    
    
    padronize_dates(historico_escolar, ['dt_inicio','dt_fim'])
    str_to_upper_ascii(historico_escolar, ['curricularidade'])
    historico_escolar.turma = historico_escolar.turma.str.strip()

    # Corrige registros que possuem datas ao invés de anos  
    historico_escolar.ano = historico_escolar.ano.astype(str)
    historico_escolar.loc[~historico_escolar.ano.str.isnumeric(), 'ano'] = np.NaN
    historico_escolar.ano.fillna(historico_escolar.dt_inicio.str[-4:], inplace=True)


    # Eliminando disciplinas canceladas ou não ofertadas em um respectivo semestre (código 15 e 9)
    historico_escolar.drop(
        historico_escolar[(historico_escolar.cod_situacao - 9) % 6 == 0].index, 
        inplace=True)

    write_result(historico_escolar, CLEAN_FILE)