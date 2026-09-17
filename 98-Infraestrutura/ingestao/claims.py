#!/usr/bin/env python3
"""Schema, validação estrita e integridade referencial para claims canônicos.

Define a estrutura de um claim, seu schema de validação, integridade referencial
com o ledger e resolução determinística de anchors em notas canônicas.

Um claim é a unidade mínima de conhecimento rastreável:
  fontes primárias + validação humana → afirmação → disposition → destino canônico + anchor

Uso como módulo:
    from claims import Claim, load_claims, save_claims, validate_claims_dataset, get_contradictions

Uso direto (validar arquivo de claims contra o vault):
    python claims.py <vault_root> [--claims] [--ledger]
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, Any

# ---------------------------------------------------------------------------
# Vocabulários controlados estritos
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
    "not_required",
    "rejected",
    "superseded",
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

CLAIM_ID_ASCII_RE = re.compile(r"^[a-z0-9_.-]+$")
DEFAULT_CLAIMS_FILE = "85-Bases-e-Consultas/Claims-Canonicos.jsonl"
DEFAULT_LEDGER_FILE = "85-Bases-e-Consultas/Ledger-de-Ingestao.jsonl"


# ---------------------------------------------------------------------------
# Dataclass do claim
# ---------------------------------------------------------------------------

@dataclass
class Claim:
    # Identidade (deve ser ASCII puro)
    claim_id: str                        # ex: "event.sudoexpo.2026.data_inicio"
    
    # Documentos de suporte primários (000-Arquivos-originais/)
    supporting_sources: list[dict]       # list of { "source_path": ..., "source_blob_sha": ... }
    
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
    disposition: str = "pending_validation"            # um de VALID_DISPOSITIONS
    validation_status: str = "pending_validation"      # um de VALID_VALIDATION_STATUSES

    # Desacoplamento de Validação Humana (quando a evidência vem de confirmação posterior)
    validation_source: Optional[str] = None            # e.g. "human_validation" / nota de pendências
    validation_record: Optional[str] = None            # e.g. "validacao_humana_2026_09_17"
    validated_at: Optional[str] = None                 # ISO timestamp de validação

    # Rastreabilidade Canônica
    canonical_destination: Optional[str] = None   # caminho relativo no vault (ex: 03-.../SudoExpo-2026.md)
    destination_anchor: Optional[str] = None       # heading slug, heading text ou block ID (^id)

    # Relações com outros claims (devem ser IDs de máquina ASCII válidos)
    supersedes: list[str] = field(default_factory=list)    # claim_ids que este substitui
    contradicts: list[str] = field(default_factory=list)   # claim_ids que contradiz
    duplicates: Optional[str] = None                       # claim_id duplicado

    # Metadados
    extractor_version: str = "manual/2.0"
    notes: Optional[str] = None


def load_claims(claims_path: Path) -> list[dict]:
    """Carrega e valida sintaticamente claims de arquivo JSONL.
    
    Lança ValueError estrito com indicação de linha em caso de erro JSON.
    """
    claims = []
    if not claims_path.exists():
        return claims
    with claims_path.open(encoding="utf-8") as f:
        for i, line in enumerate(f, 1):
            line_str = line.strip()
            if not line_str:
                continue
            try:
                claim = json.loads(line_str)
                claims.append(claim)
            except json.JSONDecodeError as exc:
                raise ValueError(
                    f"Erro de parsing JSON em '{claims_path}', linha {i}: {exc}"
                ) from exc
    return claims


def save_claims(claims_path: Path, claims: list[dict]) -> None:
    """Salva claims como JSONL ordenados por claim_id."""
    claims_path.parent.mkdir(parents=True, exist_ok=True)
    with claims_path.open("w", encoding="utf-8", newline="\n") as f:
        for claim in sorted(claims, key=lambda c: c.get("claim_id", "")):
            f.write(json.dumps(claim, ensure_ascii=False) + "\n")


def normalize_anchor_slug(text: str) -> str:
    """Normaliza o texto de um cabeçalho Markdown para um slug ASCII simples."""
    t = unicodedata.normalize("NFKD", text).encode("ASCII", "ignore").decode("ascii")
    t = t.lower().strip()
    t = re.sub(r"[^\w\s-]", "", t)
    t = re.sub(r"[\s_]+", "-", t)
    return t.strip("-")


def extract_file_anchors(canonical_file_path: Path) -> set[str]:
    """Extrai todos os anchors válidos (headings, slugs de headings e block IDs ^id) de uma nota canônica."""
    anchors = set()
    if not canonical_file_path.exists():
        return anchors

    with canonical_file_path.open(encoding="utf-8", errors="replace") as f:
        for line in f:
            line_str = line.strip()
            block_match = re.search(r"\^([a-zA-Z0-9_-]+)$", line_str)
            if block_match:
                block_id = block_match.group(1)
                anchors.add(block_id)
                anchors.add(f"^{block_id}")

            if line_str.startswith("#"):
                heading_text = line_str.lstrip("#").strip()
                if heading_text:
                    anchors.add(heading_text.lower())
                    anchors.add(normalize_anchor_slug(heading_text))

    return anchors


def validate_claim_schema(claim: dict) -> list[str]:
    """Valida o schema básico de um claim isolado."""
    errors = []

    cid = claim.get("claim_id")
    if not cid or not isinstance(cid, str):
        errors.append("campo obrigatório ausente ou inválido: claim_id")
    elif not CLAIM_ID_ASCII_RE.match(cid):
        errors.append(f"claim_id '{cid}' deve conter apenas caracteres ASCII minúsculos (a-z, 0-9, _, ., -)")

    required = [
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

    if claim.get("disposition") == "contradiction" and claim.get("validation_status") == "validated":
        errors.append("contradiction não pode ter validation_status=validated sem resolução explícita")

    if claim.get("disposition") == "promoted" and not claim.get("canonical_destination"):
        errors.append("claim com disposition=promoted deve declarar canonical_destination")

    supp_sources = claim.get("supporting_sources")
    if claim.get("disposition") == "promoted":
        if not supp_sources or not isinstance(supp_sources, list) or len(supp_sources) == 0:
            errors.append("claim promovido deve conter ao menos 1 entrada em supporting_sources")
        else:
            for idx, src in enumerate(supp_sources):
                if not isinstance(src, dict) or not src.get("source_path") or not src.get("source_blob_sha"):
                    errors.append(f"supporting_sources[{idx}] deve conter source_path e source_blob_sha")

    return errors


def validate_claims_dataset(
    vault_root: Path,
    claims: list[dict],
    ledger_map: Optional[dict[tuple[str, str], dict]] = None,
) -> list[str]:
    """Valida integridade referencial completa do dataset de claims contra o vault e o ledger."""
    errors = []
    known_claim_ids = {c.get("claim_id") for c in claims if c.get("claim_id")}

    seen_ids = set()
    for idx, claim in enumerate(claims, 1):
        cid = claim.get("claim_id")
        if cid:
            if cid in seen_ids:
                errors.append(f"Claim #{idx}: claim_id '{cid}' duplicado no dataset")
            seen_ids.add(cid)

        s_errs = validate_claim_schema(claim)
        for err in s_errs:
            errors.append(f"Claim '{cid or f'#{idx}'}': {err}")

        supp_sources = claim.get("supporting_sources") or []
        for s_idx, src in enumerate(supp_sources):
            spath = src.get("source_path")
            ssha = src.get("source_blob_sha")
            if ledger_map is not None and spath and ssha:
                if (spath, ssha) not in ledger_map:
                    errors.append(
                        f"Claim '{cid}': supporting_source[{s_idx}] (path='{spath}', sha='{ssha[:8]}') "
                        f"não foi encontrado no ledger de ingestão!"
                    )

        cdest = claim.get("canonical_destination")
        if cdest:
            dest_path = vault_root / cdest
            if not dest_path.exists():
                errors.append(f"Claim '{cid}': canonical_destination '{cdest}' não existe no disco!")
            else:
                anchor = claim.get("destination_anchor")
                if anchor:
                    valid_anchors = extract_file_anchors(dest_path)
                    anchor_norm = anchor.lower().lstrip("^").strip()
                    anchor_slug = normalize_anchor_slug(anchor)
                    if (
                        anchor not in valid_anchors
                        and anchor_norm not in valid_anchors
                        and anchor_slug not in valid_anchors
                    ):
                        errors.append(
                            f"Claim '{cid}': destination_anchor '{anchor}' não encontrado em '{cdest}'! "
                            f"(Anchors detectados: {sorted(list(valid_anchors))[:5]}...)"
                        )

        for sup_id in claim.get("supersedes") or []:
            if sup_id not in known_claim_ids:
                errors.append(f"Claim '{cid}': supersedes refere-se ao claim inexistente '{sup_id}'")

        for con_id in claim.get("contradicts") or []:
            if con_id not in known_claim_ids:
                errors.append(f"Claim '{cid}': contradicts refere-se ao claim inexistente '{con_id}'")

        dup_id = claim.get("duplicates")
        if dup_id and dup_id not in known_claim_ids:
            errors.append(f"Claim '{cid}': duplicates refere-se ao claim inexistente '{dup_id}'")

    return errors


def get_pending_validations(claims: list[dict]) -> list[dict]:
    return [c for c in claims if c.get("validation_status") == "pending_validation"]


def get_contradictions(claims: list[dict]) -> list[dict]:
    return [c for c in claims if c.get("disposition") == "contradiction"]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Valida claims canônicos e integridade referencial com o vault."
    )
    parser.add_argument("vault", type=Path, help="Pasta raiz do vault")
    parser.add_argument(
        "--claims", type=Path, default=None,
        help=f"Arquivo JSONL de claims (padrão: <vault>/{DEFAULT_CLAIMS_FILE})"
    )
    parser.add_argument(
        "--ledger", type=Path, default=None,
        help=f"Arquivo JSONL do ledger (padrão: <vault>/{DEFAULT_LEDGER_FILE})"
    )
    parser.add_argument("--verbose", "-v", action="store_true")
    args = parser.parse_args()

    vault_root = args.vault.resolve()
    if not vault_root.is_dir():
        print(f"Erro: pasta não encontrada: {vault_root}", file=sys.stderr)
        return 2

    claims_path = args.claims or (vault_root / DEFAULT_CLAIMS_FILE)
    ledger_path = args.ledger or (vault_root / DEFAULT_LEDGER_FILE)

    if not claims_path.exists():
        print(f"Arquivo de claims não encontrado: {claims_path}", file=sys.stderr)
        return 2

    claims = load_claims(claims_path)
    print(f"Claims carregados: {len(claims)}")

    from inventariar_fontes import load_ledger
    ledger_map = load_ledger(ledger_path) if ledger_path.exists() else None

    errors = validate_claims_dataset(vault_root, claims, ledger_map)

    if errors:
        print(f"\n[FAIL] {len(errors)} erro(s) de validação e integridade referencial encontrados:")
        for err in errors:
            print(f"  - {err}")
        return 1
    else:
        print("\n[OK] Todos os claims e referências são válidos e íntegros!")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
