import pandas as pd
from dac.utilities.io import write_result
from dac.new_create_ufs_codes.utilities import get_wrong_and_right
from dac.new_create_ufs_codes.utilities import merge_by_uf
from dac.new_create_ufs_codes.utilities import create_key_for_merge
from dac.new_create_ufs_codes.utilities import create_concat_key_for_merge
from dac.new_create_ufs_codes.utilities import create_dictonary_ufs
from dac.new_create_ufs_codes.utilities import merge_by_concat_key
from dac.new_create_ufs_codes.utilities import merge_by_counties
from dac.new_create_ufs_codes.utilities import give_trust
from dac.new_create_ufs_codes.utilities import concat_and_drop_duplicates
from dac.new_create_ufs_codes.utilities import copy_columns_for_perfect_merge


def probabilist_merge_by_counties(counties, ibge_data, correct_list):
    counties_keys = create_key_for_merge(counties)
    ibge_keys = create_key_for_merge(ibge_data)
    right, wrong = merge_by_counties(counties_keys, ibge_keys)

    right = give_trust(right, 4)
    final_counties = concat_and_drop_duplicates([right, wrong])
    correct_list.append(final_counties)


def probabilist_merge_by_concat_key(counties, ibge_data, correct_list):
    counties_keys = create_concat_key_for_merge(counties)
    ibge_keys = create_concat_key_for_merge(ibge_data)
    right, wrong = merge_by_concat_key(counties_keys, ibge_keys)

    right = give_trust(right, 3)
    correct_list.append(right)
    return wrong


def probabilist_merge(counties, ibge_data, correct_list):
    counties_keys = create_key_for_merge(counties)
    ibge_keys = create_key_for_merge(ibge_data)
    counties_dict = create_dictonary_ufs(counties_keys)
    right, wrong = merge_by_uf(counties_dict, ibge_keys)

    right = give_trust(right, 2)
    correct_list.append(right)
    return wrong


def perfect_merge(df, ibge_data, correct_list):
    result = pd.merge(df, ibge_data, how="left", suffixes=('','_ibge'))
    right, wrong = get_wrong_and_right(result)

    right = give_trust(right, 1)
    right = create_key_for_merge(right)
    right = copy_columns_for_perfect_merge(right)
    correct_list.append(right)
    return wrong