#!/usr/bin/env python3
"""Gerador de Relatório de Cobertura e Paridade do Vault.

Lê 85-Bases-e-Consultas/Ledger-de-Ingestao.jsonl e 85-Bases-e-Consultas/Claims-Canonicos.jsonl
para calcular métricas reais e não-tautológicas de cobertura e paridade.

Gera o relatório Markdown em 85-Bases-e-Consultas/Relatorio-de-Cobertura.md

Métricas calculadas:
- git_tracked_source_accounting_coverage (blobs no ledger vs blobs na árvore Git)
- processable_source_coverage (fontes revisadas vs fontes processáveis)
- material_claim_disposition_coverage (claims com disposition explícita)
- provenance_coverage (claims promovidos com supporting_sources completas)
- validation_coverage (claims validados vs total de claims)
- known_sensitive_paths_blocked (prova observável de isolamento de segredos)

Uso:
    python relatorio_cobertura.py <vault_root> [--output caminho/relatorio.md] [--json]
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).parent))
from safety_gate import classify, CONFIRMED_SENSITIVE_PATHS
from inventariar_fontes import (
    load_ledger, git_ls_files_with_sha,
    DEFAULT_LEDGER, SOURCES_DIR
)
from claims import load_claims, DEFAULT_CLAIMS_FILE

DEFAULT_REPORT_OUTPUT = "85-Bases-e-Consultas/Relatorio-de-Cobertura.md"


def generate_coverage_data(vault_root: Path, ledger_path: Path, claims_path: Path) -> dict[str, Any]:
    """Calcula todas as métricas não-tautológicas de cobertura e paridade."""
    ledger_index = load_ledger(ledger_path) if ledger_path.exists() else {}
    claims = load_claims(claims_path) if claims_path.exists() else []
    git_entries = git_ls_files_with_sha(vault_root)

    total_git_blobs = len(git_entries)
    ledger_blobs = len(ledger_index)

    # 1. Coverage de Accounting Git
    git_tracked_source_accounting_coverage = (
        (ledger_blobs / total_git_blobs * 100) if total_git_blobs > 0 else 0.0
    )

    # Contagem por estado no ledger
    active_sources = [e for e in ledger_index.values() if e.get("source_status", "active") == "active"]
    deleted_sources = [e for e in ledger_index.values() if e.get("source_status") == "deleted_by_human"]

    sensitive_sources = [e for e in ledger_index.values() if e.get("read_status") == "sensitive_do_not_read"]
    unsupported_sources = [e for e in ledger_index.values() if e.get("read_status") == "unsupported"]
    error_sources = [e for e in ledger_index.values() if e.get("read_status") == "error"]

    # Fontes processáveis: não sensíveis e suportadas
    processable_sources = [
        e for e in active_sources
        if e.get("read_status") not in ("sensitive_do_not_read", "unsupported", "error")
    ]

    # Fontes semanticamente revisadas (reviewed ou reviewed_no_material_change ou processed)
    reviewed_sources = [
        e for e in processable_sources
        if e.get("review_status") in ("reviewed", "reviewed_no_material_change")
        or e.get("processing_status") == "processed"
    ]

    # 2. Processable Source Coverage (revisadas vs processáveis)
    total_processable = len(processable_sources)
    total_reviewed = len(reviewed_sources)
    processable_source_coverage = (
        (total_reviewed / total_processable * 100) if total_processable > 0 else 0.0
    )

    # Contagem por domínio e tipo
    domains = Counter(e.get("domain", "desconhecido") for e in ledger_index.values())
    extensions = Counter(Path(e.get("source_path", "")).suffix.lower() for e in ledger_index.values())

    # Métricas de Claims
    total_claims = len(claims)
    claims_with_disposition = [c for c in claims if c.get("disposition")]
    material_claim_disposition_coverage = (
        (len(claims_with_disposition) / total_claims * 100) if total_claims > 0 else 0.0
    )

    promoted_claims = [c for c in claims if c.get("disposition") == "promoted"]
    promoted_with_sources = [
        c for c in promoted_claims
        if c.get("supporting_sources") and len(c["supporting_sources"]) > 0 and c.get("canonical_destination")
    ]

    # 3. Provenance Coverage
    provenance_coverage = (
        (len(promoted_with_sources) / len(promoted_claims) * 100) if len(promoted_claims) > 0 else 0.0
    )

    # 4. Validation Coverage
    validated_claims = [c for c in claims if c.get("validation_status") == "validated"]
    validation_coverage = (
        (len(validated_claims) / total_claims * 100) if total_claims > 0 else 0.0
    )

    # 5. Isolamento Observável de Segredos
    blocked_known_secrets = []
    for sensitive_path in CONFIRMED_SENSITIVE_PATHS:
        result = classify(sensitive_path)
        blocked_known_secrets.append({
            "path": sensitive_path,
            "blocked": result.read_status == "sensitive_do_not_read",
            "reason": result.reason,
        })

    all_known_blocked = all(item["blocked"] for item in blocked_known_secrets)

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "accounting": {
            "total_git_blobs": total_git_blobs,
            "ledger_blobs": ledger_blobs,
            "git_tracked_source_accounting_coverage_pct": round(git_tracked_source_accounting_coverage, 2),
            "active_sources": len(active_sources),
            "deleted_sources": len(deleted_sources),
            "sensitive_sources": len(sensitive_sources),
            "unsupported_sources": len(unsupported_sources),
            "error_sources": len(error_sources),
            "total_processable": total_processable,
            "total_reviewed": total_reviewed,
            "processable_source_coverage_pct": round(processable_source_coverage, 2),
        },
        "domains": dict(domains),
        "extensions": dict(extensions),
        "claims": {
            "total_claims": total_claims,
            "material_claim_disposition_coverage_pct": round(material_claim_disposition_coverage, 2),
            "total_promoted_claims": len(promoted_claims),
            "promoted_with_provenance": len(promoted_with_sources),
            "provenance_coverage_pct": round(provenance_coverage, 2),
            "validated_claims": len(validated_claims),
            "validation_coverage_pct": round(validation_coverage, 2),
            "dispositions": dict(Counter(c.get("disposition") for c in claims)),
            "validation_statuses": dict(Counter(c.get("validation_status") for c in claims)),
        },
        "security": {
            "known_sensitive_paths_blocked": all_known_blocked,
            "blocked_details": blocked_known_secrets,
        },
    }


def render_markdown_report(data: dict[str, Any]) -> str:
    """Renderiza relatório Markdown formatado."""
    acc = data["accounting"]
    cl = data["claims"]
    sec = data["security"]

    lines = [
        "---",
        "id: base-relatorio-de-cobertura",
        "titulo: Relatorio-de-Cobertura",
        "tipo: auditoria",
        "subtipo: cobertura",
        f"ultima_revisao: '{datetime.now(timezone.utc).strftime('%Y-%m-%d')}'",
        "confidencialidade: interno",
        "---",
        "",
        "# Relatório de Cobertura e Paridade — ACIRV Notebook",
        "",
        f"> Gerado em: `{data['generated_at']}`",
        "",
        "## 1. Cobertura de Fontes (000-Arquivos-originais/)",
        "",
        "| Métrica | Valor |",
        "|---|---:|",
        f"| Total de blobs no repositório Git | {acc['total_git_blobs']} |",
        f"| Blobs indexados no Ledger | {acc['ledger_blobs']} |",
        f"| **Accounting Coverage (Git → Ledger)** | **{acc['git_tracked_source_accounting_coverage_pct']}%** |",
        f"| Fontes Ativas | {acc['active_sources']} |",
        f"| Fontes Deletadas por Humano | {acc['deleted_sources']} |",
        f"| Fontes Sensíveis (Safety Gate Bloqueado) | {acc['sensitive_sources']} |",
        f"| Formato Não Suportado | {acc['unsupported_sources']} |",
        f"| Com Erro | {acc['error_sources']} |",
        f"| Total de Fontes Processáveis | {acc['total_processable']} |",
        f"| Fontes Semanticamente Revisadas | {acc['total_reviewed']} |",
        f"| **Processable Source Coverage** | **{acc['processable_source_coverage_pct']}%** |",
        "",
        "### Cobertura por Domínio Temático",
        "",
        "| Domínio | Fontes |",
        "|---|---:|",
    ]

    for dom, cnt in sorted(data["domains"].items()):
        lines.append(f"| {dom} | {cnt} |")

    lines.extend([
        "",
        "## 2. Paridade e Cobertura de Evidências (Claims)",
        "",
        "| Métrica de Claims | Valor |",
        "|---|---:|",
        f"| Total de Claims Registrados | {cl['total_claims']} |",
        f"| Disposition Coverage | {cl['material_claim_disposition_coverage_pct']}% |",
        f"| Claims Promovidos com Proveniência Completa | {cl['promoted_with_provenance']} / {cl['total_promoted_claims']} |",
        f"| **Provenance Coverage** | **{cl['provenance_coverage_pct']}%** |",
        f"| Claims Validados | {cl['validated_claims']} / {cl['total_claims']} |",
        f"| **Validation Coverage** | **{cl['validation_coverage_pct']}%** |",
        "",
        "### Claims por Disposition",
        "",
        "| Disposition | Quantidade |",
        "|---|---:|",
    ])

    for disp, cnt in sorted(cl["dispositions"].items()):
        lines.append(f"| {disp} | {cnt} |")

    lines.extend([
        "",
        "## 3. Isolamento Observável de Segurança",
        "",
        f"- **Caminhos Sensíveis Confirmados Bloqueados Pré-Leitura:** `{'SIM' if sec['known_sensitive_paths_blocked'] else 'NÃO'}`",
        "",
        "| Caminho Sensível | Bloqueado Pré-Leitura | Motivo do Safety Gate |",
        "|---|:---:|---|",
    ])

    for item in sec["blocked_details"]:
        lines.append(f"| `{item['path']}` | {'SIM' if item['blocked'] else 'NÃO'} | {item['reason']} |")

    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Gera Relatório de Cobertura e Paridade do Vault."
    )
    parser.add_argument("vault", type=Path, help="Pasta raiz do vault")
    parser.add_argument(
        "--output", "-o", type=Path, default=None,
        help=f"Caminho do relatório Markdown (padrão: <vault>/{DEFAULT_REPORT_OUTPUT})"
    )
    parser.add_argument(
        "--ledger", type=Path, default=None,
        help=f"Caminho do ledger JSONL (padrão: <vault>/{DEFAULT_LEDGER})"
    )
    parser.add_argument(
        "--claims", type=Path, default=None,
        help=f"Caminho dos claims JSONL (padrão: <vault>/{DEFAULT_CLAIMS_FILE})"
    )
    parser.add_argument("--json", action="store_true", help="Saída em JSON")
    args = parser.parse_args()

    vault_root = args.vault.resolve()
    if not vault_root.is_dir():
        print(f"Erro: pasta não encontrada: {vault_root}", file=sys.stderr)
        return 2

    ledger_path = args.ledger or (vault_root / DEFAULT_LEDGER)
    claims_path = args.claims or (vault_root / DEFAULT_CLAIMS_FILE)
    output_path = args.output or (vault_root / DEFAULT_REPORT_OUTPUT)

    data = generate_coverage_data(vault_root, ledger_path, claims_path)

    if args.json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        report_md = render_markdown_report(data)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(report_md, encoding="utf-8")
        print(f"Relatório salvo em: {output_path}")
        print(f"Git Tracked Accounting Coverage: {data['accounting']['git_tracked_source_accounting_coverage_pct']}%")
        print(f"Processable Source Coverage: {data['accounting']['processable_source_coverage_pct']}%")
        print(f"Provenance Coverage: {data['claims']['provenance_coverage_pct']}%")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
