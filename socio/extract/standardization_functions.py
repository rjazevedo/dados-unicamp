from difflib import SequenceMatcher


def get_first_name(name):
    names = name.split()
    return names[0]


def get_reduced_cpf(cpf):
    if cpf == "-":
        return "-"
    reduced_cpf = "***" + cpf[3:-2] + "**"
    return reduced_cpf


def get_similarity(name_a, name_b):
    last_name_a = name_a.split()[1:]
    last_name_b = name_b.split()[1:]
    similar_rate = SequenceMatcher(None, last_name_a, last_name_b).ratio()
    return similar_rate
