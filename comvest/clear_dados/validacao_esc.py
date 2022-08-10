from collections import defaultdict
import pandas as pd
import swifter
import difflib
import textdistance
import re
from unidecode import unidecode
from comvest.utilities.io import read_result, read_auxiliary, read_output, write_result
from comvest.utilities.dtypes import DTYPES_DADOS

ESTADOS = {
    "RO",
    "AC",
    "AM",
    "RR",
    "PA",
    "AP",
    "TO",
    "MA",
    "PI",
    "CE",
    "RN",
    "PB",
    "PE",
    "AL",
    "SE",
    "BA",
    "MG",
    "ES",
    "RJ",
    "SP",
    "PR",
    "SC",
    "RS",
    "MS",
    "MT",
    "GO",
    "DF",
}


def standardize_str(s, type):
    if type == "seq":
        return (
            re.sub(r"[^\w]", "", unidecode(str(s)).upper())
            .replace("COLEGIOESTADUAL", "CE")
            .replace("ESCOLAESTADUAL", "EE")
            .replace("TEMPOINTEGRAL", "")
            .replace("ESCOLAMUNICIPAL", "EM")
            .replace("CENTROEDUCACIONAL", "CE")
            .replace("EDUCACAOINFANTIL", "EI")
            .replace("ENSINOFUNDAMENTAL", "EF")
            .replace("ENSINOMEDIO", "EM")
            .replace("PERIODOINTEGRAL", "")
            .replace("CENTRODEENSINOEM", "CEEM")
            .replace("UNED", "")
            .replace("COLEGIO", "")
            .replace("ESCOLA", "")
            .replace("DOUTOR", "DR")
            .replace("PROFESSOR", "PROF")
        )
    elif type == "tok":
        return (
            re.sub(r"[^\w\s]", "", unidecode(str(s)).upper())
            .replace("PRIMEIRO E SEGUNDO GRAUS", "")
            .replace("PRIMEIRO E SEGUNDO GRAU", "")
            .replace("PROFISSIONALIZANTE", "")
            .replace("ESCOLA DE 1 E 2 GRAU", "")
            .replace("ESC EST 1 E 2 GRAUS", "")
            .replace("ESC DE 1 E 2 GRAU", "")
            .replace("EE DE 1 E 2 GRAU", "")
            .replace("E E 2 GRAU", "")
            .replace("E E 1 E 2 GRAU", "")
            .replace("1 E 2 GRAUS", "")
            .replace("1 E 2 GRAU", "")
            .replace("2 GRAU", "")
            .replace("2O GRAU", "")
            .replace("2OGRAU", "")
            .replace("CEES", "")
            .replace("E E I E E F", "")
            .replace("E E E P S G", "")
            .replace("E E P G G", "")
            .replace("E E P G", "")
            .replace("EEIPSGES", "")
            .replace("EEIEFEM", "")
            .replace("EMPSGES", "")
            .replace("EPSGEI", "")
            .replace("EMEFMP", "")
            .replace("EIEFEM", "")
            .replace("EEIEFM", "")
            .replace("EEIPSG", "")
            .replace("EMEFEM", "")
            .replace("EPSGE", "")
            .replace("EEPSG", "")
            .replace("IIPSG", "")
            .replace("EEIPG", "")
            .replace("EMPSG", "")
            .replace("EEENS", "")
            .replace("EEPEM", "")
            .replace("ERPSG", "")
            .replace("EPSG", "")
            .replace("EEMF", "")
            .replace("EEBP", "")
            .replace("EEFM", "")
            .replace("EFMT", "")
            .replace("EMSG", "")
            .replace("EEPG", "")
            .replace("EIEF", "")
            .replace("EESG", "")
            .replace("EMEF", "")
            .replace("EIE", "")
            .replace("EEB", "")
            .replace("EFM", "")
            .replace("PSG", "")
            .replace("EEI", "")
            .replace("EPE", "")
            .replace("EME ", "")
            .replace("ENS ", "")
            .replace("ESG", "")
            .replace("IEE", "")
            .replace("LTDA", "")
            .replace("CAMPUS", "")
            .replace("COL ", "")
            .replace("ENSINO MEDIO", "")
            .replace("MEDIO", "")
            .replace("ORGANIZACAO", "")
            .replace("UNED ", "")
            .replace("PERIODO INTEGRAL", "")
            .replace("CENTRO EDUCACIONAL", "")
            .replace("ENSINO FUNDAMENTAL", "")
            .replace("FUNDAMENTAL", "")
            .replace("INFANTIL", "")
            .replace("ESTADUAL", "")
            .replace("ESCOLA MUNICIPAL", "")
            .replace("CENTRO DE ENSINO", "")
            .replace("MUNICIPAL", "")
            .replace("DOUTOR", "DR")
            .replace("PROFESSOR", "PROF")
            .replace("FUNDAMENTAL", "")
            .replace("FUND ", "")
            .replace("FUN ", "")
            .strip()
        )


