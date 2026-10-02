# -*- coding: utf-8 -*-
"""Pipeline SETEMBRO/2026 — consolida capturas cruas e gera o XLSX.

Fontes:
  _grid_inventario2.json   -> metadados dos 86 posts de setembro (sc, media_id, data/hora, dono, tipo)
  _raw2_*.json / .jsonl    -> texto bruto do painel de insights por media_id

Saida:
  _set2_linhas.json        -> normalizado por post (auditoria)
  instagram_acirvoficial_insights_setembro_2026_15a30.xlsx
"""
import json, os, re, glob, datetime, sys

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)
from _insights_builder import parse, normalize, NORM   # noqa: E402

OUT_XLSX = r"C:\Users\Kevyn Lucas\Downloads\instagram_acirvoficial_insights_setembro_2026_15a30.xlsx"

# ---------------------------------------------------------------- capturas
def carregar_capturas():
    cap = {}
    for f in sorted(glob.glob(os.path.join(BASE, "_raw2_*.json")) +
                    glob.glob(os.path.join(BASE, "_raw2_*.jsonl"))):
        nome = os.path.basename(f)
        if nome == "_cap2_consolidado.json":
            continue
        mt = datetime.datetime.fromtimestamp(os.path.getmtime(f)).astimezone().isoformat(timespec="seconds")
        try:
            txt = open(f, encoding="utf-8").read().strip()
            if not txt:
                continue
            if f.endswith(".jsonl"):
                objs = [json.loads(l) for l in txt.splitlines() if l.strip()]
            else:
                o = json.loads(txt)
                objs = o["posts"] if isinstance(o, dict) and "posts" in o else [o]
        except Exception as e:
            print("  ! falha ao ler", nome, e)
            continue
        for o in objs:
            mid = str(o.get("media_id") or "")
            if not mid:
                continue
            ant = cap.get(mid)
            # fica com a captura mais longa (releitura completa vence a colapsada)
            if ant is None or len(o.get("text", "")) > len(ant["text"]):
                cap[mid] = {"media_id": mid, "pos": o.get("pos"), "url": o.get("url"),
                            "text": o.get("text", ""), "src": nome, "coletado_em": mt}
    return cap

# ---------------------------------------------------------------- metadados
def carregar_inventario():
    w = json.load(open(os.path.join(BASE, "_worklist2.json"), encoding="utf-8"))
    itens = w["itens"] if isinstance(w, dict) else w
    itens.sort(key=lambda it: it.get("ordem", it["pos"]))
    return itens

# ---------------------------------------------------------------- parsing
PCT_PAIR = re.compile(r"Seguidores\n([\d.,]+%)\nNão seguidores\n([\d.,]+%)")
HEAD_CURTIDAS = re.compile(r"^Curtidas\n(\d+)\n")
HEAD_DUPLO = re.compile(r"^(\d+)\n(\d+)\n")

NUMERICAS = {"visualizacoes", "visualizadores", "alcance", "contas_alcancadas",
             "contas_meta_alcancadas", "interacoes", "interacoes_posts", "interacoes_reels",
             "curtidas", "comentarios", "compartilhamentos", "salvamentos",
             "contas_com_engajamento", "novos_seguidores", "na_pagina_inicial", "no_perfil",
             "de_outra_pessoa", "atividade_do_perfil", "visitas_ao_perfil",
             "toques_em_links_externos", "toques_no_endereco_comercial"}


PLACEHOLDERS = {"--", "9+", "", "-", "—"}


