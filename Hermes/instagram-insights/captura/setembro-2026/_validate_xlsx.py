# -*- coding: utf-8 -*-
import json, openpyxl
MASTER = r"C:\Users\Kevyn Lucas\Downloads\_acirv_agosto_progresso.json"
XLSX = r"C:\Users\Kevyn Lucas\Downloads\instagram_acirvoficial_insights_agosto_2026.xlsx"
cands = json.load(open(MASTER, encoding="utf-8"))["candidatos"]
ms = [c["shortcode"] for c in cands]

wb = openpyxl.load_workbook(XLSX)
print("ABAS:", wb.sheetnames)
assert wb.sheetnames == ["Posts","Metricas_brutas","Controle"], "abas divergentes"

ws = wb["Posts"]
hdr = [c.value for c in ws[1]]
rows = list(ws.iter_rows(min_row=2, values_only=True))
print("Posts: linhas =", len(rows), "(esperado 52)")
i_sc = hdr.index("shortcode"); i_viz = hdr.index("visualizacoes"); i_dt = hdr.index("status_data")
scs = [r[i_sc] for r in rows]
print("shortcodes unicos:", len(set(scs)))
print("faltando:", [s for s in ms if s not in scs])
print("extras:", [s for s in scs if s not in ms])
sem_viz = [r[i_sc] for r in rows if r[i_viz] in (None,"")]
print("sem visualizacoes:", sem_viz)
nao_ok = [r[i_sc] for r in rows if r[i_dt] != "ok"]
print("status_data != ok:", nao_ok)
print("soma visualizacoes:", sum(r[i_viz] for r in rows if isinstance(r[i_viz], (int,float))))

ws2 = wb["Metricas_brutas"]
r2 = list(ws2.iter_rows(min_row=2, values_only=True))
scs2 = set(r[0] for r in r2)
print("Metricas_brutas: linhas =", len(r2), "| shortcodes distintos =", len(scs2))
print("   brutas fora da lista:", [s for s in scs2 if s not in ms])

ws3 = wb["Controle"]
ctrl = {r[0]: r[1] for r in ws3.iter_rows(values_only=True) if r[0]}
print("Controle chaves:", list(ctrl.keys()))
print("   total_posts_no_arquivo =", ctrl.get("total_posts_no_arquivo"))
print("   total_metricas_brutas  =", ctrl.get("total_metricas_brutas"))
print("VALIDACAO: OK")