def standardize_key(i, type):
    if type == "seq":
        return (
            standardize_str(i["escola"], type=type)
            + re.sub(r"[^\w]", "", unidecode(str(i["municipio"])).upper())
            + i["UF"]
        )
    elif type == "tok":
        return (
            standardize_str(i["escola"], type=type)
            + " "
            + re.sub(r"[^\w\s]", "", unidecode(str(i["municipio"])).upper())
            + " "
            + i["UF"]
        )


def get_tokens(s):
    if len(s) <= 3:
        return [s]

    return [s[:3]] + [s[-3:]] + (get_tokens(s[1:-1]) if len(s[1:-1]) >= 3 else [])


def get_match(i, escolas, by, cutoff):
    if by == "seq":
        return (
            difflib.get_close_matches(
                i["chave_seq"], escolas[i["UF"]]["chave_seq"], cutoff=cutoff
            )[:1]
            or [None]
        )[0]
    elif by == "tok":
        # para o matching por tokens, escolas é uma tupla contendo (chave original e chave tokenizada)
        best_match = 0
        best_key = pd.NA

        for tok_key in escolas[i["UF"]]:
            tokens_src = get_tokens(i["chave_tok"])

            similarity = textdistance.sorensen(tokens_src, tok_key[1])
            if similarity > best_match and similarity >= cutoff:
                best_match = similarity
                best_key = tok_key[0]

        return best_key


