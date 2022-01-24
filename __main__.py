from dac.extract_database import dac_database
from dac.create_ids import identificadores

def main():
    dac_database.extract()   
    # TODO: create EXTRACT_COMVEST, EXTRACT_RAIS and REPLICATE_IDS func
    identificadores.generate_ids()
    
# TODO: implement verbose option 
if __name__ == '__main__':
    main()