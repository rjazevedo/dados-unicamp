from dac.extract_database import dac_database
from dac.create_ids import identificadores

import comvest.extract.__main__ as comvest_database

import socio.cleaning.__main__ as clear_socio
import socio.extract.__main__ as extract_socio

def main():
    comvest_database.extract()
    dac_database.extract()  
    clear_socio.pre_process()
    extract_socio.extract_ids()
    # TODO: create EXTRACT_RAIS and REPLICATE_IDS func
    identificadores.generate_ids()
    
# TODO: implement verbose option 
if __name__ == '__main__':
    main()