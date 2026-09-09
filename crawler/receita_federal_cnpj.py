"""
Crawler pra base CNPJ da Receita Federal (empresa/estabelecimentos/socios/
simples), via o novo repositorio publico em Nextcloud
(https://arquivos.receitafederal.gov.br/index.php/s/YggdBLfdninEJX9) --
substitui a fonte antiga (dadosabertos.rfb.gov.br, scraping de HTML fragil
por posicao fixa de linha/coluna, achado morto desde ~marco/2023, ver
plan.md Fase 4).

A nova fonte e um share publico do Nextcloud com 1 pasta por mes
("YYYY-MM/"), cada uma com os mesmos arquivos que o pipeline ja consome
(Empresas0-9.zip, Estabelecimentos0-9.zip, Socios0-9.zip, Simples.zip) --
acessivel via WebDAV (PROPFIND), estruturado, sem scraping de HTML.

Dedup: nunca baixa um mes que ja tem pasta local NAO-VAZIA em
/home/input/<base>/<mes>-01/ (mesma convencao de pasta que o pipeline ja usa
hoje -- "-01" acrescentado porque o pipeline exige data ISO completa
[date.fromisoformat], ver simples/extract.py::most_recent_non_empty_folder).

Uso:
  uv run python3 -m crawler.receita_federal_cnpj --list                 # so lista, nao baixa nada
  uv run python3 -m crawler.receita_federal_cnpj --dry-run              # mostra o que baixaria
  uv run python3 -m crawler.receita_federal_cnpj                        # baixa todos os meses faltando
  uv run python3 -m crawler.receita_federal_cnpj --month 2023-05        # baixa so 1 mes especifico
  uv run python3 -m crawler.receita_federal_cnpj --base socio           # restringe a 1 base
"""

import argparse
import grp
import os
import re
import zipfile
from pathlib import Path
from xml.etree import ElementTree

import requests

# Maquina compartilhada -- outras pastas de input (empresa/estabelecimentos/
# socios/simples) usam grupo "dados" + permissao aberta (rwxrwxrwx). Achado
# real: pasta recem-criada pelo crawler saiu com grupo "rodolfo" default,
# destoando do resto -- corrigido apos cada mes baixado (ver download_month).
SHARED_GROUP = "dados"

SHARE_URL = "https://arquivos.receitafederal.gov.br"
SHARE_TOKEN = "YggdBLfdninEJX9"
WEBDAV_BASE = f"{SHARE_URL}/public.php/webdav"

# prefixo do nome do arquivo remoto -> nome da base local (bate com os
# modulos empresa/, estabelecimento/, socio/, simples/ do pipeline)
FILE_PREFIX_TO_BASE = {
    "Empresas": "empresa",
    "Estabelecimentos": "estabelecimento",
    "Socios": "socio",
    "Simples": "simples",
}

# path_input configurado em cada <base>/configuration.yaml -- mantido aqui
# em vez de importar (evita acoplar o crawler aos pacotes do pipeline, que
# tem imports pesados/efeitos colaterais nao relacionados a isso)
LOCAL_INPUT_PATH = {
    "empresa": Path("/home/input/empresa"),
    "estabelecimento": Path("/home/input/estabelecimentos"),
    "socio": Path("/home/input/socios"),
    "simples": Path("/home/input/simples"),
}

DAV_NS = {"d": "DAV:"}


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


def list_remote_months():
    entries = _propfind()
    months = []
    for e in entries:
        if not e["is_dir"]:
            continue
        name = e["href"].rstrip("/").split("/")[-1]
        if re.fullmatch(r"\d{4}-\d{2}", name):
            months.append(name)
    return sorted(months)


def list_remote_files(month):
    entries = _propfind(f"{month}/")
    files = []
    for e in entries:
        if e["is_dir"]:
            continue
        name = e["href"].split("/")[-1]
        if name:
            files.append({"name": name, "size": e["size"]})
    return files


def classify_file(filename):
    for prefix, base in FILE_PREFIX_TO_BASE.items():
        if filename.startswith(prefix):
            return base
    return None  # tabelas de referencia (Cnaes, Motivos, Municipios, etc.) -- ignoradas por ora


_SHARD_RE = re.compile(r"^(Empresas|Estabelecimentos|Socios)(\d+)(-RF\d+)?\.zip$")


# Achado real (nao teorico, 2023-08): alguns meses tem o mesmo shard listado
# 2x -- uma vez com nome liso ("Estabelecimentos6.zip") e outra com sufixo
# "-RF<numero>" ("Estabelecimentos6-RF0819000032530.zip"). A versao lisa as
# vezes esta CORROMPIDA na propria fonte (baixa exatamente o tamanho que o
# servidor anuncia, mas nao e um zip valido -- nao e erro de download nosso)
# -- o sufixo "-RF..." parece ser a substituicao/correcao publicada depois,
# deixada ao lado da versao quebrada em vez de substitui-la. Quando as duas
# existem pro mesmo (prefixo, numero do shard), mantem so a "-RF...":
# mais nova e nao tem motivo pra baixar (e arriscar) a versao provavelmente
# quebrada.
def _dedupe_replaced_shards(files):
    by_shard = {}
    for f in files:
        m = _SHARD_RE.match(f["name"])
        if not m:
            by_shard.setdefault(f["name"], []).append(f)  # nao-sharded (ex. Simples.zip)
            continue
        key = (m.group(1), m.group(2))
        by_shard.setdefault(key, []).append(f)

    result = []
    for key, group in by_shard.items():
        if len(group) == 1:
            result.append(group[0])
            continue
        rf_versions = [f for f in group if "-RF" in f["name"]]
        chosen = rf_versions[-1] if rf_versions else group[-1]
        skipped = [f["name"] for f in group if f is not chosen]
        print(f"  (varias versoes do shard {key}, usando '{chosen['name']}', pulando {skipped})")
        result.append(chosen)
    return result


