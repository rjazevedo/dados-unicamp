from clr_historico_escolar import historico
from clr_historico_escolar import creditos
from clr_historico_escolar import historico_creditos

def generate_clean_data():
    historico.generate_clean_data()
    creditos.generate_clean_data()
    historico_creditos.merge()