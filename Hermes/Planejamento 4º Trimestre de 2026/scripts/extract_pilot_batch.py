#!/usr/bin/env python3
"""
Extrai o lote piloto (publicação entre 2026-09-16 e 2026-10-05) diretamente dos
arquivos mensais canônicos da v2, e emite JSON estruturado.

Objetivo: eliminar transcrição manual. Nenhum dado é inferido ou inventado —
tudo vem dos arquivos canônicos, e campos ausentes ficam explicitamente vazios.

Formatos canônicos suportados (ambos existem no plano v2):
  A) 2026-09.md     -> `## ID — DATA — Título` + linhas `- **Campo:** valor`
                       (Pilar e Campanha na mesma linha, separadas por ` | `)
  B) 2026-10-*.md   -> `## ID | DATA | Título` + linha única com campos
                       separados por ` · `, usando `**Direção:**`
"""
import json
import re
import sys
from pathlib import Path
from datetime import date

BASE = Path(__file__).resolve().parents[1]
V2 = BASE / "01-planejamento" / "v2"

PILOT_START = date(2026, 9, 16)
PILOT_END = date(2026, 10, 5)

# Somente os arquivos mensais que podem conter o lote piloto.
FILES = ["2026-09.md", "2026-10-1.md"]

HEADER_RE = re.compile(
    r"^##\s+(ACIRV-SM-2026-\d{3})\s*[—|]\s*(\d{4}-\d{2}-\d{2})\s*[—|]\s*(.+?)\s*$"
)
KEY_RE = re.compile(
    r"\*\*(Entrega|Formato|Slides|Campanha|Pilar|CTA|Estrutura|"
    r"Direção visual|Direção|Extra leve|Métrica|Serviço|Prioridade):\*\*\s*"
)
LEGEND_RE = re.compile(r"^\*\*Legenda sugerida\*\*")
SEP_RE = re.compile(r"^---\s*$")


def parse_meta_lines(raw_lines):
    """Extrai campos tolerando os dois formatos, sem depender de separador."""
    found = {}
    for line in raw_lines:
        for i, m in enumerate(KEY_RE.finditer(line)):
            key = m.group(1)
            nxt = KEY_RE.search(line, m.end())
            end = nxt.start() if nxt else len(line)
            val = line[m.end():end].strip().rstrip("·|").strip()
            if key not in found and val:
                found[key] = val
    return found


def parse_file(path: Path):
    lines = path.read_text(encoding="utf-8").splitlines()
    posts, cur, mode = [], None, "meta"
    for line in lines:
        m = HEADER_RE.match(line)
        if m:
            if cur:
                posts.append(cur)
            cur = {
                "post_id": m.group(1),
                "publication_date": m.group(2),
                "title": m.group(3).strip(),
                "source_file": path.name,
                "raw_meta": [],
                "legend": [],
            }
            mode = "meta"
            continue
        if cur is None:
            continue
        if LEGEND_RE.match(line.strip()):
            mode = "legend"
            continue
        if SEP_RE.match(line.strip()):
            posts.append(cur)
            cur, mode = None, "meta"
            continue
        if mode == "legend":
            cur["legend"].append(line.rstrip())
        elif line.strip():
            cur["raw_meta"].append(line.strip())
    if cur:
        posts.append(cur)
    return posts


def build_record(post):
    meta = parse_meta_lines(post["raw_meta"])

    slides = meta.get("Slides", "")
    if not slides:
        m = re.search(r"(\d+)\s*slide", meta.get("Formato", ""))
        slides = m.group(1) if m else ""

    num = int(post["post_id"].rsplit("-", 1)[1])
    return {
        "post_id": post["post_id"],
        "publication_date": post["publication_date"],
        "title": post["title"],
        "source_file": post["source_file"],
        "delivery_date": meta.get("Entrega", ""),
        "prioridade": meta.get("Prioridade", ""),
        "formato": meta.get("Formato", ""),
        "slides": int(slides) if str(slides).isdigit() else None,
        "pilar": meta.get("Pilar", ""),
        "campanha": meta.get("Campanha", ""),
        "servico": meta.get("Serviço", ""),
        "cta": meta.get("CTA", ""),
        "estrutura": meta.get("Estrutura", ""),
        "direcao_visual": meta.get("Direção visual") or meta.get("Direção") or "",
        "metrica": meta.get("Métrica", ""),
        "extra_leve": "sim" if 45 <= num <= 60 else "não",
        "requer_2_slides": 45 <= num <= 60,
        "legend": "\n".join(post["legend"]).strip(),
    }


def main():
    all_posts = []
    for fname in FILES:
        p = V2 / fname
        if not p.exists():
            print(f"AVISO: arquivo canônico ausente: {p}", file=sys.stderr)
            continue
        all_posts.extend(parse_file(p))

    ids = [p["post_id"] for p in all_posts]
    dups = sorted({i for i in ids if ids.count(i) > 1})

    pilot = []
    for p in all_posts:
        d = date.fromisoformat(p["publication_date"])
        if PILOT_START <= d <= PILOT_END:
            pilot.append(build_record(p))

    pilot.sort(key=lambda r: (r["publication_date"], r["post_id"]))

    print(json.dumps({
        "pilot_window": {"start": PILOT_START.isoformat(), "end": PILOT_END.isoformat()},
        "source_files": FILES,
        "total_posts_scanned": len(all_posts),
        "duplicate_ids_in_scan": dups,
        "format_divergences": {
            "missing_delivery_date": [r["post_id"] for r in pilot if not r["delivery_date"]],
            "missing_slides": [r["post_id"] for r in pilot if r["slides"] is None],
            "missing_legend": [r["post_id"] for r in pilot if not r["legend"]],
        },
        "pilot_count": len(pilot),
        "posts": pilot,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
