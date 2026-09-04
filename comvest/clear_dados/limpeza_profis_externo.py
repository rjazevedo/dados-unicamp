import pandas as pd

from comvest.utilities.io import Bases

# tratar_dados() e o restante das funcoes de limpeza sao importadas de dentro
# das funcoes abaixo (nao no topo do modulo) porque limpeza_dados.py importa
# este arquivo -- import circular se fosse no topo aqui tambem.

PROFIS_EXTERNO_PATH = Bases.COMVEST.value + "Profis11a22.xlsx"

# Candidatos ao ProFis 2011-2021, planilha separada (Profis11a22.xlsx), nunca
# integrada ao pipeline antes -- ver plan file. tipo_ingresso_comvest=6 (5 e
# reservado pro ProFis via aba oficial profis_dados, que so existe dentro de
# ingresso2022.xlsx).
TIPO_INGRESSO_PROFIS_EXTERNO = 6

# 2022 ja tem aba profis_dados oficial dentro de ingresso2022.xlsx (ingresso=5,
# mesmos 676 registros confirmados por contagem) -- reprocessar a aba "2022"
# daqui geraria linha duplicada. So usamos essa aba pra um enriquecimento
# pontual (sexo/email) nas linhas ingresso=5 ja existentes, via enrich_2022_sexo_email.
ANOS_NOVOS = range(2011, 2022)  # 2011..2021


def tratar_profis_externo(df, ano):
    from comvest.clear_dados.limpeza_dados import tratar_dados

    df.columns = [str(c).upper() for c in df.columns]

    sexo = df["SEXO"].copy() if "SEXO" in df.columns else pd.Series([""] * len(df))
    email = df["EMAIL"].copy() if "EMAIL" in df.columns else pd.Series([""] * len(df))
    matriculado = (
        df["MATRICULADO"].copy() if "MATRICULADO" in df.columns else pd.Series([""] * len(df))
    )
    sexo = sexo.reset_index(drop=True)
    email = email.reset_index(drop=True)
    matriculado = matriculado.reset_index(drop=True)

    df = tratar_dados(df, ano, path=None, ingresso=TIPO_INGRESSO_PROFIS_EXTERNO)
    df = df.reset_index(drop=True)

    # insc/insc2 do ProFis usa numeracao diferente da inscricao real do
    # vestibular (confirmado por amostragem real: formato ano+5-digitos, ex.
    # "201100019", contra 7 digitos sem prefixo do insc_vest normal, ex.
    # "1275509"). tratar_dados() trataria uma coluna literalmente chamada
    # "insc" (presente em varios anos desta planilha) como se fosse o mesmo
    # campo do vestibular normal, arriscando colisao de merge com um
    # candidato de vestibular nao relacionado. Zera propositalmente --
    # ligacao com quem ja esta na DAC e feita por nome (profis_externo_match.py),
    # nao por numero de inscricao.
    df["insc_vest"] = pd.NA

    df["sexo_c"] = sexo.values
    df["email_c"] = email.values
    df["matriculado_c"] = matriculado.values

    return df


def extraction_profis_externo():
    dfs = []
    for ano in ANOS_NOVOS:
        df = pd.read_excel(PROFIS_EXTERNO_PATH, sheet_name=str(ano), dtype=str)
        df = tratar_profis_externo(df, ano)
        dfs.append(df)
    return pd.concat(dfs)


# Preenche sexo_c/email_c nas linhas ja existentes com tipo_ingresso_comvest==5
# (ProFis via aba oficial, so 2022) usando a aba "2022" desta planilha como
# fonte -- essas 2 colunas nao existem na aba profis_dados oficial. Casamento
# por CPF (confiavel nas linhas tipo=5, vieram da aba oficial da COMVEST).
# Nunca cria linha nova, nunca toca em outro campo dessas linhas.
def enrich_2022_sexo_email(dados_comvest):
    df_2022 = pd.read_excel(PROFIS_EXTERNO_PATH, sheet_name="2022", dtype=str)
    df_2022.columns = [str(c).upper() for c in df_2022.columns]
    if "CPF" not in df_2022.columns:
        return dados_comvest

    lookup = pd.DataFrame()
    lookup["cpf"] = df_2022["CPF"].map(lambda cpf: str(cpf).zfill(11))
    lookup["sexo_2022"] = df_2022["SEXO"] if "SEXO" in df_2022.columns else ""
    lookup["email_2022"] = df_2022["EMAIL"] if "EMAIL" in df_2022.columns else ""
    lookup = lookup.drop_duplicates(subset="cpf")

    # dados_comvest vem de pd.concat() de varias abas -- indice tem valores
    # repetidos entre abas (cada uma comeca do 0 de novo). reset_index()
    # garante alinhamento posicional seguro com o resultado do merge (que
    # sempre sai com RangeIndex novo), evitando desalinhar sexo_c/email_c
    # com a linha errada.
    dados_comvest = dados_comvest.reset_index(drop=True)
    tipo5 = dados_comvest["tipo_ingresso_comvest"] == 5
    merged = dados_comvest.merge(lookup, how="left", on="cpf")
    assert len(merged) == len(dados_comvest), "merge multiplicou linhas -- cpf duplicado no lookup"

    dados_comvest.loc[tipo5, "sexo_c"] = merged.loc[tipo5, "sexo_2022"].values
    dados_comvest.loc[tipo5, "email_c"] = merged.loc[tipo5, "email_2022"].values

    return dados_comvest
