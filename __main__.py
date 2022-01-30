from dac.extract_database import dac_database
from dac.create_ids import identificadores

import comvest.extract.__main__ as comvest_database

import rais.pre_processing.__main__ as pre_process_rais
import rais.id_generation.__main__ as id_generation
import rais.extract.__main__ as rais_database

import socio.cleaning.__main__ as clear_socio
import socio.extract.__main__ as extract_socio

def main():
    comvest_database.extract()
    dac_database.extract()
    pre_process_rais.get_identification_data()
    clear_socio.pre_process()

    id_generation.generate_ids()

    extract_socio.extract_ids()
    rais_database.clear_databse()
    # TODO: create EXTRACT_RAIS and REPLICATE_IDS func
    identificadores.generate_ids()
    
# TODO: implement verbose option 
if __name__ == '__main__':
    main()