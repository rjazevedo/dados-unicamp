import pandas as pd
from dac.utilities.io import read_result
from dac.utilities.io import write_result

SCHOOL_CODES = "escola_codigo_inep.csv"
DADOS_CADASTRAIS = "dados_cadastrais_com_uf.csv"
RESULT = "dados_cadastrais.csv"

# Atribui códigos das escolas 
def generate_school_codes():
    dados_cadastrais = read_result(DADOS_CADASTRAIS)
    code_schools = read_result(SCHOOL_CODES).loc[:, ["escola_base", "Código INEP", "escola_inep", "codigo_municipio"]]
    code_schools.columns = ["escola_em_d", "cod_escola_em_inep", "escola_em_inep", "cod_mun_form_em"]
    result = pd.merge(dados_cadastrais, code_schools, how="left", on=["escola_em_d", "cod_mun_form_em"])
    write_result(result, RESULT)