import pandas as pd


def read_database(file, dtype, index=None, squeeze=False):
    df = pd.read_csv(
        file, sep=";", encoding="latin", dtype=dtype, index_col=index, squeeze=squeeze
    )
    return df


file = "/home/larissa/rais/scripts/clean_module/codes/municipios.csv"
dtype = {"municipio": "object"}
municipios = read_database(file, dtype, squeeze=True)

file = "/home/larissa/rais/scripts/clean_module/codes/cnae95.csv"
dtype = {"cnae95": "object"}
cnae95 = read_database(file, dtype, squeeze=True)

file = "/home/larissa/rais/scripts/clean_module/codes/cbo94.csv"
dtype = {"cbo94": "object"}
cbo94 = read_database(file, dtype, squeeze=True)

file = "/home/larissa/rais/scripts/clean_module/codes/nat_juridica.csv"
dtype = {"nat_juridica": "object"}
nat_juridica = read_database(file, dtype, squeeze=True)

file = "/home/larissa/rais/scripts/clean_module/codes/cbo02.csv"
dtype = {"cbo02": "object"}
cbo02 = read_database(file, dtype, squeeze=True)

file = "/home/larissa/rais/scripts/clean_module/codes/cnae20classe.csv"
dtype = {"cnae20classe": "object"}
cnae20classe = read_database(file, dtype, squeeze=True)

file = "/home/larissa/rais/scripts/clean_module/codes/cnae20subclasse.csv"
dtype = {"cnae20subclasse": "object"}
cnae20subclasse = read_database(file, dtype, squeeze=True)
