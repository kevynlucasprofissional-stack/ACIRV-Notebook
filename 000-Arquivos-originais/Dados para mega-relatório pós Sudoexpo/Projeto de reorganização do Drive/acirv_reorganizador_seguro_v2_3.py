#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ACIRV MIGRATION ENGINE V2
=========================
Migrador transacional e auditável para o acervo ACIRV.

DESIGN DE SEGURANÇA
-------------------
1. Auditoria é somente leitura em F: e H:. Todo estado é salvo fora desses volumes.
2. SHA-256 é calculado para todos os arquivos dentro do escopo antes de gerar plano.
3. Nenhum item C (provável) ou D (ambíguo) pode chegar à execução.
4. Por padrão, só A (regra explícita aprovada) e E (legado aprovado) executam.
   B (comprovado por múltiplas evidências) exige liberação explícita no plano.
5. Nenhum overwrite. Destino aparecido depois do plano bloqueia a operação.
6. Mesmo volume: rename atômico, após validação de hash/metadata e lock de leitura.
7. Entre volumes: copy temporária -> fsync -> SHA-256 -> publish atômico ->
   SHA-256 final -> origem para quarentena (nunca apagada).
8. Journal SQLite FULL+WAL. Operações são retomáveis.
9. Rollback preserva bytes; não sobrescreve arquivos modificados depois da migração.
10. Manifesto pós-migração compara o multiconjunto de hashes: nenhum conteúdo
    esperado pode desaparecer.
11. Verificação remota opcional via rclone check --download; quando habilitada,
    REMOTE_VERIFIED=PASS é necessária para considerar a migração completa.

IMPORTANTE
----------
A primeira execução recomendada é SOMENTE "NOVA AUDITORIA".
Não execute plano real antes de revisar grupos/regras e validar o plano.

