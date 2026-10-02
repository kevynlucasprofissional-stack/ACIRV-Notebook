"""Constroi o inventario do grid a partir do sweep de 2026-10-02 e funde com o
inventario anterior (01-14/09, capturado em 14/09), gerando a worklist de captura.

Entradas : _grid_sweep_20261002.txt (novo sweep)  +  _grid_inventario.json (run anterior)
Saidas   : _grid_inventario_v2.json  (merged, ordenado por data desc)
           _worklist_v2.json         (itens de 2026-09-15 ate agora, alvo da captura)
"""
import datetime
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
A = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_"
EPOCH = 1314220021721
BRT = datetime.timezone(datetime.timedelta(hours=-3))


def sc_to_id(tok):
    """shortcode (11 chars) -> media_id numerico."""
    n = 0
    for ch in tok:
        d = A.find(ch)
        if d < 0:
            raise ValueError("char fora do alfabeto: %r em %r" % (ch, tok))
        n = n * 64 + d
    return n


def id_to_dt(media_id):
    return datetime.datetime.fromtimestamp(((media_id >> 23) + EPOCH) / 1000, BRT)


def parse_sweep(path):
    out = []
    for line in open(path, encoding="utf-8"):
        line = line.strip()
        if not line:
            continue
        pos, tok, owner, kind, pin = line.split(",")
        out.append({"pos_sweep": int(pos), "tok": tok, "dono_grid": owner,
                    "tipo_grid": kind, "pin": int(pin)})
    return out


