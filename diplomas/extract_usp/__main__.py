from extract_usp import scrapper 
from extract_usp import comvest_diplomasUSP

def main():
    scrapper.proccess_usp()
    comvest_diplomasUSP.merge()

if __name__ == '__main__':
    main()