def parse_set(text, tipo):
    """Normaliza uma captura do painel de insights (setembro).

    A cauda "Facebook" repete os rotulos Visualizacoes/Comentarios com os numeros
    do Facebook e sobrescrevia os valores reais do Instagram -> corta antes dela.
    """
    corpo = text.split("\nFacebook\n")[0]
    rows = parse(corpo.split("\n"))
    m, ausentes, bruta = normalize(rows)

    notas = []
    # 1) cabecalho: "Curtidas\nN" no topo carrega o TOTAL DE COMENTARIOS, nao curtidas
    h = HEAD_CURTIDAS.match(text)
    if h:
        notas.append("cabecalho_traz_comentarios=%s" % h.group(1))
    d = HEAD_DUPLO.match(text)
    if d:
        notas.append("cabecalho_curtidas_comentarios=%s/%s" % (d.group(1), d.group(2)))

    # 2) valores placeholder ou percentuais nao sao metricas inteiras -> separa
    for k in list(m):
        v = m[k]
        if isinstance(v, str) and ("%" in v or v.strip() in PLACEHOLDERS):
            notas.append("rotulo_sem_valor_numerico:%s=%s" % (k, v))
            m.pop(k)
            if k not in ausentes:
                ausentes.append(k)

    # 3) pares Seguidores/Nao seguidores em %
    pares = PCT_PAIR.findall(text)
    if len(pares) >= 1:
        m["pct_seguidores_alcance"] = pares[0][0]
        m["pct_nao_seguidores_alcance"] = pares[0][1]
    if len(pares) >= 2:
        m["pct_seguidores_interacoes"] = pares[1][0]
        m["pct_nao_seguidores_interacoes"] = pares[1][1]

    # 4) se nao houver 'Curtidas' rotulado no corpo, o cabecalho contaminaria o campo
    if "curtidas" not in m and h:
        notas.append("SEM_curtidas_rotulado")

    # 5) limpa a lista de ausentes: so rotulos de metrica reais
    validos = set(NORM.values())
    ausentes = sorted({a for a in ausentes if a in validos})
    return m, ausentes, bruta, notas


# ---------------------------------------------------------------- montagem
def main():
    itens = carregar_inventario()
    cap = carregar_capturas()
    print("inventario setembro:", len(itens), "| capturas distintas:", len(cap))

    faltando = [it["media_id"] for it in itens if it["media_id"] not in cap]
    print("sem captura:", len(faltando), faltando)
    if faltando:
        raise SystemExit("ABORTADO: ainda faltam capturas")

    linhas = []
    for it in itens:
        c = cap[it["media_id"]]
        m, ausentes, bruta, notas = parse_set(c["text"], it["tipo_grid"])
        dp, hp = "", ""
        if it.get("publicado_brt"):
            p = str(it["publicado_brt"]).split(" ")
            dp, hp = p[0], (p[1] if len(p) > 1 else "")
        proprio = bool(it["proprio"])
        linhas.append({
            "media_id": it["media_id"], "shortcode": it["sc"], "url": c["url"],
            "data_publicacao": dp, "hora_publicacao": hp, "tipo_midia": it["tipo_grid"],
            "vinculo": "proprio" if proprio else "colaboracao",
            "parceiro": "" if proprio else it["dono_grid"],
            "colaborativo": not proprio, "coautores": [] if proprio else [it["dono_grid"]],
            "dono_grid": it["dono_grid"], "promovido": "dados de anúncios" in c["text"].lower(),
            "metricas": m, "metricas_ausentes": ausentes,
            "metricas_brutas": bruta,
            "notas": "; ".join(notas), "insights_raw": c["text"],
            "arquivo_origem": c["src"], "coletado_em": c["coletado_em"],
            "status_data": "ok" if dp else "NAO_CONFIRMADA",
        })

    json.dump(linhas, open(os.path.join(BASE, "_set2_linhas.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)

    # ---- diagnostico
    sem_curt = [l["media_id"] for l in linhas if "curtidas" not in l["metricas"]]
    print("posts sem 'curtidas' rotulado:", len(sem_curt), sem_curt[:6])
    tot = sum(l["metricas"].get("visualizacoes", 0) or 0 for l in linhas)
    print("soma visualizacoes:", tot)
    print("-> _set2_linhas.json gravado com", len(linhas), "posts")
    return linhas


if __name__ == "__main__":
    main()