def local_month_folder(base, month):
    return LOCAL_INPUT_PATH[base] / f"{month}-01"


def already_downloaded(base, month):
    folder = local_month_folder(base, month)
    return folder.is_dir() and any(f.is_file() for f in folder.iterdir())


DOWNLOAD_RETRIES = 3


# Retry com backoff -- roda sem supervisao (ver run_unattended.sh), entao um
# erro transitorio de rede nao pode derrubar a noite inteira de download.
def _download_file(remote_name, month, dest_dir):
    url = f"{WEBDAV_BASE}/{month}/{remote_name}"
    dest = dest_dir / remote_name
    tmp = dest_dir / (remote_name + ".part")

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
            print(f"  aviso: tentativa {attempt}/{DOWNLOAD_RETRIES} falhou pra '{remote_name}': {e}")
            tmp.unlink(missing_ok=True)
    raise last_err


def _extract_and_cleanup(dest_dir):
    bad_files = []
    for zip_path in dest_dir.glob("*.zip"):
        try:
            with zipfile.ZipFile(zip_path, "r") as zf:
                zf.extractall(dest_dir)
        except zipfile.BadZipFile:
            # Nao derruba o mes/base inteiro por causa de 1 arquivo -- fica
            # registrado e o .zip permanece (nao apaga) pra inspecao manual.
            print(f"  !!! AVISO: '{zip_path.name}' nao e um zip valido, pulando (nao apagado)")
            bad_files.append(zip_path.name)
            continue
        zip_path.unlink()
    return bad_files


def _fix_shared_permissions(dest_dir):
    try:
        gid = grp.getgrnam(SHARED_GROUP).gr_gid
    except KeyError:
        return  # grupo nao existe nesta maquina -- no-op, nao trava o crawler
    for root, dirs, files in os.walk(dest_dir):
        for name in dirs + files:
            path = os.path.join(root, name)
            try:
                os.chmod(path, 0o777)
                os.chown(path, -1, gid)
            except PermissionError:
                pass  # dono diferente (ex. outro usuario), sem permissao pra chown -- ignora
    try:
        os.chmod(dest_dir, 0o777)
        os.chown(dest_dir, -1, gid)
    except PermissionError:
        pass


def download_month(month, bases=None, dry_run=False):
    bases = bases or list(LOCAL_INPUT_PATH)
    remote_files = list_remote_files(month)

    by_base = {}
    for f in remote_files:
        base = classify_file(f["name"])
        if base is None or base not in bases:
            continue
        by_base.setdefault(base, []).append(f)

    for base, files in by_base.items():
        files = _dedupe_replaced_shards(files)

        if already_downloaded(base, month):
            print(f"[{month}] {base}: ja baixado, pulando")
            continue

        total_mb = sum(f["size"] or 0 for f in files) / 1024 / 1024
        if dry_run:
            print(f"[{month}] {base}: baixaria {len(files)} arquivo(s), ~{total_mb:.0f}MB")
            continue

        dest_dir = local_month_folder(base, month)
        dest_dir.mkdir(parents=True, exist_ok=True)
        print(f"[{month}] {base}: baixando {len(files)} arquivo(s), ~{total_mb:.0f}MB")
        for f in files:
            _download_file(f["name"], month, dest_dir)
        bad_files = _extract_and_cleanup(dest_dir)
        _fix_shared_permissions(dest_dir)
        if bad_files:
            print(f"[{month}] {base}: OK com ressalva -- {len(bad_files)} arquivo(s) invalido(s): {bad_files}")
        else:
            print(f"[{month}] {base}: OK")


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--list", action="store_true", help="so lista os meses/arquivos remotos, nao baixa nada"
    )
    parser.add_argument(
        "--month", help="baixa so este mes (formato YYYY-MM), em vez de todos os faltando"
    )
    parser.add_argument(
        "--base",
        action="append",
        choices=list(LOCAL_INPUT_PATH),
        help="restringe a essas bases (default: todas)",
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="mostra o que baixaria, sem baixar de verdade"
    )
    args = parser.parse_args()

    months = [args.month] if args.month else list_remote_months()

    if args.list:
        for month in months:
            files = list_remote_files(month)
            print(f"{month}: {len(files)} arquivos")
            for f in files:
                base = classify_file(f["name"]) or "(ignorado)"
                status = (
                    "ja baixado"
                    if base != "(ignorado)" and already_downloaded(base, month)
                    else "faltando"
                )
                print(f"  {f['name']} ({(f['size'] or 0) / 1024 / 1024:.0f}MB) -> {base} [{status}]")
        return

    # Um mes que falhar (erro de rede esgotado, bug nao previsto, etc.) nao
    # pode travar os demais -- roda sem supervisao (ver run_unattended.sh),
    # entao registra e segue pro proximo em vez de derrubar o processo
    # inteiro. Resumo de falhas no final, pra checar depois.
    failed_months = []
    for month in months:
        try:
            download_month(month, bases=args.base, dry_run=args.dry_run)
        except Exception as e:
            print(f"!!! [{month}] FALHOU: {e!r} -- pulando pro proximo mes")
            failed_months.append(month)

    if failed_months:
        print(f"\n=== {len(failed_months)} mes(es) com falha, precisam de atencao manual: {failed_months} ===")
    else:
        print("\n=== todos os meses processados sem falha ===")


if __name__ == "__main__":
    main()
