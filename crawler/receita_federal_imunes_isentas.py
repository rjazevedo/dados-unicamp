"""
Crawler para o dataset "Entidades Imunes e Isentas de Tributos Federais" da
Receita Federal -- mesmo tipo de share publico em Nextcloud usado pelo
crawler de CNPJ (receita_federal_cnpj.py), token de share diferente.

Fonte confirmada (2026-09-09): o catalogo oficial da RFB
(gov.br/receitafederal/.../dados-abertos/beneficios-e-renuncias-fiscais/
entidades-imunes-e-isentas) redireciona pra
dados.gov.br/dados/conjuntos-dados/entidades-imunes-e-isentas-de-tributos-federais,
mas o arquivo real esta neste share Nextcloud (passado pelo usuario).

So "Imunes e Isentas" foi confirmada como ainda publicada -- Lucro
Real/Presumido/Arbitrado (os outros 3 arquivos que existiam na base antiga,
baixada manualmente ate 2023-02 em /home/luisfelipe/scraping/) nao aparecem
mais no catalogo oficial da RFB, provavelmente descontinuados (Imunes e
Isentas tem interesse publico de fiscalizacao; regime tributario de empresa
comum e informacao mais sensivel).

Diferente do crawler de CNPJ: sem pastas por mes, sem zip -- poucos arquivos
CSV fixos, um por bienio (2015-2016 .. 2023-2024) mais um dicionario de
dados. Dedup: nunca baixa de novo um arquivo que ja existe localmente com o
mesmo nome (os bienios sao fixos/historicos, nao um range que cresce mes a
mes como o CNPJ -- exceto o bienio mais recente, que pode ser substituido
por uma versao atualizada; ver --force).

Uso:
  uv run python3 -m crawler.receita_federal_imunes_isentas --list       # so lista, nao baixa nada
  uv run python3 -m crawler.receita_federal_imunes_isentas --dry-run    # mostra o que baixaria
  uv run python3 -m crawler.receita_federal_imunes_isentas              # baixa tudo que falta
  uv run python3 -m crawler.receita_federal_imunes_isentas --force      # rebaixa tudo, mesmo o que ja existe
"""

import argparse
import grp
import os
from pathlib import Path
from xml.etree import ElementTree

import requests

SHARED_GROUP = "dados"

SHARE_URL = "https://arquivos.receitafederal.gov.br"
SHARE_TOKEN = "WMNSnYsxCspS2Px"
WEBDAV_BASE = f"{SHARE_URL}/public.php/webdav"

LOCAL_INPUT_PATH = Path("/home/input/regime_tributario")

DAV_NS = {"d": "DAV:"}
DOWNLOAD_RETRIES = 3


def _propfind(remote_path=""):
    url = f"{WEBDAV_BASE}/{remote_path}"
    resp = requests.request(
        "PROPFIND", url, auth=(SHARE_TOKEN, ""), headers={"Depth": "1"}, timeout=30
    )
    resp.raise_for_status()
    root = ElementTree.fromstring(resp.content)
    entries = []
    for response in root.findall("d:response", DAV_NS):
        href = response.find("d:href", DAV_NS).text
        propstat = response.find("d:propstat", DAV_NS)
        prop = propstat.find("d:prop", DAV_NS)
        is_dir = prop.find("d:resourcetype/d:collection", DAV_NS) is not None
        size_el = prop.find("d:getcontentlength", DAV_NS)
        size = int(size_el.text) if size_el is not None else None
        entries.append({"href": href, "is_dir": is_dir, "size": size})
    return entries


def list_remote_files():
    entries = _propfind()
    files = []
    for e in entries:
        if e["is_dir"]:
            continue
        name = e["href"].split("/")[-1]
        if name:
            files.append({"name": name, "size": e["size"]})
    return sorted(files, key=lambda f: f["name"])


def already_downloaded(filename):
    return (LOCAL_INPUT_PATH / filename).is_file()


# Retry com backoff -- mesmo motivo do crawler de CNPJ: roda sem supervisao,
# erro transitorio de rede nao pode derrubar o download inteiro.
def _download_file(filename):
    url = f"{WEBDAV_BASE}/{filename}"
    dest = LOCAL_INPUT_PATH / filename
    tmp = LOCAL_INPUT_PATH / (filename + ".part")

    last_err = None
    for attempt in range(1, DOWNLOAD_RETRIES + 1):
        try:
            with requests.get(url, auth=(SHARE_TOKEN, ""), stream=True, timeout=120) as r:
                r.raise_for_status()
                with open(tmp, "wb") as f:
                    for chunk in r.iter_content(chunk_size=1024 * 1024 * 8):
                        f.write(chunk)
            tmp.rename(dest)
            return
        except requests.exceptions.RequestException as e:
            last_err = e
            print(f"  aviso: tentativa {attempt}/{DOWNLOAD_RETRIES} falhou pra '{filename}': {e}")
            tmp.unlink(missing_ok=True)
    raise last_err


def _fix_shared_permissions():
    try:
        gid = grp.getgrnam(SHARED_GROUP).gr_gid
    except KeyError:
        return  # grupo nao existe nesta maquina -- no-op, nao trava o crawler
    for name in os.listdir(LOCAL_INPUT_PATH):
        path = LOCAL_INPUT_PATH / name
        try:
            os.chmod(path, 0o777)
            os.chown(path, -1, gid)
        except PermissionError:
            pass  # dono diferente, sem permissao pra chown -- ignora


def download_all(force=False, dry_run=False):
    LOCAL_INPUT_PATH.mkdir(parents=True, exist_ok=True)
    files = list_remote_files()

    for f in files:
        name, size_mb = f["name"], (f["size"] or 0) / 1024 / 1024
        if not force and already_downloaded(name):
            print(f"{name}: ja baixado, pulando")
            continue
        if dry_run:
            print(f"{name}: baixaria, ~{size_mb:.0f}MB")
            continue
        print(f"{name}: baixando, ~{size_mb:.0f}MB")
        _download_file(name)
        print(f"{name}: OK")

    if not dry_run:
        _fix_shared_permissions()


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--list", action="store_true", help="so lista os arquivos remotos, nao baixa nada")
    parser.add_argument("--dry-run", action="store_true", help="mostra o que baixaria, sem baixar de verdade")
    parser.add_argument("--force", action="store_true", help="rebaixa mesmo o que ja existe localmente")
    args = parser.parse_args()

    if args.list:
        for f in list_remote_files():
            status = "ja baixado" if already_downloaded(f["name"]) else "faltando"
            print(f"  {f['name']} ({(f['size'] or 0) / 1024 / 1024:.0f}MB) [{status}]")
        return

    download_all(force=args.force, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
