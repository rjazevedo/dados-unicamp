import logging

def progresslog(sheet_name, year):
    logging.info(f'Reading in sheet {sheet_name} of Comvest\'s {year} file')

def resultlog(FILE_NAME):
    logging.info(f'Writing {FILE_NAME} result')