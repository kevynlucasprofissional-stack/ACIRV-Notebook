#!/usr/bin/env python3
"""Inventário determinístico de 000-Arquivos-originais/ com blob SHA do Git.

Gera ou atualiza o ledger JSONL em 85-Bases-e-Consultas/Ledger-de-Ingestao.jsonl
com todas as fontes primárias, usando (source_path + blob_sha) como identidade.

Garante idempotência absoluta:
- Blob conhecido e sem alteração: preserva a entrada existente sem recriação ou alteração
  de inventoried_at, sem incrementar new_entries/updated_entries e sem gerar diff no JSONL.
- Segunda execução sem mudanças produz: 0 novos blobs, 0 atualizados, 0 diffs.

Uso:
    python inventariar_fontes.py <vault_root>
    python inventariar_fontes.py <vault_root> --output caminho/ledger.jsonl

Dependências: Python 3.10+, git no PATH.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

# Importa o safety gate do mesmo diretório
sys.path.insert(0, str(Path(__file__).parent))
from safety_gate import classify, CONFIRMED_SENSITIVE_PATHS

SOURCES_DIR = "000-Arquivos-originais"
DEFAULT_LEDGER = "85-Bases-e-Consultas/Ledger-de-Ingestao.jsonl"
PROCESSOR_VERSION = "inventariar_fontes.py/2.0"

VALID_SENSITIVITIES = frozenset([
    "normal", "personal_data", "confidential_process",
    "secret_suspected", "confirmed_secret", "technical_quarantine"
])

VALID_READ_STATUSES = frozenset([
    "unread", "processed", "sensitive_do_not_read", "unsupported", "error"
])

VALID_REVIEW_STATUSES = frozenset([
    "unreviewed", "reviewed", "reviewed_no_material_change",
    "partially_reviewed", "sensitive_do_not_read", "unsupported", "error"
])

VALID_PROCESSING_STATUSES = frozenset([
    "unprocessed", "in_progress", "partially_processed", "processed", "error"
])

VALID_SOURCE_STATUSES = frozenset([
    "active", "deleted_by_human"
])

HEX_SHA_RE = re.compile(r"^[0-9a-f]{40}$", re.IGNORECASE)


def git_ls_files_with_sha(vault_root: Path) -> list[tuple[str, str]]:
    """Retorna lista de (blob_sha, path) para 000-Arquivos-originais/."""
    result = subprocess.run(
        ["git", "ls-files", "--format=%(objectname) %(path)", f"{SOURCES_DIR}/"],
        cwd=vault_root,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if result.returncode != 0:
        raise RuntimeError(f"git ls-files falhou: {result.stderr}")

    entries = []
    for line in result.stdout.splitlines():
        line = line.strip()
        if not line:
            continue
        parts = line.split(" ", 1)
        if len(parts) == 2:
            blob_sha = parts[0].strip()
            raw_path = parts[1].strip()
            # git ls-files envolve caminhos com caracteres não-ASCII entre aspas
            if raw_path.startswith('"') and raw_path.endswith('"'):
                raw_path = raw_path[1:-1]
                raw_path = _decode_git_octal(raw_path)
            # Normalizar separadores para barra normal para consistência entre OS
            raw_path = raw_path.replace("\\", "/")
            entries.append((blob_sha, raw_path))
    return entries


def _decode_git_octal(s: str) -> str:
    """Decodifica sequências octal do git (\\303\\243 → UTF-8 bytes → str Unicode)."""
    byte_list = []
    j = 0
    while j < len(s):
        if s[j] == '\\' and j + 3 < len(s) and all(c in '01234567' for c in s[j+1:j+4]):
            byte_list.append(int(s[j+1:j+4], 8))
            j += 4
        else:
            byte_list.append(ord(s[j]))
            j += 1
    try:
        return bytes(byte_list).decode('utf-8')
    except (UnicodeDecodeError, ValueError):
        return s


def git_log_first_commit(vault_root: Path, path: str) -> str | None:
    """Retorna o SHA do primeiro commit que incluiu este arquivo."""
    result = subprocess.run(
        ["git", "log", "--follow", "--diff-filter=A", "--format=%H", "--", path],
        cwd=vault_root,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    lines = [l.strip() for l in result.stdout.splitlines() if l.strip()]
    return lines[-1] if lines else None


def git_log_last_commit(vault_root: Path, path: str) -> str | None:
    """Retorna o SHA do commit mais recente que tocou este arquivo."""
    result = subprocess.run(
        ["git", "log", "-1", "--format=%H", "--", path],
        cwd=vault_root,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    lines = [l.strip() for l in result.stdout.splitlines() if l.strip()]
    return lines[0] if lines else None


def infer_domain(path: str) -> str:
    """Infere domínio temático pelo nome do arquivo."""
    name = path.lower()
    if any(k in name for k in ["sudoexpo", "sudo expo", "expositora"]):
        return "sudoexpo"
    if any(k in name for k in ["conecta", "saas", "ecossistema"]):
        return "conecta"
    if any(k in name for k in ["metrica", "relatorio", "relatório", "kpi", "indicador", "dados"]):
        return "metricas"
    if any(k in name for k in ["reuniao", "reunião", "scrum", "assembleia"]):
        return "reunioes"
    if any(k in name for k in ["campanha", "pertencimento", "indica", "indicação"]):
        return "campanhas"
    if any(k in name for k in ["tom de voz", "marca", "manual", "playbook"]):
        return "marca"
    if any(k in name for k in ["servico", "serviço", "beneficio", "benefício", "certificado", "consultoria"]):
        return "servicos"
    if any(k in name for k in ["imprensa", "release", "materia", "noticia"]):
        return "imprensa"
    if any(k in name for k in ["stake", "diretoria", "presidente", "vcom", "janaine", "raphael"]):
        return "stakeholders"
    if any(k in name for k in ["cam ", "cam/", "juridic", "legal", "câmara"]):
        return "cam"
    if any(k in name for k in ["acirv meet", "saas", "lovable"]):
        return "tecnologia"
    return "geral"


def infer_source_type(path: str, suffix: str) -> str:
    """Infere o tipo de fonte."""
    name = path.lower()
    if any(k in name for k in ["reuniao", "reunião", "scrum"]):
        return "ata_reuniao"
    if any(k in name for k in ["relatorio", "relatório", "metricas", "métrica"]):
        return "relatorio"
    if any(k in name for k in ["planejamento", "plano"]):
        return "planejamento"
    if any(k in name for k in ["transcricao", "transcrição"]):
        return "transcricao"
    if any(k in name for k in ["dossie", "dossiê"]):
        return "dossie"
    if any(k in name for k in ["roteiro", "cerimonial"]):
        return "roteiro"
    if any(k in name for k in ["release"]):
        return "release"
    if suffix in (".zip", ".pdf"):
        return "artefato_tecnico"
    return "nota_operacional"


def load_ledger(ledger_path: Path) -> dict[tuple[str, str], dict]:
    """Carrega e valida estritamente o ledger existente indexado por (source_path, blob_sha).
    
    Lança ValueError explícito com indicação de linha em caso de erro JSON ou schema inválido.
    """
    index: dict[tuple[str, str], dict] = {}
    if not ledger_path.exists():
        return index

    with ledger_path.open(encoding="utf-8") as f:
        for i, line in enumerate(f, 1):
            line_str = line.strip()
            if not line_str:
                continue
            try:
                entry = json.loads(line_str)
            except json.JSONDecodeError as exc:
                raise ValueError(
                    f"Erro de parsing JSON no ledger '{ledger_path}', linha {i}: {exc}"
                ) from exc

            # Normalização e validação estrita dos campos
            source_path = entry.get("source_path")
            blob_sha = entry.get("blob_sha")
            if not source_path or not isinstance(source_path, str):
                raise ValueError(
                    f"Campo 'source_path' ausente ou inválido no ledger '{ledger_path}', linha {i}"
                )
            if not blob_sha or not isinstance(blob_sha, str):
                raise ValueError(
                    f"Campo 'blob_sha' ausente ou inválido no ledger '{ledger_path}', linha {i}"
                )

            # Normalizar separador do caminho para barra normal
            source_path_norm = source_path.replace("\\", "/")
            entry["source_path"] = source_path_norm

            # Validar enums se presentes
            if entry.get("sensitivity") and entry["sensitivity"] not in VALID_SENSITIVITIES:
                raise ValueError(
                    f"Valor inválido de 'sensitivity' ('{entry['sensitivity']}') no ledger '{ledger_path}', linha {i}"
                )
            if entry.get("processing_status") and entry["processing_status"] not in VALID_PROCESSING_STATUSES:
                raise ValueError(
                    f"Valor inválido de 'processing_status' ('{entry['processing_status']}') no ledger '{ledger_path}', linha {i}"
                )

            key = (source_path_norm, blob_sha)
            if key in index:
                raise ValueError(
                    f"Entrada duplicada para (source_path='{source_path_norm}', blob_sha='{blob_sha}') no ledger '{ledger_path}', linha {i}"
                )
            index[key] = entry

    return index


def save_ledger(ledger_path: Path, entries: list[dict]) -> None:
    """Salva ledger como JSONL ordenado por source_path e blob_sha."""
    ledger_path.parent.mkdir(parents=True, exist_ok=True)
    with ledger_path.open("w", encoding="utf-8", newline="\n") as f:
        for entry in sorted(entries, key=lambda e: (e.get("source_path", "").replace("\\", "/"), e.get("blob_sha", ""))):
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def run(vault_root: Path, ledger_path: Path, verbose: bool = False, with_commits: bool = False) -> dict:
    """Executa inventário determinístico e retorna estatísticas."""
    now_iso = datetime.now(timezone.utc).isoformat()

    existing = load_ledger(ledger_path)
    git_entries = git_ls_files_with_sha(vault_root)

    stats = {
        "total_fontes": len(git_entries),
        "unchanged_skip": 0,
        "existing_unprocessed": 0,
        "new_entries": 0,
        "updated_entries": 0,
        "sensitive_do_not_read": 0,
        "unsupported": 0,
        "normal_unread": 0,
        "deleted_detected": 0,
    }

    current_paths = {path for _, path in git_entries}
    new_ledger_map: dict[tuple[str, str], dict] = {}

    # 1. Detecta remoções humanas
    for key, entry in existing.items():
        src_path = entry.get("source_path", "")
        if src_path not in current_paths and entry.get("source_status", "active") == "active":
            entry = dict(entry)
            entry["source_status"] = "deleted_by_human"
            entry["deleted_detected_at"] = now_iso
            stats["deleted_detected"] += 1
            if verbose:
                print(f"[DELETED] {src_path}")
        new_ledger_map[key] = entry

    # 2. Processa entradas atuais do Git
    for blob_sha, source_path in git_entries:
        source_path = source_path.replace("\\", "/")
        key = (source_path, blob_sha)

        # IDEMPOTÊNCIA ABSOLUTA: Se a tupla (source_path, blob_sha) já existe no ledger
        if key in existing:
            entry = existing[key]
            # Mantém exatamente a entrada existente, sem re-criação ou alteração de inventoried_at
            new_ledger_map[key] = entry
            if entry.get("review_status") == "unreviewed" or entry.get("processing_status") == "unprocessed":
                stats["existing_unprocessed"] += 1
            else:
                stats["unchanged_skip"] += 1
            if verbose:
                print(f"[EXISTS]  {source_path} (review_status: {entry.get('review_status', 'unreviewed')})")
            continue

        # Novo blob para este source_path (arquivo novo ou editado)
        safety = classify(source_path)

        suffix = Path(source_path).suffix.lower()
        domain = infer_domain(source_path)
        source_type = infer_source_type(source_path, suffix)

        previous_entries = [
            e for (p, s), e in existing.items()
            if p == source_path and s != blob_sha
        ]
        is_update = len(previous_entries) > 0

        first_seen_commit = None
        last_seen_commit = None
        if with_commits:
            first_seen_commit = git_log_first_commit(vault_root, source_path)
            last_seen_commit = git_log_last_commit(vault_root, source_path)

        entry = {
            "source_path": source_path,
            "blob_sha": blob_sha,
            "first_seen_commit": first_seen_commit,
            "last_seen_commit": last_seen_commit,
            "source_date": None,
            "effective_date": None,
            "media_type": suffix.lstrip(".") or "unknown",
            "domain": domain,
            "source_type": source_type,
            "authority": "nota_operacional_humana",
            "sensitivity": safety.sensitivity,
            "read_status": safety.read_status,
            "review_status": "unreviewed" if safety.read_status == "unread" else safety.read_status,
            "processing_status": "unprocessed",
            "last_reviewed_at": None,
            "reviewed_by": None,
            "processor_version": PROCESSOR_VERSION,
            "source_status": "active",
            "safety_reason": safety.reason,
            "inventoried_at": now_iso,
            "is_version_update": is_update,
            "supersedes_sha": [e.get("blob_sha") for e in previous_entries] if previous_entries else [],
            "claims_detected": 0,
            "claims_by_disposition": {},
            "processing_result": None,
        }

        if safety.read_status == "sensitive_do_not_read":
            stats["sensitive_do_not_read"] += 1
        elif safety.read_status == "unsupported":
            stats["unsupported"] += 1
        else:
            stats["normal_unread"] += 1

        if is_update:
            stats["updated_entries"] += 1
            if verbose:
                print(f"[UPDATE]  {source_path} (SHA anterior: {previous_entries[-1].get('blob_sha', '?')[:8]})")
        else:
            stats["new_entries"] += 1
            if verbose:
                print(f"[NEW]     {source_path}")

        new_ledger_map[key] = entry

    save_ledger(ledger_path, list(new_ledger_map.values()))
    stats["ledger_total"] = len(new_ledger_map)
    return stats


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Inventaria 000-Arquivos-originais/ e atualiza o ledger JSONL."
    )
    parser.add_argument("vault", type=Path, help="Pasta raiz do vault")
    parser.add_argument(
        "--output", "-o", type=Path, default=None,
        help=f"Caminho do ledger JSONL (padrão: <vault>/{DEFAULT_LEDGER})"
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true",
        help="Mostra cada arquivo processado"
    )
    parser.add_argument(
        "--with-commits", action="store_true",
        help="Inclui git log para first/last commit (lento — ~394 chamadas git log)"
    )
    args = parser.parse_args()

    vault_root = args.vault.resolve()
    if not vault_root.is_dir():
        print(f"Erro: pasta não encontrada: {vault_root}", file=sys.stderr)
        return 2

    ledger_path = args.output or (vault_root / DEFAULT_LEDGER)

    try:
        stats = run(vault_root, ledger_path, verbose=args.verbose, with_commits=args.with_commits)
    except Exception as exc:
        print(f"Erro: {exc}", file=sys.stderr)
        return 2

    print(json.dumps(stats, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