Compatibilidade de execução real: Windows 10/11, Python 3.10+.
Self-tests funcionam também em POSIX usando volumes simulados.
"""
from __future__ import annotations

import argparse
import base64
import contextlib
import concurrent.futures
import csv
import ctypes
import datetime as dt
import hashlib
import html
import importlib
import json
import mimetypes
import os
import re
import shutil
import sqlite3
import stat
import subprocess
import sys
import tempfile
import threading
import time
import traceback
import unicodedata
import uuid
from collections import Counter, defaultdict
from dataclasses import dataclass, asdict
from pathlib import Path, PureWindowsPath
from typing import Any, BinaryIO, Callable, Iterable, Iterator, Optional, Sequence

APP_NAME = "ACIRV MIGRATION ENGINE V2.3"
APP_VERSION = "2.3.0"
CENTRAL_NAME = "ACIRV — CENTRAL"
ARCHIVE_NAME = "ACIRV — ARQUIVO MESTRE"
STATE_FOLDER_NAME = "ACIRV_MIGRATION_V2_STATE"
RULES_NAME = "regras_aprovadas.yaml"
RULES_SIG_NAME = "regras_aprovadas.yaml.sha256"
DB_NAME = "migration_v2.sqlite3"
DEFAULT_RESERVE_GB = 20
COPY_CHUNK = 8 * 1024 * 1024
MAX_SAFE_DEST_PATH = 238
MAX_FILENAME = 180
DEFAULT_AUDIT_WORKERS = 12
MAX_AUDIT_WORKERS = 12
CHECKPOINT_JSON_NAME = "AUDIT_CHECKPOINT.json"

LEVEL_A = "A"
LEVEL_B = "B"
LEVEL_C = "C"
LEVEL_D = "D"
LEVEL_E = "E"
LEVELS = {LEVEL_A, LEVEL_B, LEVEL_C, LEVEL_D, LEVEL_E}
EXECUTABLE_DEFAULT = {LEVEL_A, LEVEL_E}

STATUS_PLANNED = "PLANNED"
STATUS_COPYING = "COPYING"
STATUS_COPIED = "COPIED"
STATUS_HASH_VERIFIED = "HASH_VERIFIED"
STATUS_PUBLISHED = "PUBLISHED"
STATUS_SOURCE_QUARANTINED = "SOURCE_QUARANTINED"
STATUS_REMOTE_VERIFIED = "REMOTE_VERIFIED"
STATUS_DONE = "DONE"
STATUS_FAILED = "FAILED"
STATUS_SKIPPED_CHANGED = "SKIPPED_LOCKED_OR_CHANGED"
STATUS_ROLLBACK_DONE = "ROLLBACK_DONE"
STATUS_ROLLBACK_BLOCKED = "ROLLBACK_BLOCKED_MODIFIED"

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".heic", ".heif", ".jfif", ".tif", ".tiff", ".bmp", ".avif"}
VIDEO_EXTS = {".mp4", ".mov", ".m4v", ".avi", ".mkv", ".mts", ".m2ts", ".webm", ".3gp"}
AUDIO_EXTS = {".mp3", ".m4a", ".wav", ".aac", ".flac", ".ogg", ".opus"}
DESIGN_EXTS = {".psd", ".ai", ".cdr", ".eps", ".svg", ".indd", ".afdesign", ".fig", ".xd"}
DOC_EXTS = {".pdf", ".doc", ".docx", ".odt", ".rtf", ".txt", ".md", ".ppt", ".pptx", ".odp", ".xls", ".xlsx", ".xlsm", ".csv", ".ods", ".gdoc", ".gsheet", ".gform", ".gslides"}
ARCHIVE_EXTS = {".zip", ".rar", ".7z", ".tar", ".gz"}
GOOGLE_NATIVE_STUBS = {".gdoc", ".gsheet", ".gslides", ".gform"}
SYSTEM_NAMES = {"desktop.ini", "thumbs.db", ".ds_store"}
PROTECTED_F_TOP = {"$recycle.bin", "system volume information", ".trash-1000"}

DRIVE_SCOPE_PREFIXES = (
    "GESTÃO 2025 2028",
    "COMERCIAL",
    "CADASTRO DE NOVOS ASSOCIADOS – ACIRV (File responses)",
    "Possíveis associados",
    "Solicitações para agência de marketing - Comunicação (File responses)",
)

MONTHS = {
    "janeiro": "01_Janeiro", "fevereiro": "02_Fevereiro", "marco": "03_Março", "abril": "04_Abril",
    "maio": "05_Maio", "junho": "06_Junho", "julho": "07_Julho", "agosto": "08_Agosto",
    "setembro": "09_Setembro", "outubro": "10_Outubro", "novembro": "11_Novembro", "dezembro": "12_Dezembro",
}

# ---------------------------------------------------------------------------
# Bootstrap de dependências (nenhuma alteração em F:/H: ocorre aqui)
# ---------------------------------------------------------------------------

def ensure_dependency(module: str, package: str) -> None:
    """Instala automaticamente uma dependência ausente sem tocar em F:/H:.

    Tenta pip normal, recupera pip via ensurepip quando necessário e, por fim,
    tenta instalação no escopo do usuário (útil em Windows sem privilégios de admin).
    """
    try:
        importlib.import_module(module)
        return
    except ImportError:
        pass

    print(f"[setup] Dependência ausente: {package}")
    base = [sys.executable, "-m", "pip", "install", "--disable-pip-version-check", package]
    attempts = [base, base[:-1] + ["--user", package]]

    for idx, cmd in enumerate(attempts, 1):
        print(f"[setup] Tentativa {idx}: {' '.join(cmd)}")
        proc = subprocess.run(cmd)
        if proc.returncode == 0:
            importlib.invalidate_caches()
            try:
                importlib.import_module(module)
                return
            except ImportError:
                pass
        if idx == 1:
            # Alguns Python embutidos/novos chegam sem pip inicializado.
            subprocess.run([sys.executable, "-m", "ensurepip", "--upgrade"],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    raise SystemExit(
        f"Falha ao instalar {package}. Nenhum dado de F:/H: foi alterado. "
        "Verifique acesso à internet/permissões do Python e execute novamente."
    )


def bootstrap_tui() -> None:
    # Tudo que a interface e a auditoria enriquecida usam é auto-instalável.
    ensure_dependency("rich", "rich>=13.7,<15")
    ensure_dependency("questionary", "questionary>=2.0,<3")
    ensure_dependency("yaml", "PyYAML>=6.0,<7")
    ensure_dependency("PIL", "Pillow>=10,<13")


# imports TUI são atrasados para --self-test não depender de instalação.
console = None
questionary = None
_yaml = None


def load_tui_modules() -> None:
    global console, questionary, _yaml
    bootstrap_tui()
    from rich.console import Console
    import questionary as q
    import yaml as y
    console = Console()
    questionary = q
    _yaml = y

# ---------------------------------------------------------------------------
# Utilitários puros
# ---------------------------------------------------------------------------

def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")


def ntext(value: str) -> str:
    value = unicodedata.normalize("NFKD", str(value))
    value = "".join(c for c in value if not unicodedata.combining(c))
    value = value.lower().replace("º", "o").replace("ª", "a")
    value = re.sub(r"[^a-z0-9]+", " ", value)
    return re.sub(r"\s+", " ", value).strip()


def bytes_human(n: int) -> str:
    v = float(n)
    for u in ("B", "KB", "MB", "GB", "TB"):
        if v < 1024 or u == "TB":
            return f"{int(v)} B" if u == "B" else f"{v:.1f} {u}"
        v /= 1024
    return str(n)


def sha256_file(path: Path, chunk: int = COPY_CHUNK, on_bytes: Optional[Callable[[int], None]] = None) -> str:
    h = hashlib.sha256()
    with path.open("rb", buffering=0) as f:
        while True:
            b = f.read(chunk)
            if not b:
                return h.hexdigest()
            h.update(b)
            if on_bytes:
                on_bytes(len(b))


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def atomic_write_bytes(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + f".tmp-{uuid.uuid4().hex}")
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    fd = os.open(tmp, flags, 0o600)
    try:
        with os.fdopen(fd, "wb", closefd=True) as f:
            f.write(data)
            f.flush(); os.fsync(f.fileno())
        os.replace(tmp, path)
        fsync_dir(path.parent)
    except Exception:
        with contextlib.suppress(FileNotFoundError):
            tmp.unlink()
        raise


def atomic_write_text(path: Path, text: str, encoding: str = "utf-8") -> None:
    atomic_write_bytes(path, text.encode(encoding))


def fsync_dir(path: Path) -> None:
    if os.name == "nt":
        return
    try:
        fd = os.open(path, os.O_RDONLY)
        try: os.fsync(fd)
        finally: os.close(fd)
    except OSError:
        pass


def same_volume(a: Path, b: Path) -> bool:
    if os.name == "nt":
        return a.drive.upper() == b.drive.upper() and bool(a.drive)
    try:
        return a.stat().st_dev == b.parent.stat().st_dev
    except Exception:
        # self-tests podem consultar antes de dst.parent existir
        return os.path.commonpath([str(a), str(b)]) == os.path.commonpath([str(a), str(b.parent)])


def path_is_relative_to(path: Path, root: Path) -> bool:
    try:
        path.resolve(strict=False).relative_to(root.resolve(strict=False)); return True
    except Exception:
        return False


def sanitize_component(name: str) -> tuple[str, bool]:
    original = name
    # Caracteres inválidos no Windows, sem remover Unicode/acento válido.
    name = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "_", name).rstrip(" .")
    if not name:
        name = "_SEM_NOME"
    if len(name) > MAX_FILENAME:
        p = Path(name)
        token = hashlib.sha256(original.encode("utf-8", errors="replace")).hexdigest()[:10]
        keep = max(20, MAX_FILENAME - len(p.suffix) - len(token) - 3)
        name = f"{p.stem[:keep]}__{token}{p.suffix}"
    return name, name != original


def sanitize_relpath(rel: Path) -> tuple[Path, list[dict[str, str]]]:
    changes = []
    parts = []
    for p in rel.parts:
        q, changed = sanitize_component(p)
        parts.append(q)
        if changed: changes.append({"from": p, "to": q})
    return Path(*parts), changes


def fit_windows_path(root: Path, rel: Path, source: Path) -> tuple[Path, list[dict[str, str]]]:
    rel2, changes = sanitize_relpath(rel)
    dst = root / rel2
    if len(str(dst)) <= MAX_SAFE_DEST_PATH:
        return rel2, changes
    token = hashlib.sha256(str(source).encode("utf-8", errors="replace")).hexdigest()[:16]
    leaf, leaf_change = sanitize_component(source.name)
    long_rel = Path("90_LEGADO — A REVISAR") / "_CAMINHOS_LONGOS" / token[:2] / token / leaf
    changes.append({"from": str(rel2), "to": str(long_rel), "reason": "caminho_longo"})
    return long_rel, changes


def infer_year(text: str, fallback: Optional[int] = None) -> Optional[int]:
    """Ano só é aceito em formas plausíveis; evita IMG_2084 -> ano 2084."""
    n = ntext(text)
    years = [int(x) for x in re.findall(r"(?<!\d)(20(?:1\d|2\d))(?!\d)", n)]
    years = [y for y in years if 2010 <= y <= 2035]
    if years:
        return years[-1]
    # datas/timestamps compactos: YYYYMMDD e YYYYMMDDHHMMSS (nomes de câmera/celular).
    m = re.search(r"(?<!\d)(20(?:1\d|2\d))[01]\d[0-3]\d", text)
    if m:
        y = int(m.group(1))
        if 2010 <= y <= 2035: return y
    return fallback


def detect_month(text: str) -> Optional[str]:
    n = ntext(text)
    for k, v in MONTHS.items():
        if re.search(rf"\b{k}\b", n): return v
    m = re.search(r"(?<!\d)(20\d{2})[-_. ]?(0[1-9]|1[0-2])(?!\d)", text)
    if m:
        idx = int(m.group(2)); return list(MONTHS.values())[idx-1]
    return None


def event_candidates(text: str) -> list[str]:
    n = ntext(text)
    patterns = [
        ("Fórum de IA", ("forum de ia", "forum ia", "1o forum de ia", "2o forum de ia")),
        ("SudoExpo", ("sudoexpo", "sudo expo")),
        ("Conecta Saúde", ("conecta saude",)),
        ("Conecta ACIRV", ("conecta acirv", "conecta 3o ed", "conecta 4o ed", "conecta 5o ed", "3o conecta", "4o conecta", "5o conecta")),
        ("Café Entre Amigos", ("cafe entre amigos",)),
        ("Café com o Presidente", ("cafe com o presidente", "cafe com presidente")),
        ("ACIRV Mulher", ("acirv mulher",)),
        ("Fórum da Indústria", ("forum da industria",)),
        ("Café da Indústria", ("cafe da industria", "cafe da manha da industria")),
    ]
    out = []
    for name, aliases in patterns:
        if any(a in n for a in aliases): out.append(name)
    # Conecta Saúde é especialização; evita dupla com Conecta ACIRV.
    if "Conecta Saúde" in out and "Conecta ACIRV" in out:
        out.remove("Conecta ACIRV")
    return out


def media_category(ext: str, text: str = "") -> str:
    n = ntext(text)
    if ext.lower() in IMAGE_EXTS: return "03_Fotos"
    if ext.lower() in VIDEO_EXTS or ext.lower() in AUDIO_EXTS: return "04_Vídeos"
    if ext.lower() in DESIGN_EXTS or any(k in n for k in ("arte", "criativo", "identidade", "logo")): return "02_Identidade e Artes"
    if ext.lower() in DOC_EXTS: return "05_Textos e Documentos"
    return "06_Outros Materiais"


def event_rel(event: str, year: Optional[int], ext: str, text: str) -> Path:
    y = str(year or "Ano a confirmar")
    return Path("02_PROJETOS E EVENTOS") / event / y / media_category(ext, text)


def mime_guess(path: Path) -> str:
    typ, enc = mimetypes.guess_type(str(path))
    return typ or (f"encoding/{enc}" if enc else "application/octet-stream")


def file_attributes(path: Path, st: os.stat_result) -> str:
    attrs = getattr(st, "st_file_attributes", None)
    if attrs is not None: return hex(int(attrs))
    flags = []
    if not os.access(path, os.W_OK): flags.append("readonly")
    if path.name.startswith("."): flags.append("hidden-ish")
    return ",".join(flags)


def is_reparse_or_symlink(path: Path, st: Optional[os.stat_result] = None) -> bool:
    try:
        if path.is_symlink(): return True
        st = st or path.lstat()
        attrs = getattr(st, "st_file_attributes", 0)
        return bool(attrs & 0x400)  # FILE_ATTRIBUTE_REPARSE_POINT
    except OSError:
        return True

# ---------------------------------------------------------------------------
# Metadados EXIF / vídeo
# ---------------------------------------------------------------------------

def extract_exif(path: Path) -> tuple[Optional[str], Optional[str]]:
    if path.suffix.lower() not in IMAGE_EXTS:
        return None, None
    try:
        import PIL.Image  # optional lazy dependency
    except ImportError:
        return None, None
    try:
        with PIL.Image.open(path) as im:
            exif = im.getexif()
            date = exif.get(36867) or exif.get(306)
            make = exif.get(271)
            model = exif.get(272)
            camera = " ".join(str(x) for x in (make, model) if x) or None
            return str(date) if date else None, camera
    except Exception:
        return None, None


def ffprobe_path() -> Optional[str]:
    return shutil.which("ffprobe")


def ffmpeg_path() -> Optional[str]:
    return shutil.which("ffmpeg")


def extract_video_meta(path: Path) -> tuple[Optional[str], Optional[float], Optional[int], Optional[int], Optional[str]]:
    if path.suffix.lower() not in VIDEO_EXTS:
        return None, None, None, None, None
    exe = ffprobe_path()
    if not exe:
        return None, None, None, None, None
    cmd = [exe, "-v", "error", "-print_format", "json", "-show_format", "-show_streams", str(path)]
    try:
        cp = subprocess.run(cmd, capture_output=True, text=True, timeout=30, check=True)
        data = json.loads(cp.stdout or "{}")
        fmt = data.get("format", {})
        tags = fmt.get("tags", {}) or {}
        creation = tags.get("creation_time")
        duration = float(fmt["duration"]) if fmt.get("duration") else None
        stream = next((s for s in data.get("streams", []) if s.get("codec_type") == "video"), {})
        return creation, duration, stream.get("width"), stream.get("height"), stream.get("codec_name")
    except Exception:
        return None, None, None, None, None

# ---------------------------------------------------------------------------
# Leitura bloqueada / estável
# ---------------------------------------------------------------------------

class LockedSource:
    """No Windows, abre GENERIC_READ compartilhando READ+DELETE, mas negando WRITE.
    Isso permite que o próprio migrador renomeie o arquivo após a cópia, enquanto
    impede novos writers e conflita com writers incompatíveis já abertos.
    Em POSIX, usa flock compartilhado como best-effort (self-test)."""
    def __init__(self, path: Path):
        self.path = path
        self.file: Optional[BinaryIO] = None
        self._handle = None

    def __enter__(self) -> BinaryIO:
        if os.name == "nt":
            import msvcrt
            kernel32 = ctypes.windll.kernel32
            GENERIC_READ = 0x80000000
            FILE_SHARE_READ = 0x00000001
            FILE_SHARE_DELETE = 0x00000004
            OPEN_EXISTING = 3
            FILE_ATTRIBUTE_NORMAL = 0x80
            FILE_FLAG_SEQUENTIAL_SCAN = 0x08000000
            INVALID_HANDLE_VALUE = ctypes.c_void_p(-1).value
            CreateFileW = kernel32.CreateFileW
            CreateFileW.argtypes = [ctypes.c_wchar_p, ctypes.c_uint32, ctypes.c_uint32, ctypes.c_void_p, ctypes.c_uint32, ctypes.c_uint32, ctypes.c_void_p]
            CreateFileW.restype = ctypes.c_void_p
            h = CreateFileW(str(self.path), GENERIC_READ, FILE_SHARE_READ | FILE_SHARE_DELETE, None, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL | FILE_FLAG_SEQUENTIAL_SCAN, None)
            if h == INVALID_HANDLE_VALUE or h is None:
                raise PermissionError(f"Não foi possível obter lock de leitura estável: {self.path}")
            self._handle = h
            try:
                fd = msvcrt.open_osfhandle(int(h), os.O_RDONLY | getattr(os, "O_BINARY", 0))
                self._handle = None  # ownership passou para fd
                self.file = os.fdopen(fd, "rb", buffering=0)
                return self.file
            except Exception:
                kernel32.CloseHandle(h)
                self._handle = None
                raise
        else:
            import fcntl
            f = self.path.open("rb", buffering=0)
            try:
                fcntl.flock(f.fileno(), fcntl.LOCK_SH | fcntl.LOCK_NB)
            except Exception:
                f.close(); raise PermissionError(f"Arquivo em uso: {self.path}")
            self.file = f
            return f

    def __exit__(self, exc_type, exc, tb):
        if self.file:
            if os.name != "nt":
                with contextlib.suppress(Exception):
                    import fcntl; fcntl.flock(self.file.fileno(), fcntl.LOCK_UN)
            self.file.close(); self.file = None


def hash_open_file(f: BinaryIO, on_bytes: Optional[Callable[[int], None]] = None) -> str:
    f.seek(0)
    h = hashlib.sha256()
    while True:
        b = f.read(COPY_CHUNK)
        if not b: break
        h.update(b)
        if on_bytes:
            on_bytes(len(b))
    f.seek(0)
    return h.hexdigest()

# ---------------------------------------------------------------------------
# Regras aprovadas e assinatura
# ---------------------------------------------------------------------------

@dataclass
class Rule:
    id: str
    source: str
    destination: str
    storage: str
    classification: str
    approved_by_user: bool
    recursive: bool = True
    note: str = ""
    created_at: str = ""


def rules_default_bytes() -> bytes:
    return b"schema_version: 1\nsource_rules: []\n"


def ensure_rules_file(state_dir: Path) -> tuple[Path, Path]:
    rules = state_dir / RULES_NAME
    sig = state_dir / RULES_SIG_NAME
    if not rules.exists():
        atomic_write_bytes(rules, rules_default_bytes())
        atomic_write_text(sig, sha256_file(rules) + "\n")
    elif not sig.exists():
        # arquivo existente sem assinatura não ganha confiança implicitamente
        raise RuntimeError(f"Arquivo de regras existe sem assinatura: {rules}")
    return rules, sig


def validate_rules_signature(state_dir: Path) -> str:
    rules, sig = ensure_rules_file(state_dir)
    expected = sig.read_text(encoding="utf-8").strip().lower()
    actual = sha256_file(rules)
    if expected != actual:
        raise RuntimeError("ASSINATURA DAS REGRAS INVÁLIDA. O YAML foi alterado fora do fluxo aprovado.")
    return actual


def load_rules(state_dir: Path) -> list[Rule]:
    validate_rules_signature(state_dir)
    global _yaml
    if _yaml is None:
        try: import yaml as y
        except ImportError: return []
        _yaml = y
    data = _yaml.safe_load((state_dir / RULES_NAME).read_text(encoding="utf-8")) or {}
    out = []
    for raw in data.get("source_rules", []) or []:
        r = Rule(
            id=str(raw.get("id") or uuid.uuid4().hex[:12]), source=str(raw["source"]),
            destination=str(raw["destination"]), storage=str(raw.get("storage", "DRIVE")).upper(),
            classification=str(raw.get("classification", "A")).upper(), approved_by_user=bool(raw.get("approved_by_user")),
            recursive=bool(raw.get("recursive", True)), note=str(raw.get("note", "")), created_at=str(raw.get("created_at", "")),
        )
        if r.classification not in {LEVEL_A, LEVEL_E} or not r.approved_by_user:
            raise RuntimeError(f"Regra {r.id} não é uma regra humana A/E aprovada válida.")
        if r.storage not in {"DRIVE", "ARCHIVE"}: raise RuntimeError(f"Storage inválido em {r.id}")
        out.append(r)
    return out


def save_rules(state_dir: Path, rules: Sequence[Rule]) -> str:
    global _yaml
    if _yaml is None:
        import yaml as y; _yaml = y
    payload = {"schema_version": 1, "source_rules": [asdict(r) for r in rules]}
    text = _yaml.safe_dump(payload, allow_unicode=True, sort_keys=False)
    rules_path = state_dir / RULES_NAME
    atomic_write_text(rules_path, text)
    h = sha256_file(rules_path)
    atomic_write_text(state_dir / RULES_SIG_NAME, h + "\n")
    return h


def windows_prefix_match(path: str, prefix: str) -> bool:
    p = ntext(str(PureWindowsPath(path)))
    q = ntext(str(PureWindowsPath(prefix)))
    return p == q or p.startswith(q + " ")  # ntext transforma separadores em espaços


def windows_parent_match(path: str, parent: str) -> bool:
    return ntext(str(PureWindowsPath(path).parent)) == ntext(str(PureWindowsPath(parent)))

def best_rule(path: str, rules: Sequence[Rule]) -> Optional[Rule]:
    matches = [r for r in rules if (windows_prefix_match(path, r.source) if r.recursive else windows_parent_match(path, r.source))]
    if not matches: return None
    return max(matches, key=lambda r: (len(PureWindowsPath(r.source).parts), 1 if not r.recursive else 0))

# ---------------------------------------------------------------------------
# Classificação multifatorial (SUGESTÕES; não aprova A/E sem regra humana)
# ---------------------------------------------------------------------------

@dataclass
class Classification:
    storage: str
    relative: Path
    level: str
    score: int
    evidence: list[str]
    reason: str
    rule_id: Optional[str] = None


def classify_item(source_path: str, surface: str, relative_path: str, filename: str, ext: str,
                  sha256: str, duplicate_count: int, exif_datetime: Optional[str], media_creation: Optional[str],
                  rules: Sequence[Rule]) -> Classification:
    # 1) Ground truth humano sempre vence.
    rule = best_rule(source_path, rules)
    if rule:
        rel_src = PureWindowsPath(source_path)
        rel_rule = PureWindowsPath(rule.source)
        try:
            if rule.recursive:
                tail = rel_src.relative_to(rel_rule)
                tail_path = Path(*tail.parts)
            else:
                tail_path = Path(filename)
        except Exception:
            tail_path = Path(filename)
        base = Path(rule.destination)
        return Classification(rule.storage, base / tail_path, rule.classification, 100,
                              ["regra explícita aprovada pelo usuário", f"rule:{rule.id}"],
                              rule.note or "Destino definido por regra humana assinada", rule.id)

    text = f"{relative_path} {filename}"
    n = ntext(text)
    e: list[str] = []
    year_path = infer_year(relative_path)
    year_meta = infer_year(exif_datetime or media_creation or "")
    if year_path: e.append(f"ano no caminho:{year_path}")
    if year_meta: e.append(f"ano em metadata:{year_meta}")
    year = year_meta or year_path
    if surface == "H" and ext.lower() in GOOGLE_NATIVE_STUBS:
        e.append("arquivo ponteiro para objeto Google Workspace nativo; SHA-256 local não representa o conteúdo remoto")

    # Restritos: propositalmente não entram em Drive automaticamente.
    restricted = any(k in n for k in (
        "conversa do whatsapp", "conversas zap", "dados whatsapp", "instagram messages", "instagram messages inbox",
        "diario", "privado", "whatsapp privado", "apagada conversa", "dados completos", "dump"
    ))
    if restricted:
        e += ["marcador de conteúdo restrito", "política: não publicar no Drive compartilhado"]
        return Classification("ARCHIVE", Path("01_ORIGINAIS BRUTOS") / "Dados de trabalho e restritos" / Path(relative_path), LEVEL_B, 86, e,
                              "Conteúdo potencialmente privado/restrito; manter no arquivo mestre até aprovação")

    top = ntext(PureWindowsPath(relative_path).parts[0]) if PureWindowsPath(relative_path).parts else ""
    if surface == "F":
        backup_tops = {ntext(x) for x in ("BACKUP DRIVE", "Backup Drive 180526", "BACKUP Notebook VAIO", "Backup Samsung", "Seagate")}
        if top in backup_tops:
            e += ["top-level identificado como backup", "destino permanece no HD"]
            return Classification("ARCHIVE", Path("04_BACKUPS DO DRIVE") / Path(relative_path), LEVEL_B, 92, e, "Backup histórico")
        if top == ntext("ARQUIVOS ANTIGOS (2017)"):
            e += ["top-level histórico explícito", "ano histórico no nome"]
            return Classification("ARCHIVE", Path("03_HISTÓRICO ACIRV") / "Até 2017" / Path(*PureWindowsPath(relative_path).parts[1:]), LEVEL_B, 94, e, "Acervo histórico explícito")
        if top == ntext("Gestão 2014 - 2024"):
            e += ["top-level de gestão encerrada", "intervalo temporal explícito"]
            return Classification("ARCHIVE", Path("03_HISTÓRICO ACIRV") / "2014-2024" / Path(*PureWindowsPath(relative_path).parts[1:]), LEVEL_B, 94, e, "Gestão histórica encerrada")
        if top == ntext("ACIRV"):
            e += ["top-level legado ACIRV", "acervo anterior"]
            return Classification("ARCHIVE", Path("03_HISTÓRICO ACIRV") / "Legado ACIRV" / Path(*PureWindowsPath(relative_path).parts[1:]), LEVEL_B, 82, e, "Acervo ACIRV legado")
        if top == ntext("temp"):
            return Classification("ARCHIVE", Path("90_LEGADO — A REVISAR") / "TEMP — origem F" / Path(*PureWindowsPath(relative_path).parts[1:]), LEVEL_D, 20,
                                  ["origem temporária", "sem significado institucional seguro"], "Temporário precisa de decisão humana")

    if filename.lower() in SYSTEM_NAMES:
        storage = "DRIVE" if surface == "H" else "ARCHIVE"
        return Classification(storage, Path("90_LEGADO — A REVISAR") / "_ARQUIVOS_DE_SISTEMA" / Path(relative_path), LEVEL_C, 55,
                              ["arquivo de metadado do sistema"], "Pode ir ao legado, mas exige aprovação E")

    # Banco curado existente é evidência forte de função, não só nome de arquivo.
    if "banco de imagens da acirv" in n:
        parts = list(PureWindowsPath(relative_path).parts)
        idx = next((i for i,p in enumerate(parts) if ntext(p)=="banco de imagens da acirv"), 0)
        tail = Path(*parts[idx+1:]) if idx+1 < len(parts) else Path(filename)
        e += ["ancestral Banco de Imagens da ACIRV", "estrutura existente de reutilização"]
        return Classification("DRIVE", Path("04_BANCO DE MÍDIA") / tail, LEVEL_B, 91, e, "Banco de mídia curado existente")

    if any(k in n for k in ("identidade visual", "logos dos projetos acirv", "timbrado acirv", "logo masters sudoexpo", "identidade sudoexpo")):
        e += ["marcador explícito de identidade", "tipo de ativo recorrente"]
        return Classification("DRIVE", Path("01_MARCA E IDENTIDADE") / "ACIRV e Projetos" / Path(relative_path), LEVEL_B, 88, e, "Identidade/master institucional")

    events = event_candidates(text)
    if len(events) > 1:
        return Classification("DRIVE", Path("02_PROJETOS E EVENTOS") / "_AMBÍGUO" / Path(relative_path), LEVEL_D, 30,
                              [f"múltiplos eventos:{', '.join(events)}"], "Mais de um evento plausível")
    if len(events) == 1:
        event = events[0]
        e.append(f"evento no contexto:{event}")
        if year: e.append(f"ano corroborado:{year}")
        if ext.lower() in IMAGE_EXTS | VIDEO_EXTS | DESIGN_EXTS | DOC_EXTS | AUDIO_EXTS: e.append(f"tipo compatível:{ext.lower()}")
        if duplicate_count > 1: e.append(f"duplicata por SHA-256:{duplicate_count} cópias")
        score = 74 + (10 if year else 0) + (4 if year_path and year_meta and year_path == year_meta else 0)
        level = LEVEL_B if score >= 84 else LEVEL_C
        return Classification("DRIVE", event_rel(event, year, ext, text) / Path(filename), level, min(score, 96), e, f"Material relacionado a {event}")

    if any(k in n for k in ("comercial", "novo associado", "novos associados", "cadastro de novos associados", "possiveis associados", "indicacao de expositor", "propostas comerciais")):
        e += ["marcador comercial/associados"]
        return Classification("DRIVE", Path("06_COMERCIAL E ASSOCIADOS") / Path(relative_path), LEVEL_C, 70, e, "Material comercial provável")

    if any(k in n for k in ("relatorio", "pesquisa", "dados marketing", "kpi", "metricas", "métricas")):
        e += ["marcador de dados/relatórios"]
        return Classification("DRIVE", Path("07_DADOS E RELATÓRIOS") / Path(relative_path), LEVEL_C, 69, e, "Dados/relatório provável")

    if any(k in n for k in ("fotos diretoria", "fotos equipe acirv", "fotos e videos institucionais", "fachada acirv", "fotos acirvetes")):
        e += ["marcador de mídia institucional reutilizável"]
        return Classification("DRIVE", Path("04_BANCO DE MÍDIA") / Path(relative_path), LEVEL_C, 72, e, "Mídia institucional provável")

    if "planejamento vcom" in n or (surface == "F" and top == ntext("KEVYN") and "criativos" in n):
        y = year or 2026
        month = detect_month(text) or "00_Sem mês confirmado"
        e += ["origem de produção editorial", f"ano sugerido:{y}", f"mês:{month}"]
        return Classification("DRIVE", Path("03_COMUNICAÇÃO E CONTEÚDO") / str(y) / month / "Produção a revisar" / Path(filename), LEVEL_C, 61, e,
                              "Origem editorial, mas o assunto específico não está comprovado")

    if surface == "F" and top == ntext("KEVYN") and "dados acirv" in n:
        return Classification("ARCHIVE", Path("01_ORIGINAIS BRUTOS") / "Dados de trabalho e restritos" / Path(relative_path), LEVEL_C, 62,
                              ["origem KEVYN/DADOS ACIRV", "conteúdo institucional/pessoal misturado"], "Não publicar sem revisão")

    # Sem fallback automático para legado: D bloqueia.
    storage = "ARCHIVE" if surface == "F" else "DRIVE"
    return Classification(storage, Path("_SEM_DESTINO_APROVADO") / Path(relative_path), LEVEL_D, 0, ["nenhuma regra semântica suficiente"], "Classificação ambígua; revisão obrigatória")

# ---------------------------------------------------------------------------
# Banco de estado
# ---------------------------------------------------------------------------

SCHEMA = r"""
PRAGMA journal_mode=WAL;
PRAGMA synchronous=FULL;
PRAGMA foreign_keys=ON;
CREATE TABLE IF NOT EXISTS runs(
 run_id TEXT PRIMARY KEY, created_at TEXT NOT NULL, app_version TEXT NOT NULL,
 f_root TEXT NOT NULL, h_root TEXT NOT NULL, central_root TEXT NOT NULL, archive_root TEXT NOT NULL,
 state_dir TEXT NOT NULL, include_entire_drive INTEGER NOT NULL DEFAULT 0,
 reserve_bytes INTEGER NOT NULL, status TEXT NOT NULL,
 rules_hash TEXT, manifest_hash TEXT, plan_signature TEXT, plan_allow_b INTEGER NOT NULL DEFAULT 0,
 scanned_files INTEGER NOT NULL DEFAULT 0, scanned_bytes INTEGER NOT NULL DEFAULT 0,
 scan_errors INTEGER NOT NULL DEFAULT 0, notes TEXT
);
CREATE TABLE IF NOT EXISTS manifest(
 run_id TEXT NOT NULL, item_id INTEGER NOT NULL, source_path TEXT NOT NULL, surface TEXT NOT NULL,
 relative_path TEXT NOT NULL, filename TEXT NOT NULL, extension TEXT NOT NULL, size INTEGER NOT NULL,
 sha256 TEXT NOT NULL, created_ns INTEGER, modified_ns INTEGER, attributes TEXT, mime TEXT,
 exif_datetime TEXT, exif_camera TEXT, media_creation_time TEXT, video_duration REAL,
 video_width INTEGER, video_height INTEGER, video_codec TEXT, duplicate_count INTEGER NOT NULL DEFAULT 1,
 canonical_path TEXT, scan_status TEXT NOT NULL DEFAULT 'OK', error TEXT,
 PRIMARY KEY(run_id,item_id), UNIQUE(run_id,source_path)
);
CREATE INDEX IF NOT EXISTS idx_manifest_hash ON manifest(run_id,sha256);
CREATE TABLE IF NOT EXISTS dirs(
 run_id TEXT NOT NULL, surface TEXT NOT NULL, path TEXT NOT NULL, relative_path TEXT NOT NULL,
 empty_at_scan INTEGER NOT NULL DEFAULT 0, protected INTEGER NOT NULL DEFAULT 0, reason TEXT,
 PRIMARY KEY(run_id,path)
);
CREATE TABLE IF NOT EXISTS classifications(
 run_id TEXT NOT NULL, item_id INTEGER NOT NULL, storage TEXT NOT NULL, relative_dest TEXT NOT NULL,
 level TEXT NOT NULL, score INTEGER NOT NULL, evidence_json TEXT NOT NULL, reason TEXT NOT NULL,
 rule_id TEXT, PRIMARY KEY(run_id,item_id)
);
CREATE INDEX IF NOT EXISTS idx_cls_level ON classifications(run_id,level);
CREATE TABLE IF NOT EXISTS groups(
 run_id TEXT NOT NULL, group_id TEXT NOT NULL, source_prefix TEXT NOT NULL, surface TEXT NOT NULL,
 level TEXT NOT NULL, storage TEXT NOT NULL, relative_dest TEXT NOT NULL,
 item_count INTEGER NOT NULL, total_bytes INTEGER NOT NULL, evidence_json TEXT NOT NULL,
 status TEXT NOT NULL DEFAULT 'PENDING', PRIMARY KEY(run_id,group_id)
);
CREATE TABLE IF NOT EXISTS ops(
 run_id TEXT NOT NULL, op_id INTEGER NOT NULL, item_id INTEGER NOT NULL,
 source_before TEXT NOT NULL, destination_after TEXT NOT NULL, storage TEXT NOT NULL, level TEXT NOT NULL,
 op_mode TEXT NOT NULL, expected_size INTEGER NOT NULL, expected_mtime_ns INTEGER,
 sha256_before TEXT NOT NULL, sha256_after TEXT, quarantine_path TEXT, final_path TEXT,
 status TEXT NOT NULL, error TEXT, updated_at TEXT NOT NULL,
 PRIMARY KEY(run_id,op_id)
);
CREATE TABLE IF NOT EXISTS post_manifest(
 run_id TEXT NOT NULL, path TEXT NOT NULL, surface TEXT NOT NULL, size INTEGER NOT NULL, sha256 TEXT NOT NULL,
 PRIMARY KEY(run_id,path)
);
CREATE INDEX IF NOT EXISTS idx_post_hash ON post_manifest(run_id,sha256);
CREATE TABLE IF NOT EXISTS journal(
 id INTEGER PRIMARY KEY AUTOINCREMENT, run_id TEXT NOT NULL, ts TEXT NOT NULL, level TEXT NOT NULL,
 event TEXT NOT NULL, payload_json TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS audit_scan_queue(
 run_id TEXT NOT NULL, surface TEXT NOT NULL, root_path TEXT NOT NULL, path TEXT NOT NULL,
 relative_path TEXT NOT NULL, status TEXT NOT NULL DEFAULT 'PENDING', error TEXT, updated_at TEXT NOT NULL,
 PRIMARY KEY(run_id,path)
);
CREATE INDEX IF NOT EXISTS idx_audit_scan_status ON audit_scan_queue(run_id,status);
CREATE TABLE IF NOT EXISTS audit_file_queue(
 run_id TEXT NOT NULL, item_id INTEGER NOT NULL, source_path TEXT NOT NULL, surface TEXT NOT NULL,
 root_path TEXT NOT NULL, size INTEGER NOT NULL, created_ns INTEGER, modified_ns INTEGER,
 status TEXT NOT NULL DEFAULT 'PENDING', error TEXT, attempts INTEGER NOT NULL DEFAULT 0, updated_at TEXT NOT NULL,
 PRIMARY KEY(run_id,item_id), UNIQUE(run_id,source_path)
);
CREATE INDEX IF NOT EXISTS idx_audit_file_status ON audit_file_queue(run_id,status);
CREATE TABLE IF NOT EXISTS audit_errors(
 run_id TEXT NOT NULL, phase TEXT NOT NULL, path TEXT NOT NULL, error TEXT NOT NULL, updated_at TEXT NOT NULL,
 PRIMARY KEY(run_id,phase,path)
);
CREATE TABLE IF NOT EXISTS audit_checkpoint(
 run_id TEXT PRIMARY KEY, phase TEXT NOT NULL, workers INTEGER NOT NULL,
 inventory_dirs_done INTEGER NOT NULL DEFAULT 0, inventory_dirs_pending INTEGER NOT NULL DEFAULT 0,
 total_files INTEGER NOT NULL DEFAULT 0, total_bytes INTEGER NOT NULL DEFAULT 0,
 completed_files INTEGER NOT NULL DEFAULT 0, completed_bytes INTEGER NOT NULL DEFAULT 0,
 failed_files INTEGER NOT NULL DEFAULT 0, error_count INTEGER NOT NULL DEFAULT 0,
 updated_at TEXT NOT NULL
);
"""

class DB:
    def __init__(self, path: Path):
        path.parent.mkdir(parents=True, exist_ok=True)
        self.path = path
        self.conn = sqlite3.connect(path)
        self.conn.row_factory = sqlite3.Row
        self.conn.executescript(SCHEMA)
        self.conn.commit()
    def close(self): self.conn.close()
    def log(self, run_id: str, event: str, payload: Any = None, level: str = "INFO"):
        self.conn.execute("INSERT INTO journal(run_id,ts,level,event,payload_json) VALUES(?,?,?,?,?)",
                          (run_id, utc_now(), level, event, json.dumps(payload or {}, ensure_ascii=False, sort_keys=True)))
        self.conn.commit()
    def run(self, run_id: str): return self.conn.execute("SELECT * FROM runs WHERE run_id=?", (run_id,)).fetchone()
    def runs(self): return self.conn.execute("SELECT * FROM runs ORDER BY created_at DESC").fetchall()

# ---------------------------------------------------------------------------
# Scanner forense
# ---------------------------------------------------------------------------

def drive_in_scope(rel: Path, include_entire: bool) -> bool:
    if include_entire: return True
    if not rel.parts: return False
    top = ntext(rel.parts[0])
    if any(top == ntext(x) for x in DRIVE_SCOPE_PREFIXES): return True
    # Arquivos ACIRV soltos na raiz são incluídos apenas se nome indicar ACIRV.
    if len(rel.parts) == 1 and "acirv" in ntext(rel.name): return True
    return False


def iter_tree(root: Path, excluded_roots: Sequence[Path], surface: str, include_entire_drive: bool) -> Iterator[tuple[str, Path, Optional[os.stat_result], Optional[str]]]:
    excluded_resolved = [p.resolve(strict=False) for p in excluded_roots]
    stack = [root]
    while stack:
        d = stack.pop()
        try:
            with os.scandir(d) as it:
                entries = list(it)
        except OSError as e:
            yield "ERROR", d, None, f"listdir:{e}"
            continue
        yield "DIR", d, None, None
        for ent in entries:
            p = Path(ent.path)
            try:
                # protege destinos do próprio migrador e state dir
                rp = p.resolve(strict=False)
                if any(path_is_relative_to(rp, ex) for ex in excluded_resolved):
                    continue
                rel = p.relative_to(root)
                if surface == "F" and rel.parts and ntext(rel.parts[0]) in {ntext(x) for x in PROTECTED_F_TOP}:
                    yield "PROTECTED", p, None, "diretório de sistema/lixeira"
                    continue
                if surface == "H" and not drive_in_scope(rel, include_entire_drive):
                    continue
                st = p.lstat()
                if is_reparse_or_symlink(p, st):
                    yield "PROTECTED", p, st, "symlink/junction/reparse point"
                    continue
                if stat.S_ISDIR(st.st_mode):
                    stack.append(p)
                elif stat.S_ISREG(st.st_mode):
                    yield "FILE", p, st, None
                else:
                    yield "PROTECTED", p, st, "tipo especial não regular"
            except OSError as e:
                yield "ERROR", p, None, f"stat:{e}"


def ensure_pillow_for_audit() -> bool:
    try:
        import PIL.Image
        return True
    except ImportError:
        return False


def _emit_progress(progress_cb: Optional[Callable[[str, dict[str, Any]], None]], event: str, **payload: Any) -> None:
    """Notifica a TUI sem permitir que um erro visual interrompa o motor de segurança."""
    if not progress_cb:
        return
    try:
        progress_cb(event, payload)
    except Exception:
        pass


def audit_worker_count(requested: Optional[int] = None) -> int:
    """Número de threads para hashing/metadados.

    O padrão da V2.3 é 12 threads. Threads evitam o overhead de multiprocessing no
    Windows e sobrepõem I/O, SHA-256 (OpenSSL libera o GIL em blocos grandes), EXIF
    e ffprobe. O teto continua em 12 para impedir paralelismo acidental excessivo.
    """
    if requested is None:
        raw = os.environ.get("ACIRV_AUDIT_WORKERS", "").strip()
        if raw:
            try:
                requested = int(raw)
            except ValueError:
                requested = None
    n = requested if requested is not None else DEFAULT_AUDIT_WORKERS
    return max(1, min(MAX_AUDIT_WORKERS, int(n)))


def _checkpoint_json_path(state_dir: Path) -> Path:
    return state_dir / CHECKPOINT_JSON_NAME


_CHECKPOINT_MIRROR_LAST: dict[str, float] = {}


def _audit_checkpoint_payload(db: DB, run_id: str) -> dict[str, Any]:
    run = db.run(run_id)
    cp = db.conn.execute("SELECT * FROM audit_checkpoint WHERE run_id=?", (run_id,)).fetchone()
    if not run:
        return {"run_id": run_id, "missing": True, "updated_at": utc_now()}
    counts = {
        r["status"]: int(r["c"])
        for r in db.conn.execute(
            "SELECT status,COUNT(*) c FROM audit_file_queue WHERE run_id=? GROUP BY status", (run_id,)
        )
    }
    payload: dict[str, Any] = {
        "schema_version": 1,
        "app_version": APP_VERSION,
        "run_id": run_id,
        "run_status": run["status"],
        "state_database": str(db.path),
        "updated_at": utc_now(),
        "resume_guarantee": (
            "Diretórios inventariados e arquivos com SHA-256 concluído são persistidos em SQLite. "
            "Se houver interrupção no meio de um arquivo individual, somente esse arquivo é hasheado novamente."
        ),
        "file_queue": counts,
    }
    if cp:
        payload.update({k: cp[k] for k in cp.keys()})
        total = int(cp["total_files"] or 0)
        done = int(cp["completed_files"] or 0)
        failed = int(cp["failed_files"] or 0)
        payload["processed_files"] = done + failed
        payload["remaining_files"] = max(0, total - done - failed)
        payload["percent_files"] = round(((done + failed) / total * 100.0), 2) if total else 0.0
    return payload


def write_audit_checkpoint_mirror(db: DB, state_dir: Path, run_id: str, force: bool = False) -> None:
    """Espelho humano do checkpoint. SQLite é a fonte de verdade; JSON é diagnóstico/visibilidade."""
    now = time.monotonic()
    last = _CHECKPOINT_MIRROR_LAST.get(run_id, 0.0)
    if not force and now - last < 1.0:
        return
    payload = _audit_checkpoint_payload(db, run_id)
    atomic_write_text(_checkpoint_json_path(state_dir), json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    _CHECKPOINT_MIRROR_LAST[run_id] = now


def _record_audit_error(db: DB, run_id: str, phase: str, path: Path | str, error: BaseException | str) -> None:
    db.conn.execute(
        "INSERT OR REPLACE INTO audit_errors(run_id,phase,path,error,updated_at) VALUES(?,?,?,?,?)",
        (run_id, phase, str(path), repr(error) if isinstance(error, BaseException) else str(error), utc_now()),
    )


def _audit_error_count(db: DB, run_id: str) -> int:
    return int(db.conn.execute("SELECT COUNT(*) FROM audit_errors WHERE run_id=?", (run_id,)).fetchone()[0])


def _ensure_audit_checkpoint(db: DB, run_id: str, f_root: Path, h_root: Path, workers: int) -> None:
    cp = db.conn.execute("SELECT 1 FROM audit_checkpoint WHERE run_id=?", (run_id,)).fetchone()
    if not cp:
        db.conn.execute(
            """INSERT INTO audit_checkpoint(
                 run_id,phase,workers,inventory_dirs_done,inventory_dirs_pending,total_files,total_bytes,
                 completed_files,completed_bytes,failed_files,error_count,updated_at
               ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)""",
            (run_id, "INVENTORY", workers, 0, 0, 0, 0, 0, 0, 0, 0, utc_now()),
        )
    else:
        db.conn.execute("UPDATE audit_checkpoint SET workers=?,updated_at=? WHERE run_id=?", (workers, utc_now(), run_id))

    roots = (("H", h_root), ("F", f_root))
    for surface, root in roots:
        db.conn.execute(
            """INSERT OR IGNORE INTO audit_scan_queue(
                 run_id,surface,root_path,path,relative_path,status,error,updated_at
               ) VALUES(?,?,?,?,?,'PENDING',NULL,?)""",
            (run_id, surface, str(root), str(root), ".", utc_now()),
        )
    pending = int(db.conn.execute(
        "SELECT COUNT(*) FROM audit_scan_queue WHERE run_id=? AND status='PENDING'", (run_id,)
    ).fetchone()[0])
    db.conn.execute(
        "UPDATE audit_checkpoint SET inventory_dirs_pending=?,updated_at=? WHERE run_id=?",
        (pending, utc_now(), run_id),
    )
    db.conn.commit()


def _queue_file_from_inventory(
    db: DB,
    run_id: str,
    path: Path,
    root: Path,
    surface: str,
    st: os.stat_result,
    next_item_id: int,
) -> tuple[int, int, int, int, int]:
    """Retorna (next_item_id, novos_arquivos, novos_bytes, hashes_reaproveitados, bytes_reaproveitados)."""
    existing_q = db.conn.execute(
        "SELECT item_id FROM audit_file_queue WHERE run_id=? AND source_path=?", (run_id, str(path))
    ).fetchone()
    if existing_q:
        return next_item_id, 0, 0, 0, 0

    old = db.conn.execute(
        "SELECT item_id,size,modified_ns FROM manifest WHERE run_id=? AND source_path=?", (run_id, str(path))
    ).fetchone()
    item_id = int(old["item_id"]) if old else next_item_id
    if not old:
        next_item_id += 1
    stable_old = bool(
        old
        and int(old["size"]) == int(st.st_size)
        and int(old["modified_ns"] or -1) == int(st.st_mtime_ns)
    )
    if old and not stable_old:
        db.conn.execute("DELETE FROM manifest WHERE run_id=? AND item_id=?", (run_id, item_id))

    db.conn.execute(
        """INSERT INTO audit_file_queue(
             run_id,item_id,source_path,surface,root_path,size,created_ns,modified_ns,status,error,attempts,updated_at
           ) VALUES(?,?,?,?,?,?,?,?,?,?,0,?)""",
        (
            run_id, item_id, str(path), surface, str(root), int(st.st_size),
            int(getattr(st, "st_ctime_ns", int(st.st_ctime * 1e9))), int(st.st_mtime_ns),
            "DONE" if stable_old else "PENDING", None, utc_now(),
        ),
    )
    return next_item_id, 1, int(st.st_size), 1 if stable_old else 0, int(st.st_size) if stable_old else 0


def _inventory_resume(
    db: DB,
    state_dir: Path,
    run_id: str,
    include_entire_drive: bool,
    excluded_roots: Sequence[Path],
    progress_cb: Optional[Callable[[str, dict[str, Any]], None]],
) -> None:
    cp = db.conn.execute("SELECT * FROM audit_checkpoint WHERE run_id=?", (run_id,)).fetchone()
    worker_n = int(cp["workers"]) if cp else DEFAULT_AUDIT_WORKERS
    _emit_progress(progress_cb, "inventory_start", run_id=run_id, workers=worker_n, resumed=True)

    row = db.conn.execute("SELECT COALESCE(MAX(item_id),0) FROM manifest WHERE run_id=?", (run_id,)).fetchone()
    qrow = db.conn.execute("SELECT COALESCE(MAX(item_id),0) FROM audit_file_queue WHERE run_id=?", (run_id,)).fetchone()
    next_item_id = max(int(row[0]), int(qrow[0])) + 1
    excluded_resolved = [p.resolve(strict=False) for p in excluded_roots]

    while True:
        q = db.conn.execute(
            """SELECT * FROM audit_scan_queue
               WHERE run_id=? AND status='PENDING'
               ORDER BY CASE surface WHEN 'H' THEN 0 ELSE 1 END, path LIMIT 1""",
            (run_id,),
        ).fetchone()
        if not q:
            break

        surface = q["surface"]
        root = Path(q["root_path"])
        d = Path(q["path"])
        _emit_progress(progress_cb, "inventory_surface", surface=surface, root=str(d))
        inserted_files = inserted_bytes = inserted_dirs = reused_hashes = reused_bytes = 0
        try:
            with os.scandir(d) as it:
                entries = list(it)
        except OSError as exc:
            _record_audit_error(db, run_id, "INVENTORY", d, f"listdir:{exc}")
            db.conn.execute(
                "UPDATE audit_scan_queue SET status='ERROR',error=?,updated_at=? WHERE run_id=? AND path=?",
                (repr(exc), utc_now(), run_id, str(d)),
            )
            db.conn.execute(
                """UPDATE audit_checkpoint SET inventory_dirs_done=inventory_dirs_done+1,
                   inventory_dirs_pending=MAX(0,inventory_dirs_pending-1),error_count=?,updated_at=? WHERE run_id=?""",
                (_audit_error_count(db, run_id), utc_now(), run_id),
            )
            db.conn.commit()
            write_audit_checkpoint_mirror(db, state_dir, run_id)
            continue

        try:
            for ent in entries:
                p = Path(ent.path)
                try:
                    rp = p.resolve(strict=False)
                    if any(path_is_relative_to(rp, ex) for ex in excluded_resolved):
                        continue
                    rel = p.relative_to(root)
                    if surface == "F" and rel.parts and ntext(rel.parts[0]) in {ntext(x) for x in PROTECTED_F_TOP}:
                        db.conn.execute(
                            "INSERT OR REPLACE INTO dirs(run_id,surface,path,relative_path,empty_at_scan,protected,reason) VALUES(?,?,?,?,0,1,?)",
                            (run_id, surface, str(p), str(PureWindowsPath(*rel.parts)), "diretório de sistema/lixeira"),
                        )
                        continue
                    if surface == "H" and not drive_in_scope(rel, include_entire_drive):
                        continue
                    st = p.lstat()
                    if is_reparse_or_symlink(p, st):
                        db.conn.execute(
                            "INSERT OR REPLACE INTO dirs(run_id,surface,path,relative_path,empty_at_scan,protected,reason) VALUES(?,?,?,?,0,1,?)",
                            (run_id, surface, str(p), str(PureWindowsPath(*rel.parts)), "symlink/junction/reparse point"),
                        )
                        continue
                    if stat.S_ISDIR(st.st_mode):
                        db.conn.execute(
                            "INSERT OR IGNORE INTO dirs(run_id,surface,path,relative_path,empty_at_scan,protected,reason) VALUES(?,?,?,?,0,0,NULL)",
                            (run_id, surface, str(p), str(PureWindowsPath(*rel.parts))),
                        )
                        cur = db.conn.execute(
                            """INSERT OR IGNORE INTO audit_scan_queue(
                                 run_id,surface,root_path,path,relative_path,status,error,updated_at
                               ) VALUES(?,?,?,?,?,'PENDING',NULL,?)""",
                            (run_id, surface, str(root), str(p), str(PureWindowsPath(*rel.parts)), utc_now()),
                        )
                        if cur.rowcount:
                            inserted_dirs += 1
                    elif stat.S_ISREG(st.st_mode):
                        next_item_id, nf, nb, rh, rb = _queue_file_from_inventory(
                            db, run_id, p, root, surface, st, next_item_id
                        )
                        inserted_files += nf; inserted_bytes += nb; reused_hashes += rh; reused_bytes += rb
                    else:
                        db.conn.execute(
                            "INSERT OR REPLACE INTO dirs(run_id,surface,path,relative_path,empty_at_scan,protected,reason) VALUES(?,?,?,?,0,1,?)",
                            (run_id, surface, str(p), str(PureWindowsPath(*rel.parts)), "tipo especial não regular"),
                        )
                except OSError as exc:
                    _record_audit_error(db, run_id, "INVENTORY", p, f"stat:{exc}")

            db.conn.execute(
                "UPDATE audit_scan_queue SET status='DONE',error=NULL,updated_at=? WHERE run_id=? AND path=?",
                (utc_now(), run_id, str(d)),
            )
            db.conn.execute(
                """UPDATE audit_checkpoint SET
                   inventory_dirs_done=inventory_dirs_done+1,
                   inventory_dirs_pending=MAX(0,inventory_dirs_pending-1+?),
                   total_files=total_files+?, total_bytes=total_bytes+?,
                   completed_files=completed_files+?, completed_bytes=completed_bytes+?,
                   error_count=?, updated_at=? WHERE run_id=?""",
                (inserted_dirs, inserted_files, inserted_bytes, reused_hashes, reused_bytes,
                 _audit_error_count(db, run_id), utc_now(), run_id),
            )
            db.conn.commit()
        except BaseException:
            db.conn.rollback()
            raise

        write_audit_checkpoint_mirror(db, state_dir, run_id)
        cp2 = db.conn.execute("SELECT * FROM audit_checkpoint WHERE run_id=?", (run_id,)).fetchone()
        _emit_progress(
            progress_cb, "inventory_tick", files=int(cp2["total_files"]), bytes=int(cp2["total_bytes"]),
            path=str(d), surface=surface, reused=int(cp2["completed_files"]),
            dirs_done=int(cp2["inventory_dirs_done"]), dirs_pending=int(cp2["inventory_dirs_pending"]),
        )

    # Remove hashes legados de arquivos que desapareceram desde uma execução antiga interrompida.
    db.conn.execute(
        "DELETE FROM manifest WHERE run_id=? AND source_path NOT IN (SELECT source_path FROM audit_file_queue WHERE run_id=?)",
        (run_id, run_id),
    )
    totals = db.conn.execute(
        """SELECT COUNT(*) files,COALESCE(SUM(size),0) bytes,
           SUM(CASE WHEN status='DONE' THEN 1 ELSE 0 END) done_files,
           COALESCE(SUM(CASE WHEN status='DONE' THEN size ELSE 0 END),0) done_bytes,
           SUM(CASE WHEN status='ERROR' THEN 1 ELSE 0 END) failed_files
           FROM audit_file_queue WHERE run_id=?""", (run_id,)
    ).fetchone()
    db.conn.execute(
        """UPDATE audit_checkpoint SET phase='HASHING',inventory_dirs_pending=0,total_files=?,total_bytes=?,
           completed_files=?,completed_bytes=?,failed_files=?,error_count=?,updated_at=? WHERE run_id=?""",
        (int(totals["files"] or 0), int(totals["bytes"] or 0), int(totals["done_files"] or 0),
         int(totals["done_bytes"] or 0), int(totals["failed_files"] or 0), _audit_error_count(db, run_id),
         utc_now(), run_id),
    )
    db.conn.commit()
    write_audit_checkpoint_mirror(db, state_dir, run_id, force=True)


class _ThreadByteCounter:
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._value = 0
    def add(self, n: int) -> None:
        with self._lock:
            self._value += int(n)
    def value(self) -> int:
        with self._lock:
            return self._value


def manifest_record(
    path: Path,
    root: Path,
    surface: str,
    st: os.stat_result,
    with_media_meta: bool,
    on_bytes: Optional[Callable[[int], None]] = None,
) -> dict[str, Any]:
    # Hash é lido de handle estável para detectar writers incompatíveis já na auditoria.
    with LockedSource(path) as f:
        before = path.stat()
        h = hash_open_file(f, on_bytes=on_bytes)
        after = path.stat()
        if before.st_size != after.st_size or before.st_mtime_ns != after.st_mtime_ns:
            raise RuntimeError("arquivo mudou durante a leitura")
    exif_date = camera = None
    mc = None; dur = None; w = None; he = None; codec = None
    if with_media_meta:
        exif_date, camera = extract_exif(path)
        mc, dur, w, he, codec = extract_video_meta(path)
    rel = path.relative_to(root)
    return {
        "source_path": str(path), "surface": surface, "relative_path": str(PureWindowsPath(*rel.parts)),
        "filename": path.name, "extension": path.suffix.lower(), "size": int(st.st_size), "sha256": h,
        "created_ns": int(getattr(st, "st_ctime_ns", int(st.st_ctime*1e9))), "modified_ns": int(st.st_mtime_ns),
        "attributes": file_attributes(path, st), "mime": mime_guess(path), "exif_datetime": exif_date, "exif_camera": camera,
        "media_creation_time": mc, "video_duration": dur, "video_width": w, "video_height": he, "video_codec": codec,
    }


def _manifest_worker(
    task: tuple[int, Path, Path, str, int, int],
    with_media_meta: bool,
    byte_counter: Optional[_ThreadByteCounter] = None,
) -> tuple[int, dict[str, Any]]:
    item_id, path, root, surface, known_size, known_mtime_ns = task
    st = path.lstat()
    if not stat.S_ISREG(st.st_mode):
        raise RuntimeError("arquivo deixou de ser regular antes da leitura")
    if int(st.st_size) != int(known_size) or int(st.st_mtime_ns) != int(known_mtime_ns):
        raise RuntimeError("arquivo mudou desde o inventário; refaça a auditoria após estabilizar a origem")
    return item_id, manifest_record(
        path, root, surface, st, with_media_meta,
        on_bytes=byte_counter.add if byte_counter else None,
    )


def _parallel_manifest_records(
    tasks: Sequence[tuple[int, Path, Path, str, int, int]],
    with_media_meta: bool,
    workers: int,
    progress_cb: Optional[Callable[[str, dict[str, Any]], None]] = None,
    base_bytes: int = 0,
    total_bytes: int = 0,
) -> Iterator[tuple[tuple[int, Path, Path, str, int, int], Optional[dict[str, Any]], Optional[BaseException]]]:
    """Hash em paralelo com fila limitada e telemetria de bytes em tempo real."""
    if not tasks:
        return
    iterator = iter(tasks)
    max_in_flight = max(workers * 3, workers)
    byte_counter = _ThreadByteCounter()
    last_emit = 0.0
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers, thread_name_prefix="acirv-audit") as pool:
        pending: dict[concurrent.futures.Future, tuple[int, Path, Path, str, int, int]] = {}

        def submit_next() -> bool:
            try:
                task = next(iterator)
            except StopIteration:
                return False
            fut = pool.submit(_manifest_worker, task, with_media_meta, byte_counter)
            pending[fut] = task
            return True

        for _ in range(min(max_in_flight, len(tasks))):
            if not submit_next():
                break

        while pending:
            done, _ = concurrent.futures.wait(
                tuple(pending), timeout=0.20, return_when=concurrent.futures.FIRST_COMPLETED
            )
            now = time.monotonic()
            if now - last_emit >= 0.20:
                _emit_progress(
                    progress_cb, "hash_bytes", session_bytes=byte_counter.value(),
                    base_bytes=base_bytes, total_bytes=total_bytes, active=len(pending),
                )
                last_emit = now
            for fut in done:
                task = pending.pop(fut)
                try:
                    _item_id, rec = fut.result()
                    yield task, rec, None
                except Exception as exc:
                    yield task, None, exc
                submit_next()


def compute_manifest_signature(db: DB, run_id: str) -> str:
    h = hashlib.sha256()
    for r in db.conn.execute("SELECT source_path,size,sha256,created_ns,modified_ns FROM manifest WHERE run_id=? ORDER BY source_path", (run_id,)):
        h.update(json.dumps(dict(r), ensure_ascii=False, sort_keys=True, separators=(",",":")).encode())
        h.update(b"\n")
    return h.hexdigest()


def _hash_resume(
    db: DB,
    state_dir: Path,
    run_id: str,
    with_media_meta: bool,
    workers: int,
    progress_cb: Optional[Callable[[str, dict[str, Any]], None]],
) -> None:
    totals = db.conn.execute(
        """SELECT COUNT(*) files,COALESCE(SUM(size),0) bytes,
           SUM(CASE WHEN status='DONE' THEN 1 ELSE 0 END) done_files,
           COALESCE(SUM(CASE WHEN status='DONE' THEN size ELSE 0 END),0) done_bytes,
           SUM(CASE WHEN status='ERROR' THEN 1 ELSE 0 END) failed_files
           FROM audit_file_queue WHERE run_id=?""", (run_id,)
    ).fetchone()
    total_files = int(totals["files"] or 0); total_bytes = int(totals["bytes"] or 0)
    done_files = int(totals["done_files"] or 0); done_bytes = int(totals["done_bytes"] or 0)
    failed_files = int(totals["failed_files"] or 0)
    errors = _audit_error_count(db, run_id)
    tasks = [
        (int(r["item_id"]), Path(r["source_path"]), Path(r["root_path"]), r["surface"], int(r["size"]), int(r["modified_ns"] or 0))
        for r in db.conn.execute(
            "SELECT * FROM audit_file_queue WHERE run_id=? AND status='PENDING' ORDER BY item_id", (run_id,)
        ).fetchall()
    ]
    _emit_progress(
        progress_cb, "hash_start", total_files=total_files, total_bytes=total_bytes, workers=workers,
        completed=done_files + failed_files, completed_files=done_files, completed_bytes=done_bytes,
        failed_files=failed_files, resumed=bool(done_files or failed_files),
    )

    processed = done_files + failed_files
    for task, rec, exc in _parallel_manifest_records(
        tasks, with_media_meta, workers, progress_cb=progress_cb, base_bytes=done_bytes, total_bytes=total_bytes
    ):
        task_item_id, p, _root, surface, known_size, _known_mtime = task
        processed += 1
        if exc is not None or rec is None:
            _record_audit_error(db, run_id, "HASH", p, exc or "erro desconhecido")
            db.conn.execute(
                """UPDATE audit_file_queue SET status='ERROR',error=?,attempts=attempts+1,updated_at=?
                   WHERE run_id=? AND item_id=?""",
                (repr(exc), utc_now(), run_id, task_item_id),
            )
            failed_files += 1
            errors += 1
        else:
            db.conn.execute(
                """INSERT OR REPLACE INTO manifest(
                   run_id,item_id,source_path,surface,relative_path,filename,extension,size,sha256,created_ns,modified_ns,
                   attributes,mime,exif_datetime,exif_camera,media_creation_time,video_duration,video_width,video_height,video_codec
                   ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (run_id,task_item_id,rec["source_path"],rec["surface"],rec["relative_path"],rec["filename"],rec["extension"],
                 rec["size"],rec["sha256"],rec["created_ns"],rec["modified_ns"],rec["attributes"],rec["mime"],rec["exif_datetime"],
                 rec["exif_camera"],rec["media_creation_time"],rec["video_duration"],rec["video_width"],rec["video_height"],rec["video_codec"]),
            )
            db.conn.execute(
                "UPDATE audit_file_queue SET status='DONE',error=NULL,attempts=attempts+1,updated_at=? WHERE run_id=? AND item_id=?",
                (utc_now(), run_id, task_item_id),
            )
            db.conn.execute("DELETE FROM audit_errors WHERE run_id=? AND phase='HASH' AND path=?", (run_id, str(p)))
            done_files += 1
            done_bytes += int(rec["size"])
        db.conn.execute(
            """UPDATE audit_checkpoint SET phase='HASHING',total_files=?,total_bytes=?,completed_files=?,completed_bytes=?,
               failed_files=?,error_count=?,updated_at=? WHERE run_id=?""",
            (total_files, total_bytes, done_files, done_bytes, failed_files, errors, utc_now(), run_id),
        )
        db.conn.execute(
            "UPDATE runs SET scanned_files=?,scanned_bytes=?,scan_errors=? WHERE run_id=?",
            (done_files, done_bytes, errors, run_id),
        )
        # Commit por arquivo: em uma queda, tudo que chegou a DONE já está duravelmente salvo.
        db.conn.commit()
        write_audit_checkpoint_mirror(db, state_dir, run_id)
        _emit_progress(
            progress_cb, "file_done", completed=done_files + failed_files, completed_files=done_files,
            total_files=total_files, size=known_size, completed_bytes=done_bytes, total_bytes=total_bytes,
            path=str(p), surface=surface, errors=errors, failed_files=failed_files,
        )

    db.conn.execute(
        "UPDATE audit_checkpoint SET phase='FINALIZING',error_count=?,updated_at=? WHERE run_id=?",
        (_audit_error_count(db, run_id), utc_now(), run_id),
    )
    db.conn.commit()
    write_audit_checkpoint_mirror(db, state_dir, run_id, force=True)


def _finalize_audit(
    db: DB,
    state_dir: Path,
    run_id: str,
    workers: int,
    progress_cb: Optional[Callable[[str, dict[str, Any]], None]],
) -> str:
    _emit_progress(progress_cb, "finalizing", message="Consolidando diretórios, duplicatas e assinatura do manifesto")
    for r in db.conn.execute("SELECT path FROM dirs WHERE run_id=? AND protected=0 ORDER BY LENGTH(path) DESC", (run_id,)).fetchall():
        p = Path(r["path"])
        try:
            empty = not any(p.iterdir())
        except OSError:
            empty = False
        if empty:
            db.conn.execute("UPDATE dirs SET empty_at_scan=1 WHERE run_id=? AND path=?", (run_id, str(p)))
    for r in db.conn.execute("SELECT sha256,COUNT(*) c,MIN(source_path) canonical FROM manifest WHERE run_id=? GROUP BY sha256", (run_id,)):
        db.conn.execute(
            "UPDATE manifest SET duplicate_count=?,canonical_path=? WHERE run_id=? AND sha256=?",
            (r["c"], r["canonical"], run_id, r["sha256"]),
        )
    manifest_hash = compute_manifest_signature(db, run_id)
    total_files = int(db.conn.execute("SELECT COUNT(*) FROM audit_file_queue WHERE run_id=?", (run_id,)).fetchone()[0])
    done = db.conn.execute(
        "SELECT COUNT(*) c,COALESCE(SUM(size),0) b FROM audit_file_queue WHERE run_id=? AND status='DONE'", (run_id,)
    ).fetchone()
    errors = _audit_error_count(db, run_id)
    final_status = "AUDIT_BLOCKED_ERRORS" if errors else "AUDITED"
    db.conn.execute(
        "UPDATE runs SET scanned_files=?,scanned_bytes=?,scan_errors=?,manifest_hash=?,status=? WHERE run_id=?",
        (total_files, int(done["b"] or 0), errors, manifest_hash, final_status, run_id),
    )
    db.conn.execute(
        "UPDATE audit_checkpoint SET phase=?,completed_files=?,completed_bytes=?,failed_files=?,error_count=?,updated_at=? WHERE run_id=?",
        ("BLOCKED" if errors else "DONE", int(done["c"] or 0), int(done["b"] or 0),
         int(db.conn.execute("SELECT COUNT(*) FROM audit_file_queue WHERE run_id=? AND status='ERROR'", (run_id,)).fetchone()[0]),
         errors, utc_now(), run_id),
    )
    db.conn.commit()
    db.log(run_id, "AUDIT_FINISHED", {"files": total_files, "bytes": int(done["b"] or 0), "errors": errors, "manifest_hash": manifest_hash, "workers": workers})
    write_audit_checkpoint_mirror(db, state_dir, run_id, force=True)
    _emit_progress(progress_cb, "audit_done", files=total_files, bytes=int(done["b"] or 0), errors=errors, run_id=run_id)
    if errors:
        raise RuntimeError(f"Auditoria encontrou {errors} erro(s). O checkpoint foi salvo; nenhum plano executável será gerado até resolver.")
    classify_run(db, state_dir, run_id)
    export_audit(db, state_dir, run_id)
    return run_id


def _audit_execute_existing(
    db: DB,
    state_dir: Path,
    run_id: str,
    with_media_meta: bool,
    workers: Optional[int],
    progress_cb: Optional[Callable[[str, dict[str, Any]], None]],
) -> str:
    run = db.run(run_id)
    if not run:
        raise RuntimeError("Run não encontrado")
    f_root = Path(run["f_root"]); h_root = Path(run["h_root"])
    central = Path(run["central_root"]); archive = Path(run["archive_root"])
    if path_is_relative_to(state_dir, f_root) or path_is_relative_to(state_dir, h_root):
        raise RuntimeError("STATE_DIR precisa ficar fora de F:/H: para sobreviver a rollback/migração.")
    if not f_root.exists() or not h_root.exists():
        raise RuntimeError("F: ou H: não encontrados.")
    validate_rules_signature(state_dir)
    worker_n = audit_worker_count(workers)
    db.conn.execute("UPDATE runs SET status='AUDITING',app_version=? WHERE run_id=?", (APP_VERSION, run_id))
    db.conn.commit()
    _ensure_audit_checkpoint(db, run_id, f_root, h_root, worker_n)
    write_audit_checkpoint_mirror(db, state_dir, run_id, force=True)
    try:
        _inventory_resume(
            db, state_dir, run_id, bool(run["include_entire_drive"]), [central, archive, state_dir], progress_cb
        )
        _hash_resume(db, state_dir, run_id, with_media_meta, worker_n, progress_cb)
        return _finalize_audit(db, state_dir, run_id, worker_n, progress_cb)
    except KeyboardInterrupt:
        db.conn.rollback()
        db.conn.execute("UPDATE runs SET status='AUDIT_INTERRUPTED' WHERE run_id=?", (run_id,))
        db.conn.commit()
        with contextlib.suppress(Exception):
            write_audit_checkpoint_mirror(db, state_dir, run_id, force=True)
        raise
    except Exception:
        db.conn.rollback()
        current = db.run(run_id)
        if current and current["status"] == "AUDITING":
            db.conn.execute("UPDATE runs SET status='AUDIT_INTERRUPTED' WHERE run_id=?", (run_id,))
            db.conn.commit()
        with contextlib.suppress(Exception):
            write_audit_checkpoint_mirror(db, state_dir, run_id, force=True)
        raise


def audit_new(
    db: DB,
    state_dir: Path,
    f_root: Path,
    h_root: Path,
    include_entire_drive: bool,
    reserve_gb: int,
    with_media_meta: bool = True,
    workers: Optional[int] = None,
    progress_cb: Optional[Callable[[str, dict[str, Any]], None]] = None,
) -> str:
    central = h_root / CENTRAL_NAME; archive = f_root / ARCHIVE_NAME
    if path_is_relative_to(state_dir, f_root) or path_is_relative_to(state_dir, h_root):
        raise RuntimeError("STATE_DIR precisa ficar fora de F:/H: para sobreviver a rollback/migração.")
    if not f_root.exists() or not h_root.exists():
        raise RuntimeError("F: ou H: não encontrados.")
    rules_hash = validate_rules_signature(state_dir)
    run_id = dt.datetime.now().strftime("%Y%m%d-%H%M%S") + "-" + uuid.uuid4().hex[:6].upper()
    db.conn.execute(
        """INSERT INTO runs(run_id,created_at,app_version,f_root,h_root,central_root,archive_root,state_dir,
           include_entire_drive,reserve_bytes,status,rules_hash) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)""",
        (run_id, utc_now(), APP_VERSION, str(f_root), str(h_root), str(central), str(archive), str(state_dir),
         int(include_entire_drive), reserve_gb*1024**3, "AUDITING", rules_hash),
    )
    db.conn.commit(); db.log(run_id, "AUDIT_STARTED", {"workers": audit_worker_count(workers)})
    return _audit_execute_existing(db, state_dir, run_id, with_media_meta, workers, progress_cb)


def audit_resume(
    db: DB,
    state_dir: Path,
    run_id: str,
    with_media_meta: bool = True,
    workers: Optional[int] = None,
    progress_cb: Optional[Callable[[str, dict[str, Any]], None]] = None,
) -> str:
    run = db.run(run_id)
    if not run:
        raise RuntimeError("Auditoria para retomar não encontrada.")
    if run["status"] not in {"AUDITING", "AUDIT_INTERRUPTED"}:
        raise RuntimeError(f"A auditoria {run_id} não está em estado retomável: {run['status']}")
    db.log(run_id, "AUDIT_RESUMED", {"workers": audit_worker_count(workers)})
    return _audit_execute_existing(db, state_dir, run_id, with_media_meta, workers, progress_cb)

# ---------------------------------------------------------------------------
# Classificar + agrupar
# ---------------------------------------------------------------------------

def classify_run(db: DB, state_dir: Path, run_id: str) -> None:
    rules = load_rules(state_dir)
    db.conn.execute("DELETE FROM classifications WHERE run_id=?", (run_id,))
    db.conn.execute("DELETE FROM groups WHERE run_id=?", (run_id,))
    for r in db.conn.execute("SELECT * FROM manifest WHERE run_id=? ORDER BY item_id", (run_id,)):
        c = classify_item(r["source_path"], r["surface"], r["relative_path"], r["filename"], r["extension"], r["sha256"], r["duplicate_count"], r["exif_datetime"], r["media_creation_time"], rules)
        db.conn.execute("INSERT INTO classifications(run_id,item_id,storage,relative_dest,level,score,evidence_json,reason,rule_id) VALUES(?,?,?,?,?,?,?,?,?)",
                        (run_id,r["item_id"],c.storage,str(PureWindowsPath(*c.relative.parts)),c.level,c.score,json.dumps(c.evidence,ensure_ascii=False),c.reason,c.rule_id))
    db.conn.commit()
    build_groups(db, run_id)
    db.conn.execute("UPDATE runs SET rules_hash=? WHERE run_id=?", (validate_rules_signature(state_dir), run_id)); db.conn.commit()


def group_anchor(relative_path: str, level: str) -> str:
    """Agrupa por diretório pai imediato. Aprovação humana gerada pela TUI é
    não-recursiva, portanto nunca vaza silenciosamente para subpastas irmãs/filhas."""
    p = PureWindowsPath(relative_path)
    parent = p.parent
    return str(parent) if str(parent) not in {".", ""} else str(p)


def build_groups(db: DB, run_id: str) -> None:
    buckets: dict[tuple, list[sqlite3.Row]] = defaultdict(list)
    q = """SELECT m.*,c.level,c.storage,c.relative_dest,c.evidence_json FROM manifest m JOIN classifications c USING(run_id,item_id) WHERE m.run_id=?"""
    for r in db.conn.execute(q,(run_id,)):
        anchor = group_anchor(r["relative_path"], r["level"])
        # B/C por destino sem filename para juntar série; D por origem.
        dest_parts = list(PureWindowsPath(r["relative_dest"]).parts)
        dest_base = str(PureWindowsPath(*dest_parts[:-1])) if len(dest_parts)>1 else r["relative_dest"]
        key = (r["surface"], anchor, r["level"], r["storage"], dest_base)
        buckets[key].append(r)
    for idx, (key, rows) in enumerate(sorted(buckets.items(), key=lambda kv: (kv[0][2],kv[0][1])),1):
        surface, anchor, level, storage, dest_base = key
        root = db.run(run_id)["f_root"] if surface=="F" else db.run(run_id)["h_root"]
        prefix = str(Path(root) / Path(*PureWindowsPath(anchor).parts))
        ev = []
        for r in rows[:20]: ev.extend(json.loads(r["evidence_json"]))
        ev = list(dict.fromkeys(ev))[:12]
        gid = f"G{idx:05d}"
        db.conn.execute("INSERT INTO groups(run_id,group_id,source_prefix,surface,level,storage,relative_dest,item_count,total_bytes,evidence_json,status) VALUES(?,?,?,?,?,?,?,?,?,?,?)",
                        (run_id,gid,prefix,surface,level,storage,dest_base,len(rows),sum(int(r["size"]) for r in rows),json.dumps(ev,ensure_ascii=False),"PENDING"))
    db.conn.commit()


def level_counts(db: DB, run_id: str) -> dict[str,int]:
    d = {k:0 for k in LEVELS}
    for r in db.conn.execute("SELECT level,COUNT(*) c FROM classifications WHERE run_id=? GROUP BY level",(run_id,)):
        d[r["level"]] = r["c"]
    return d

# ---------------------------------------------------------------------------
# Exportação / plano imutável
# ---------------------------------------------------------------------------

def export_audit(db: DB, state_dir: Path, run_id: str) -> None:
    out = state_dir / f"AUDITORIA_{run_id}"
    out.mkdir(parents=True, exist_ok=True)
    cols = ["item_id","source_path","surface","relative_path","filename","extension","size","sha256","created_ns","modified_ns","attributes","mime","exif_datetime","exif_camera","media_creation_time","video_duration","video_width","video_height","video_codec","duplicate_count","canonical_path"]
    with (out/"manifesto_pre.csv").open("w",encoding="utf-8-sig",newline="") as f:
        w=csv.writer(f,delimiter=";"); w.writerow(cols)
        for r in db.conn.execute("SELECT * FROM manifest WHERE run_id=? ORDER BY item_id",(run_id,)): w.writerow([r[c] for c in cols])
    with (out/"manifesto_pre.jsonl").open("w",encoding="utf-8") as f:
        for r in db.conn.execute("SELECT * FROM manifest WHERE run_id=? ORDER BY item_id",(run_id,)):
            f.write(json.dumps(dict(r),ensure_ascii=False,sort_keys=True)+"\n")
    with (out/"classificacoes.csv").open("w",encoding="utf-8-sig",newline="") as f:
        w=csv.writer(f,delimiter=";"); w.writerow(["item_id","source","level","score","storage","destino_sugerido","motivo","evidencias"])
        q="""SELECT m.source_path,c.* FROM manifest m JOIN classifications c USING(run_id,item_id) WHERE m.run_id=? ORDER BY c.level,c.score DESC"""
        for r in db.conn.execute(q,(run_id,)): w.writerow([r["item_id"],r["source_path"],r["level"],r["score"],r["storage"],r["relative_dest"],r["reason"],r["evidence_json"]])
    with (out/"grupos.csv").open("w",encoding="utf-8-sig",newline="") as f:
        w=csv.writer(f,delimiter=";"); w.writerow(["group_id","level","origem","storage","destino_sugerido","arquivos","bytes","evidencias"])
        for r in db.conn.execute("SELECT * FROM groups WHERE run_id=? ORDER BY level,source_prefix",(run_id,)): w.writerow([r["group_id"],r["level"],r["source_prefix"],r["storage"],r["relative_dest"],r["item_count"],r["total_bytes"],r["evidence_json"]])
    counts = level_counts(db,run_id); run=db.run(run_id)
    summary = [f"{APP_NAME} v{APP_VERSION}",f"RUN: {run_id}",f"Manifest SHA-256: {run['manifest_hash']}",f"Rules SHA-256: {run['rules_hash']}","",
               f"A — EXPLÍCITO: {counts['A']}",f"B — COMPROVADO: {counts['B']}",f"C — PROVÁVEL: {counts['C']}",f"D — AMBÍGUO: {counts['D']}",f"E — LEGADO APROVADO: {counts['E']}","",
               "ZERO-AMBIGUITY GATE: "+("PASS" if counts['C']==0 and counts['D']==0 else "BLOCKED"),
               "Nenhuma alteração em F:/H: ocorreu durante esta auditoria."]
    atomic_write_text(out/"RESUMO.txt","\n".join(summary)+"\n")


def plan_signature(db: DB, run_id: str, rules_hash: str, allow_b: bool) -> str:
    run=db.run(run_id); h=hashlib.sha256()
    header={"run_id":run_id,"manifest_hash":run["manifest_hash"],"rules_hash":rules_hash,"allow_b":bool(allow_b),"reserve_bytes":run["reserve_bytes"],"app_version":APP_VERSION}
    h.update(json.dumps(header,sort_keys=True,separators=(",",":")).encode()); h.update(b"\n")
    for r in db.conn.execute("SELECT item_id,source_before,destination_after,storage,level,op_mode,expected_size,expected_mtime_ns,sha256_before FROM ops WHERE run_id=? ORDER BY op_id",(run_id,)):
        h.update(json.dumps(dict(r),ensure_ascii=False,sort_keys=True,separators=(",",":")).encode()); h.update(b"\n")
    return h.hexdigest()


def cross_space_requirements(db: DB, run_id: str) -> tuple[int,int]:
    """Retorna (bytes_para_H, bytes_para_F)."""
    to_h = to_f = 0
    for r in db.conn.execute("SELECT storage,expected_size FROM ops WHERE run_id=? AND op_mode='CROSS_VOLUME_SAFE_COPY'",(run_id,)):
        if r["storage"] == "DRIVE": to_h += int(r["expected_size"])
        else: to_f += int(r["expected_size"])
    return to_h,to_f

def free_space_required(db: DB, run_id: str) -> int:
    a,b=cross_space_requirements(db,run_id); return a+b


def generate_plan(db: DB, state_dir: Path, run_id: str, allow_b: bool=False) -> str:
    run=db.run(run_id)
    if not run: raise RuntimeError("Run não encontrado")
    if run["scan_errors"]: raise RuntimeError("Run possui erros de auditoria.")
    validate_rules_signature(state_dir)
    classify_run(db,state_dir,run_id)
    counts=level_counts(db,run_id)
    if counts[LEVEL_C] or counts[LEVEL_D]:
        raise RuntimeError(f"ZERO-AMBIGUITY GATE bloqueado: C={counts['C']} D={counts['D']}")
    if counts[LEVEL_B] and not allow_b:
        raise RuntimeError(f"Existem {counts['B']} itens B. Aprove-os como A/E ou gere plano explicitamente liberando B.")
    db.conn.execute("DELETE FROM ops WHERE run_id=?",(run_id,)); db.conn.commit()
    reserved=set(); op_id=0
    q="""SELECT m.*,c.storage,c.relative_dest,c.level FROM manifest m JOIN classifications c USING(run_id,item_id) WHERE m.run_id=? ORDER BY m.item_id"""
    for r in db.conn.execute(q,(run_id,)):
        if r["level"] not in ({LEVEL_A,LEVEL_E,LEVEL_B} if allow_b else {LEVEL_A,LEVEL_E}):
            raise RuntimeError(f"Nível não executável encontrado: {r['level']}")
        src=Path(r["source_path"]); storage=r["storage"]
        dst_root=Path(run["central_root"]) if storage=="DRIVE" else Path(run["archive_root"])
        rel=Path(*PureWindowsPath(r["relative_dest"]).parts)
        rel, changes=fit_windows_path(dst_root,rel,src)
        dst=dst_root/rel
        key=os.path.normcase(str(dst))
        if key in reserved or dst.exists():
            token=hashlib.sha256(r["source_path"].encode("utf-8",errors="replace")).hexdigest()[:10]
            base=dst
            i=1
            while True:
                suffix=f"__COLISAO_{token}" if i==1 else f"__COLISAO_{token}_{i}"
                candidate=base.with_name(f"{base.stem}{suffix}{base.suffix}")
                ckey=os.path.normcase(str(candidate))
                if ckey not in reserved and not candidate.exists():
                    dst=candidate;key=ckey;break
                i+=1
            db.log(run_id,"DESTINATION_COLLISION_PLANNED",{"source":str(src),"chosen":str(dst)})
        reserved.add(key)
        # H->central e F->archive são same volume; F->central é cross.
        mode="SAME_VOLUME"
        if r["surface"]=="F" and storage=="DRIVE": mode="CROSS_VOLUME_SAFE_COPY"
        if r["surface"]=="H" and storage=="ARCHIVE": mode="CROSS_VOLUME_SAFE_COPY"  # raro/restrito: H -> F
        op_id+=1
        db.conn.execute("INSERT INTO ops(run_id,op_id,item_id,source_before,destination_after,storage,level,op_mode,expected_size,expected_mtime_ns,sha256_before,status,updated_at) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)",
                        (run_id,op_id,r["item_id"],str(src),str(dst),storage,r["level"],mode,r["size"],r["modified_ns"],r["sha256"],STATUS_PLANNED,utc_now()))
        if changes: db.log(run_id,"PATH_SANITIZED",{"source":str(src),"changes":changes})
    db.conn.commit()
    to_h,to_f=cross_space_requirements(db,run_id); required=to_h+to_f
    h_root=Path(run["h_root"]); f_root=Path(run["f_root"]); reserve=int(run["reserve_bytes"])
    if to_h and h_root.exists():
        free_h=shutil.disk_usage(h_root).free
        if to_h + reserve > free_h:
            raise RuntimeError(f"Espaço insuficiente em H:. necessário={bytes_human(to_h+reserve)}, livre={bytes_human(free_h)}")
    if to_f and f_root.exists():
        free_f=shutil.disk_usage(f_root).free
        if to_f + reserve > free_f:
            raise RuntimeError(f"Espaço insuficiente em F: para transferências H→F. necessário={bytes_human(to_f+reserve)}, livre={bytes_human(free_f)}")
    rh=validate_rules_signature(state_dir); sig=plan_signature(db,run_id,rh,allow_b)
    db.conn.execute("UPDATE runs SET plan_signature=?,plan_allow_b=?,rules_hash=?,status='PLAN_VALIDATED' WHERE run_id=?",(sig,int(allow_b),rh,run_id)); db.conn.commit()
    out=state_dir/f"AUDITORIA_{run_id}"; out.mkdir(parents=True,exist_ok=True)
    with (out/"plano.csv").open("w",encoding="utf-8-sig",newline="") as f:
        w=csv.writer(f,delimiter=";"); w.writerow(["op_id","level","modo","origem","destino","bytes","sha256"])
        for r in db.conn.execute("SELECT * FROM ops WHERE run_id=? ORDER BY op_id",(run_id,)): w.writerow([r["op_id"],r["level"],r["op_mode"],r["source_before"],r["destination_after"],r["expected_size"],r["sha256_before"]])
    atomic_write_text(out/"plano.sha256",sig+"\n")
    db.log(run_id,"PLAN_GENERATED",{"signature":sig,"allow_b":allow_b,"cross_bytes":required})
    return sig


def validate_plan_immutable(db: DB, state_dir: Path, run_id: str) -> str:
    run=db.run(run_id); current_rules=validate_rules_signature(state_dir)
    if current_rules != run["rules_hash"]: raise RuntimeError("Regras mudaram desde a geração do plano.")
    current_manifest=compute_manifest_signature(db,run_id)
    if current_manifest != run["manifest_hash"]: raise RuntimeError("Manifesto interno mudou desde a auditoria.")
    sig=plan_signature(db,run_id,current_rules,bool(run["plan_allow_b"]))
    if sig != run["plan_signature"]: raise RuntimeError("Plano foi alterado/adulterado.")
    side=state_dir/f"AUDITORIA_{run_id}"/"plano.sha256"
    if not side.exists() or side.read_text(encoding="utf-8").strip()!=sig: raise RuntimeError("Assinatura externa do plano inválida.")
    return sig

# ---------------------------------------------------------------------------
# Execução transacional
# ---------------------------------------------------------------------------

def stable_stat_matches(path: Path, expected_size: int, expected_mtime_ns: Optional[int]) -> bool:
    try: st=path.stat()
    except OSError: return False
    return st.st_size==expected_size and (expected_mtime_ns is None or st.st_mtime_ns==expected_mtime_ns)


def make_parent(dst: Path): dst.parent.mkdir(parents=True,exist_ok=True)


def exclusive_tmp(dst: Path) -> Path:
    return dst.with_name(dst.name+f".ACIRV-V2-TMP-{uuid.uuid4().hex}")


def copy_locked_to_temp(src: Path, dst: Path, expected_hash: str, expected_size: int,
                        mutate_hook: Optional[Callable[[Path,Path],None]]=None,
                        on_copy_bytes: Optional[Callable[[int], None]]=None) -> tuple[Path,str]:
    if dst.exists(): raise FileExistsError(f"Destino já existe: {dst}")
    make_parent(dst); tmp=exclusive_tmp(dst)
    if tmp.exists(): raise FileExistsError(tmp)
    with LockedSource(src) as sf:
        st1=src.stat()
        if st1.st_size != expected_size: raise RuntimeError("SOURCE_CHANGED:size")
        sf.seek(0); hsrc=hashlib.sha256(); copied=0
        fd=os.open(tmp,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
        try:
            with os.fdopen(fd,"wb",buffering=0) as df:
                while True:
                    b=sf.read(COPY_CHUNK)
                    if not b: break
                    hsrc.update(b); df.write(b); copied+=len(b)
                    if on_copy_bytes:
                        on_copy_bytes(len(b))
                df.flush(); os.fsync(df.fileno())
            if mutate_hook: mutate_hook(src,tmp)
            if copied != expected_size: raise RuntimeError("SOURCE_CHANGED:copied_size")
            src_hash=hsrc.hexdigest()
            if src_hash != expected_hash: raise RuntimeError("SOURCE_CHANGED:hash")
            tmp_hash=sha256_file(tmp)
            if tmp_hash != expected_hash: raise RuntimeError("COPY_CORRUPTED:hash")
            with contextlib.suppress(Exception): shutil.copystat(src,tmp,follow_symlinks=False)
            return tmp,tmp_hash
        except Exception:
            with contextlib.suppress(FileNotFoundError): tmp.unlink()
            raise


def quarantine_path_for(src: Path, run: sqlite3.Row, expected_hash: str) -> Path:
    archive=Path(run["archive_root"])
    try: rel=src.relative_to(Path(run["f_root"]))
    except Exception: rel=Path(src.name)
    return archive/"99_DUPLICADOS — QUARENTENA"/"_MIGRADOS_PARA_DRIVE"/expected_hash[:2]/expected_hash[:12]/rel


def h_rollback_copy_path(dst: Path, run: sqlite3.Row, expected_hash: str) -> Path:
    central=Path(run["central_root"])
    try: rel=dst.relative_to(central)
    except Exception: rel=Path(dst.name)
    return central/"90_LEGADO — A REVISAR"/"_ROLLBACK_COPIES"/expected_hash[:12]/rel


def execute_one(
    db: DB,
    run_id: str,
    op: sqlite3.Row,
    test_mutate_hook=None,
    progress_cb: Optional[Callable[[str, dict[str, Any]], None]] = None,
) -> None:
    run=db.run(run_id); src=Path(op["source_before"]); dst=Path(op["destination_after"]); expected=op["sha256_before"]
    if op["status"] in {STATUS_DONE,STATUS_REMOTE_VERIFIED}:
        _emit_progress(progress_cb, "op_done", op_id=op["op_id"], size=int(op["expected_size"]), path=str(src), skipped=True)
        return
    _emit_progress(progress_cb, "op_start", op_id=op["op_id"], size=int(op["expected_size"]), path=str(src), destination=str(dst), mode=op["op_mode"])
    if dst.exists() and op["status"] == STATUS_PLANNED:
        raise FileExistsError("Destino apareceu após o plano; operação bloqueada")
    if not src.exists() and op["status"] == STATUS_PLANNED:
        raise FileNotFoundError("Origem desapareceu após o plano")
    if op["status"] == STATUS_PLANNED and not stable_stat_matches(src,op["expected_size"],op["expected_mtime_ns"]):
        raise RuntimeError("SOURCE_CHANGED:stat")
    db.conn.execute("UPDATE ops SET status=?,updated_at=? WHERE run_id=? AND op_id=?",(STATUS_COPYING,utc_now(),run_id,op["op_id"])); db.conn.commit()

    def byte_tick(n: int) -> None:
        _emit_progress(progress_cb, "op_bytes", op_id=op["op_id"], delta=int(n), path=str(src))

    if op["op_mode"]=="SAME_VOLUME":
        _emit_progress(progress_cb, "op_phase", op_id=op["op_id"], phase="Validando hash da origem", path=str(src))
        with LockedSource(src) as f:
            if hash_open_file(f, on_bytes=byte_tick)!=expected: raise RuntimeError("SOURCE_CHANGED:hash")
            if dst.exists(): raise FileExistsError(dst)
            make_parent(dst)
            _emit_progress(progress_cb, "op_phase", op_id=op["op_id"], phase="Movendo no mesmo volume", path=str(src))
            os.rename(src,dst); fsync_dir(dst.parent)
        _emit_progress(progress_cb, "op_phase", op_id=op["op_id"], phase="Verificando destino", path=str(dst))
        if sha256_file(dst)!=expected: raise RuntimeError("POST_RENAME_HASH_MISMATCH")
        db.conn.execute("UPDATE ops SET sha256_after=?,final_path=?,status=?,updated_at=? WHERE run_id=? AND op_id=?",(expected,str(dst),STATUS_DONE,utc_now(),run_id,op["op_id"]));db.conn.commit()
    else:
        _emit_progress(progress_cb, "op_phase", op_id=op["op_id"], phase="Copiando com hash simultâneo", path=str(src))
        tmp,tmp_hash=copy_locked_to_temp(src,dst,expected,op["expected_size"],test_mutate_hook,on_copy_bytes=byte_tick)
        db.conn.execute("UPDATE ops SET status=?,sha256_after=?,updated_at=? WHERE run_id=? AND op_id=?",(STATUS_HASH_VERIFIED,tmp_hash,utc_now(),run_id,op["op_id"]));db.conn.commit()
        if dst.exists():
            tmp.unlink(missing_ok=True); raise FileExistsError(dst)
        _emit_progress(progress_cb, "op_phase", op_id=op["op_id"], phase="Publicando destino", path=str(dst))
        os.rename(tmp,dst); fsync_dir(dst.parent)
        if sha256_file(dst)!=expected: raise RuntimeError("POST_PUBLISH_HASH_MISMATCH")
        db.conn.execute("UPDATE ops SET status=?,final_path=?,updated_at=? WHERE run_id=? AND op_id=?",(STATUS_PUBLISHED,str(dst),utc_now(),run_id,op["op_id"]));db.conn.commit()
        # F -> Drive: origem vai para quarentena; H -> F também preserva a origem em quarentena do volume de origem.
        if str(src).lower().startswith(str(Path(run["f_root"])).lower()):
            q=quarantine_path_for(src,run,expected)
        else:
            # cópia H->F: preserva origem H em central/rollback-like quarantine
            q=h_rollback_copy_path(src,run,expected)
        if q.exists(): raise FileExistsError(f"Quarentena já existe: {q}")
        make_parent(q)
        _emit_progress(progress_cb, "op_phase", op_id=op["op_id"], phase="Revalidando origem e enviando à quarentena", path=str(src))
        # revalida fonte imediatamente antes do rename para quarentena.
        with LockedSource(src) as f:
            if hash_open_file(f)!=expected: raise RuntimeError("SOURCE_CHANGED_AFTER_COPY")
            os.rename(src,q); fsync_dir(q.parent)
        if sha256_file(q)!=expected: raise RuntimeError("QUARANTINE_HASH_MISMATCH")
        db.conn.execute("UPDATE ops SET quarantine_path=?,status=?,updated_at=? WHERE run_id=? AND op_id=?",(str(q),STATUS_DONE,utc_now(),run_id,op["op_id"]));db.conn.commit()
    _emit_progress(progress_cb, "op_done", op_id=op["op_id"], size=int(op["expected_size"]), path=str(src), skipped=False)


def execute_plan(
    db: DB,
    state_dir: Path,
    run_id: str,
    confirmation: str,
    progress_cb: Optional[Callable[[str, dict[str, Any]], None]] = None,
) -> None:
    if os.name != "nt" and os.environ.get("ACIRV_V2_TEST_EXECUTION")!="1":
        raise RuntimeError("Execução real é bloqueada fora do Windows.")
    sig=validate_plan_immutable(db,state_dir,run_id)
    expected_phrase=f"EXECUTAR {sig[:12].upper()}"
    if confirmation.strip()!=expected_phrase: raise RuntimeError(f"Confirmação inválida. Era necessário: {expected_phrase}")
    counts=level_counts(db,run_id)
    if counts[LEVEL_C] or counts[LEVEL_D]: raise RuntimeError("Zero-Ambiguity Gate deixou de ser PASS")
    run=db.run(run_id); to_h,to_f=cross_space_requirements(db,run_id); reserve=int(run["reserve_bytes"])
    if to_h and shutil.disk_usage(Path(run["h_root"])).free < to_h+reserve: raise RuntimeError("Espaço em H: deixou de ser suficiente")
    if to_f and shutil.disk_usage(Path(run["f_root"])).free < to_f+reserve: raise RuntimeError("Espaço em F: deixou de ser suficiente")
    ops=db.conn.execute("SELECT * FROM ops WHERE run_id=? ORDER BY op_id",(run_id,)).fetchall()
    total_bytes=sum(int(op["expected_size"]) for op in ops if op["status"] not in {STATUS_DONE,STATUS_REMOTE_VERIFIED})
    _emit_progress(progress_cb, "plan_start", total_ops=len(ops), total_bytes=total_bytes)
    db.conn.execute("UPDATE runs SET status='EXECUTING' WHERE run_id=?",(run_id,));db.conn.commit()
    for index,op in enumerate(ops,1):
        _emit_progress(progress_cb, "plan_op", index=index, total_ops=len(ops), op_id=op["op_id"], path=op["source_before"])
        try:
            execute_one(db,run_id,op,progress_cb=progress_cb)
            db.log(run_id,"OP_DONE",{"op_id":op["op_id"]})
        except (PermissionError,RuntimeError) as e:
            msg=str(e)
            status=STATUS_SKIPPED_CHANGED if ("SOURCE_CHANGED" in msg or isinstance(e,PermissionError)) else STATUS_FAILED
            db.conn.execute("UPDATE ops SET status=?,error=?,updated_at=? WHERE run_id=? AND op_id=?",(status,msg,utc_now(),run_id,op["op_id"]));db.conn.commit()
            db.log(run_id,"OP_BLOCKED",{"op_id":op["op_id"],"error":msg},"ERROR")
            db.conn.execute("UPDATE runs SET status='EXECUTION_BLOCKED' WHERE run_id=?",(run_id,));db.conn.commit()
            _emit_progress(progress_cb, "plan_error", op_id=op["op_id"], error=msg)
            raise
        except Exception as e:
            db.conn.execute("UPDATE ops SET status=?,error=?,updated_at=? WHERE run_id=? AND op_id=?",(STATUS_FAILED,repr(e),utc_now(),run_id,op["op_id"]));db.conn.commit()
            db.conn.execute("UPDATE runs SET status='EXECUTION_BLOCKED' WHERE run_id=?",(run_id,));db.conn.commit()
            _emit_progress(progress_cb, "plan_error", op_id=op["op_id"], error=repr(e))
            raise
    _emit_progress(progress_cb, "plan_phase", message="Arquivando estrutura de pastas vazias")
    archive_empty_directories(db,run_id)
    db.conn.execute("UPDATE runs SET status='EXECUTED_LOCAL' WHERE run_id=?",(run_id,));db.conn.commit()
    _emit_progress(progress_cb, "plan_done", total_ops=len(ops), total_bytes=total_bytes)


def resume_plan(
    db: DB,
    state_dir: Path,
    run_id: str,
    confirmation: str,
    progress_cb: Optional[Callable[[str, dict[str, Any]], None]] = None,
) -> None:
    # Estados intermediários não são repetidos cegamente. Primeiro reconciliamos.
    _emit_progress(progress_cb, "plan_phase", message="Reconciliando execução interrompida")
    reconcile_interrupted(db,run_id)
    execute_plan(db,state_dir,run_id,confirmation,progress_cb=progress_cb)


def reconcile_interrupted(db: DB, run_id: str) -> None:
    for op in db.conn.execute("SELECT * FROM ops WHERE run_id=? AND status NOT IN (?,?,?,?)",(run_id,STATUS_PLANNED,STATUS_DONE,STATUS_REMOTE_VERIFIED,STATUS_ROLLBACK_DONE)).fetchall():
        src=Path(op["source_before"]); dst=Path(op["destination_after"]); q=Path(op["quarantine_path"]) if op["quarantine_path"] else None; h=op["sha256_before"]
        # Se dst publicado e fonte/quarentena preservada, reconhece progresso.
        try:
            dst_ok=dst.exists() and sha256_file(dst)==h
            q_ok=q is not None and q.exists() and sha256_file(q)==h
            src_ok=src.exists() and sha256_file(src)==h
        except Exception:
            dst_ok=q_ok=src_ok=False
        if dst_ok and (q_ok or src_ok):
            if src_ok and op["op_mode"]=="CROSS_VOLUME_SAFE_COPY" and q is None:
                # ainda falta quarentenar; volta para PLANNED só se dst for removido? Não removemos.
                db.conn.execute("UPDATE ops SET status=?,error=? WHERE run_id=? AND op_id=?",(STATUS_FAILED,"Destino já publicado, fonte ainda não quarentenada; auditoria manual necessária",run_id,op["op_id"]))
            else:
                db.conn.execute("UPDATE ops SET status=?,sha256_after=?,final_path=?,error=NULL WHERE run_id=? AND op_id=?",(STATUS_DONE,h,str(dst),run_id,op["op_id"]))
        elif not dst_ok and src_ok:
            # temp residual pode ser removido apenas se nome do próprio migrador; bytes fonte intactos.
            for tmp in dst.parent.glob(dst.name+".ACIRV-V2-TMP-*") if dst.parent.exists() else []:
                with contextlib.suppress(Exception): tmp.unlink()
            db.conn.execute("UPDATE ops SET status=?,error=NULL WHERE run_id=? AND op_id=?",(STATUS_PLANNED,run_id,op["op_id"]))
        else:
            db.conn.execute("UPDATE ops SET status=?,error=? WHERE run_id=? AND op_id=?",(STATUS_FAILED,"Estado interrompido não reconciliável automaticamente",run_id,op["op_id"]))
    db.conn.commit()


def archive_empty_directories(db: DB, run_id: str) -> None:
    run=db.run(run_id)
    rows=db.conn.execute("SELECT * FROM dirs WHERE run_id=? AND empty_at_scan=1 AND protected=0 ORDER BY LENGTH(path) DESC",(run_id,)).fetchall()
    for r in rows:
        p=Path(r["path"])
        if not p.exists() or not p.is_dir(): continue
        try:
            if any(p.iterdir()): continue
        except OSError: continue
        if r["surface"]=="F": root=Path(run["archive_root"]); rel=Path("90_LEGADO — A REVISAR")/"_PASTAS_VAZIAS"/Path(*PureWindowsPath(r["relative_path"]).parts)
        else: root=Path(run["central_root"]); rel=Path("90_LEGADO — A REVISAR")/"_PASTAS_VAZIAS"/Path(*PureWindowsPath(r["relative_path"]).parts)
        dst=root/rel
        if dst.exists(): continue
        dst.mkdir(parents=True,exist_ok=False)
        # rmdir somente diretório vazio; não apaga conteúdo.
        with contextlib.suppress(OSError): p.rmdir()

# ---------------------------------------------------------------------------
# Rollback preservador
# ---------------------------------------------------------------------------

def rollback_run(db: DB, state_dir: Path, run_id: str, confirmation: str) -> tuple[int,int]:
    validate_plan_immutable(db,state_dir,run_id)
    expected=f"REVERTER {run_id}"
    if confirmation.strip()!=expected: raise RuntimeError(f"Confirmação inválida. Use exatamente: {expected}")
    done=blocked=0; run=db.run(run_id)
    for op in db.conn.execute("SELECT * FROM ops WHERE run_id=? AND status IN (?,?,?) ORDER BY op_id DESC",(run_id,STATUS_DONE,STATUS_REMOTE_VERIFIED,STATUS_ROLLBACK_BLOCKED)).fetchall():
        src=Path(op["source_before"]); dst=Path(op["final_path"] or op["destination_after"]); h=op["sha256_before"]
        try:
            if not dst.exists() or sha256_file(dst)!=h:
                raise RuntimeError("destino modificado ou ausente")
            if src.exists(): raise RuntimeError("caminho original já ocupado")
            if op["op_mode"]=="SAME_VOLUME":
                src.parent.mkdir(parents=True,exist_ok=True); os.rename(dst,src)
                if sha256_file(src)!=h: raise RuntimeError("hash pós-rollback divergente")
            else:
                q=Path(op["quarantine_path"] or "")
                if not q.exists() or sha256_file(q)!=h: raise RuntimeError("fonte em quarentena modificada/ausente")
                src.parent.mkdir(parents=True,exist_ok=True); os.rename(q,src)
                # Preserva a cópia do Drive em quarentena de rollback em vez de apagar.
                rb=h_rollback_copy_path(dst,run,h); rb.parent.mkdir(parents=True,exist_ok=True)
                if rb.exists(): raise RuntimeError("quarentena de rollback já existe")
                os.rename(dst,rb)
            db.conn.execute("UPDATE ops SET status=?,updated_at=?,error=NULL WHERE run_id=? AND op_id=?",(STATUS_ROLLBACK_DONE,utc_now(),run_id,op["op_id"]));db.conn.commit();done+=1
        except Exception as e:
            db.conn.execute("UPDATE ops SET status=?,updated_at=?,error=? WHERE run_id=? AND op_id=?",(STATUS_ROLLBACK_BLOCKED,utc_now(),str(e),run_id,op["op_id"]));db.conn.commit();blocked+=1
    db.conn.execute("UPDATE runs SET status=? WHERE run_id=?",("ROLLED_BACK" if blocked==0 else "ROLLBACK_PARTIAL",run_id));db.conn.commit()
    return done,blocked

# ---------------------------------------------------------------------------
# Manifesto pós + multiconjunto de hashes
# ---------------------------------------------------------------------------

def post_audit(db: DB, run_id: str) -> dict[str,Any]:
    run=db.run(run_id); db.conn.execute("DELETE FROM post_manifest WHERE run_id=?",(run_id,));db.conn.commit()
    f_root=Path(run["f_root"]);h_root=Path(run["h_root"]); central=Path(run["central_root"]);archive=Path(run["archive_root"])
    # pós-auditoria inclui todo escopo original + destinos, sem excluir central/archive.
    for surface,root in (("H",h_root),("F",f_root)):
        for kind,p,st,issue in iter_tree(root,[],surface,bool(run["include_entire_drive"])):
            if kind!="FILE": continue
            try:
                h=sha256_file(p)
                db.conn.execute("INSERT OR REPLACE INTO post_manifest(run_id,path,surface,size,sha256) VALUES(?,?,?,?,?)",(run_id,str(p),surface,st.st_size,h))
            except Exception as e:
                db.log(run_id,"POST_AUDIT_ERROR",{"path":str(p),"error":repr(e)},"ERROR")
        db.conn.commit()
    # ACIRV — CENTRAL é excluído do escopo H pré-migração por design; no pós ele precisa
    # ser incluído explicitamente para provar movimentos H→Central.
    if central.exists():
        for kind,p,st,issue in iter_tree(central,[],"H",True):
            if kind!="FILE": continue
            try:
                h=sha256_file(p)
                db.conn.execute("INSERT OR REPLACE INTO post_manifest(run_id,path,surface,size,sha256) VALUES(?,?,?,?,?)",(run_id,str(p),"H",st.st_size,h))
            except Exception as e:
                db.log(run_id,"POST_AUDIT_ERROR",{"path":str(p),"error":repr(e)},"ERROR")
        db.conn.commit()
    pre=Counter({r["sha256"]:r["c"] for r in db.conn.execute("SELECT sha256,COUNT(*) c FROM manifest WHERE run_id=? GROUP BY sha256",(run_id,))})
    post=Counter({r["sha256"]:r["c"] for r in db.conn.execute("SELECT sha256,COUNT(*) c FROM post_manifest WHERE run_id=? GROUP BY sha256",(run_id,))})
    missing={h:c-post.get(h,0) for h,c in pre.items() if post.get(h,0)<c}
    result={"status":"PASS" if not missing else "FAIL","expected_unique_hashes":len(pre),"post_unique_hashes":len(post),"missing":missing}
    db.log(run_id,"GLOBAL_INTEGRITY",result,"INFO" if not missing else "ERROR")
    return result

# ---------------------------------------------------------------------------
# Verificação remota opcional via rclone
# ---------------------------------------------------------------------------

def remote_verify_rclone(db: DB, state_dir: Path, run_id: str, remote_root: str) -> dict[str,Any]:
    exe=shutil.which("rclone")
    if not exe: return {"status":"NOT_ENABLED","reason":"rclone não instalado"}
    run=db.run(run_id); central=Path(run["central_root"])
    rels=[]; native_unverifiable=[]
    for r in db.conn.execute("SELECT final_path FROM ops WHERE run_id=? AND storage='DRIVE' AND status IN (?,?)",(run_id,STATUS_DONE,STATUS_REMOTE_VERIFIED)):
        p=Path(r["final_path"])
        try: rel=p.relative_to(central)
        except Exception: continue
        if p.suffix.lower() in GOOGLE_NATIVE_STUBS:
            native_unverifiable.append(rel.as_posix()); continue
        rels.append(rel.as_posix())
    if not rels:
        return {"status":"PARTIAL" if native_unverifiable else "PASS","checked":0,"google_native_unverifiable":native_unverifiable}
    files_from=state_dir/f"AUDITORIA_{run_id}"/"rclone-files-from.txt"
    atomic_write_text(files_from,"\n".join(rels)+"\n")
    report=state_dir/f"AUDITORIA_{run_id}"/"rclone-combined.txt"
    cmd=[exe,"check",str(central),remote_root,"--files-from-raw",str(files_from),"--one-way","--download","--combined",str(report)]
    cp=subprocess.run(cmd,capture_output=True,text=True)
    if cp.returncode==0:
        db.conn.execute("UPDATE ops SET status=?,updated_at=? WHERE run_id=? AND storage='DRIVE' AND status=?",(STATUS_REMOTE_VERIFIED,utc_now(),run_id,STATUS_DONE));db.conn.commit()
        return {"status":"PARTIAL" if native_unverifiable else "PASS","checked":len(rels),"command":cmd,"google_native_unverifiable":native_unverifiable}
    return {"status":"FAIL","checked":len(rels),"returncode":cp.returncode,"stderr":cp.stderr[-4000:],"report":str(report),"google_native_unverifiable":native_unverifiable}

# ---------------------------------------------------------------------------
# Galeria HTML de revisão
# ---------------------------------------------------------------------------

def ensure_pillow() -> None:
    try: import PIL.Image
    except ImportError:
        ensure_dependency("PIL","Pillow>=10,<13")


def thumb_image(src: Path,dst: Path,max_size=(320,220)) -> bool:
    try:
        from PIL import Image,ImageOps
        dst.parent.mkdir(parents=True,exist_ok=True)
        with Image.open(src) as im:
            im=ImageOps.exif_transpose(im); im.thumbnail(max_size); im.convert("RGB").save(dst,"JPEG",quality=82,optimize=True)
        return True
    except Exception: return False


def video_frames(src: Path,out_dir: Path) -> list[Path]:
    exe=ffmpeg_path()
    if not exe: return []
    out=[]
    # três tempos relativos simples; -ss antes de -i é rápido e não altera original.
    for i,sec in enumerate((1,5,12),1):
        p=out_dir/f"frame{i}.jpg"; p.parent.mkdir(parents=True,exist_ok=True)
        cp=subprocess.run([exe,"-y","-ss",str(sec),"-i",str(src),"-frames:v","1","-vf","scale='min(480,iw)':-2",str(p)],capture_output=True)
        if cp.returncode==0 and p.exists(): out.append(p)
    return out


def generate_gallery(db: DB,state_dir: Path,run_id: str,levels=(LEVEL_C,LEVEL_D)) -> Path:
    ensure_pillow(); out=state_dir/f"AUDITORIA_{run_id}"/"galeria"; media=out/"thumbs"; out.mkdir(parents=True,exist_ok=True)
    rows=db.conn.execute("""SELECT m.*,c.level,c.relative_dest,c.reason FROM manifest m JOIN classifications c USING(run_id,item_id) WHERE m.run_id=? AND c.level IN (%s) ORDER BY m.relative_path""" % ",".join("?"*len(levels)),(run_id,*levels)).fetchall()
    cards=[]
    for r in rows:
        src=Path(r["source_path"]); thumbs=[]
        if r["extension"] in IMAGE_EXTS:
            t=media/f"{r['item_id']}.jpg"
            if thumb_image(src,t): thumbs=[t]
        elif r["extension"] in VIDEO_EXTS:
            thumbs=video_frames(src,media/f"video_{r['item_id']}")
        imgs="".join(f'<img src="{html.escape(str(t.relative_to(out)).replace(os.sep,"/"))}">' for t in thumbs) or '<div class="noimg">sem miniatura</div>'
        cards.append(f'''<article><div class="imgs">{imgs}</div><h3>{html.escape(r['filename'])}</h3><p><b>{r['level']}</b> — {html.escape(r['reason'])}</p><p>{html.escape(r['source_path'])}</p><p>Destino sugerido: {html.escape(r['relative_dest'])}</p><p>EXIF: {html.escape(r['exif_datetime'] or '-')} | câmera: {html.escape(r['exif_camera'] or '-')}</p></article>''')
    doc=f'''<!doctype html><meta charset="utf-8"><title>ACIRV V2 — Revisão</title><style>body{{font-family:system-ui;margin:24px;background:#f5f5f5}}article{{background:white;padding:14px;margin:12px 0;border-radius:10px}}.imgs{{display:flex;gap:8px;overflow:auto}}img{{max-width:320px;max-height:220px;object-fit:contain;background:#eee}}p{{overflow-wrap:anywhere}}.noimg{{padding:40px;background:#eee}}</style><h1>ACIRV Migration Engine V2 — Galeria</h1><p>Somente revisão. Nenhum original foi modificado.</p>{''.join(cards)}'''
    index=out/"index.html"; atomic_write_text(index,doc);return index

# ---------------------------------------------------------------------------
# Revisão humana por grupo
# ---------------------------------------------------------------------------

def approve_group(db: DB,state_dir: Path,run_id: str,group_id: str,action: str,new_destination: Optional[str]=None,new_storage: Optional[str]=None,note: str="") -> Rule:
    g=db.conn.execute("SELECT * FROM groups WHERE run_id=? AND group_id=?",(run_id,group_id)).fetchone()
    if not g: raise RuntimeError("Grupo não encontrado")
    rules=load_rules(state_dir)
    if action=="LEGACY":
        storage="ARCHIVE" if g["surface"]=="F" else "DRIVE"
        dest=new_destination or str(PureWindowsPath("90_LEGADO — A REVISAR")/PureWindowsPath(g["relative_dest"]).name)
        level=LEVEL_E
    else:
        storage=(new_storage or g["storage"]).upper();dest=new_destination or g["relative_dest"];level=LEVEL_A
    rule=Rule(id="USR-"+uuid.uuid4().hex[:10].upper(),source=g["source_prefix"],destination=dest,storage=storage,classification=level,approved_by_user=True,recursive=False,note=note or f"Aprovação do grupo {group_id}",created_at=utc_now())
    rules.append(rule);save_rules(state_dir,rules);classify_run(db,state_dir,run_id);export_audit(db,state_dir,run_id);return rule

# ---------------------------------------------------------------------------
# Inventários TXT: auditoria de lógica sem tocar nos arquivos reais
# ---------------------------------------------------------------------------

INV_LINE_RE=re.compile(r"^\[Arquivo\]\s+(.*?)\s+\|\s+(.+)$")

def parse_inventory_paths(path: Path) -> Iterator[str]:
    with path.open("r",encoding="utf-8",errors="replace") as f:
        for line in f:
            m=INV_LINE_RE.match(line.rstrip("\n"))
            if m: yield m.group(1)


def inventory_classifier_audit(f_inventory: Path,h_inventory: Path) -> dict[str,Any]:
    dummy_rules=[]; counts={"F":Counter(),"H":Counter()};special=defaultdict(Counter);errors=[]
    topics=["forum de ia","sudoexpo","conecta acirv","conecta saude","cafe entre amigos","cafe com o presidente","acirv mulher","identidade visual","banco de imagens","relatorio","comercial","backup","temp","dados acirv"]
    for surface,inv in (("F",f_inventory),("H",h_inventory)):
        for rel in parse_inventory_paths(inv):
            try:
                pw=PureWindowsPath(rel);name=pw.name;ext=Path(name).suffix.lower();text=ntext(rel)
                c=classify_item(f"{surface}:\\{rel}",surface,rel,name,ext,"0"*64,1,None,None,dummy_rules)
                counts[surface][c.level]+=1
                for t in topics:
                    if t in text: special[t][c.level]+=1
                # sanity: filename deve sobreviver na sugestão, exceto D sem destino.
                if c.level!=LEVEL_D and ntext(name) not in ntext(str(c.relative)):
                    # regras de backup/histórico preservam path; se não, sinaliza.
                    errors.append({"type":"filename_missing","surface":surface,"rel":rel,"dest":str(c.relative)})
            except Exception as e:
                errors.append({"type":"exception","surface":surface,"rel":rel,"error":repr(e)})
    return {"counts":{s:dict(c) for s,c in counts.items()},"special":{k:dict(v) for k,v in special.items()},"errors":errors[:100],"error_count":len(errors)}

# ---------------------------------------------------------------------------
# Self-tests
# ---------------------------------------------------------------------------

def _mkdb(tmp: Path) -> tuple[DB,Path]:
    state=tmp/"state";state.mkdir();
    # yaml precisa existir para assinatura, sem importar PyYAML em self-test.
    atomic_write_bytes(state/RULES_NAME,rules_default_bytes());atomic_write_text(state/RULES_SIG_NAME,sha256_file(state/RULES_NAME)+"\n")
    return DB(state/DB_NAME),state


def _fake_run(db: DB,state: Path,f: Path,h: Path,run_id="T"):
    central=h/CENTRAL_NAME;archive=f/ARCHIVE_NAME
    db.conn.execute("INSERT INTO runs(run_id,created_at,app_version,f_root,h_root,central_root,archive_root,state_dir,include_entire_drive,reserve_bytes,status,rules_hash,manifest_hash,plan_allow_b) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,0)",
                    (run_id,utc_now(),APP_VERSION,str(f),str(h),str(central),str(archive),str(state),1,0,"PLAN_VALIDATED",sha256_file(state/RULES_NAME),"x"));db.conn.commit()


def _seal_test_plan(db: DB, state: Path, run_id: str="T") -> str:
    mh=compute_manifest_signature(db,run_id);rh=validate_rules_signature(state)
    db.conn.execute("UPDATE runs SET manifest_hash=?,rules_hash=?,plan_allow_b=0 WHERE run_id=?",(mh,rh,run_id));db.conn.commit()
    sig=plan_signature(db,run_id,rh,False)
    db.conn.execute("UPDATE runs SET plan_signature=? WHERE run_id=?",(sig,run_id));db.conn.commit()
    out=state/f"AUDITORIA_{run_id}";out.mkdir(parents=True,exist_ok=True);atomic_write_text(out/"plano.sha256",sig+"\n")
    return sig


def run_self_tests() -> tuple[int,list[tuple[str,bool,str]]]:
    results=[]
    def test(name,fn):
        try: fn();results.append((name,True,"OK"))
        except Exception as e: results.append((name,False,f"{type(e).__name__}: {e}"))
    os.environ["ACIRV_V2_TEST_EXECUTION"]="1"

    def t_same_volume():
        with tempfile.TemporaryDirectory() as td:
            p=Path(td);src=p/"a.txt";dst=p/"x"/"a.txt";src.write_bytes(b"abc");h=sha256_file(src)
            with LockedSource(src) as f:
                assert hash_open_file(f)==h;dst.parent.mkdir();os.rename(src,dst)
            assert not src.exists() and sha256_file(dst)==h
    test("01 movimentação mesmo volume",t_same_volume)

    def t_cross():
        with tempfile.TemporaryDirectory() as td:
            p=Path(td);src=p/"src"/"a.bin";dst=p/"dst"/"a.bin";src.parent.mkdir();src.write_bytes(os.urandom(50000));h=sha256_file(src)
            tmp,hh=copy_locked_to_temp(src,dst,h,src.stat().st_size);os.rename(tmp,dst);assert hh==h==sha256_file(dst)==sha256_file(src)
    test("02 movimentação entre volumes simulada",t_cross)

    def t_interrupted():
        with tempfile.TemporaryDirectory() as td:
            p=Path(td);src=p/"a";dst=p/"b";src.write_bytes(b"z"*1000);h=sha256_file(src)
            # temp parcial não pode afetar origem
            dst.parent.mkdir(exist_ok=True);tmp=exclusive_tmp(dst);tmp.write_bytes(b"partial");assert sha256_file(src)==h;tmp.unlink()
    test("03 cópia interrompida",t_interrupted)

    def t_corrupt():
        with tempfile.TemporaryDirectory() as td:
            p=Path(td);src=p/"a";dst=p/"b";src.write_bytes(b"abc"*100);h=sha256_file(src)
            def hook(s,t): t.write_bytes(b"CORRUPT")
            try: copy_locked_to_temp(src,dst,h,src.stat().st_size,hook);raise AssertionError("corrupção não detectada")
            except RuntimeError as e: assert "COPY_CORRUPTED" in str(e)
            assert src.exists() and sha256_file(src)==h
    test("04 corrupção deliberada",t_corrupt)

    def t_collision():
        with tempfile.TemporaryDirectory() as td:
            p=Path(td);src=p/"a";dst=p/"b";src.write_bytes(b"a");dst.write_bytes(b"b")
            try: copy_locked_to_temp(src,dst,sha256_file(src),1);raise AssertionError()
            except FileExistsError: pass
    test("05 colisão de filename",t_collision)
    test("06 destino já existente",t_collision)

    def t_dup():
        with tempfile.TemporaryDirectory() as td:
            p=Path(td);a=p/"a";b=p/"b";a.write_bytes(b"same");b.write_bytes(b"same");assert sha256_file(a)==sha256_file(b)
    test("07 duplicata verdadeira SHA-256",t_dup)

    def t_same_name_diff():
        with tempfile.TemporaryDirectory() as td:
            p=Path(td);(p/"x").mkdir();(p/"y").mkdir();a=p/"x"/"a";b=p/"y"/"a";a.write_bytes(b"1");b.write_bytes(b"2");assert sha256_file(a)!=sha256_file(b)
    test("08 mesmo nome conteúdo diferente",t_same_name_diff)

    def t_changed_after_plan():
        with tempfile.TemporaryDirectory() as td:
            p=Path(td);a=p/"a";a.write_bytes(b"1");st=a.stat();a.write_bytes(b"22");assert not stable_stat_matches(a,st.st_size,st.st_mtime_ns)
    test("09 arquivo alterado após plano",t_changed_after_plan)

    def t_changed_during_copy():
        with tempfile.TemporaryDirectory() as td:
            p=Path(td);state=p/"s";state.mkdir();f=p/"F";h=p/"H";f.mkdir();h.mkdir();db=DB(state/DB_NAME)
            atomic_write_bytes(state/RULES_NAME,rules_default_bytes());atomic_write_text(state/RULES_SIG_NAME,sha256_file(state/RULES_NAME)+"\n");_fake_run(db,state,f,h)
            src=f/"a.bin";dst=h/CENTRAL_NAME/"a.bin";src.write_bytes(b"ORIGINAL"*100);st=src.stat();hh=sha256_file(src)
            db.conn.execute("INSERT INTO ops(run_id,op_id,item_id,source_before,destination_after,storage,level,op_mode,expected_size,expected_mtime_ns,sha256_before,status,updated_at) VALUES('T',1,1,?,?,?,?,?,?,?,?,?,?)",(str(src),str(dst),"DRIVE","A","CROSS_VOLUME_SAFE_COPY",st.st_size,st.st_mtime_ns,hh,STATUS_PLANNED,utc_now()));db.conn.commit()
            op=db.conn.execute("SELECT * FROM ops WHERE run_id='T' AND op_id=1").fetchone()
            def mutate_source(s,t): s.write_bytes(b"MODIFICADO")
            try:
                execute_one(db,"T",op,test_mutate_hook=mutate_source);raise AssertionError("mudança da origem não detectada")
            except RuntimeError as e:
                assert "SOURCE_CHANGED_AFTER_COPY" in str(e)
            assert src.exists() and sha256_file(src)!=hh
            assert dst.exists() and sha256_file(dst)==hh  # cópia íntegra publicada, origem não removida
            db.close()
    test("10 arquivo alterado durante cópia",t_changed_during_copy)

    def t_lock():
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"a";p.write_bytes(b"x")
            with LockedSource(p) as f: assert f.read()==b"x"
    test("11 arquivo bloqueado/lock abstraction",t_lock)

    def t_rollback_normal():
        with tempfile.TemporaryDirectory() as td:
            p=Path(td);state=p/"state";state.mkdir();f=p/"F";h=p/"H";f.mkdir();h.mkdir();db=DB(state/DB_NAME)
            atomic_write_bytes(state/RULES_NAME,rules_default_bytes());atomic_write_text(state/RULES_SIG_NAME,sha256_file(state/RULES_NAME)+"\n")
            _fake_run(db,state,f,h);src=f/"orig";dst=f/ARCHIVE_NAME/"x";src.write_bytes(b"abc");dst.parent.mkdir(parents=True);os.rename(src,dst);hh=sha256_file(dst)
            db.conn.execute("INSERT INTO ops(run_id,op_id,item_id,source_before,destination_after,storage,level,op_mode,expected_size,expected_mtime_ns,sha256_before,sha256_after,final_path,status,updated_at) VALUES('T',1,1,?,?,?,?,?,?,?,?,?,?,?,?)",(str(src),str(dst),"ARCHIVE","A","SAME_VOLUME",3,0,hh,hh,str(dst),STATUS_DONE,utc_now()));db.conn.commit();_seal_test_plan(db,state)
            done,blocked=rollback_run(db,state,"T","REVERTER T")
            assert done==1 and blocked==0 and src.exists() and not dst.exists() and sha256_file(src)==hh
            db.close()
    test("12 rollback normal",t_rollback_normal)

    def t_rollback_modified():
        with tempfile.TemporaryDirectory() as td:
            p=Path(td);state=p/"state";state.mkdir();f=p/"F";h=p/"H";f.mkdir();h.mkdir();db=DB(state/DB_NAME)
            atomic_write_bytes(state/RULES_NAME,rules_default_bytes());atomic_write_text(state/RULES_SIG_NAME,sha256_file(state/RULES_NAME)+"\n")
            _fake_run(db,state,f,h);src=f/"orig";dst=f/ARCHIVE_NAME/"x";src.write_bytes(b"abc");dst.parent.mkdir(parents=True);os.rename(src,dst);hh=sha256_file(dst)
            db.conn.execute("INSERT INTO ops(run_id,op_id,item_id,source_before,destination_after,storage,level,op_mode,expected_size,expected_mtime_ns,sha256_before,sha256_after,final_path,status,updated_at) VALUES('T',1,1,?,?,?,?,?,?,?,?,?,?,?,?)",(str(src),str(dst),"ARCHIVE","A","SAME_VOLUME",3,0,hh,hh,str(dst),STATUS_DONE,utc_now()));db.conn.commit();_seal_test_plan(db,state)
            dst.write_bytes(b"EDITADO DEPOIS")
            done,blocked=rollback_run(db,state,"T","REVERTER T")
            assert done==0 and blocked==1 and not src.exists() and dst.exists()
            assert db.conn.execute("SELECT status FROM ops WHERE run_id='T'").fetchone()[0]==STATUS_ROLLBACK_BLOCKED
            db.close()
    test("13 rollback bloqueado se editado",t_rollback_modified)

    def t_resume():
        with tempfile.TemporaryDirectory() as td:
            p=Path(td);state=p/"s";state.mkdir();f=p/"F";h=p/"H";f.mkdir();h.mkdir();db=DB(state/DB_NAME);atomic_write_bytes(state/RULES_NAME,rules_default_bytes());atomic_write_text(state/RULES_SIG_NAME,sha256_file(state/RULES_NAME)+"\n");_fake_run(db,state,f,h)
            src=f/"a";dst=h/CENTRAL_NAME/"a";src.write_bytes(b"abc");dst.parent.mkdir(parents=True);shutil.copy2(src,dst);hh=sha256_file(src)
            db.conn.execute("INSERT INTO ops(run_id,op_id,item_id,source_before,destination_after,storage,level,op_mode,expected_size,expected_mtime_ns,sha256_before,sha256_after,final_path,status,updated_at) VALUES('T',1,1,?,?,?,?,?,?,?,?,?,?,?,?)",(str(src),str(dst),"DRIVE","A","CROSS_VOLUME_SAFE_COPY",3,src.stat().st_mtime_ns,hh,hh,str(dst),STATUS_PUBLISHED,utc_now()));db.conn.commit();reconcile_interrupted(db,"T");r=db.conn.execute("SELECT status FROM ops WHERE run_id='T'").fetchone()[0];assert r in {STATUS_FAILED,STATUS_DONE};db.close()
    test("14 retomada após interrupção",t_resume)

    def t_multiset_ok():
        pre=Counter({"a":2,"b":1});post=Counter({"a":3,"b":1});assert not {h:c-post.get(h,0) for h,c in pre.items() if post.get(h,0)<c}
    test("15 manifesto pré/pós idêntico/superset",t_multiset_ok)
    def t_multiset_missing():
        pre=Counter({"a":2});post=Counter({"a":1});assert {h:c-post.get(h,0) for h,c in pre.items() if post.get(h,0)<c}=={"a":1}
    test("16 manifesto com arquivo ausente",t_multiset_missing)

    def t_long():
        rel=Path("x"*100)/("y"*180+".jpg");out,changes=fit_windows_path(Path("C:/ROOT"),rel,Path("F:/"+"z"*220+".jpg"));assert changes
    test("17 caminho longo",t_long)
    def t_unicode():
        p,c=sanitize_relpath(Path("Fórum de IA")/"Café — ação.jpg");assert "Fórum" in str(p) and "Café" in str(p)
    test("18 Unicode/acentuação",t_unicode)
    def t_space():
        # cálculo determinístico
        required=80*1024**3;reserve=20*1024**3;free=90*1024**3;assert required+reserve>free
    test("19 pouco espaço em disco",t_space)

    def t_rules_tamper():
        with tempfile.TemporaryDirectory() as td:
            s=Path(td);atomic_write_bytes(s/RULES_NAME,rules_default_bytes());atomic_write_text(s/RULES_SIG_NAME,sha256_file(s/RULES_NAME)+"\n");(s/RULES_NAME).write_text("tampered",encoding="utf-8")
            try: validate_rules_signature(s);raise AssertionError()
            except RuntimeError: pass
    test("20 regra YAML adulterada",t_rules_tamper)

    def t_plan_tamper():
        with tempfile.TemporaryDirectory() as td:
            p=Path(td);state=p/"s";state.mkdir();f=p/"F";h=p/"H";f.mkdir();h.mkdir();db=DB(state/DB_NAME)
            atomic_write_bytes(state/RULES_NAME,rules_default_bytes());atomic_write_text(state/RULES_SIG_NAME,sha256_file(state/RULES_NAME)+"\n");_fake_run(db,state,f,h)
            db.conn.execute("INSERT INTO ops(run_id,op_id,item_id,source_before,destination_after,storage,level,op_mode,expected_size,expected_mtime_ns,sha256_before,status,updated_at) VALUES('T',1,1,?,?,?,?,?,?,?,?,?,?)",(str(f/'a'),str(f/'b'),"ARCHIVE","A","SAME_VOLUME",1,0,"0"*64,STATUS_PLANNED,utc_now()));db.conn.commit();_seal_test_plan(db,state)
            validate_plan_immutable(db,state,"T")
            db.conn.execute("UPDATE ops SET destination_after=? WHERE run_id='T' AND op_id=1",(str(f/'adulterado'),));db.conn.commit()
            try: validate_plan_immutable(db,state,"T");raise AssertionError("adulteração não detectada")
            except RuntimeError as e: assert "alterado/adulterado" in str(e)
            db.close()
    test("21 plano adulterado",t_plan_tamper)

    def t_ambiguous():
        c=classify_item(r"F:\\temp\\xyz.bin","F",r"temp\\xyz.bin","xyz.bin",".bin","0"*64,1,None,None,[]);assert c.level==LEVEL_D
    test("22 classificação ambígua",t_ambiguous)
    def t_zero_gate():
        counts={"C":1,"D":0};assert not (counts["C"]==0 and counts["D"]==0)
    test("23 Zero-Ambiguity Gate",t_zero_gate)
    def t_photo_group():
        a=group_anchor(r"KEVYN\\Criativos\\Novembro\\Fórum IA\\MAT\\_Fotos\\a.jpg","C");b=group_anchor(r"KEVYN\\Criativos\\Novembro\\Fórum IA\\MAT\\_Fotos\\b.jpg","C");assert a==b
    test("24 agrupamento de fotos",t_photo_group)
    test("25 deduplicação SHA-256",t_dup)

    def t_hash_progress():
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"progress.bin"; data=b"x"*(COPY_CHUNK+123); p.write_bytes(data); seen=[0]
            h=sha256_file(p,on_bytes=lambda n: seen.__setitem__(0,seen[0]+n))
            assert seen[0]==len(data) and h==hashlib.sha256(data).hexdigest()
    test("26 callback de progresso de hash",t_hash_progress)

    def t_worker_bounds():
        assert audit_worker_count(0)==1
        assert audit_worker_count(999)==MAX_AUDIT_WORKERS
        assert 1 <= audit_worker_count() <= MAX_AUDIT_WORKERS
    test("27 limites de paralelismo",t_worker_bounds)

    failed=sum(1 for _,ok,_ in results if not ok)
    return failed,results

# ---------------------------------------------------------------------------
# TUI — fluxo guiado V2.1
# ---------------------------------------------------------------------------

def default_state_dir() -> Path:
    home = Path.home()
    downloads = home / "Downloads"
    return (downloads if downloads.exists() else home) / STATE_FOLDER_NAME


def latest_run(db: DB) -> Optional[sqlite3.Row]:
    rows = db.runs()
    return rows[0] if rows else None


def select_run(db: DB) -> Optional[str]:
    """Usado apenas nas ferramentas avançadas. O fluxo normal sempre usa o run mais recente."""
    rows = db.runs()
    if not rows:
        return None
    choices = [f"{r['run_id']} | {r['status']} | {r['scanned_files']} arquivos" for r in rows]
    ans = questionary.select("Escolha a auditoria:", choices=choices).ask()
    return ans.split(" | ", 1)[0] if ans else None


def show_counts(db: DB, run_id: str, compact: bool = False):
    from rich.table import Table
    c = level_counts(db, run_id)
    if compact:
        console.print(
            f"[bold]Classificação:[/] "
            f"[green]A {c['A']}[/] · [cyan]B {c['B']}[/] · "
            f"[yellow]C {c['C']}[/] · [red]D {c['D']}[/] · [magenta]E {c['E']}[/]"
        )
        return c
    t = Table(title=f"Segurança semântica — {run_id}")
    t.add_column("Nível")
    t.add_column("Arquivos", justify="right")
    for k, label in (
        ("A", "A — EXPLÍCITO"),
        ("B", "B — COMPROVADO"),
        ("C", "C — PROVÁVEL"),
        ("D", "D — AMBÍGUO"),
        ("E", "E — LEGADO APROVADO"),
    ):
        t.add_row(label, str(c[k]))
    console.print(t)
    console.print(
        "[green]SEM AMBIGUIDADES[/]"
        if c["C"] == 0 and c["D"] == 0
        else f"[yellow]Precisa de você:[/] {c['C'] + c['D']} arquivo(s) em grupos C/D."
    )
    return c


def _default_roots() -> tuple[Path, Path]:
    return Path("F:\\"), Path(r"H:\Meu Drive")


def _resolve_roots_minimal() -> tuple[Path, Path]:
    """Usa os caminhos oficiais sem perguntar. Só pede intervenção se eles não existirem."""
    f_default, h_default = _default_roots()
    if f_default.exists() and h_default.exists():
        return f_default, h_default

    console.print("[yellow]Não encontrei automaticamente um ou ambos os locais padrão.[/]")
    f = f_default
    h = h_default
    if not f.exists():
        f = Path(questionary.path("Onde está o HD da ACIRV?", default=str(f_default)).ask() or str(f_default))
    if not h.exists():
        h = Path(questionary.path("Onde está a pasta local do Google Drive?", default=str(h_default)).ask() or str(h_default))
    return f, h


def _run_progress_text(db: DB, run: sqlite3.Row) -> tuple[str, str]:
    status = run["status"]
    rid = run["run_id"]
    c = level_counts(db, rid) if status not in {"AUDITING", "AUDIT_INTERRUPTED"} else {k: 0 for k in LEVELS}

    if status in {"AUDITING", "AUDIT_INTERRUPTED"}:
        return "Auditoria retomável", "O checkpoint automático preservou o inventário e os SHA-256 concluídos. Continuar retoma somente o que falta."
    if status == "AUDIT_BLOCKED_ERRORS":
        return "Auditoria bloqueada", "Há erros de leitura que precisam ser resolvidos antes de continuar."
    if status in {"AUDITED"}:
        if c["C"] or c["D"]:
            return "Decisões necessárias", f"{c['C'] + c['D']} arquivo(s) ainda dependem de revisão humana."
        if not run["plan_signature"]:
            return "Pronto para fechar o plano", "Todas as ambiguidades foram resolvidas; falta autorizar B, se houver, e selar o plano."
    if status == "PLAN_VALIDATED":
        return "Plano pronto", "O plano está assinado e imutável. A próxima etapa é a execução real."
    if status in {"EXECUTING", "EXECUTION_BLOCKED"}:
        return "Migração interrompida", "O journal permite reconciliar o estado e continuar com segurança."
    if status == "EXECUTED_LOCAL":
        return "Arquivos reorganizados", "Falta executar a auditoria matemática pós-migração."
    if status == "LOCAL_AUDIT_PASS":
        return "Concluído localmente", "Integridade local comprovada. Verificação remota do Drive continua opcional/recomendada."
    if status == "LOCAL_AUDIT_FAIL":
        return "Integridade bloqueada", "A auditoria pós-migração encontrou conteúdo ausente; não avance."
    if status == "ROLLED_BACK":
        return "Migração revertida", "O rollback foi concluído."
    if status == "ROLLBACK_PARTIAL":
        return "Rollback parcial", "Há itens que exigem auditoria manual."
    return status, "O estado atual exige inspeção pelas ferramentas avançadas."


def show_home(db: DB, state: Path) -> Optional[sqlite3.Row]:
    from rich.panel import Panel
    run = latest_run(db)
    if not run:
        body = (
            "[bold]Nenhuma auditoria criada ainda.[/]\n\n"
            "O fluxo seguro é automático:\n"
            "1. inventariar e calcular hashes\n"
            "2. pedir apenas decisões realmente ambíguas\n"
            "3. selar o plano\n"
            "4. executar com verificação e journal\n"
            "5. auditar o resultado"
        )
        console.print(Panel(body, title=APP_NAME, border_style="cyan"))
        return None

    title, desc = _run_progress_text(db, run)
    body = (
        f"[bold]{title}[/]\n{desc}\n\n"
        f"Auditoria: [dim]{run['run_id']}[/]\n"
        f"Estado técnico: [dim]{run['status']}[/]\n"
        f"Arquivos: {run['scanned_files']} · {bytes_human(int(run['scanned_bytes'] or 0))}"
    )
    console.print(Panel(body, title=APP_NAME, border_style="cyan"))
    if run["status"] not in {"AUDITING", "AUDIT_INTERRUPTED", "AUDIT_BLOCKED_ERRORS"}:
        show_counts(db, run["run_id"], compact=True)
    return run


def _group_evidence_text(g: sqlite3.Row) -> str:
    try:
        ev = json.loads(g["evidence_json"] or "[]")
    except Exception:
        ev = []
    if not ev:
        return "Nenhuma evidência estruturada disponível."
    return "\n".join(f"  ✓ {x}" for x in ev[:8])


def review_groups_tui(db: DB, state: Path, run_id: str) -> None:
    """
    Fluxo linear: mostra sempre o próximo grupo C/D mais relevante.
    O usuário não escolhe IDs, runs ou ordem de revisão.
    """
    from rich.panel import Panel
    while True:
        classify_run(db, state, run_id)
        groups = db.conn.execute(
            """SELECT * FROM groups
               WHERE run_id=? AND level IN ('C','D')
               ORDER BY CASE level WHEN 'D' THEN 0 ELSE 1 END, total_bytes DESC, item_count DESC""",
            (run_id,),
        ).fetchall()

        if not groups:
            console.print("[green bold]Todas as decisões obrigatórias foram resolvidas.[/]")
            return

        g = groups[0]
        remaining = len(groups)
        console.print()
        console.print(
            Panel(
                f"[bold]{g['source_prefix']}[/]\n\n"
                f"{g['item_count']} arquivo(s) · {bytes_human(int(g['total_bytes']))}\n"
                f"Nível: [yellow]{g['level']}[/]\n"
                f"Sugestão: [cyan]{g['storage']} → {g['relative_dest']}[/]\n\n"
                f"Evidências:\n{_group_evidence_text(g)}",
                title=f"Decisão necessária · {remaining} grupo(s) restante(s)",
                border_style="yellow" if g["level"] == "C" else "red",
            )
        )

        if g["level"] == "C":
            choices = [
                "✓ Confirmar sugestão",
                "✎ Escolher outro destino",
                "▣ Ver galeria / exemplos",
                "⌂ Guardar como legado",
                "⏸ Pausar revisão",
            ]
        else:
            # Em D não promovemos uma sugestão ambígua como ação padrão.
            choices = [
                "✎ Escolher destino",
                "▣ Ver galeria / exemplos",
                "⌂ Guardar como legado",
                "⏸ Pausar revisão",
            ]

        act = questionary.select(
            "O que este grupo é?",
            choices=choices,
            instruction="Use ↑↓ e Enter",
        ).ask()

        if not act or "Pausar" in act:
            return
        if "galeria" in act.lower():
            p = generate_gallery(db, state, run_id)
            console.print(f"[cyan]Galeria criada:[/] {p}")
            with contextlib.suppress(Exception):
                if os.name == "nt":
                    os.startfile(str(p))
            continue
        if "legado" in act.lower():
            approve_group(db, state, run_id, g["group_id"], "LEGACY")
            continue
        if "Confirmar" in act:
            approve_group(db, state, run_id, g["group_id"], "CONFIRM")
            continue

        storage = questionary.select(
            "Onde este grupo deve viver?",
            choices=[
                "Drive — uso recorrente / oficial",
                "HD — arquivo frio / histórico",
            ],
        ).ask()
        storage_code = "DRIVE" if storage and storage.startswith("Drive") else "ARCHIVE"
        default_dest = g["relative_dest"]
        dest = questionary.text(
            "Pasta de destino relativa:",
            default=default_dest,
            validate=lambda x: bool(str(x).strip()) or "Informe uma pasta.",
        ).ask()
        if dest:
            approve_group(db, state, run_id, g["group_id"], "CONFIRM", dest, storage_code)


def _authorize_b_once(db: DB, run_id: str) -> bool:
    c = level_counts(db, run_id)
    if not c["B"]:
        return False
    from rich.panel import Panel
    console.print(
        Panel(
            f"Restam [cyan bold]{c['B']} arquivos B — COMPROVADOS[/].\n\n"
            "Eles possuem múltiplas evidências independentes convergindo para o mesmo destino.\n"
            "Liberar B não transforma itens C/D em executáveis; o Zero-Ambiguity Gate já precisa estar zerado.",
            title="Uma decisão importante",
            border_style="cyan",
        )
    )
    ans = questionary.select(
        "Usar as classificações B comprovadas neste plano?",
        choices=[
            "Sim — autorizar B somente neste plano",
            "Não — manter bloqueado e revisar depois",
        ],
    ).ask()
    return bool(ans and ans.startswith("Sim"))



def _display_path(value: str, limit: int = 72) -> str:
    text = str(value)
    if len(text) <= limit:
        return text
    return "…" + text[-(limit-1):]


def _audit_with_progress(
    db: DB,
    state: Path,
    f: Path,
    h: Path,
    include_entire_drive: bool,
    reserve_gb: int,
    resume_run_id: Optional[str] = None,
) -> str:
    """Executa/retoma auditoria com confirmação visual contínua e checkpoint durável."""
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn, TimeRemainingColumn

    processed_bytes = 0
    total_bytes_seen = 0
    with Progress(
        SpinnerColumn(),
        TextColumn("{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        TextColumn("{task.fields[detail]}"),
        TimeRemainingColumn(),
        console=console,
        refresh_per_second=8,
    ) as progress:
        task_id = progress.add_task("[cyan]Mapeando arquivos…[/]", total=None, detail="checkpoint ativo")

        def cb(event: str, data: dict[str, Any]) -> None:
            nonlocal processed_bytes, total_bytes_seen
            if event == "inventory_start":
                suffix = " · retomando checkpoint" if data.get("resumed") else ""
                progress.update(
                    task_id, description="[cyan]Mapeando arquivos…[/]",
                    detail=f"{data.get('workers', '?')} threads{suffix} · salvamento automático ativo",
                )
            elif event == "inventory_surface":
                progress.update(task_id, detail=f"mapeando {data.get('surface')}: {_display_path(data.get('root', ''), 56)}")
            elif event == "inventory_tick":
                reused = int(data.get("reused", 0))
                progress.update(
                    task_id,
                    detail=(
                        f"{data.get('files', 0)} arquivos · {bytes_human(int(data.get('bytes', 0)))} · "
                        f"pastas {data.get('dirs_done', 0)} concluídas/{data.get('dirs_pending', 0)} pendentes"
                        + (f" · {reused} hashes reaproveitados" if reused else "")
                    ),
                )
            elif event == "hash_start":
                total_files = int(data.get("total_files", 0))
                completed = int(data.get("completed", 0))
                processed_bytes = int(data.get("completed_bytes", 0))
                total_bytes_seen = int(data.get("total_bytes", 0))
                resumed = " · retomado" if data.get("resumed") else ""
                progress.update(
                    task_id,
                    description=f"[cyan]Lendo + SHA-256 ({data.get('workers', '?')} threads){resumed}…[/]",
                    total=max(total_files, 1),
                    completed=completed,
                    detail=(
                        f"{completed}/{total_files} · persistidos {bytes_human(processed_bytes)}/"
                        f"{bytes_human(total_bytes_seen)} · checkpoint por arquivo"
                    ),
                )
            elif event == "hash_bytes":
                live = min(
                    int(data.get("total_bytes", total_bytes_seen) or total_bytes_seen),
                    int(data.get("base_bytes", processed_bytes)) + int(data.get("session_bytes", 0)),
                )
                progress.update(
                    task_id,
                    detail=(
                        f"leitura SHA-256 em curso: ~{bytes_human(live)}/{bytes_human(int(data.get('total_bytes', total_bytes_seen)))} · "
                        f"{data.get('active', 0)} arquivo(s) ativos · auto-save ativo"
                    ),
                )
            elif event == "file_done":
                processed_bytes = int(data.get("completed_bytes", processed_bytes))
                total_files = int(data.get("total_files", 0))
                completed = int(data.get("completed", 0))
                detail = (
                    f"{completed}/{total_files} · SHA-256 salvos {bytes_human(processed_bytes)}/"
                    f"{bytes_human(int(data.get('total_bytes', total_bytes_seen)))} · erros {data.get('errors', 0)} · "
                    f"{_display_path(data.get('path', ''), 42)}"
                )
                progress.update(task_id, completed=completed, detail=detail)
            elif event == "finalizing":
                progress.update(
                    task_id, description="[cyan]Finalizando auditoria…[/]",
                    detail=str(data.get("message", "consolidando resultados")),
                )
            elif event == "audit_done":
                progress.update(
                    task_id,
                    completed=progress.tasks[task_id].total or progress.tasks[task_id].completed,
                    description="[green]Auditoria lida e registrada[/]",
                    detail=f"{data.get('files', 0)} arquivos · {bytes_human(int(data.get('bytes', 0)))} · erros {data.get('errors', 0)}",
                )

        if resume_run_id:
            return audit_resume(
                db, state, resume_run_id, with_media_meta=True,
                workers=audit_worker_count(12), progress_cb=cb,
            )
        return audit_new(
            db, state, f, h,
            include_entire_drive=include_entire_drive,
            reserve_gb=reserve_gb,
            with_media_meta=True,
            workers=audit_worker_count(12),
            progress_cb=cb,
        )


def _execute_with_progress(db: DB, state: Path, run_id: str, confirmation: str, resume: bool = False) -> None:
    """Mostra bytes/arquivo/fase durante a reorganização sem paralelizar mutações."""
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, DownloadColumn, TransferSpeedColumn, TimeRemainingColumn

    seen: dict[int, int] = defaultdict(int)
    current_index = 0
    total_ops = 0
    with Progress(
        SpinnerColumn(),
        TextColumn("{task.description}"),
        BarColumn(),
        DownloadColumn(),
        TransferSpeedColumn(),
        TimeRemainingColumn(),
        TextColumn("{task.fields[detail]}"),
        console=console,
        refresh_per_second=8,
    ) as progress:
        task_id = progress.add_task("[red]Preparando reorganização…[/]", total=None, detail="validando plano")

        def cb(event: str, data: dict[str, Any]) -> None:
            nonlocal current_index, total_ops
            if event == "plan_start":
                total_ops = int(data.get("total_ops", 0))
                total_bytes = int(data.get("total_bytes", 0))
                progress.update(task_id, total=max(total_bytes, 1), completed=0, description="[red]Reorganizando com verificação…[/]", detail=f"0/{total_ops} arquivos")
            elif event == "plan_op":
                current_index = int(data.get("index", 0))
                total_ops = int(data.get("total_ops", total_ops))
                progress.update(task_id, detail=f"{current_index}/{total_ops} · {_display_path(data.get('path', ''), 58)}")
            elif event == "op_phase":
                progress.update(task_id, description=f"[red]{data.get('phase', 'Processando')}…[/]", detail=f"{current_index}/{total_ops} · {_display_path(data.get('path', ''), 55)}")
            elif event == "op_bytes":
                op_id = int(data.get("op_id", 0))
                delta = int(data.get("delta", 0))
                seen[op_id] += delta
                progress.advance(task_id, delta)
            elif event == "op_done":
                if data.get("skipped"):
                    return
                op_id = int(data.get("op_id", 0))
                size = int(data.get("size", 0))
                missing = max(0, size - seen.get(op_id, 0))
                if missing:
                    seen[op_id] = size
                    progress.advance(task_id, missing)
                progress.update(task_id, description="[red]Reorganizando com verificação…[/]", detail=f"{current_index}/{total_ops} concluído")
            elif event == "plan_phase":
                progress.update(task_id, description="[cyan]Finalizando…[/]", detail=str(data.get("message", "")))
            elif event == "plan_done":
                if progress.tasks[task_id].total is not None:
                    progress.update(task_id, completed=progress.tasks[task_id].total)
                progress.update(task_id, description="[green]Reorganização local concluída[/]", detail=f"{data.get('total_ops', total_ops)} operações")
            elif event == "plan_error":
                progress.update(task_id, description="[red]Operação bloqueada[/]", detail=str(data.get("error", "erro")))

        if resume:
            resume_plan(db, state, run_id, confirmation, progress_cb=cb)
        else:
            execute_plan(db, state, run_id, confirmation, progress_cb=cb)

def guided_continue(db: DB, state: Path) -> None:
    run = latest_run(db)

    # 1) Primeira vez: zero configuração para o caso normal.
    if run is None:
        f, h = _resolve_roots_minimal()
        if not f.exists() or not h.exists():
            raise RuntimeError("Os locais de origem não existem. Corrija os caminhos antes de continuar.")
        # EXIF é útil e seguro; não transformamos isso em decisão de UX.
        if not ensure_pillow_for_audit():
            ensure_dependency("PIL", "Pillow>=10,<13")
        console.print(
            "[cyan]Vou apenas ler F:/H:, calcular hashes e gerar o diagnóstico. "
            "Nenhum arquivo será movido nesta etapa.[/]"
        )
        rid = _audit_with_progress(
            db, state, f, h,
            include_entire_drive=False,
            reserve_gb=DEFAULT_RESERVE_GB,
        )
        console.print(f"[green bold]Auditoria concluída.[/] {rid}")
        show_counts(db, rid)
        console.print("\n[bold]Próximo passo:[/] escolha CONTINUAR para revisar apenas o que realmente precisa de você.")
        return

    rid = run["run_id"]
    status = run["status"]

    if status in {"AUDITING", "AUDIT_INTERRUPTED"}:
        db.conn.execute("UPDATE runs SET status='AUDIT_INTERRUPTED' WHERE run_id=?", (rid,))
        db.conn.commit()
        console.print(
            "[yellow]A auditoria anterior não terminou.[/] Vou retomar o checkpoint existente. "
            "Diretórios já inventariados e arquivos com SHA-256 concluído não serão refeitos.\n"
            f"[dim]Controle: {state / CHECKPOINT_JSON_NAME}[/]"
        )
        f = Path(run["f_root"]); h = Path(run["h_root"])
        if not f.exists() or not h.exists():
            raise RuntimeError("As raízes originais da auditoria não estão disponíveis; não é seguro trocar de origem durante uma retomada.")
        reserve_gb = max(1, int(run["reserve_bytes"] or (DEFAULT_RESERVE_GB * 1024**3)) // 1024**3)
        rid_same = _audit_with_progress(
            db, state, f, h,
            include_entire_drive=bool(run["include_entire_drive"]),
            reserve_gb=reserve_gb,
            resume_run_id=rid,
        )
        console.print(f"[green bold]Auditoria retomada e concluída.[/] {rid_same}")
        show_counts(db, rid_same)
        return

    if status == "AUDIT_BLOCKED_ERRORS":
        raise RuntimeError(
            "A auditoria encontrou erros de leitura. Por segurança, o fluxo automático está bloqueado. "
            "Abra Ferramentas avançadas → Exportar relatórios para localizar os erros."
        )

    if status == "AUDITED":
        classify_run(db, state, rid)
        c = level_counts(db, rid)
        if c["C"] or c["D"]:
            review_groups_tui(db, state, rid)
            classify_run(db, state, rid)
            c = level_counts(db, rid)
            if c["C"] or c["D"]:
                console.print(
                    f"[yellow]Revisão pausada.[/] Ainda restam {c['C'] + c['D']} arquivo(s) C/D. "
                    "Nenhuma migração pode acontecer."
                )
                return

        allow_b = _authorize_b_once(db, rid)
        if level_counts(db, rid)["B"] and not allow_b:
            console.print("[yellow]Plano não foi gerado.[/] Os itens B continuam bloqueados.")
            return

        sig = generate_plan(db, state, rid, allow_b=allow_b)
        console.print(
            f"[green bold]Plano seguro criado e selado.[/]\n"
            f"Assinatura: [dim]{sig}[/]\n\n"
            "Nada foi movido ainda. Escolha CONTINUAR novamente quando estiver pronto para executar."
        )
        return

    if status == "PLAN_VALIDATED":
        sig = validate_plan_immutable(db, state, rid)
        phrase = f"EXECUTAR {sig[:12].upper()}"
        from rich.panel import Panel
        console.print(
            Panel(
                "Esta é a única etapa do fluxo normal que altera F:/H:.\n"
                "O plano já está selado, sem C/D e com espaço verificado.\n"
                "A confirmação digitada evita execução acidental.",
                title="Execução real",
                border_style="red",
            )
        )
        conf = questionary.text(f"Digite exatamente: {phrase}").ask()
        _execute_with_progress(db, state, rid, conf or "", resume=False)
        console.print("[green bold]Movimentação local concluída.[/] Escolha CONTINUAR para provar a integridade final.")
        return

    if status in {"EXECUTING", "EXECUTION_BLOCKED"}:
        sig = validate_plan_immutable(db, state, rid)
        phrase = f"EXECUTAR {sig[:12].upper()}"
        console.print(
            "[yellow]Existe uma execução incompleta.[/] O journal será reconciliado antes de qualquer nova operação."
        )
        conf = questionary.text(f"Para retomar, digite exatamente: {phrase}").ask()
        _execute_with_progress(db, state, rid, conf or "", resume=True)
        console.print("[green]Retomada concluída.[/]")
        return

    if status == "EXECUTED_LOCAL":
        console.print("[cyan]Executando auditoria matemática pós-migração…[/]")
        result = post_audit(db, rid)
        new_status = "LOCAL_AUDIT_PASS" if result["status"] == "PASS" else "LOCAL_AUDIT_FAIL"
        db.conn.execute("UPDATE runs SET status=? WHERE run_id=?", (new_status, rid))
        db.conn.commit()
        export_audit(db, state, rid)
        if result["status"] == "PASS":
            console.print(
                "[green bold]MIGRATION_INTEGRITY = PASS[/]\n"
                "Todo conteúdo esperado continua presente no multiconjunto de hashes."
            )
        else:
            console.print(
                f"[red bold]MIGRATION_INTEGRITY = FAIL[/]\n"
                f"Hashes ausentes: {len(result.get('missing', {}))}. Nenhuma conclusão segura será declarada."
            )
        return

    if status == "LOCAL_AUDIT_PASS":
        console.print(
            "[green bold]A migração está concluída e comprovada localmente.[/]\n"
            "A verificação do Google Drive remoto é uma camada adicional disponível em Ferramentas avançadas."
        )
        return

    if status == "LOCAL_AUDIT_FAIL":
        raise RuntimeError(
            "A auditoria pós-migração falhou. Não continue automaticamente. "
            "Use Ferramentas avançadas → Exportar relatórios / Rollback."
        )

    if status in {"ROLLED_BACK", "ROLLBACK_PARTIAL"}:
        console.print("[yellow]Este ciclo já passou por rollback.[/] Inicie uma nova auditoria pelas ferramentas avançadas.")
        return

    raise RuntimeError(f"Estado não reconhecido pelo fluxo guiado: {status}")


def advanced_menu(db: DB, state: Path) -> None:
    while True:
        choice = questionary.select(
            "Ferramentas avançadas",
            choices=[
                "Ver detalhes da auditoria atual",
                "Gerar / abrir galeria",
                "Ver regras aprovadas",
                "Exportar relatórios",
                "Verificação remota do Google Drive",
                "Rollback",
                "Criar nova auditoria do zero",
                "Escolher auditoria antiga",
                "Voltar",
            ],
        ).ask()
        if not choice or choice == "Voltar":
            return

        run = latest_run(db)
        rid = run["run_id"] if run else None

        if choice == "Ver detalhes da auditoria atual":
            if not rid:
                console.print("Nenhuma auditoria.")
            else:
                show_counts(db, rid)
                console.print(dict(db.run(rid)))
        elif choice == "Gerar / abrir galeria":
            if not rid:
                console.print("Nenhuma auditoria.")
            else:
                p = generate_gallery(db, state, rid)
                console.print(f"Galeria: {p}")
                with contextlib.suppress(Exception):
                    if os.name == "nt":
                        os.startfile(str(p))
        elif choice == "Ver regras aprovadas":
            rules = load_rules(state)
            if not rules:
                console.print("Nenhuma regra humana aprovada ainda.")
            for r in rules:
                console.print(
                    f"[bold]{r.id}[/] {r.classification} · {r.source} → "
                    f"{r.storage}:{r.destination} · recursive={r.recursive}"
                )
        elif choice == "Exportar relatórios":
            if rid:
                export_audit(db, state, rid)
                console.print(f"[green]Relatórios:[/] {state / f'AUDITORIA_{rid}'}")
        elif choice == "Verificação remota do Google Drive":
            if not rid:
                console.print("Nenhuma auditoria.")
                continue
            if db.run(rid)["status"] not in {"EXECUTED_LOCAL", "LOCAL_AUDIT_PASS"}:
                console.print("[yellow]Disponível somente após a execução local.[/]")
                continue
            remote = questionary.text(
                "Remote rclone correspondente a ACIRV — CENTRAL:",
                instruction="Ex.: gdrive:ACIRV — CENTRAL",
            ).ask()
            if remote:
                console.print(remote_verify_rclone(db, state, rid, remote))
        elif choice == "Rollback":
            if not rid:
                console.print("Nenhuma auditoria.")
                continue
            phrase = f"REVERTER {rid}"
            conf = questionary.text(f"Digite exatamente: {phrase}").ask()
            console.print(rollback_run(db, state, rid, conf or ""))
        elif choice == "Criar nova auditoria do zero":
            f, h = _resolve_roots_minimal()
            entire = questionary.confirm(
                "Incluir TODO o Drive, inclusive áreas não ACIRV?",
                default=False,
            ).ask()
            reserve = int(questionary.text(
                "Reserva mínima de segurança (GB):",
                default=str(DEFAULT_RESERVE_GB),
            ).ask())
            rid_new = _audit_with_progress(db, state, f, h, bool(entire), reserve)
            console.print(f"[green]Nova auditoria:[/] {rid_new}")
        elif choice == "Escolher auditoria antiga":
            selected = select_run(db)
            if selected:
                show_counts(db, selected)
                console.print(dict(db.run(selected)))


def tui() -> int:
    load_tui_modules()
    state = default_state_dir()
    state.mkdir(parents=True, exist_ok=True)
    ensure_rules_file(state)
    db = DB(state / DB_NAME)

    try:
        while True:
            console.clear()
            run = show_home(db, state)

            if run is None:
                continue_label = "▶ COMEÇAR AUDITORIA SEGURA"
            else:
                title, _ = _run_progress_text(db, run)
                continue_label = f"▶ CONTINUAR — {title}"

            choice = questionary.select(
                " ",
                choices=[
                    continue_label,
                    "⚙ Ferramentas avançadas",
                    "Sair",
                ],
                instruction="Enter continua pelo caminho recomendado",
            ).ask()

            if not choice or choice == "Sair":
                break

            try:
                if choice.startswith("▶"):
                    guided_continue(db, state)
                else:
                    advanced_menu(db, state)
            except Exception as e:
                console.print(f"\n[red bold]BLOQUEADO POR SEGURANÇA:[/] {e}")

            questionary.press_any_key_to_continue("Pressione uma tecla para voltar…").ask()
    finally:
        db.close()
    return 0

# ---------------------------------------------------------------------------
# CLI developer/test
# ---------------------------------------------------------------------------

def main(argv: Optional[Sequence[str]]=None) -> int:
    ap=argparse.ArgumentParser(description=APP_NAME)
    ap.add_argument("--self-test",action="store_true")
    ap.add_argument("--inventory-audit",nargs=2,metavar=("F_TXT","H_TXT"))
    args=ap.parse_args(argv)
    if args.self_test:
        failed,results=run_self_tests()
        for name,ok,msg in results: print(("PASS" if ok else "FAIL"),name,"-",msg)
        print(f"RESULT: {len(results)-failed}/{len(results)} passed")
        return 1 if failed else 0
    if args.inventory_audit:
        res=inventory_classifier_audit(Path(args.inventory_audit[0]),Path(args.inventory_audit[1]));print(json.dumps(res,ensure_ascii=False,indent=2));return 1 if res["error_count"] else 0
    return tui()

if __name__=="__main__":
    raise SystemExit(main())
