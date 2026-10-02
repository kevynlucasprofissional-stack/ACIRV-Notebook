"""Consolida o inventario do grid do Instagram (setembro/2026) a partir do
payload baixado do navegador, datando cada shortcode pela formula snowflake
do media-id (validada contra <time datetime> e taken_at da API).

Entrada : ../ig_grid_set2026.json   (baixado de Downloads via Blob do navegador)
Saida   : _grid_inventario.json     (itens com sc, data_brt, dono, tipo)
"""
import json
import os
from collections import Counter, OrderedDict
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(os.path.dirname(HERE), "ig_grid_set2026.json")
BRT = ZoneInfo("America/Sao_Paulo")
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_"
IG_EPOCH_MS = 1314220021721
TARGET = "acirvoficial"


def media_id(shortcode: str) -> int:
    n = 0
    for ch in shortcode:
        n = n * 64 + ALPHABET.index(ch)
    return n


def published_utc(shortcode: str) -> datetime:
    ms = (media_id(shortcode) >> 23) + IG_EPOCH_MS
    return datetime.fromtimestamp(ms / 1000, tz=timezone.utc)


def main() -> None:
    data = json.load(open(SRC, encoding="utf-8"))
    order, meta = data["order"], data["meta"]

    items = []
    for idx, sc in enumerate(order):
        m = meta.get(sc, {})
        dt = published_utc(sc).astimezone(BRT)
        items.append(
            OrderedDict(
                pos=idx,
                sc=sc,
                media_id=str(media_id(sc)),
                publicado_brt=dt.strftime("%Y-%m-%d %H:%M:%S"),
                data=dt.strftime("%Y-%m-%d"),
                dono_grid=m.get("o", ""),
                tipo_grid=m.get("t", ""),
                proprio=m.get("o") == TARGET,
            )
        )

    setembro = [i for i in items if i["data"] >= "2026-09-01"]
    out = {
        "gerado_em": datetime.now(BRT).strftime("%Y-%m-%d %H:%M:%S %z"),
        "fonte": os.path.basename(SRC),
        "total_grid": len(items),
        "total_setembro": len(setembro),
        "setembro_proprios": sum(1 for i in setembro if i["proprio"]),
        "setembro_colab_terceiros": sum(1 for i in setembro if not i["proprio"]),
        "cobertura_grid": (items[0]["data"], items[-1]["data"]) if items else None,
        "itens": items,
    }
    dst = os.path.join(HERE, "_grid_inventario.json")
    json.dump(out, open(dst, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    print(f"grid total={len(items)} cobertura={items[0]['data']}..{items[-1]['data']}")
    print(f"setembro={len(setembro)} proprios={out['setembro_proprios']} "
          f"colab_terceiros={out['setembro_colab_terceiros']}")
    print("por dia (total/proprios):")
    per = Counter(i["data"] for i in setembro)
    per_own = Counter(i["data"] for i in setembro if i["proprio"])
    for d in sorted(per, reverse=True):
        print(f"  {d}: {per[d]:>2} / {per_own[d]:>2}")
    print("proprios de setembro (ordem do grid):")
    for i in setembro:
        if i["proprio"]:
            print(f"  {i['publicado_brt']}  {i['sc']}  {i['tipo_grid']}")
    print("terceiros em setembro:")
    for i in setembro:
        if not i["proprio"]:
            print(f"  {i['publicado_brt']}  {i['sc']}  {i['dono_grid']}")
    print(f"-> {dst}")
    _ = timedelta


if __name__ == "__main__":
    main()
