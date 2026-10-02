# -*- coding: utf-8 -*-
"""Valida o XLSX gerado contra o inventario de setembro."""
import json, os, openpyxl

BASE = os.path.dirname(os.path.abspath(__file__))
XLSX = r"C:\Github\ACIRV-Notebook\000-Arquivos-originais\Dados para mega-relatório pós Sudoexpo\Redes sociais\instagram_acirvoficial_insights_setembro_2026_15a30.xlsx"

w = json.load(open(os.path.join(BASE, "_worklist2.json"), encoding="utf-8"))
alvo = {it["media_id"]: it for it in w["itens"]}
assert len(alvo) == 29, f"worklist 15-30/09 != 29 ({len(alvo)})"

wb = openpyxl.load_workbook(XLSX)
print("ABAS:", wb.sheetnames)
assert wb.sheetnames == ["Posts", "Metricas_brutas", "Resumo", "Controle"], "abas divergentes"

ws = wb["Posts"]
hdr = [c.value for c in ws[1]]
rows = list(ws.iter_rows(min_row=2, values_only=True))
print("Posts: linhas =", len(rows), "(esperado 29)")
assert len(rows) == 29, "contagem divergente"

for col in ("media_id", "shortcode", "vinculo", "parceiro", "visualizacoes", "status_data",
            "data_publicacao", "tipo_midia"):
    assert col in hdr, f"coluna ausente: {col}"

i = {c: hdr.index(c) for c in ("media_id", "shortcode", "vinculo", "parceiro", "visualizacoes",
                               "interacoes", "status_data", "colaborativo", "url",
                               "data_publicacao", "tipo_midia")}
mids = [r[i["media_id"]] for r in rows]
print("media_ids unicos:", len(set(mids)))
faltando = [m for m in alvo if m not in mids]
extras = [m for m in mids if m not in alvo]
print("faltando do inventario:", faltando)
print("extras fora do inventario:", extras)
assert not faltando and not extras, "conjunto de posts divergente do inventario"

# vinculo x inventario
erros_vinculo = []
erros_parceiro = []
for r in rows:
    it = alvo[r[i["media_id"]]]
    esperado = "proprio" if it["proprio"] else "colaboracao"
    if r[i["vinculo"]] != esperado:
        erros_vinculo.append((it["media_id"], r[i["vinculo"]], esperado))
    esp_parc = "" if it["proprio"] else it["dono_grid"]
    if (r[i["parceiro"]] or "") != esp_parc:
        erros_parceiro.append((it["media_id"], r[i["parceiro"]], esp_parc))
print("vinculo divergente:", erros_vinculo)
print("parceiro divergente:", erros_parceiro)
assert not erros_vinculo and not erros_parceiro

n_prop = sum(1 for r in rows if r[i["vinculo"]] == "proprio")
n_col = sum(1 for r in rows if r[i["vinculo"]] == "colaboracao")
print("proprios:", n_prop, "| colaboracoes:", n_col)
assert (n_prop, n_col) == (18, 11), "quebra de escopo 18/11"

sem_viz = [r[i["media_id"]] for r in rows if r[i["visualizacoes"]] in (None, "")]
print("sem visualizacoes:", sem_viz)
assert not sem_viz

nao_ok = [r[i["media_id"]] for r in rows if r[i["status_data"]] != "ok"]
print("status_data != ok:", nao_ok)
assert not nao_ok

urls_ok = all(str(r[i["url"]]).startswith("https://www.instagram.com/insights/media/") for r in rows)
print("todas as urls de insights:", urls_ok)
assert urls_ok

# datas dentro de setembro
foras = [(r[i["media_id"]], r[i["data_publicacao"]]) for r in rows
         if not str(r[i["data_publicacao"]]).startswith("2026-09")]
print("datas fora de setembro:", foras)
assert not foras

# datas dentro da janela 15-30/09
fora_janela = [(r[i["media_id"]], r[i["data_publicacao"]]) for r in rows
               if not ("2026-09-15" <= str(r[i["data_publicacao"]]) <= "2026-09-30")]
print("datas fora de 15-30/09:", fora_janela)
assert not fora_janela

soma = sum(r[i["visualizacoes"]] for r in rows)
soma_inter = sum(r[i["interacoes"]] or 0 for r in rows)

ws4 = wb["Controle"]
ctrl = {r[0]: r[1] for r in ws4.iter_rows(min_row=2, values_only=True) if r[0]}
print("Controle total_posts_no_arquivo =", ctrl.get("total_posts_no_arquivo"))
print("Controle soma_visualizacoes      =", ctrl.get("soma_visualizacoes"))
print("Controle soma_interacoes         =", ctrl.get("soma_interacoes"))
print("soma calculada (Posts)           =", soma, "/", soma_inter)
assert ctrl.get("total_posts_no_arquivo") == 29
assert ctrl.get("soma_visualizacoes") == soma, "soma de visualizacoes divergente"
assert ctrl.get("soma_interacoes") == soma_inter, "soma de interacoes divergente"

ws2 = wb["Metricas_brutas"]
r2 = list(ws2.iter_rows(min_row=2, values_only=True))
mids2 = {r[0] for r in r2}
print("Metricas_brutas: linhas =", len(r2), "| media_ids distintos =", len(mids2))
assert mids2 == set(mids), "metricas brutas nao cobrem todos os posts"
assert ctrl.get("total_metricas_brutas") == len(r2)

ws3 = wb["Resumo"]
print("Resumo: linhas =", ws3.max_row)
valores = [[c.value for c in r] for r in ws3.iter_rows(min_row=2, max_row=4)]
for v in valores:
    print("   ", v)
assert valores[0][0] == "proprio" and valores[1][0] == "colaboracao" and valores[2][0] == "TOTAL"
assert valores[2][2] == soma and valores[0][2] + valores[1][2] == soma, "agregado do Resumo inconsistente"

print()
print("VALIDACAO: OK")