def validation():
    df_inep = read_auxiliary("INEP data.csv", dtype=object, sep=";").loc[
        :,
        [
            "Escola",
            "Código INEP",
            "UF",
            "Município",
            "Etapas e Modalidade de Ensino Oferecidas",
        ],
    ]
    df_fechadas = read_auxiliary(
        "cadescfechadassh19952021.csv", dtype=object, sep=";", encoding="latin1"
    ).loc[:, ["NO_ENTIDADE", "CO_ENTIDADE", "SG_UF", "NO_MUNICIPIO"]]
    df_comvest = read_result("dados_comvest.csv", dtype=DTYPES_DADOS)
    # df_dac = read_output("dados_cadastrais.csv")

    df_fechadas.insert(
        loc=len(df_fechadas.columns),
        column="Etapas e Modalidade de Ensino Oferecidas",
        value="Médio",
    )
    df_fechadas.columns = df_inep.columns

    base_escolas = pd.concat([df_inep, df_fechadas])
    base_escolas.columns = [
        "escola",
        "Código INEP",
        "UF",
        "municipio",
        "Etapas e Modalidade de Ensino Oferecidas",
    ]

    comvest_esc = df_comvest.loc[:, ["esc_em_c", "mun_esc_em_c", "uf_esc_em"]]
    # dac_esc = df_dac.loc[:, ["escola_em_d", "mun_esc_form_em", "uf_esc_form_em"]]
    COLUMNS = ["escola", "municipio", "UF"]
    comvest_esc.columns = COLUMNS
    # dac_esc.columns, comvest_esc.columns = COLUMNS, COLUMNS

    # Pré-processamentos
    comvest_esc = comvest_esc[comvest_esc["UF"].isin(ESTADOS)]
    # dac_esc = dac_esc[dac_esc["UF"].isin(ESTADOS)]
    comvest_esc = comvest_esc.dropna()
    # dac_esc = dac_esc.dropna()

    comvest_esc = comvest_esc[
        ~comvest_esc["escola"].isin(
            ["ENEM", "ENCCEJA", "EJA", "NAN", "", "0", "1", "00", "000"]
        )
    ]
    """
    dac_esc = dac_esc[
        ~dac_esc["escola"].isin(
            ["ENEM", "ENCCEJA", "EJA", "NAN", "", "0", "1", "00", "000"]
        )
    ]
    """
    comvest_esc = comvest_esc[~comvest_esc["municipio"].isin(["NAN", ""])]

    base_escolas = base_escolas[
        base_escolas["Etapas e Modalidade de Ensino Oferecidas"].str.contains(
            "Médio", regex=False, na=False
        )
    ]

    comvest_esc["chave_seq"] = comvest_esc.apply(
        lambda r: standardize_key(r, type="seq"), axis=1
    )
    """
    dac_esc["chave_seq"] = dac_esc.apply(
        lambda r: standardize_key(r, type="seq"), axis=1
    )
    """
    base_escolas["chave_seq"] = base_escolas.apply(
        lambda r: standardize_key(r, type="seq"), axis=1
    )

    comvest_esc["chave_tok"] = comvest_esc.apply(
        lambda r: standardize_key(r, type="tok"), axis=1
    )
    """
    dac_esc["chave_tok"] = dac_esc.apply(
        lambda r: standardize_key(r, type="tok"), axis=1
    )
    """
    base_escolas["chave_tok"] = base_escolas.apply(
        lambda r: standardize_key(r, type="tok"), axis=1
    )

    comvest_esc.drop_duplicates(subset="chave_seq", inplace=True)
    # dac_esc.drop_duplicates(subset="chave_seq", inplace=True)
    base_escolas.drop_duplicates(subset="chave_seq", inplace=True)

    comvest_esc.drop_duplicates(subset="chave_tok", inplace=True)
    # dac_esc.drop_duplicates(subset="chave_tok", inplace=True)
    base_escolas.drop_duplicates(subset="chave_tok", inplace=True)

    # Sample para teste
    comvest_esc = comvest_esc.sample(frac=0.05)

    escolas = {
        uf: base_escolas[base_escolas["UF"] == uf][["chave_seq", "chave_tok"]]
        for uf in ESTADOS
    }

    comvest_esc["chave_seq"] = comvest_esc.apply(
        lambda k: get_match(k, escolas, by="seq", cutoff=0.85), axis=1
    )
    """
    dac_esc["chave_seq"] = dac_esc.apply(
        lambda k: get_match(k, escolas, by="seq", cutoff=0.8), axis=1
    )
    """

    # dac_etapaTokens = dac_esc[dac_esc["chave_seq"].isna()]
    comvest_etapaTokens = comvest_esc[comvest_esc["chave_seq"].isna()]

    escolas_triplets = defaultdict(list, {uf: [] for uf in ESTADOS})
    for uf in ESTADOS:
        for key in escolas[uf]["chave_tok"]:
            escolas_triplets[uf].append((key, get_tokens(key)))

    print(escolas_triplets["SP"])
    """
    dac_etapaTokens["chave_tok"] = dac_etapaTokens.apply(
        lambda k: get_match(k, escolas_triplets, by="tok", cutoff=0.7), axis=1
    )
    """

    comvest_etapaTokens["chave_tok"] = comvest_etapaTokens.apply(
        lambda k: get_match(k, escolas_triplets, by="tok", cutoff=0.7), axis=1
    )

    sem_match = comvest_etapaTokens[comvest_etapaTokens["chave_tok"].isna()]

    res = comvest_esc.merge(
        base_escolas, on="chave_seq", suffixes=("_base", "_inep")
    ).drop(columns=["chave_tok_base", "chave_tok_inep"])
    res_etapaTokens = comvest_etapaTokens.merge(
        base_escolas, on="chave_tok", suffixes=("_base", "_inep")
    ).drop(columns=["chave_seq_base", "chave_seq_inep"])

    res = pd.concat([res, res_etapaTokens])

    # res['confianca'] = res.apply(get_ratio, axis=1)
    # res.sort_values(by=['confianca'], ascending=False, inplace=True)

    res.to_csv("comvest_inep_test.csv", index=False)
    sem_match.to_csv("comvest_inep_test_null.csv", index=False)
    # merged_dados.to_csv('teste_dados_dac-co80.csv', index=False)
