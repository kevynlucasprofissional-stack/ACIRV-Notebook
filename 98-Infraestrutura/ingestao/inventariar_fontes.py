#!/usr/bin/env python3
"""Inventário de 000-Arquivos-originais/ com blob SHA do Git.

Gera ou atualiza o ledger JSONL em 85-Bases-e-Consultas/Ledger-de-Ingestao.jsonl
com todas as fontes primárias, usando (source_path + blob_sha) como identidade.

Garante idempotência: se blob_sha não mudou, a entrada não é reprocessada.

Uso:
    python inventariar_fontes.py <vault_root>
    python inventariar_fontes.py <vault_root> --output caminho/ledger.jsonl

Dependências: Python 3.10+, git no PATH.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime, timezone

# Importa o safety gate do mesmo diretório
sys.path.insert(0, str(Path(__file__).parent))
from safety_gate import classify

SOURCES_DIR = "000-Arquivos-originais"
DEFAULT_LEDGER = "85-Bases-e-Consultas/Ledger-de-Ingestao.jsonl"
PROCESSOR_VERSION = "inventariar_fontes.py/1.0"


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
            # Ex: '"000-Arquivos-originais/Reuni\303\243o.md"' → '000-Arquivos-originais/Reunião.md'
            if raw_path.startswith('"') and raw_path.endswith('"'):
                raw_path = raw_path[1:-1]
                # Decodifica sequências octal do git (\303\243 → ã)
                raw_path = _decode_git_octal(raw_path)
            entries.append((blob_sha, raw_path))
    return entries


def _decode_git_octal(s: str) -> str:
    """Decodifica sequências octal do git (\\303\\243 → UTF-8 bytes → str Unicode)."""
    import re as _re
    octal_re = _re.compile(r'\\([0-7]{3})')
    
    def replace_octal(m: "re.Match") -> str:
        return chr(int(m.group(1), 8))
    
    # Substituir sequências octal por bytes
    result = []
    pos = 0
    raw_bytes = []
    i = 0
    chars = list(s)
    
    # Abordagem: converter para bytes primeiro, depois decodificar como UTF-8
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
        return s  # fallback: retorna original


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


def load_ledger(ledger_path: Path) -> dict[str, dict]:
    """Carrega ledger existente indexado por (source_path, blob_sha)."""
    index = {}
    if not ledger_path.exists():
        return index
    with ledger_path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
                key = (entry.get("source_path", ""), entry.get("blob_sha", ""))
                index[key] = entry
            except json.JSONDecodeError:
                continue
    return index


def save_ledger(ledger_path: Path, entries: list[dict]) -> None:
    """Salva ledger como JSONL."""
    ledger_path.parent.mkdir(parents=True, exist_ok=True)
    with ledger_path.open("w", encoding="utf-8", newline="\n") as f:
        for entry in sorted(entries, key=lambda e: e.get("source_path", "")):
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def run(vault_root: Path, ledger_path: Path, verbose: bool = False, with_commits: bool = False) -> dict:
    """Executa inventário e retorna estatísticas."""
    now_iso = datetime.now(timezone.utc).isoformat()

    # Carrega ledger existente
    existing = load_ledger(ledger_path)

    # Obtém lista atual de arquivos com blob SHA
    git_entries = git_ls_files_with_sha(vault_root)

    stats = {
        "total_fontes": len(git_entries),
        "unchanged_skip": 0,
        "new_entries": 0,
        "updated_entries": 0,
        "sensitive_do_not_read": 0,
        "unsupported": 0,
        "normal_unread": 0,
        "deleted_detected": 0,
    }

    # Mapeia caminhos atuais (para detecção de remoção)
    current_paths = {path for _, path in git_entries}

    # Detecta entradas no ledger cujo arquivo não existe mais no Git
    new_ledger_map: dict[tuple, dict] = {}
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

    # Processa entradas atuais
    for blob_sha, source_path in git_entries:
        key = (source_path, blob_sha)

        # Verifica se já existe no ledger com mesmo blob_sha → skip (idempotência)
        if key in existing:
            entry = existing[key]
            if entry.get("processing_status") not in ("unprocessed", "error"):
                stats["unchanged_skip"] += 1
                new_ledger_map[key] = entry
                if verbose:
                    print(f"[SKIP]    {source_path}")
                continue

        # Safety gate — classifica ANTES de qualquer leitura
        safety = classify(source_path)

        # Infere metadados pelo caminho
        suffix = Path(source_path).suffix.lower()
        domain = infer_domain(source_path)
        source_type = infer_source_type(source_path, suffix)

        # Verifica se é uma versão nova de arquivo existente (mesmo path, SHA diferente)
        previous_entries = [
            e for (p, s), e in existing.items()
            if p == source_path and s != blob_sha
        ]
        is_update = len(previous_entries) > 0

        # Obtém commits apenas se solicitado e necessário (operação cara)
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
            "source_date": None,      # inferência futura por conteúdo ou nome
            "effective_date": None,   # data efetiva do fato
            "media_type": suffix.lstrip(".") or "unknown",
            "domain": domain,
            "source_type": source_type,
            "authority": "nota_operacional_humana",
            "sensitivity": safety.sensitivity,
            "read_status": safety.read_status,
            "processing_status": "unprocessed",
            "last_processed": None,
            "processor_version": PROCESSOR_VERSION,
            "source_status": "active",
            "safety_reason": safety.reason,
            "inventoried_at": now_iso,
            "is_version_update": is_update,
            "supersedes_sha": [e.get("blob_sha") for e in previous_entries] if previous_entries else [],
        }

        # Atualiza contadores
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

    # Salva ledger atualizado
    save_ledger(ledger_path, list(new_ledger_map.values()))

    stats["ledger_total"] = len(new_ledger_map)
    return stats


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Inventaria 000-Arquivos-originais/ e atualiza o ledger JSONL."
    )
    parser.add_argument(
        "vault",
        type=Path,
        help="Pasta raiz do vault",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        default=None,
        help=f"Caminho do ledger JSONL (padrão: <vault>/{DEFAULT_LEDGER})",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Mostra cada arquivo processado",
    )
    parser.add_argument(
        "--with-commits",
        action="store_true",
        help="Inclui git log para first/last commit (lento — ~394 chamadas git log)",
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
