from unidecode import unidecode 

def clean_string(name : str) -> str:
    """
    Limpa o nome fornecido, removendo acentos, convertendo para maiúsculas 
    e eliminando espaços em branco extras.

    Parâmetros:
        name (str): O nome a ser limpo.

    Retorna:
        str: O nome limpo, ou uma string vazia se o nome for nulo.
    """
    if not name:
        return ""
    else:
        s = unidecode(name).upper().strip()
        return " ".join(s.split())
