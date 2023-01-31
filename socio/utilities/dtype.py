def get_dtype(columns_info, is_original=False):
    dtype = {}
    for column in columns_info:
        if is_original:
            dtype[column] = get_type_column_original(column, columns_info)
        else:
            dtype[column] = get_type_column_clean(column, columns_info)
    return dtype


def get_type_column_original(column, columns_info):
    if "has_null_value" in columns_info[column]:
        return "object"
    else:
        return columns_info[column]["type"]


def get_type_column_clean(column, columns_info):
    return columns_info[column]["type"]