def main():
    sweep = parse_sweep(os.path.join(HERE, "_grid_sweep_20261002.txt"))
    # resolve tokens: 11 chars = shortcode; mais longo = id "largo" (usa os 11 primeiros
    # como shortcode canonico, guardando o token original)
    for it in sweep:
        it["sc"] = it["tok"][:11]
        it["tok_longo"] = len(it["tok"]) > 11
    for it in sweep:
        try:
            it["media_id"] = str(sc_to_id(it["sc"]))
            it["dt"] = id_to_dt(int(it["media_id"]))
        except Exception as e:  # noqa
            it["media_id"] = None
            it["dt"] = None
            print("ERRO token", it["tok"], e)

    ok = [x for x in sweep if x["dt"]]
    print("sweep: %d itens, %d com data" % (len(sweep), len(ok)))
    print("janela sweep: %s .. %s" % (min(x["dt"] for x in ok).strftime("%Y-%m-%d"),
                                     max(x["dt"] for x in ok).strftime("%Y-%m-%d")))
    # token longo: confere posicao na vizinhanca
    for it in sweep:
        if it["tok_longo"]:
            prevs = [x["dt"] for x in ok if x["pos_sweep"] < it["pos_sweep"]][-2:]
            nxts = [x["dt"] for x in ok if x["pos_sweep"] > it["pos_sweep"]][:2]
            print("TOKEN LONGO", it["tok"], "->", it["dt"], "| vizinhos:",
                  [d.strftime("%m-%d %H:%M") for d in prevs],
                  [d.strftime("%m-%d %H:%M") for d in nxts])

    # ---- merge com inventario anterior (01-14/09) ----
    old = json.load(open(os.path.join(HERE, "_grid_inventario.json"), encoding="utf-8"))
    old_items = old["itens"] if isinstance(old, dict) else old
    print("inventario anterior: %d itens (%s .. %s)" % (
        len(old_items), min(x["data"] for x in old_items), max(x["data"] for x in old_items)))
    print("chaves antigas:", sorted(old_items[0].keys()))
    known = {x["sc"] for x in old_items}

    novos = [x for x in sweep if x["sc"] not in known]
    print("sweep sem sobreposicao: %d  |  sobrepostos: %d" % (
        len(novos), len(sweep) - len(novos)))

    # validacao de sobreposicao: itens presentes nos dois devem ter mesma data/dono
    diff = 0
    for x in sweep:
        if x["sc"] in known:
            o = [y for y in old_items if y["sc"] == x["sc"]][0]
            if o["data"][:10] != x["dt"].strftime("%Y-%m-%d") or o["dono_grid"] != x["dono_grid"]:
                diff += 1
                if diff <= 6:
                    print("  DIVERGENCIA", x["sc"], o["data"], x["dt"], o["dono_grid"], x["dono_grid"])
    print("divergencias na sobreposicao:", diff)

    # ---- registro de capturas existentes ----
    cap_dir = os.path.join(HERE, "_capturas")
    caps = {}
    if os.path.isdir(cap_dir):
        for f in os.listdir(cap_dir):
            if f.endswith(".json") and f.startswith("m_"):
                try:
                    d = json.load(open(os.path.join(cap_dir, f), encoding="utf-8"))
                    caps[str(d.get("media_id"))] = f
                except Exception:
                    pass
    print("capturas ja existentes:", len(caps))

    merged = []
    for x in sweep:
        if x["dt"] and x["dt"].strftime("%Y-%m") in ("2026-09", "2026-10"):
            merged.append({
                "pos": x["pos_sweep"], "sc": x["sc"], "media_id": x["media_id"],
                "dono_grid": x["dono_grid"], "tipo_grid": x["tipo_grid"],
                "data": x["dt"].strftime("%Y-%m-%d %H:%M:%S"),
                "publicado_brt": x["dt"].strftime("%Y-%m-%d %H:%M:%S -03:00"),
                "origem": "sweep_20261002",
                "tok_original": x["tok"] if x["tok_longo"] else None,
            })
    for o in old_items:
        if o["sc"] in {m["sc"] for m in merged}:
            continue
        merged.append(o)
    merged.sort(key=lambda z: z["data"], reverse=True)
    for i, m in enumerate(merged):
        m["pos_ordem"] = i
    json.dump({"gerado": "2026-10-02", "total": len(merged), "itens": merged},
              open(os.path.join(HERE, "_grid_inventario_v2.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print("merged: %d itens (%s .. %s)" % (
        len(merged), merged[-1]["data"], merged[0]["data"]))

    # ---- worklist: 2026-09-15 em diante ----
    ini = datetime.datetime(2026, 9, 15, 0, 0, 0, tzinfo=BRT)

    def parse_dt(s):
        s = (s or "").strip()
        for f in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
            try:
                return datetime.datetime.strptime(s[:19] if len(s) > 10 else s, f).replace(tzinfo=BRT)
            except ValueError:
                continue
        raise ValueError("data ilegivel: %r" % s)

    work = [m for m in merged if parse_dt(m["data"]) >= ini]
    work.sort(key=lambda z: z["data"])
    for i, w in enumerate(work):
        w["ordem"] = i
    json.dump({"gerado": "2026-10-02", "de": "2026-09-15", "total": len(work),
               "ja_capturados": sum(1 for w in work if str(w["media_id"]) in caps),
               "itens": work},
              open(os.path.join(HERE, "_worklist_v2.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print("worklist 15/09->hoje: %d itens (%d ja capturados)" % (
        len(work), sum(1 for w in work if str(w["media_id"]) in caps)))

    dias = {}
    for w in work:
        dias.setdefault(w["data"][:10], []).append(1)
    print("por dia:", " ".join("%s=%d" % (d, len(v)) for d, v in sorted(dias.items())))
    donos = {}
    for w in work:
        donos[w["dono_grid"]] = donos.get(w["dono_grid"], 0) + 1
    print("proprios:", sum(v for k, v in donos.items() if k == "acirvoficial"),
          "| colab:", sum(v for k, v in donos.items() if k != "acirvoficial"))
    print("exemplo media_id antigo:", old_items[0]["media_id"], "| sc", old_items[0]["sc"],
          "| calculado:", sc_to_id(old_items[0]["sc"]))


if __name__ == "__main__":
    main()
