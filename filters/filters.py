import pandas as pd
import numpy as np


def filterby_year(df, years):
    return df[df["ano_vest"].isin(years)]["id"]


def filterby_course(df, courses, db):
    if db == "comvest":
        return df.loc[
            (df["opc1"].isin(courses))
            | (df["opc2"].isin(courses))
            | (df["opc3"].isin(courses))
            | (df["curso_matric"].isin(courses))
            | (df["curso_convocado"].isin(courses))
        ]["id"]
    elif db == "dac":
        return df[df["curso"].isin(courses)]["id"]


def filterby_joindate(df, year, how="exact"):
    if how == "exact":
        return df[df["ano_ingresso"] == year]["id"]
    elif how == "after":
        return pd.concat(
            [
                filterby_joindate(df, i)
                for i in range(year, int(np.max(df["ano_ingresso"])) + 1)
            ]
        )
    elif how == "before":
        return pd.concat(
            [
                filterby_joindate(df, i)
                for i in range(int(np.min(df["ano_ingresso"])), year + 1)
            ]
        )


def filterby_exitdate(df, year, how="exact"):
    if how == "exact":
        return df[df["ano_saida"] == year]["id"]
    elif how == "after":
        return pd.concat(
            [
                filterby_exitdate(df, i)
                for i in range(year, int(np.max(df["ano_saida"])) + 1)
            ]
        )
    elif how == "before":
        return pd.concat(
            [
                filterby_exitdate(df, i)
                for i in range(int(np.min(df["ano_saida"])), year + 1)
            ]
        )
