from dac import extract_dac

import socio.cleaning.__main__ as clear_socio
import socio.extract.__main__ as extract_socio

def main():
    extract_dac.main()    
    clear_socio.pre_process()
    extract_socio.extract_ids()
    # TODO: create EXTRACT_COMVEST, EXTRACT_RAIS and REPLICATE_IDS func

# TODO: implement verbose option 
if __name__ == '__main__':
    main()