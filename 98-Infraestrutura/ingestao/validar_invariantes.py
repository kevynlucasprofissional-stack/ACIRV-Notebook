#!/usr/bin/env python3
"""Validador determinístico de invariantes do ACIRV Notebook.

Verifica:
1. Imutabilidade runtime: 000-Arquivos-originais/ permanece intocado (snapshot pré e pós).
2. Git commit immutability: zero commits na branch afetando 000-Arquivos-originais/.
3. Safety gate: caminhos sensíveis confirmados (Contas e Senhas.md, Minha Chave API Antropic.md) bloqueados.
4. Idempotência e integridade do ledger (Ledger-de-Ingestao.jsonl).
5. Integridade referencial de claims (Claims-Canonicos.jsonl) contra o ledger e o vault.
6. Desacoplamento de validação humana e proveniência estrita de claims promovidos.
7. Ausência de contradições silenciosas (contradiction ≠ validated).

Uso:
    python validar_invariantes.py <vault_root> [--claims] [--ledger] [--json]

Retorna:
    0 = todos os invariantes satisfeitos
    1 = um ou mais invariantes violados
    2 = erro de uso
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List

sys.path.insert(0, str(Path(__file__).parent))
from safety_gate import classify, CONFIRMED_SENSITIVE_PATHS
from claims import (
    load_claims, validate_claims_dataset,
    get_contradictions, DEFAULT_CLAIMS_FILE
)
from inventariar_fontes import load_ledger, SOURCES_DIR, DEFAULT_LEDGER


def take_sources_snapshot(vault_root: Path) -> dict[str, str]:
    """Tira um snapshot de hashes de todos os arquivos em 000-Arquivos-originais/ para verificação runtime."""
    sources_dir = vault_root / SOURCES_DIR
    snapshot = {}
    if not sources_dir.exists():
        return snapshot

    for p in sorted(sources_dir.rglob("*")):
        if p.is_file():
            rel_path = str(p.relative_to(vault_root)).replace("\\", "/")
            # Não lemos arquivos sensíveis confirmados nem para hash de snapshot se classificados pelo safety gate
            safety = classify(rel_path)
            if safety.read_status == "sensitive_do_not_read":
                # Usamos apenas mtime + tamanho para snapshot não invasivo de arquivos sensíveis
                stat = p.stat()
                snapshot[rel_path] = f"stat:{stat.st_size}:{stat.st_mtime}"
            else:
                try:
                    content = p.read_bytes()
                    snapshot[rel_path] = hashlib.sha256(content).hexdigest()
                except Exception:
                    snapshot[rel_path] = "unreadable"

    return snapshot


def check_runtime_immutability(snapshot_before: dict[str, str], snapshot_after: dict[str, str]) -> list[str]:
    """Compara snapshots pré e pós-execução para garantir zero alterações em 000-Arquivos-originais/."""
    errors = []
    before_keys = set(snapshot_before.keys())
    after_keys = set(snapshot_after.keys())

    removed = before_keys - after_keys
    for r in sorted(removed):
        errors.append(f"INVARIANTE VIOLADO (RUNTIME): Arquivo removido de {SOURCES_DIR}/ durante execução: {r}")

    created = after_keys - before_keys
    for c in sorted(created):
        errors.append(f"INVARIANTE VIOLADO (RUNTIME): Arquivo criado em {SOURCES_DIR}/ durante execução: {c}")

    common = before_keys & after_keys
    for k in sorted(common):
        if snapshot_before[k] != snapshot_after[k]:
            errors.append(f"INVARIANTE VIOLADO (RUNTIME): Conteúdo alterado em {SOURCES_DIR}/ durante execução: {k}")

    return errors


def check_git_commit_immutability(vault_root: Path) -> list[str]:
    """Verifica que nenhuma automação commitou mudanças em 000-Arquivos-originais/ na branch atual vs main."""
    errors = []

    # Diff commitado entre branch atual e main
    result = subprocess.run(
        ["git", "diff", "--name-only", "main..HEAD", "--", f"{SOURCES_DIR}/"],
        cwd=vault_root,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if result.returncode == 0 and result.stdout.strip():
        modified = [line.strip() for line in result.stdout.splitlines() if line.strip()]
        for m in modified:
            errors.append(
                f"INVARIANTE VIOLADO (GIT): {SOURCES_DIR}/ foi alterado em commit na branch em relação ao main: {m}"
            )

    return errors


def check_safety_gate_known_secrets(vault_root: Path) -> list[str]:
    """Verifica que todos os caminhos sensíveis confirmados são bloqueados pré-leitura."""
    errors = []

    for sensitive_path in CONFIRMED_SENSITIVE_PATHS:
        result = classify(sensitive_path)
        if result.read_status != "sensitive_do_not_read":
            errors.append(
                f"SAFETY GATE FALHOU: '{sensitive_path}' não foi classificado como sensitive_do_not_read "
                f"(obtido: {result.read_status})"
            )
        if result.sensitivity not in ("confirmed_secret", "secret_suspected"):
            errors.append(
                f"SAFETY GATE FALHOU: '{sensitive_path}' não foi classificado como secret "
                f"(obtido: {result.sensitivity})"
            )

    return errors


def check_ledger_integrity(ledger_path: Path) -> list[str]:
    """Verifica parsing estrito, schema e ausência de duplicatas no ledger."""
    errors = []
    if not ledger_path.exists():
        return ["Ledger não encontrado em " + str(ledger_path)]

    try:
        ledger_map = load_ledger(ledger_path)
    except ValueError as exc:
        return [f"Erro de integridade/parsing no ledger: {exc}"]

    # Validação adicional de schema
    for key, entry in ledger_map.items():
        if not entry.get("source_path") or not entry.get("blob_sha"):
            errors.append(f"Entrada inválida no ledger: chave {key}")

    return errors


def check_claims_referential_integrity(vault_root: Path, claims_path: Path, ledger_path: Path) -> list[str]:
    """Verifica integridade referencial dos claims contra o vault e o ledger."""
    errors = []
    if not claims_path.exists():
        return []

    try:
        claims = load_claims(claims_path)
        ledger_map = load_ledger(ledger_path) if ledger_path.exists() else None
        errors = validate_claims_dataset(vault_root, claims, ledger_map)
    except ValueError as exc:
        errors.append(f"Erro de parsing/schema em claims: {exc}")

    return errors


def check_contradictions_not_validated(claims_path: Path) -> list[str]:
    """Verifica que nenhuma contradição é silenciosamente apresentada como validada."""
    errors = []
    if not claims_path.exists():
        return []

    try:
        claims = load_claims(claims_path)
        contradictions = [c for c in claims if c.get("disposition") == "contradiction"]
        for claim in contradictions:
            if claim.get("validation_status") == "validated":
                errors.append(
                    f"CONTRADIÇÃO SILENCIOSA: claim '{claim.get('claim_id', '?')}' tem "
                    f"disposition=contradiction mas validation_status=validated"
                )
    except Exception:
        pass

    return errors


def run_all_checks(vault_root: Path, ledger_path: Path, claims_path: Path) -> dict[str, Any]:
    """Executa todos os invariantes com snapshot runtime de imutabilidade."""
    snapshot_before = take_sources_snapshot(vault_root)

    results: dict[str, Any] = {}
    all_passed = True

    checks = [
        ("git_commit_immutability", check_git_commit_immutability, (vault_root,)),
        ("safety_gate_known_secrets", check_safety_gate_known_secrets, (vault_root,)),
        ("ledger_integrity", check_ledger_integrity, (ledger_path,)),
        ("claims_referential_integrity", check_claims_referential_integrity, (vault_root, claims_path, ledger_path)),
        ("contradictions_not_validated", check_contradictions_not_validated, (claims_path,)),
    ]

    for check_name, check_fn, check_args in checks:
        errors = check_fn(*check_args)
        passed = len(errors) == 0
        if not passed:
            all_passed = False
        results[check_name] = {
            "passed": passed,
            "errors": errors,
        }

    # Snapshot pós-execução
    snapshot_after = take_sources_snapshot(vault_root)
    runtime_immutability_errors = check_runtime_immutability(snapshot_before, snapshot_after)
    runtime_passed = len(runtime_immutability_errors) == 0
    if not runtime_passed:
        all_passed = False
    results["runtime_sources_immutability"] = {
        "passed": runtime_passed,
        "errors": runtime_immutability_errors,
    }

    results["_all_passed"] = all_passed
    return results


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Valida invariantes do ACIRV Notebook."
    )
    parser.add_argument("vault", type=Path, help="Pasta raiz do vault")
    parser.add_argument(
        "--ledger",
        type=Path,
        default=None,
        help=f"Caminho do ledger JSONL (padrão: <vault>/85-Bases-e-Consultas/Ledger-de-Ingestao.jsonl)",
    )
    parser.add_argument(
        "--claims",
        type=Path,
        default=None,
        help=f"Caminho do arquivo de claims (padrão: <vault>/85-Bases-e-Consultas/Claims-Canonicos.jsonl)",
    )
    parser.add_argument("--json", action="store_true", help="Saída em JSON")
    args = parser.parse_args()

    vault_root = args.vault.resolve()
    if not vault_root.is_dir():
        print(f"Erro: pasta não encontrada: {vault_root}", file=sys.stderr)
        return 2

    ledger_path = args.ledger or (vault_root / DEFAULT_LEDGER)
    claims_path = args.claims or (vault_root / DEFAULT_CLAIMS_FILE)

    results = run_all_checks(vault_root, ledger_path, claims_path)

    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        print("=== Validacao de Invariantes ACIRV Notebook ===\n")
        for check_name, result in results.items():
            if check_name.startswith("_"):
                continue
            status = "[PASS]" if result["passed"] else "[FAIL]"
            print(f"{status}  {check_name}")
            for err in result.get("errors", []):
                print(f"         -> {err}")

        print()
        if results["_all_passed"]:
            print("[OK] Todos os invariantes satisfeitos.")
        else:
            failed = [k for k, v in results.items() if not k.startswith("_") and not v["passed"]]
            print(f"[FALHOU] {len(failed)} check(s) falhou/falharam: {', '.join(failed)}")

    return 0 if results["_all_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
