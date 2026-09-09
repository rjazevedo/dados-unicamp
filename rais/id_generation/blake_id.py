"""
Gera um identificador externo estavel por CPF via BLAKE2s (hash com chave),
complementar ao ID sequencial atual (random_index.py, que usa pd.factorize
sobre a populacao embaralhada inteira -- muda entre execucoes porque depende
de todo o resto da base presente naquela rodada, nao so do CPF individual).

Integrado a partir de 2026-09-08 (commit da migracao): random_index.py grava
os dois IDs lado a lado em dac_comvest_ids.csv (coluna "id" = sequencial,
"id_blake2s" = este) -- decisao deliberada do usuario de manter os dois
durante o periodo de migracao, nao substituir de uma vez.
"""

import base64
import hashlib
import secrets
from pathlib import Path

# Onde a chave de producao fica (gerada e guardada em 2026-09-07, fora de
# /home/input/ de proposito -- ver discussao no plan.md). So essa chave
# precisa ficar em segredo; person/versao abaixo nao sao sensiveis.
SECRET_KEY_PATH = Path.home() / ".config/dados-unicamp/secrets/blake2s_cpf.key"

# 10 bytes (80 bits) de digest. Com a base de dados ficando restrita a poucas
# pessoas controladas (nao publico amplo), o risco relevante e colisao
# acidental (2 pessoas reais caindo no mesmo ID), nao correlacao adversaria
# entre releases publicos ao longo de anos -- 80 bits cobre folgadamente
# ate dezenas de milhoes de linhas pela regra do aniversario (N=10^7 ainda
# deixa a chance de colisao muito abaixo de 1 em 1 bilhao).
DIGEST_SIZE = 10

# Separador de dominio fixo (8 bytes, limite do BLAKE2s pra person=) --
# garante que esta chave, se um dia reaproveitada em outro contexto por
# engano, nao produz o mesmo hash que aqui.
PERSON = b"dadosuni"
assert len(PERSON) == hashlib.blake2s.PERSON_SIZE

# Versao da chave/epoca. So incrementar quando a chave for rotacionada de
# verdade (evento raro) -- cada versao usa um salt derivado diferente, entao
# a MESMA chave com versoes diferentes produz IDs diferentes, protegendo
# contra reaproveitar por engano um digest de uma epoca em outra. O numero
# da versao vira prefixo public no ID final (estilo salt do crypt(3) antigo
# -- e seguro expor QUAL epoca gerou o ID, o segredo de verdade e so a
# chave).
CURRENT_VERSION = 1


def generate_secret_key(n_bytes: int = 16) -> str:
    """
    Gera uma chave nova, em hex, pra salvar no arquivo de segredo. Uso
    manual/setup (ex. `python3 -c "from rais.id_generation.blake_id import
    generate_secret_key as g; print(g())"` > arquivo de segredo), nunca
    chamado durante a execucao normal do pipeline.
    """
    return secrets.token_hex(n_bytes)


def load_secret_key(path: str) -> bytes:
    """Le a chave (hex, 1 linha) de um arquivo fora do repositorio git."""
    with open(path, "r") as f:
        hex_key = f.read().strip()
    key = bytes.fromhex(hex_key)
    if not (1 <= len(key) <= hashlib.blake2s.MAX_KEY_SIZE):
        raise ValueError(
            f"chave invalida: {len(key)} bytes "
            f"(esperado 1-{hashlib.blake2s.MAX_KEY_SIZE})"
        )
    return key


def _salt_for_version(version: int) -> bytes:
    salt_size = hashlib.blake2s.SALT_SIZE
    salt = str(version).encode()
    if len(salt) > salt_size:
        raise ValueError(f"versao {version} nao cabe no salt ({salt_size} bytes)")
    return salt.rjust(salt_size, b"0")


def generate_blake_id(cpf: str, key: bytes, version: int = CURRENT_VERSION) -> str:
    """
    cpf: string ja normalizada, 11 digitos numericos -- mesma forma que
    validar_CPF() (dac/uniao_dac_comvest/utilities.py) retorna quando
    valido. Formas diferentes do mesmo CPF (com pontuacao, zero-padding
    distinto, etc.) gerariam IDs diferentes pro mesmo CPF real -- normalizar
    ANTES de chamar esta funcao, ela so valida o formato, nao normaliza.
    """
    if not (isinstance(cpf, str) and len(cpf) == 11 and cpf.isdigit()):
        raise ValueError(f"cpf deve ser string de 11 digitos, recebido: {cpf!r}")

    digest = hashlib.blake2s(
        cpf.encode(),
        digest_size=DIGEST_SIZE,
        key=key,
        person=PERSON,
        salt=_salt_for_version(version),
    ).digest()

    encoded = base64.b32encode(digest).decode().rstrip("=")
    return f"{version}-{encoded}"


def generate_blake_id_column(cpf_series, key: bytes, version: int = CURRENT_VERSION):
    """
    Aplica generate_blake_id() numa coluna inteira (ex. df["cpf"]) de uma
    vez. Linhas sem CPF valido (formato != 11 digitos -- inclui o sentinela
    "-" usado no resto do pipeline pra "sem CPF") viram None: sem CPF real
    nao ha ID estavel possivel, e o ID sequencial ("id") continua cobrindo
    esses casos como sempre cobriu.
    """
    def safe(cpf):
        if not (isinstance(cpf, str) and len(cpf) == 11 and cpf.isdigit()):
            return None
        return generate_blake_id(cpf, key, version)

    return cpf_series.map(safe)


def check_collisions(ids) -> list:
    """
    Recebe um iteravel de IDs ja gerados e retorna os que colidiram
    (apareceram mais de uma vez). Checagem barata pra rodar depois de gerar
    a populacao inteira, nao substitui a analise de margem teorica, e sim
    complementa -- roda em cima do resultado real.
    """
    seen = {}
    dups = set()
    for i in ids:
        if i in seen:
            dups.add(i)
        else:
            seen[i] = True
    return sorted(dups)
