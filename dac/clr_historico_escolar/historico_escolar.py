from dac.clr_historico_escolar import historico
from dac.clr_historico_escolar import creditos
from dac.clr_historico_escolar import historico_creditos

def generate_clean_data():
    historico.generate_clean_data()
    creditos.generate_clean_data()
    historico_creditos.merge()