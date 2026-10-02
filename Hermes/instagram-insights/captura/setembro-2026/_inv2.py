# -*- coding: utf-8 -*-
"""Gera _grid_inventario2.json (inventario do grid de 02/10/2026) e _worklist2.json
(posts de 15 a 30/09/2026), mantendo o esquema dos arquivos da run 01-14/09.

Entradas : _grid_sweep_20261002.txt (sweep do grid de 02/10) + _grid_inventario.json (run anterior)
Saidas   : _grid_inventario2.json, _worklist2.json
Nao altera nenhum arquivo preexistente da run 01-14/09.
"""
import datetime
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
A = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_"
EPOCH = 1314220021721
BRT = datetime.timezone(datetime.timedelta(hours=-3))
PROP = "acirvoficial"


def sc_to_id(tok):
    n = 0
    for ch in tok:
        d = A.find(ch)
        if d < 0:
            raise ValueError("char invalido %r em %r" % (ch, tok))
        n = n * 64 + d
    return n


def dt_of(tok):
    """media_id <- shortcode (11 primeiros chars) -> datetime BRT."""
    mid = sc_to_id(tok[:11])
    ms = (mid >> 23) + EPOCH
    return mid, datetime.datetime.fromtimestamp(ms / 1000, BRT)


def main():
    itens = []
    for line in open(os.path.join(HERE, "_grid_sweep_20261002.txt"), encoding="utf-8"):
        line = line.strip()
        if not line:
            continue
        pos, tok, owner, kind, pin = line.split(",")
        mid, dt = dt_of(tok)
        itens.append({
            "pos": int(pos),
            "sc": tok[:11],
            "media_id": str(mid),
            "publicado_brt": dt.strftime("%Y-%m-%d %H:%M:%S -03:00"),
            "data": dt.strftime("%Y-%m-%d %H:%M:%S"),
            "dono_grid": owner,
            "tipo_grid": kind,
            "proprio": owner == PROP,
            "pin": int(pin),
            "shortcode_completo": tok if len(tok) > 11 else None,
        })
    itens.sort(key=lambda x: x["pos"])
    itens[0].pop("shortcode_completo", None)
    for it in itens:
        if it.get("shortcode_completo") is None:
            it.pop("shortcode_completo", None)

    set_ = [it for it in itens if it["data"].startswith("2026-09")]
    inv2 = {
        "gerado": "2026-10-02",
        "fonte": "grid acirvoficial (browser Hermes Work), scroll continuo ate o fundo",
        "total_grid": len(itens),
        "janela_grid": "%s .. %s" % (min(i["data"] for i in itens), max(i["data"] for i in itens)),
        "setembro_total": len(set_),
        "setembro_proprios": sum(1 for it in set_ if it["proprio"]),
        "setembro_colab_terceiros": sum(1 for it in set_ if not it["proprio"]),
        "itens": itens,
    }
    json.dump(inv2, open(os.path.join(HERE, "_grid_inventario2.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)

    # ---- worklist 15 a 30/09/2026 ----
    sel = [it for it in itens if "2026-09-15" <= it["data"][:10] <= "2026-09-30"]
    sel.sort(key=lambda x: x["data"])
    for i, it in enumerate(sel):
        it["ordem"] = i
    por_dia = {}
    for it in sel:
        d = it["data"][:10]
        por_dia[d] = por_dia.get(d, 0) + 1
    wl = {
        "gerado": "2026-10-02",
        "de": "2026-09-15",
        "ate": "2026-09-30",
        "total": len(sel),
        "proprios": sum(1 for it in sel if it["proprio"]),
        "colab": sum(1 for it in sel if not it["proprio"]),
        "por_dia": por_dia,
        "itens": sel,
    }
    json.dump(wl, open(os.path.join(HERE, "_worklist2.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)

    print("grid:", len(itens), "itens |", inv2["janela_grid"])
    print("setembro no grid:", len(set_), "(proprios %d / colab %d)" %
          (inv2["setembro_proprios"], inv2["setembro_colab_terceiros"]))
    print("worklist 15-30/09:", len(sel), "(proprios %d / colab %d)" % (wl["proprios"], wl["colab"]))
    print("por dia:", " ".join("%s=%d" % (d, n) for d, n in sorted(por_dia.items())))
    for it in sel:
        print("  %2d %s %-24s %-4s %s" % (it["ordem"], it["data"], it["dono_grid"],
                                          it["tipo_grid"], it["media_id"]))
    # fronteira: vizinhos fora da janela
    antes = [it for it in itens if it["data"][:10] == "2026-09-14"]
    depois = [it for it in itens if it["data"][:10] >= "2026-10-01"]
    print("fronteira inferior 14/09:", len(antes), "posts |", [i["media_id"] for i in antes])
    print("fronteira superior (>=01/10):", len(depois), "posts |", [(i["data"], i["media_id"]) for i in depois])


if __name__ == "__main__":
    main()
