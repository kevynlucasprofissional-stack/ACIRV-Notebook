# -*- coding: utf-8 -*-
"""Cobertura restrita a SETEMBRO/2026."""
import json, os, glob

BASE = os.path.dirname(os.path.abspath(__file__))
inv = json.load(open(os.path.join(BASE, "_grid_inventario2.json"), encoding="utf-8"))
itens = inv["itens"]

setembro = [it for it in itens if str(it.get("data", "")).startswith("2026-09")]
outros = [it for it in itens if not str(it.get("data", "")).startswith("2026-09")]
print("itens no grid:", len(itens), "| setembro:", len(setembro), "| fora de setembro:", len(outros))
print("proprios(set):", sum(1 for it in setembro if it["proprio"]),
      "| colab(set):", sum(1 for it in setembro if not it["proprio"]))
print("datas fora de setembro:", sorted({it["data"] for it in outros}))
print("range setembro:", min(it["data"] for it in setembro), "->", max(it["data"] for it in setembro))

cap = json.load(open(os.path.join(BASE, "_cap2_consolidado.json"), encoding="utf-8"))
faltando = [it for it in setembro if it["media_id"] not in cap]
print("\nsetembro capturados:", len(setembro) - len(faltando), "/", len(setembro))
print("FALTANDO em setembro:", len(faltando))
for it in faltando:
    print("   pos %-4s %s  %s  %s  %s" % (it["pos"], it["media_id"], it["data"], it["dono_grid"], it["sc"]))

# confere se algum desses está em algum arquivo cru com texto
todos = {}
for f in sorted(glob.glob(os.path.join(BASE, "_raw2_*.json*")) +
                glob.glob(os.path.join(BASE, "_raw_*.json*"))):
    if f.endswith("_cap2_consolidado.json"):
        continue
    txt = open(f, encoding="utf-8").read()
    for it in faltando:
        if it["media_id"] in txt:
            todos.setdefault(it["media_id"], []).append(os.path.basename(f))
print("\nmedia_ids 'faltando' citados em arquivos crus:", json.dumps(todos, indent=1, ensure_ascii=False))

json.dump([it["media_id"] for it in faltando],
          open(os.path.join(BASE, "_pendentes2.json"), "w", encoding="utf-8"), indent=1)
print("-> _pendentes2.json com", len(faltando), "media_ids")
