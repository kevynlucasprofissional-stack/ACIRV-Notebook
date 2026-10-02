# -*- coding: utf-8 -*-
"""Conferencia final, dentro do vault restaurado."""
import json, csv, io, os, collections

V = r"C:\Github\ACIRV-Notebook"
CAP = os.path.join(V, "Hermes", "instagram-insights", "captura", "setembro-2026")
BASE = os.path.join(V, "85-Bases-e-Consultas")

print("== 1. ARTEFATOS DA ENTREGA ==")
alvos = [
    r"85-Bases-e-Consultas\Instagram-Publicacoes-2026-09.csv",
    r"85-Bases-e-Consultas\Instagram-Publicacoes-2026-09.xlsx",
    r"85-Bases-e-Consultas\LEIA-ME-Instagram-Insights.md",
    r"05-Metricas-e-Decisao\Base-Instagram-Setembro-2026.md",
    r"97-Fontes-Brutas\01-Indices\Fonte - Instagram Insights.md",
    r"Hermes\instagram-insights\README.md",
    r"Hermes\instagram-insights\captura\setembro-2026\_grid_inventario2.json",
    r"Hermes\instagram-insights\captura\setembro-2026\_setembro_2026_116.jsonl",
    r"Hermes\instagram-insights\captura\setembro-2026\_unificar_setembro.py",
]
for a in alvos:
    p = os.path.join(V, a)
    ok = os.path.exists(p)
    print(("  OK   " if ok else "  FALTA") + " " + a + (f"  ({os.path.getsize(p)} b)" if ok else ""))

print()
print("== 2. INVENTARIO x BASE x CAPTURAS ==")
def itens(p):
    d = json.load(open(p, encoding="utf-8"))
    if isinstance(d, dict):
        for k in ("itens", "items", "posts", "dados"):
            if k in d and isinstance(d[k], list):
                return d[k]
        return list(d.values())
    return d

grid = itens(os.path.join(CAP, "_grid_inventario2.json"))
set_g = [x for x in grid if str(x.get("publicado_brt", "")).startswith("2026-09")]
ids_grid = {str(x["media_id"]) for x in set_g}

rd = list(csv.reader(io.StringIO(open(os.path.join(BASE, "Instagram-Publicacoes-2026-09.csv"), encoding="utf-8").read()), delimiter=";"))
rows = [dict(zip(rd[0], r)) for r in rd[1:] if any(c.strip() for c in r)]
ids_csv = {r["media_id"] for r in rows}

recs = [json.loads(l) for l in open(os.path.join(CAP, "_setembro_2026_116.jsonl"), encoding="utf-8") if l.strip()]
ids_rec = {str(r.get("media_id")) for r in recs}

print(f"  grid total {len(grid)} | setembro no grid {len(ids_grid)}")
print(f"  base canonica: {len(rows)} linhas | {len(ids_csv)} media_id unicos | {len(rd[0])} colunas")
print(f"  capturas normalizadas: {len(recs)} registros | {len(ids_rec)} unicos")
print(f"  grid == base  -> {ids_grid == ids_csv}")
print(f"  grid == raws  -> {ids_grid == ids_rec}")
print(f"  nao capturados: {sorted(ids_grid - ids_csv)}")
print(f"  fora do grid  : {sorted(ids_csv - ids_grid)}")

print()
print("== 3. COMPLETUDE POR METRICA ==")
for c in ["visualizacoes", "visualizadores", "interacoes_raw", "curtidas_raw",
          "comentarios_raw", "compartilhamentos_raw", "salvamentos_raw",
          "contas_com_engajamento_raw", "novos_seguidores_raw",
          "atividade_do_perfil_raw", "visitas_ao_perfil_raw", "toques_em_links_externos_raw"]:
    n = sum(1 for r in rows if r.get(c, "").strip())
    print(f"  {c:34s} {n:3d}/116")

sem_core = [r["shortcode"] for r in rows if not r["visualizacoes"].strip()]
print("  sem visualizacoes:", sem_core or "nenhum")

print()
print("== 4. TOTAIS DO MES ==")
def s(c):
    t = 0
    for r in rows:
        v = r.get(c, "").strip()
        if v:
            try: t += int(float(v))
            except ValueError: pass
    return t
print(f"  visualizacoes {s('visualizacoes'):,} | interacoes {s('interacoes_raw'):,} | curtidas {s('curtidas_raw'):,}")
print(f"  comentarios {s('comentarios_raw'):,} | compartilhamentos {s('compartilhamentos_raw'):,} | salvamentos {s('salvamentos_raw'):,}")
print(f"  por vinculo: {dict(collections.Counter(r['vinculo'] for r in rows))}")
print(f"  por tipo   : {dict(collections.Counter(r['tipo_midia'] for r in rows))}")
print(f"  periodo    : {min(r['data_publicacao'] for r in rows)} .. {max(r['data_publicacao'] for r in rows)}")
