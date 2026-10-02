# -*- coding: utf-8 -*-
"""QA e numeros de apoio para a nota canonica de setembro/2026."""
import csv, io, os, collections

BASE = os.path.dirname(os.path.abspath(__file__))
_d = BASE
while not os.path.isdir(os.path.join(_d, "85-Bases-e-Consultas")):
    _d = os.path.dirname(_d)
CSV = os.path.join(_d, "85-Bases-e-Consultas", "Instagram-Publicacoes-2026-09.csv")

rd = list(csv.reader(io.StringIO(open(CSV, encoding="utf-8").read()), delimiter=";"))
h = rd[0]
i = {k: n for n, k in enumerate(h)}
rows = rd[1:]


def n(v):
    v = (v or "").replace(".", "").replace(",", ".").strip()
    try:
        return float(v)
    except ValueError:
        return None


def col(r, k):
    return r[i[k]]


print("TOP 3 por visualizacoes:")
for r in sorted(rows, key=lambda r: -(n(col(r, "visualizacoes")) or -1))[:3]:
    print("  %s %-5s views=%-7s int=%-6s curt=%-6s parceiro=%s" % (
        col(r, "data_publicacao"), col(r, "tipo_midia"), col(r, "visualizacoes"),
        col(r, "interacoes_raw"), col(r, "curtidas_raw"),
        col(r, "parceiro_coautores") or col(r, "vinculo")))

print("\nPor decada:")
for a, b in [("2026-09-01", "2026-09-10"), ("2026-09-11", "2026-09-20"), ("2026-09-21", "2026-09-30")]:
    sel = [r for r in rows if a <= col(r, "data_publicacao") <= b]
    print("  %s a %s: %2d posts | views=%8d | int=%6d" % (
        a[8:], b[8:], len(sel),
        sum(n(col(r, "visualizacoes")) or 0 for r in sel),
        sum(n(col(r, "interacoes_raw")) or 0 for r in sel)))

print("\nParceiros por visualizacoes:")
agg = collections.Counter()
for r in rows:
    p = col(r, "parceiro_coautores")
    if p:
        agg[p] += n(col(r, "visualizacoes")) or 0
for p, v in agg.most_common(6):
    print("  %-24s %8d" % (p, v))

print("\nSem curtidas:", [col(r, "media_id") for r in rows if not col(r, "curtidas_raw")])
print("Status:", dict(collections.Counter(col(r, "status_validacao") for r in rows)))
med = sorted(n(col(r, "visualizacoes")) for r in rows if n(col(r, "visualizacoes")))
print("Mediana views:", med[len(med) // 2])
rr = [r for r in rows if col(r, "tipo_midia") == "reel"]
pp = [r for r in rows if col(r, "tipo_midia") != "reel"]
print("reels: %d | views=%d | int=%d" % (len(rr),
      sum(n(col(r, "visualizacoes")) or 0 for r in rr), sum(n(col(r, "interacoes_raw")) or 0 for r in rr)))
print("nao-reels: %d | views=%d | int=%d" % (len(pp),
      sum(n(col(r, "visualizacoes")) or 0 for r in pp), sum(n(col(r, "interacoes_raw")) or 0 for r in pp)))
