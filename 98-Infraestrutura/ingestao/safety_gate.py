#!/usr/bin/env python3
"""Safety gate para classificação de sensibilidade de arquivos.

Classifica arquivos ANTES da abertura, usando apenas nome/caminho/extensão.
Nunca abre o conteúdo de arquivos classificados como sensíveis.

Uso:
    python safety_gate.py <caminho>
    python safety_gate.py --batch  # lê caminhos do stdin

Retorna código de saída:
    0 = normal (seguro para leitura)
    1 = sensível (NÃO abrir)
    2 = erro de uso
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path, PurePath
from typing import NamedTuple

# ---------------------------------------------------------------------------
# Caminhos conhecidos como confirmados sensíveis (por path exato relativo ao
# vault — validados na auditoria de 2026-09-17).
# Esses dois arquivos NUNCA devem ser abertos por automação.
# ---------------------------------------------------------------------------
CONFIRMED_SENSITIVE_PATHS: frozenset[str] = frozenset([
    "000-Arquivos-originais/Contas e Senhas.md",
    "000-Arquivos-originais/Minha Chave API Antropic.md",
])

# Padrões nos tokens do nome do arquivo (lowercase)
_SECRET_TOKENS_RE = re.compile(
    r"""
    senha | password | senhas | passwords |
    token | tokens |
    api.?key | apikey | api_key |
    chave.?api | chave.?privada | private.?key |
    secret | segredo |
    credential | credencial |
    \.env |
    webhook |
    private.?key | certificate | certificado.?privado |
    seed | mnemonic |
    access.?key | access_key |
    auth.?token | bearer |
    ssh.?key | rsa |
    contas.?e.?senhas | minha.?chave
    """,
    re.VERBOSE | re.IGNORECASE,
)

_SENSITIVE_EXTENSIONS: frozenset[str] = frozenset([
    ".pem", ".p12", ".pfx", ".key", ".ppk", ".env",
    ".keystore", ".jks", ".cer", ".crt",
])


class SensitivityResult(NamedTuple):
    path: str
    sensitivity: str
    read_status: str
    reason: str


def classify(path_str: str) -> SensitivityResult:
    """Classifica um arquivo pela sensibilidade sem abrir seu conteúdo."""
    p = PurePath(path_str)
    name_lower = p.name.lower()
    stem_lower = p.stem.lower()
    suffix_lower = p.suffix.lower()

    # 1. Caminhos confirmados explicitamente
    # Normalizar para comparar independente de separador
    normalized = path_str.replace("\\", "/")
    for sensitive in CONFIRMED_SENSITIVE_PATHS:
        if normalized.endswith(sensitive) or normalized == sensitive:
            return SensitivityResult(
                path=path_str,
                sensitivity="confirmed_secret",
                read_status="sensitive_do_not_read",
                reason=f"caminho confirmado sensível na auditoria de segurança: {sensitive}",
            )

    # 2. Extensão sabidamente sensível
    if suffix_lower in _SENSITIVE_EXTENSIONS:
        return SensitivityResult(
            path=path_str,
            sensitivity="secret_suspected",
            read_status="sensitive_do_not_read",
            reason=f"extensão suspeita de credencial: {suffix_lower}",
        )

    # 3. Nome/stem contém token suspeito
    if _SECRET_TOKENS_RE.search(name_lower) or _SECRET_TOKENS_RE.search(stem_lower):
        return SensitivityResult(
            path=path_str,
            sensitivity="secret_suspected",
            read_status="sensitive_do_not_read",
            reason=f"nome do arquivo contém padrão suspeito de credencial: {p.name}",
        )

    # 4. Acessos (pode conter credenciais de sistemas)
    if "acess" in stem_lower and ("site" in stem_lower or "sistema" in stem_lower or "admin" in stem_lower):
        return SensitivityResult(
            path=path_str,
            sensitivity="secret_suspected",
            read_status="sensitive_do_not_read",
            reason=f"nome sugere credenciais de acesso: {p.name}",
        )

    # 5. Arquivo .zip ou .pdf de protótipo com padrão técnico
    if suffix_lower in (".zip", ".tar", ".gz"):
        return SensitivityResult(
            path=path_str,
            sensitivity="technical_quarantine",
            read_status="sensitive_do_not_read",
            reason="arquivo compactado — pode conter .env ou secrets; inspecionar manualmente",
        )

    # Formato não suportado para extração de texto
    _UNSUPPORTED_EXTENSIONS = frozenset([
        ".pdf", ".xlsx", ".xlsm", ".xls", ".docx", ".doc",
        ".pptx", ".ppt", ".png", ".jpg", ".jpeg", ".gif", ".svg",
        ".mp4", ".mp3", ".wav", ".avi", ".bpmn",
    ])
    if suffix_lower in _UNSUPPORTED_EXTENSIONS:
        return SensitivityResult(
            path=path_str,
            sensitivity="normal",
            read_status="unsupported",
            reason=f"formato não suportado para extração de texto: {suffix_lower}",
        )

    return SensitivityResult(
        path=path_str,
        sensitivity="normal",
        read_status="unread",
        reason="nenhum padrão suspeito detectado",
    )


def classify_batch(paths: list[str]) -> list[dict]:
    return [result._asdict() for result in (classify(p) for p in paths)]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Safety gate — classifica sensibilidade de arquivos sem abrir conteúdo."
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("path", nargs="?", help="Caminho do arquivo a classificar")
    group.add_argument(
        "--batch",
        action="store_true",
        help="Lê caminhos do stdin (um por linha) e produz JSON em stdout",
    )
    parser.add_argument("--json", action="store_true", help="Saída em JSON")
    args = parser.parse_args()

    if args.batch:
        paths = [line.strip() for line in sys.stdin if line.strip()]
        results = classify_batch(paths)
        print(json.dumps(results, ensure_ascii=False, indent=2))
        # Retorna 1 se qualquer arquivo for sensível
        return 1 if any(r["read_status"] == "sensitive_do_not_read" for r in results) else 0

    result = classify(args.path)
    if args.json:
        print(json.dumps(result._asdict(), ensure_ascii=False, indent=2))
    else:
        print(f"sensitivity : {result.sensitivity}")
        print(f"read_status : {result.read_status}")
        print(f"reason      : {result.reason}")

    return 1 if result.read_status == "sensitive_do_not_read" else 0


if __name__ == "__main__":
    raise SystemExit(main())
