# Keep only the first ocurrence of an instance
def remove_duplicated_rows(df, columns):
    isnt_first_occurrence = df.duplicated(subset=columns, keep="first")
    first_occurrence = df[~isnt_first_occurrence]
    return first_occurrence


# Subtract df2 from df1
def subtract(df1, df2, columns):
    df2 = df2.loc[:, columns]
    df2["present"] = True
    is_present = df1.merge(df2, on=columns, how="left")

    is_not_present = is_present[is_present["present"] != True]
    del is_not_present["present"]
    is_not_present = is_not_present.drop_duplicates()
    return is_not_present
