#!/usr/bin/env python3
"""Schema e operações para claims canônicos.

Define a estrutura de um claim, seu schema de validação, e funções de
leitura/escrita do arquivo Claims-Canonicos.jsonl.

Um claim é a unidade mínima de conhecimento rastreável:
  fonte → versão/blob → afirmação → disposition → destino canônico

Uso como módulo:
    from claims import Claim, load_claims, save_claims, validate_claim

Uso direto (validar arquivo existente):
    python claims.py 85-Bases-e-Consultas/Claims-Canonicos.jsonl
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

# ---------------------------------------------------------------------------
# Vocabulários controlados
# ---------------------------------------------------------------------------

VALID_EVIDENCE_CLASSES = frozenset([
    "fato_documentado",
    "dado_calculado",
    "interpretacao_operacional",
    "hipotese_de_trabalho",
    "recurso_pedagogico",
    "representacao_visual",
])

VALID_DISPOSITIONS = frozenset([
    "promoted",           # promovido para nota canônica
    "duplicate",          # duplicata de claim já registrado
    "superseded",         # substituído por fonte/claim mais recente
    "contradiction",      # contradição registrada, aguarda resolução
    "pending_validation", # aguarda validação humana
    "not_material",       # não material o suficiente para promoção
    "sensitive_skip",     # pulado por conter dado sensível
    "unsupported",        # formato não suportado para extração
    "error",              # erro durante processamento
])

VALID_VALIDATION_STATUSES = frozenset([
    "validated",
    "pending_validation",
    "rejected",
    "superseded",
    "not_required",
])

VALID_SEMANTIC_ROLES = frozenset([
    "fato",
    "decisao",
    "metrica",
    "processo",
    "responsabilidade",
    "prazo",
    "valor_financeiro",
    "risco",
    "politica",
    "historico",
    "planejamento",
    "resultado",
    "conflito",
    "hipotese",
])

VALID_AUTHORITY_LEVELS = frozenset([
    "registro_primario",          # nível 1
    "documento_institucional",    # nível 2
    "dado_estruturado",           # nível 3
    "nota_operacional_humana",    # nível 4
    "sintese_auditada",           # nível 5
    "conversa_ou_ia",             # nível 6 — indício, não autoridade
])

DEFAULT_CLAIMS_FILE = "85-Bases-e-Consultas/Claims-Canonicos.jsonl"


# ---------------------------------------------------------------------------
# Dataclass do claim
# ---------------------------------------------------------------------------

@dataclass
class Claim:
    # Identidade
    claim_id: str                        # ex: "event.sudoexpo.2026.data_inicio"
    source_path: str                     # caminho relativo em 000-Arquivos-originais/
    source_blob_sha: str                 # SHA do blob Git — identidade da versão

    # Conteúdo
    statement: str                       # afirmação em linguagem natural
    entity: str                          # entidade principal (ex: "SudoExpo 2026")
    property: str                        # propriedade (ex: "data_inicio")
    value: str                           # valor afirmado

    # Epistemologia
    semantic_role: str                   # um de VALID_SEMANTIC_ROLES
    evidence_class: str                  # um de VALID_EVIDENCE_CLASSES
    authority: str                       # um de VALID_AUTHORITY_LEVELS
    confidence: str                      # "alto", "medio_alto", "medio", "medio_baixo", "baixo"

    # Temporal
    observed_at: str                     # ISO 8601 — quando o claim foi extraído
    valid_from: Optional[str] = None     # início do período de validade do fato
    valid_to: Optional[str] = None       # fim do período de validade

    # Estado
    disposition: str = "pending_validation"    # um de VALID_DISPOSITIONS
    validation_status: str = "pending_validation"  # um de VALID_VALIDATION_STATUSES

    # Rastreabilidade
    canonical_destination: Optional[str] = None   # nota canônica de destino
    destination_anchor: Optional[str] = None       # heading ou block ID na nota

    # Relações com outros claims
    supersedes: list[str] = field(default_factory=list)    # claim_ids que este substitui
    contradicts: list[str] = field(default_factory=list)   # claim_ids que contradiz
    duplicates: Optional[str] = None                       # claim_id duplicado

    # Metadados
    extractor_version: str = "manual"
    notes: Optional[str] = None


def validate_claim(claim: dict) -> list[str]:
    """Retorna lista de erros de validação (vazia = válido)."""
    errors = []

    required = [
        "claim_id", "source_path", "source_blob_sha",
        "statement", "entity", "property", "value",
        "semantic_role", "evidence_class", "authority", "confidence",
        "observed_at", "disposition", "validation_status",
    ]
    for field_name in required:
        if not claim.get(field_name):
            errors.append(f"campo obrigatório ausente ou vazio: {field_name}")

    if claim.get("evidence_class") and claim["evidence_class"] not in VALID_EVIDENCE_CLASSES:
        errors.append(f"evidence_class inválida: {claim['evidence_class']}")

    if claim.get("disposition") and claim["disposition"] not in VALID_DISPOSITIONS:
        errors.append(f"disposition inválida: {claim['disposition']}")

    if claim.get("validation_status") and claim["validation_status"] not in VALID_VALIDATION_STATUSES:
        errors.append(f"validation_status inválido: {claim['validation_status']}")

    if claim.get("semantic_role") and claim["semantic_role"] not in VALID_SEMANTIC_ROLES:
        errors.append(f"semantic_role inválido: {claim['semantic_role']}")

    if claim.get("authority") and claim["authority"] not in VALID_AUTHORITY_LEVELS:
        errors.append(f"authority inválida: {claim['authority']}")

    # Contradição não pode ser silenciosamente validada
    if claim.get("disposition") == "contradiction" and claim.get("validation_status") == "validated":
        errors.append(
            "contradiction não pode ter validation_status=validated sem resolução explícita"
        )

    # Claim promovido deve ter destino canônico
    if claim.get("disposition") == "promoted" and not claim.get("canonical_destination"):
        errors.append("claim com disposition=promoted deve ter canonical_destination")

    # Claim promovido deve ter source_blob_sha
    if claim.get("disposition") == "promoted" and not claim.get("source_blob_sha"):
        errors.append("claim promovido requer source_blob_sha")

    return errors


def load_claims(claims_path: Path) -> list[dict]:
    """Carrega claims de arquivo JSONL."""
    claims = []
    if not claims_path.exists():
        return claims
    with claims_path.open(encoding="utf-8") as f:
        for i, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                claims.append(json.loads(line))
            except json.JSONDecodeError as exc:
                print(f"Aviso: linha {i} inválida em {claims_path}: {exc}", file=sys.stderr)
    return claims


def save_claims(claims_path: Path, claims: list[dict]) -> None:
    """Salva claims como JSONL."""
    claims_path.parent.mkdir(parents=True, exist_ok=True)
    with claims_path.open("w", encoding="utf-8", newline="\n") as f:
        for claim in sorted(claims, key=lambda c: c.get("claim_id", "")):
            f.write(json.dumps(claim, ensure_ascii=False) + "\n")


def claim_exists(claims: list[dict], claim_id: str) -> bool:
    return any(c.get("claim_id") == claim_id for c in claims)


def get_claims_by_source(claims: list[dict], source_path: str) -> list[dict]:
    return [c for c in claims if c.get("source_path") == source_path]


def get_pending_validations(claims: list[dict]) -> list[dict]:
    return [c for c in claims if c.get("validation_status") == "pending_validation"]


def get_contradictions(claims: list[dict]) -> list[dict]:
    return [c for c in claims if c.get("disposition") == "contradiction"]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Valida arquivo Claims-Canonicos.jsonl."
    )
    parser.add_argument(
        "claims_file",
        type=Path,
        nargs="?",
        help="Arquivo JSONL de claims (padrão: <cwd>/" + DEFAULT_CLAIMS_FILE + ")",
    )
    parser.add_argument("--verbose", "-v", action="store_true")
    args = parser.parse_args()

    claims_file = args.claims_file or Path.cwd() / DEFAULT_CLAIMS_FILE

    if not claims_file.exists():
        print(f"Arquivo não encontrado: {claims_file}", file=sys.stderr)
        return 2

    claims = load_claims(claims_file)
    print(f"Claims carregados: {len(claims)}")

    all_valid = True
    for i, claim in enumerate(claims):
        errors = validate_claim(claim)
        if errors:
            all_valid = False
            print(f"\nClaim #{i + 1} ({claim.get('claim_id', '?')}): {len(errors)} erro(s)")
            for err in errors:
                print(f"  ✗ {err}")
        elif args.verbose:
            print(f"  ✓ {claim.get('claim_id', '?')}")

    pending = get_pending_validations(claims)
    contradictions = get_contradictions(claims)

    print(f"\nResumo:")
    print(f"  Total: {len(claims)}")
    print(f"  Pending validation: {len(pending)}")
    print(f"  Contradições: {len(contradictions)}")
    print(f"  Válidos (schema): {'SIM' if all_valid else 'NÃO'}")

    return 0 if all_valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
