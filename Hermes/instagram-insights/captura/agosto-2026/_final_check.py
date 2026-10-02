import json, glob, os
from openpyxl import load_workbook

DL = r"C:\Users\Kevyn Lucas\Downloads"
XLSX = os.path.join(DL, "instagram_acirvoficial_insights_agosto_2026.xlsx")
D = os.path.join(DL, "_acirv_agosto")

files = [p for p in sorted(glob.glob(os.path.join(D, "*.json"))) if not os.path.basename(p).startswith("_")]
master = {}
for p in files:
    j = json.load(open(p, encoding="utf-8"))
    master[j["shortcode"]] = {
        "data": j.get("data_publicacao"),
        "viz": j["melhores_metricas"].get("visualizacoes"),
        "status": j.get("status_insights"),
        "promovido": "dados de anúncios" in (j.get("insights_raw") or ""),
    }

print("JSONs no disco:", len(files))
fora = {s: v["data"] for s, v in master.items() if not (v["data"] and "2026-08-01" <= v["data"] <= "2026-08-31")}
semviz = [s for s, v in master.items() if v["viz"] in (None, "")]
print("fora do periodo:", fora or "nenhum", "| sem visualizacoes:", semviz or "nenhum")
print("promovidos (banner de anuncio):", sum(1 for v in master.values() if v["promovido"]))

wb = load_workbook(XLSX)
print("\nXLSX abas:", wb.sheetnames)
for ws in wb.worksheets:
    print("   %-18s %4d linhas x %d colunas" % (ws.title, ws.max_row - 1, ws.max_column))
hdr = [c.value for c in wb["Posts"][1]]
print("colunas Posts:", hdr)
ci = hdr.index("shortcode")
sc_posts = [r[ci] for r in wb["Posts"].iter_rows(min_row=2, values_only=True) if r and r[ci]]
print("aba Posts: linhas =", len(sc_posts), "| shortcodes unicos =", len(set(sc_posts)))
print("faltando no XLSX:", sorted(set(master) - set(sc_posts)) or "nenhum")
print("extras no XLSX:", sorted(set(sc_posts) - set(master)) or "nenhum")

rep = {
    "varredura_grid_acirvoficial": {
        "executada_em": "2026-09-14",
        "fonte": "grid do perfil @acirvoficial (browser autenticado), scroll ate o fim p/ disparar infinite scroll",
        "itens_grid_enumerados": 167,
        "master_no_grid": 52,
        "master_fora_do_grid": 0,
        "itens_fora_do_master": 115,
        "nao_master_com_data_dentro_de_agosto": [
            {"shortcode": "DcmMX4pvjg7", "autor": "raphael_valongo", "data": "2026-08-28",
             "nota": "sem botao 'Ver insights' => nao e post do acirvoficial"},
            {"shortcode": "Dchm6kFDjxS", "autor": "aplausoaudiovisual", "data": "2026-08-26 (alt)",
             "nota": "URL redireciona p/ /aplausoaudiovisual/; sem 'Ver insights'"},
            {"shortcode": "DchK9ycv_Tu", "autor": "raphael_valongo", "data": "~2026-08-26/27",
             "nota": "autor por og:description"},
            {"shortcode": "DcdwpbfPsgs", "autor": "raphael_valongo", "data": "~2026-08-24/26",
             "nota": "autor por og:description"},
            {"shortcode": "DcbmO6GPfhb", "autor": "raphael_valongo", "data": "2026-08-24",
             "nota": "autor por og:description"},
        ],
        "fronteira_do_periodo": {
            "master_mais_recente": {"shortcode": "DcrgQC6gknC", "data": "2026-08-30"},
            "master_mais_antigo": {"shortcode": "Dbd6DYGA0y3", "data": "2026-08-01"},
            "item_nao_master_mais_antigo_no_grid": {"shortcode": "Dcrgb9wP9LW", "autor": "raphael_valongo",
                                                   "datetime": "2026-08-30T21:45:52Z"},
            "item_acirvoficial_nao_master_imediatamente_acima": {"shortcode": "DcbD8kGAZY3",
                                                                 "data_exibida": "1 de setembro", "tem_ver_insights": True},
        },
        "candidatos_de_setembro_antes_tratados_como_faltantes": {
            "DclVoHkAc3R": "2026-09-08 (time datetime do DOM)",
            "DcbEPp2gwNj": "~2026-09-08 ('ha 6 dias')",
            "DcbD8kGAZY3": "2026-09-01 ('1 de setembro')",
            "DcbEHlnA9uZ": "entre 01 e 08/set (posicao no grid)",
            "DclVejgguEv": "entre 01 e 08/set (posicao no grid)",
            "DcbECTUAleR": "entre 01 e 08/set (posicao no grid)",
            "DclVRnSg4Sm": "entre 01 e 08/set (posicao no grid)",
        },
        "causa_do_falso_positivo": ("og:description do post devolve a data de UPLOAD/agendamento, nao a de publicacao "
                                    "(lote criado 23-28/ago, publicado 01-08/set)"),
        "metodo_valido_para_data": "elemento <time datetime> do DOM do post; o grid appenda itens apenas ao atingir o fim da pagina",
        "conclusao": ("Master de 52 posts validado como COMPLETO para agosto/2026. Nenhuma coleta adicional necessaria; "
                      "XLSX permanece valido."),
    }
}
out = os.path.join(DL, "_acirv_agosto_sweep_report.json")
with open(out, "w", encoding="utf-8") as f:
    json.dump(rep, f, ensure_ascii=False, indent=1)
print("\nrelatorio salvo:", out)
print("conclusao:", rep["varredura_grid_acirvoficial"]["conclusao"])
