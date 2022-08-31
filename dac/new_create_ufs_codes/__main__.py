import pandas as pd
from dac.utilities.io import write_result
from dac.new_create_ufs_codes.comvest import generate_comvest
from dac.new_create_ufs_codes.dac import generate_dac
from dac.new_create_ufs_codes.dados_ibge import generate_ibge_data
from dac.new_create_ufs_codes.utilities import concat_and_drop_duplicates
from dac.new_create_ufs_codes.merges import probabilist_merge_by_counties
from dac.new_create_ufs_codes.merges import probabilist_merge_by_concat_key
from dac.new_create_ufs_codes.merges import probabilist_merge
from dac.new_create_ufs_codes.merges import perfect_merge


def main():
    counties = setup_conties()
    ibge_data = generate_ibge_data()
    correct_list = []
    
    wrong = perfect_merge(counties, ibge_data, correct_list)
    wrong = probabilist_merge(wrong, ibge_data, correct_list)
    wrong = probabilist_merge_by_concat_key(wrong, ibge_data, correct_list)
    probabilist_merge_by_counties(wrong, ibge_data, correct_list)
    
    final_df = concat_and_drop_duplicates(correct_list)
    final_df = final_df.drop(['key'], axis=1)
    write_result(final_df, "final_counties.csv")


def setup_conties():
    comvest = generate_comvest()
    dac = generate_dac()
    result = concat_and_drop_duplicates([comvest, dac])
    return result


if __name__ == '__main__':
    main()