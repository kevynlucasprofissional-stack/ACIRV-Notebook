# -*- coding: utf-8 -*-
"""
Unifica TODA a coleta de setembro/2026 do Instagram @acirvoficial em um unico
artefato canonico.

Entradas (mesma pasta):
  _grid_inventario2.json   -> inventario do grid (116 itens de setembro)
  _set_linhas.json         -> 86 posts normalizados (01-14/09)
  _set2_linhas.json        -> 29 posts normalizados (15-30/09)
  _raw2_p69.jsonl          -> captura avulsa do post 69 (keniasleite, 09/09)

Saidas:
  _setembro_2026_116.jsonl                                     (normalizado, unificado)
  85-Bases-e-Consultas/Instagram-Publicacoes-2026-09.csv       (base canonica do vault)

Uso: python _unificar_setembro.py
"""
import ast
import csv
import hashlib
import io
import json
import os
import re
from collections import Counter

def achar_vault(start):
    """Sobe a arvore ate encontrar a raiz do vault (a que contem 85-Bases-e-Consultas)."""
    d = os.path.abspath(start)
    while True:
        if os.path.isdir(os.path.join(d, "85-Bases-e-Consultas")):
            return d
        pai = os.path.dirname(d)
        if pai == d:
            raise SystemExit("raiz do vault nao encontrada a partir de " + start)
        d = pai


BASE = os.path.dirname(os.path.abspath(__file__))
VAULT = achar_vault(BASE)
CSV_OUT = os.path.join(VAULT, "85-Bases-e-Consultas", "Instagram-Publicacoes-2026-09.csv")

PERIODO = "2026-09"

# ordem canonica das colunas (identica a Instagram-Publicacoes-2026-08-09.csv)
HEADER = [
    "periodo_fonte", "data_publicacao", "hora_publicacao", "shortcode", "media_id",
    "tipo_midia", "vinculo", "parceiro_coautores", "promovido", "url",
    "visualizacoes", "visualizadores", "contas_meta_alcancadas",
    "interacoes_raw", "interacoes_posts_raw", "interacoes_reels_raw",
    "curtidas_raw", "comentarios_raw", "compartilhamentos_raw", "salvamentos_raw",
    "contas_com_engajamento_raw", "novos_seguidores_raw", "novos_seguidores_normalizado",
    "atividade_do_perfil_raw", "visitas_ao_perfil_raw", "toques_em_links_externos_raw",
    "pct_seguidores_alcance_raw", "pct_nao_seguidores_alcance_raw", "taxa_interacao_pct_raw",
    "metricas_ausentes", "notas", "source_path", "source_blob_sha", "status_validacao",
]


def lit(v, default):
    """Os JSONs intermediarios guardam dicts/listas como repr de Python (string)."""
    if isinstance(v, (dict, list)):
        return v
    if isinstance(v, str) and v.strip():
        try:
            return ast.literal_eval(v)
        except Exception:
            return default
    return default


def num(v):
    if isinstance(v, bool):
        return None
    if isinstance(v, (int, float)):
        return v
    if isinstance(v, str) and re.fullmatch(r"-?\d+", v.strip()):
        return int(v.strip())
    return None


def txt(v):
    n = num(v)
    return "" if n is None else str(n)


def git_blob_sha(raw):
    return hashlib.sha1(b"blob %d\0" % len(raw) + raw).hexdigest()


# ---------------------------------------------------------------- inventario
inv = json.load(open(os.path.join(BASE, "_grid_inventario2.json"), encoding="utf-8"))
itens = inv["itens"]
sep = [it for it in itens if it["data"].startswith(PERIODO)]
alvo = {it["media_id"]: it for it in sep}

# ---------------------------------------------------------------- normalizados
linhas = []
for arq in ("_set_linhas.json", "_set2_linhas.json"):
    for r in json.load(open(os.path.join(BASE, arq), encoding="utf-8")):
        r["_arq_linhas"] = arq
        linhas.append(r)

por_mid = {r["media_id"]: r for r in linhas}

# ------------------------------------------------- post 69 (captura avulsa)
p69_path = os.path.join(BASE, "_raw2_p69.jsonl")
p69 = None
if os.path.exists(p69_path):
    p69 = json.loads(open(p69_path, encoding="utf-8").read().strip().splitlines()[0])

registros = []
faltando = []
for it in sep:
    mid = it["media_id"]
    r = por_mid.get(mid)
    if r is None and p69 and p69["media_id"] == mid:
        # painel de insights degradado: metricas preenchidas a mao, uma a uma,
        # a partir do texto bruto; nada e inferido.
        metricas = {
            "curtidas": 210,
            "comentarios": 28,
            "salvamentos": 2,
            "compartilhamentos": 0,
            "interacoes_reels": 0,
        }
        ausentes = ["visualizacoes", "visualizadores", "interacoes",
                    "contas_com_engajamento", "contas_meta_alcancadas",
                    "atividade_do_perfil", "novos_seguidores"]
        r = {
            "media_id": mid,
            "shortcode": p69["shortcode"],
            "url": p69["url"],
            "data_publicacao": p69["publicado_brt"][:10],
            "hora_publicacao": p69["publicado_brt"][11:19],
            "tipo_midia": p69["tipo"],
            "vinculo": "colaboracao",
            "coautores": str(p69["coautores"]),
            "dono_grid": p69["autor_login"],
            "promovido": "False",
            "metricas": metricas,
            "metricas_ausentes": ausentes,
            "notas": ("insights_da_acirv_nao_expoem_metricas_deste_reel_colaborativo_"
                      "placeholder_--; api_publica_play_count=2970_curtidas=210_comentarios=28; "
                      "rodape_numerico_4_descartado_como_ruido_de_interface"),
            "insights_raw": p69["text"],
            "arquivo_origem": "_raw2_p69.jsonl",
            "coletado_em": p69["coletado_em"],
            "status_data": "ok",
        }
        r["_arq_linhas"] = "_raw2_p69.jsonl"
    if r is None:
        faltando.append(mid)
        continue
    registros.append((it, r))

