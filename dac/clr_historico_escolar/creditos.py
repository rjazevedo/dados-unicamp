from dac.utilities.io import read_input
from dac.utilities.io import write_result
from dac.utilities.columns import credito_columns

DATABASE_FILE = 'Rodolfo_Disciplina_Creditos.xlsx'
RESULT_FILE = 'creditos.csv'

def generate_clean_data(): 
    creditos = read_input(DATABASE_FILE)
    creditos.columns = credito_columns
    write_result(creditos, RESULT_FILE)