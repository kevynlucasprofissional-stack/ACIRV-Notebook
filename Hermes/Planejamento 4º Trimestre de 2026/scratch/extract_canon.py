# -*- coding: utf-8 -*-
"""Extrai os blocos 'DESCRICAO CANONICA PARA O TRELLO' dos arquivos mensais canonicos.

Fonte de verdade: 01-planejamento/v2/2026-09.md e 2026-10-1.md
Saida: scratch/canon.json  (mapa post_id -> texto literal do bloco)
Nenhuma decisao editorial: copia literal do conteudo do bloco.
"""
import json
import re
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
V2 = BASE / "01-planejamento" / "v2"
OUT_DIR = Path(__file__).resolve().parent

FILES = [V2 / "2026-09.md", V2 / "2026-10-1.md"]

FENCE = chr(96) * 3
HEADER_RE = re.compile(r"^##\s+(ACIRV-SM-2026-\d{3})\b", re.M)
BLOCK_RE = re.compile(
    r"^###\s+DESCRIÇÃO CANÔNICA PARA O TRELLO\s*$\s*" + FENCE + r"(?:text)?\s*\n(.*?)\n" + FENCE,
    re.M | re.S,
)


def extract(path):
    raw = path.read_text(encoding="utf-8")
    out = {}
    headers = [(m.start(), m.group(1)) for m in HEADER_RE.finditer(raw)]
    for idx, (pos, post_id) in enumerate(headers):
        end = headers[idx + 1][0] if idx + 1 < len(headers) else len(raw)
        segment = raw[pos:end]
        m = BLOCK_RE.search(segment)
        if not m:
            out[post_id] = None
            continue
        line_no = raw[:pos].count("\n") + 1 + segment[: m.start()].count("\n")
        text = m.group(1)
        out[post_id] = {
            "texto": text,
            "chars": len(text),
            "linhas": text.count("\n") + 1,
            "arquivo": path.name,
            "linha": line_no,
        }
    return out


def main():
    canon = {}
    for f in FILES:
        if not f.exists():
            print("ERRO: fonte ausente -> " + str(f), file=sys.stderr)
            return 2
        for k, v in extract(f).items():
            if k in canon:
                print("AVISO: duplicado " + k, file=sys.stderr)
            canon[k] = v
    (OUT_DIR / "canon.json").write_text(
        json.dumps(canon, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print("%-20s %6s %6s  %-14s %s" % ("POST ID", "chars", "linhas", "arquivo", "linha"))
    print("-" * 58)
    total = 0
    for k in sorted(canon):
        v = canon[k]
        if v is None:
            print("%-20s %6s" % (k, "FALTA"))
            continue
        total += v["chars"]
        print("%-20s %6d %6d  %-14s %d" % (k, v["chars"], v["linhas"], v["arquivo"], v["linha"]))
    print("-" * 58)
    print("%d posts | %d chars" % (len(canon), total))
    return 0


if __name__ == "__main__":
    sys.exit(main())
