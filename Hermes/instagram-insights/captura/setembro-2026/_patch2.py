# -*- coding: utf-8 -*-
"""Ajusta os scripts *2 (XLSX de saida, janela 15-30/09, globs das capturas)."""
import os, sys

BASE = os.path.dirname(os.path.abspath(__file__))
VAULT = (r"C:\Github\ACIRV-Notebook\000-Arquivos-originais"
         r"\Dados para mega-relatório pós Sudoexpo\Redes sociais"
         r"\instagram_acirvoficial_insights_setembro_2026_15a30.xlsx")
DL = r"C:\Users\Kevyn Lucas\Downloads\instagram_acirvoficial_insights_setembro_2026_15a30.xlsx"


def edit(nome, pares):
    p = os.path.join(BASE, nome)
    t = open(p, encoding="utf-8").read()
    for old, new in pares:
        if old not in t:
            print("!! NAO ENCONTRADO em %s: %s" % (nome, old[:70]))
            sys.exit(1)
        t = t.replace(old, new, 1)
    open(p, "w", encoding="utf-8").write(t)
    print("ok", nome, len(pares), "trocas")


# ------------------------------------------------------------------ XLSX saida
edit("_gerar_xlsx_set2.py", [("SAIDA = r\"%s\"" % DL, "SAIDA = r\"%s\"" % VAULT)])
edit("_validar_set2.py", [("XLSX = r\"%s\"" % DL, "XLSX = r\"%s\"" % VAULT)])

# --------------------------------------------------- metadados da aba Controle
edit("_gerar_xlsx_set2.py", [
    ('("capturas_cruas", "_raw2_01.json + _raw2_b02..b39.jsonl (ver coluna arquivo_origem)")',
     '("capturas_cruas", "_raw2_b01..b02.jsonl + _raw2_p10..p28.jsonl (29 posts; ver coluna arquivo_origem)")'),
    ('("gerado_por", "pipeline _build_set.py + _gerar_xlsx_set.py")',
     '("gerado_por", "pipeline _build_set2.py + _gerar_xlsx_set2.py")'),
    ('("AVISO_alcance", "o painel de setembro/2026 nao expoe mais \'Alcance\'/\'Contas alcancadas\'; ha \'Visualizadores\' e, em alguns posts, \'Contas Meta alcancadas\'")',
     '("AVISO_alcance", "o painel de setembro/2026 nao expoe mais \'Alcance\'/\'Contas alcancadas\'; ha \'Visualizadores\' e, em alguns posts, \'Contas Meta alcancadas\'"),\n'
     '        ("janela_desta_planilha", "2026-09-15 a 2026-09-30 (os posts de 01-14/09 estao em instagram_acirvoficial_insights_setembro_2026.xlsx)"),\n'
     '        ("escopo_15a30", "worklist _worklist2.json; grid re-varrido em 2026-10-02 (_grid_inventario2.json, 204 itens, 2026-06-22 a 2026-10-01)")'),
])

# ------------------------------------------------------ validacao: janela 15-30
edit("_validar_set2.py", [
    ('inv = json.load(open(os.path.join(BASE, "_grid_inventario2.json"), encoding="utf-8"))\n'
     'alvo = {it["media_id"]: it for it in inv["itens"] if str(it.get("data", "")).startswith("2026-09")}\n'
     'assert len(alvo) == 86, f"inventario setembro != 86 ({len(alvo)})"',
     'w = json.load(open(os.path.join(BASE, "_worklist2.json"), encoding="utf-8"))\n'
     'alvo = {it["media_id"]: it for it in w["itens"]}\n'
     'assert len(alvo) == 29, f"worklist 15-30/09 != 29 ({len(alvo)})"'),
    ('print("Posts: linhas =", len(rows), "(esperado 86)")\nassert len(rows) == 86, "contagem divergente"',
     'print("Posts: linhas =", len(rows), "(esperado 29)")\nassert len(rows) == 29, "contagem divergente"'),
    ('assert (n_prop, n_col) == (42, 44), "quebra de escopo 42/44"',
     'assert (n_prop, n_col) == (18, 11), "quebra de escopo 18/11"'),
    ('assert ctrl.get("total_posts_no_arquivo") == 86',
     'assert ctrl.get("total_posts_no_arquivo") == 29'),
    ('print("datas fora de setembro:", foras)\nassert not foras',
     'print("datas fora de setembro:", foras)\nassert not foras\n\n'
     '# datas dentro da janela 15-30/09\n'
     'fora_janela = [(r[i["media_id"]], r[i["data_publicacao"]]) for r in rows\n'
     '               if not ("2026-09-15" <= str(r[i["data_publicacao"]]) <= "2026-09-30")]\n'
     'print("datas fora de 15-30/09:", fora_janela)\nassert not fora_janela'),
])

# --------------------------------------------------------- globs das capturas
edit("_consolidar2.py", [
    ('for f in sorted(glob.glob(os.path.join(BASE, "_raw2_b*.jsonl"))):',
     'for f in sorted(glob.glob(os.path.join(BASE, "_raw2_b*.jsonl")) +\n'
     '                glob.glob(os.path.join(BASE, "_raw2_p*.jsonl"))):'),
])
edit("_cobertura_set2.py", [
    ('for f in sorted(glob.glob(os.path.join(BASE, "_raw2_*.json*"))):',
     'for f in sorted(glob.glob(os.path.join(BASE, "_raw2_*.json*")) +\n'
     '                glob.glob(os.path.join(BASE, "_raw_*.json*"))):'),
])
print("patches aplicados")
