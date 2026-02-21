import pandas as pd

from comvest.utilities.dtypes import DTYPES_DADOS
from comvest.utilities.io import read_auxiliary
from comvest.utilities.io import read_result
from comvest.utilities.io import write_result


COLUNAS_ESCOLAS = ["nome_escola", "codigo_municipio", "municipio", "uf"]


def exportar_bases_iniciais_escolas():
    dados_comvest = read_result("dados_comvest_com_uf.csv", dtype=DTYPES_DADOS)
    dados_dac = read_result("dados_cadastrais_com_uf.csv", dtype=object)

    escolas_comvest = dados_comvest.loc[
        :, ["esc_em_c", "cod_mun_esc_em_c", "mun_esc_em_c", "uf_esc_em"]
    ].copy()
    escolas_comvest.columns = COLUNAS_ESCOLAS
    escolas_comvest.insert(0, "fonte", "comvest")

    escolas_dac = dados_dac.loc[
        :, ["escola_em_d", "cod_mun_form_em", "mun_esc_form_em", "uf_esc_form_em"]
    ].copy()
    escolas_dac.columns = COLUNAS_ESCOLAS
    escolas_dac.insert(0, "fonte", "dac")

    escolas_base_raw = pd.concat([escolas_comvest, escolas_dac], ignore_index=True)

    write_result(escolas_comvest, "escolas_origem_comvest_raw.csv")
    write_result(escolas_dac, "escolas_origem_dac_raw.csv")
    write_result(escolas_base_raw, "escolas_origem_unificada_raw.csv")


def exportar_bases_iniciais_inep():
    inep_abertas = read_auxiliary("INEP data.csv", dtype=object, sep=";").loc[
        :,
        [
            "Escola",
            "Código INEP",
            "UF",
            "Município",
            "Etapas e Modalidade de Ensino Oferecidas",
        ],
    ].copy()

    inep_abertas.columns = [
        "nome_escola",
        "codigo_inep",
        "uf",
        "municipio",
        "etapas_modalidades",
    ]
    inep_abertas.insert(0, "situacao", "aberta")
    inep_abertas.insert(1, "ano_censo", None)

    inep_fechadas = read_auxiliary(
        "cadescfechadassh19952021.csv", dtype=object, sep=";", encoding="latin1"
    ).loc[:, ["NU_ANO_CENSO", "NO_ENTIDADE", "CO_ENTIDADE", "SG_UF", "NO_MUNICIPIO"]].copy()

    inep_fechadas.columns = ["ano_censo", "nome_escola", "codigo_inep", "uf", "municipio"]
    inep_fechadas.insert(0, "situacao", "fechada")
    inep_fechadas.insert(6, "etapas_modalidades", None)

    inep_raw = pd.concat([inep_abertas, inep_fechadas], ignore_index=True)

    write_result(inep_abertas, "inep_escolas_abertas_raw.csv")
    write_result(inep_fechadas, "inep_escolas_fechadas_raw.csv")
    write_result(inep_raw, "inep_escolas_unificada_raw.csv")


def exportar_bases_iniciais():
    exportar_bases_iniciais_escolas()
    exportar_bases_iniciais_inep()


if __name__ == "__main__":
    exportar_bases_iniciais()
