from extract import extract_from_base

def main():
    base_file = '/home/processados/base_comvest-2001_2018.csv' 
    extract_from_base.extract(base_file, ['insc_vest', 'ano_vest', 'id'])

if __name__ == '__main__':
    main()