if faltando:
    raise SystemExit("ABORTADO: %d posts de setembro sem captura: %s" % (len(faltando), faltando))

# ---------------------------------------------------------------- ordenacao
registros.sort(key=lambda t: (t[0]["data"], t[0]["media_id"]))
print("posts de setembro unificados:", len(registros), "| inventario:", len(sep))

# ---------------------------------------------------------------- linhas canonicas
out_rows = []
normalizado = []
for it, r in registros:
    m = lit(r.get("metricas"), {})
    ausentes = [str(a) for a in lit(r.get("metricas_ausentes"), [])]
    notas = str(r.get("notas") or "")
    raw_file = r.get("arquivo_origem") or r.get("_arq_linhas")
    raw_path = "Hermes/instagram-insights/captura/setembro-2026/" + str(raw_file)
    raw_abs = os.path.join(BASE, raw_file)
    sha = git_blob_sha(open(raw_abs, "rb").read()) if os.path.exists(raw_abs) else ""

    inter = num(m.get("interacoes"))
    views = num(m.get("visualizacoes"))
    taxa = "%.2f" % (inter / views * 100) if inter and views else ""

    proprio = it.get("proprio") is True or it.get("dono_grid") == "acirvoficial"
    vinculo = "proprio" if proprio else "colaboracao"
    parceiro = "" if proprio else str(it.get("dono_grid") or "")

    if "dados de anúncios" in str(r.get("insights_raw", "")).lower():
        promovido = "sim"
    else:
        promovido = "nao_informado"

    status = "completo_2026-09_insights_dom"
    if r.get("_arq_linhas") == "_raw2_p69.jsonl":
        status = "colab_metricas_principais_indisponiveis_no_painel"

    def g(k):
        return txt(m.get(k))

    out_rows.append([
        PERIODO,
        r.get("data_publicacao") or it["data"],
        r.get("hora_publicacao") or "",
        it["sc"],
        it["media_id"],
        r.get("tipo_midia") or it["tipo_grid"],
        vinculo,
        parceiro,
        promovido,
        r.get("url") or "https://www.instagram.com/insights/media/%s/" % it["media_id"],
        g("visualizacoes"),
        g("visualizadores"),
        g("contas_meta_alcancadas"),
        g("interacoes"),
        g("interacoes_posts"),
        g("interacoes_reels"),
        g("curtidas"),
        g("comentarios"),
        g("compartilhamentos"),
        g("salvamentos"),
        g("contas_com_engajamento"),
        g("novos_seguidores"),
        g("novos_seguidores"),
        g("atividade_do_perfil"),
        g("visitas_ao_perfil"),
        g("toques_em_links_externos"),
        str(m.get("pct_seguidores_alcance") or ""),
        str(m.get("pct_nao_seguidores_alcance") or ""),
        taxa,
        ";".join(ausentes),
        notas,
        raw_path,
        sha,
        status,
    ])

    normalizado.append({
        "media_id": it["media_id"],
        "shortcode": it["sc"],
        "pos_grid": it["pos"],
        "publicado_brt": it["publicado_brt"],
        "tipo_midia": r.get("tipo_midia") or it["tipo_grid"],
        "vinculo": vinculo,
        "parceiro": parceiro,
        "promovido": promovido,
        "metricas": m,
        "metricas_ausentes": ausentes,
        "notas": notas,
        "insights_raw": r.get("insights_raw", ""),
        "arquivo_origem": raw_file,
        "coletado_em": r.get("coletado_em"),
        "status_validacao": status,
    })

# ---------------------------------------------------------------- gravacao
with open(os.path.join(BASE, "_setembro_2026_116.jsonl"), "w", encoding="utf-8") as fh:
    for n in normalizado:
        fh.write(json.dumps(n, ensure_ascii=False) + "\n")

buf = io.StringIO()
w = csv.writer(buf, delimiter=";", lineterminator="\r\n")
w.writerow(HEADER)
w.writerows(out_rows)
data = buf.getvalue()
os.makedirs(os.path.dirname(CSV_OUT), exist_ok=True)
with open(CSV_OUT, "w", encoding="utf-8", newline="") as fh:
    fh.write(data)

# ---------------------------------------------------------------- QA
tot = Counter()
vistos = 0
sem_views = []
for it, r in registros:
    m = lit(r.get("metricas"), {})
    if num(m.get("visualizacoes")):
        vistos += num(m["visualizacoes"])
    else:
        sem_views.append(it["media_id"])
print("csv canonico:", CSV_OUT)
print("linhas de dados:", len(out_rows), "| colunas:", len(HEADER))
print("por vinculo:", dict(Counter(x[6] for x in out_rows)))
print("por tipo:", dict(Counter(x[5] for x in out_rows)))
print("soma visualizacoes:", vistos)
print("sem visualizacoes:", len(sem_views), sem_views)
print("dias:", len(set(x[1] for x in out_rows)), "| janela:", min(x[1] for x in out_rows), "..", max(x[1] for x in out_rows))
print("ausencias por metrica:", dict(Counter(a for it, r in registros for a in lit(r.get("metricas_ausentes"), []))))
