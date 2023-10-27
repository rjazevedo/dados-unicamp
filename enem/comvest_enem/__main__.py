from enem.comvest_enem import clear_comvest 
from enem.comvest_enem import divide_comvest
from enem.comvest_enem import comvest_enem
from enem.comvest_enem import comvest_vest_ids
from enem.comvest_enem import comvest_enem_ids

def main():
    clear_comvest.clean_all()
    comvest_enem.merge()
    divide_comvest.split_all()
    comvest_vest_ids.retrieve()
    comvest_enem_ids.merge()


if __name__ == '__main__':
    main()