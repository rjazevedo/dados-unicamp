from collections import defaultdict
import pandas as pd
import swifter
import difflib
import textdistance
import re
from unidecode import unidecode
from comvest.utilities.io import read_auxiliary, write_auxiliary
from comvest.utilities.io import read_result, read_output, write_result
from comvest.escolas.inep_base import load_inep_base
from comvest.escolas.escolas_base import load_esc_bases
from comvest.escolas.utility import standardize_str
from comvest.escolas.utility import get_match
from collections import Counter


def validation():
    inep = load_inep_base()
    escs = load_esc_bases()

    escs["chave_seq"] = escs['escola'].apply(lambda r: standardize_str(r))
    inep["chave_seq"] = inep['escola'].apply(lambda r: standardize_str(r))

    esc_dict = create_escs_dict(escs, inep)
    escs = get_closest_schools(esc_dict, inep)
    result = pd.merge(escs, inep, on=['codigo_municipio', 'chave_seq'], how='left', suffixes=("_base", "_inep"))

    filt = result['escola_inep'].isnull()
    print(result[~filt].shape[0] / result.shape[0])
    #result = result.sort_values(by=['codigo_municipio'], ascending=True)

    no_match = result[filt]

    write_auxiliary(no_match, "escolas_sem_match.csv")
    write_auxiliary(result, "escs_tudo_junto.csv")
    

def get_closest_schools(esc_dict, inep):
    dfs = []
    soma = 0

    maior_comvest = 0
    maior_inep = 0

    for key, value in esc_dict.items():
        escolas = inep[inep['codigo_municipio'] == key]
        new_df = value.copy()
        new_df["chave_seq"] = value['chave_seq'].apply(lambda k: get_match(k, escolas['chave_seq'], cutoff=0.65))
        dfs.append(new_df)

        if value.shape[0] > maior_comvest:
            maior_comvest = value.shape[0]
            maior_inep = escolas.shape[0]

        if (soma % 100) == 0:
            print(f'{soma}/5541 -> code:{key} /// {maior_comvest} escolas com {maior_inep} inep') 
            maior_comvest = 0

        #if (soma == 1000):
        #    break

        soma += 1

    final_df = pd.concat(dfs)
    return final_df


def create_escs_dict(esc, inep):
    uf_codes = inep['codigo_municipio'].unique()
    escolas = esc.copy()
    dict = {}
    for code in uf_codes:
        filt = (escolas['codigo_municipio'] == code)
        dict[code] = escolas[filt]

    return dict