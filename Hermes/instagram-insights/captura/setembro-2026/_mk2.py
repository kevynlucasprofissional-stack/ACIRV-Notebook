# -*- coding: utf-8 -*-
"""Cria as copias *2 dos scripts da run 01-14/09 (sem tocar nos originais).

Aplica a renomeacao de artefatos (sufixo 2) e ajusta o _build_set2.py para ler
a worklist 15-30/09. Imprime apenas as linhas sensivelmente alteradas.
"""
import os, re, sys

BASE = os.path.dirname(os.path.abspath(__file__))

MAP = [
    ("_grid_inventario.json", "_grid_inventario2.json"),
    ("_worklist_set.json", "_worklist2.json"),
    ("_cap_consolidado.json", "_cap2_consolidado.json"),
    ("_pendentes.json", "_pendentes2.json"),
    ("_set_linhas.json", "_set2_linhas.json"),
    ("_cobertura_set.json", "_cobertura_set2.json"),
    ("_raw_", "_raw2_"),
    ("instagram_acirvoficial_insights_setembro_2026.xlsx",
     "instagram_acirvoficial_insights_setembro_2026_15a30.xlsx"),
]

SCRIPTS = ["_consolidar.py", "_cobertura_set.py", "_build_set.py",
           "_gerar_xlsx_set.py", "_validar_set.py"]

INV_OLD = '''def carregar_inventario():
    inv = json.load(open(os.path.join(BASE, "_grid_inventario2.json"), encoding="utf-8"))
    itens = [it for it in inv["itens"] if str(it.get("data", "")).startswith("2026-09")]
    itens.sort(key=lambda it: it["pos"])
    return itens'''

INV_NEW = '''def carregar_inventario():
    w = json.load(open(os.path.join(BASE, "_worklist2.json"), encoding="utf-8"))
    itens = w["itens"] if isinstance(w, dict) else w
    itens.sort(key=lambda it: it.get("ordem", it["pos"]))
    return itens'''

for nome in SCRIPTS:
    src = open(os.path.join(BASE, nome), encoding="utf-8").read()
    novo = src
    for a, b in MAP:
        novo = novo.replace(a, b)
    novo = novo.replace(nome.replace(".py", "") + " import", nome.replace(".py", "") + "2 import")
    destino = nome.replace(".py", "2.py")
    mudou = []
    for i, (l0, l1) in enumerate(zip(src.splitlines(), novo.splitlines()), 1):
        if l0 != l1:
            mudou.append((i, l1.strip()[:150]))
    if destino == "_build_set2.py":
        if INV_OLD not in novo:
            print("!! padrao carregar_inventario nao encontrado em", nome)
        else:
            novo = novo.replace(INV_OLD, INV_NEW)
            mudou.append(("inventario", "carregar_inventario -> _worklist2.json"))
    open(os.path.join(BASE, destino), "w", encoding="utf-8").write(novo)
    print("==", destino, "(", len(mudou), "trechos)")
    for i, t in mudou:
        print("   ", i, t)
print("ok")
