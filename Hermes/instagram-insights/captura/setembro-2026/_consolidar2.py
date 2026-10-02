# -*- coding: utf-8 -*-
"""Consolida as capturas cruas de setembro e reporta cobertura/qualidade."""
import json, os, glob, re, sys

BASE = os.path.dirname(os.path.abspath(__file__))

inv = json.load(open(os.path.join(BASE, "_grid_inventario2.json"), encoding="utf-8"))
itens = inv["itens"]
alvo = {it["media_id"]: it for it in itens}

cap = {}  # media_id -> {"pos":, "text":, "src":}

# _raw2_01.json (formato dict com posts[])
p1 = os.path.join(BASE, "_raw2_01.json")
if os.path.exists(p1):
    d = json.load(open(p1, encoding="utf-8"))
    for post in d.get("posts", []):
        cap.setdefault(post["media_id"], {"pos": post.get("pos"), "text": post.get("text", ""), "src": "_raw2_01.json"})

# _raw2_bNN.jsonl
for f in sorted(glob.glob(os.path.join(BASE, "_raw2_b*.jsonl")) +
                glob.glob(os.path.join(BASE, "_raw2_p*.jsonl"))):
    for line in open(f, encoding="utf-8"):
        line = line.strip()
        if not line:
            continue
        try:
            o = json.loads(line)
        except Exception as e:
            print("LINHA INVALIDA em", os.path.basename(f), "->", e)
            continue
        mid = o.get("media_id")
        if not mid:
            continue
        # se já existe, mantém o mais longo
        prev = cap.get(mid)
        if prev is None or len(o.get("text", "")) > len(prev["text"]):
            cap[mid] = {"pos": o.get("pos"), "text": o.get("text", ""), "src": os.path.basename(f)}

print("=" * 70)
print("INVENTARIO setembro:", len(itens), "posts  (proprios:", inv.get("setembro_proprios"),
      "| colab:", inv.get("setembro_colab_terceiros"), ")")
print("CAPTURADOS (media_ids distintos):", len(cap))
faltando = [it for it in itens if it["media_id"] not in cap]
print("FALTANDO:", len(faltando))
for it in faltando:
    print("   pos %-4s %s  %s  %s" % (it["pos"], it["media_id"], it["data"], it["dono_grid"]))

# qualidade: texto curto / sem métrica-chave
CHAVE = ["Visualizações", "Interações", "Curtidas"]
ruins = []
for it in itens:
    mid = it["media_id"]
    if mid not in cap:
        continue
    t = cap[mid]["text"]
    if len(t) < 200 or sum(1 for k in CHAVE if k in t) < 3:
        ruins.append((it["pos"], mid, len(t), cap[mid]["src"], t.replace("\n", "|")))
print()
print("LEITURAS SUSPEITAS (curtas / sem metricas-chave):", len(ruins))
for pos, mid, n, src, t in ruins:
    print("   pos %-4s %s  len=%-5s %s" % (pos, mid, n, src))
    print("        ", t[:160])

print()
print("capturas extras (nao no inventario):",
      [m for m in cap if m not in alvo])

json.dump(cap, open(os.path.join(BASE, "_cap2_consolidado.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print("\n-> _cap2_consolidado.json gravado com", len(cap), "capturas")
