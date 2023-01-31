import pandas as pd

from dac.extract_database import dac_database
from dac.create_ids import identificadores

from comvest.utilities.io import read_output
from comvest.utilities.dtypes import (
    DTYPES_DADOS,
    DTYPES_PERFIL,
    DTYPES_MATRICULADOS,
    DTYPES_NOTAS
)
from comvest.assign_ids import comvest_ids
import comvest.extract.__main__ as comvest_database

import rais.pre_processing.__main__ as pre_process_rais
import rais.id_generation.__main__ as id_generation
import rais.extract.__main__ as rais_database

import socio.cleaning.__main__ as clear_socio
import socio.extract.__main__ as extract_socio

def exportar_comvest():
    comvest = read_output(
        "comvest_amostra.csv",
        dtype={**DTYPES_DADOS, **DTYPES_PERFIL, **DTYPES_MATRICULADOS, **DTYPES_NOTAS},
    )

    comvest.to_csv('/home/processados/pedido_0/comvest_amostra.csv', index=False)

def exportar_dac():
    pass

def exportar_rais():
    pass

def exportar_socios():
    pass

def exportar_pedido_0():
    exportar_comvest()


def main():
    comvest_database.extract()

    ''' Insert other database extractions here '''

    exportar_pedido_0()
    

if __name__ == '__main__':
    main()