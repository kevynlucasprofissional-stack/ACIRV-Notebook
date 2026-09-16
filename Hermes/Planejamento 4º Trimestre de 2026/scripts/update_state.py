#!/usr/bin/env python3
"""
Atualiza 02-estado/execution_state_v2.json de forma idempotente.

Uso:
  python scripts/update_state.py --post ACIRV-SM-2026-045 --status CARTAO_CRIADO \
      --card-id <id> --card-url <url> --desc-saved true --desc-len 1234

  python scripts/update_state.py --recount          # recalcula contadores
  python scripts/update_state.py --due-pending "msg" # registra pendência de due

Nunca apaga o histórico interno das pautas: apenas completa/atualiza campos.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
STATE_PATH = os.path.join(ROOT, "02-estado", "execution_state_v2.json")
META_DIR = os.path.join(ROOT, "06-referencias-visuais", "cartoes", "_meta")

TZ = dt.timezone(dt.timedelta(hours=-3))  # America/Sao_Paulo (UTC-03:00)


def now_iso() -> str:
    return dt.datetime.now(TZ).replace(microsecond=0).isoformat()


def load_state() -> dict:
    with open(STATE_PATH, encoding="utf-8") as fh:
        return json.load(fh)


def save_state(state: dict) -> None:
    state["updated_at"] = now_iso()
    with open(STATE_PATH, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(state, fh, ensure_ascii=False, indent=2)
        fh.write("\n")


def load_meta(pid: str) -> dict:
    """Metadados internos da pauta (pilar, campanha, reconciliação, refs...)."""
    path = os.path.join(META_DIR, pid.replace("ACIRV-SM-2026-", "") + ".json")
    if not os.path.exists(path):
        return {}
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def ensure_post(state: dict, pid: str) -> dict:
    posts = state.setdefault("posts", {})
    post = posts.setdefault(pid, {})
    meta = load_meta(pid)
    # campos internos: só preenche se ainda não existirem (nunca apaga histórico)
    for src, dst in (
        ("pilar_estrategico", "pilar_estrategico"),
        ("campanha_frente", "campanha_frente"),
        ("servico_beneficio", "servico_beneficio"),
        ("metrica_principal", "metrica_principal"),
        ("prioridade", "prioridade"),
        ("publication_date", "publication_date"),
        ("delivery_date", "delivery_date"),
        ("formato", "formato"),
        ("slides", "slides"),
        ("requer_2_slides", "requer_2_slides"),
        ("dedupe_key", "dedupe_key"),
        ("fontes_internas", "fontes_internas"),
        ("observacoes_internas", "observacoes_internas_historicas"),
        ("referencias_historicas", "referencias_historicas"),
        ("dados_a_validar", "dados_a_validar"),
    ):
        if meta.get(src) not in (None, "", []) and dst not in post:
            post[dst] = meta[src]
    return post


def recount(state: dict) -> dict:
    posts = state.get("posts", {})
    counters = state.setdefault("counters", {})
    created = [p for p, v in posts.items() if (v.get("trello") or {}).get("card_object_id")]
    desc_ok = [p for p, v in posts.items() if (v.get("trello") or {}).get("description_saved")]
    counters["trello_created"] = len(created)
    counters["visual_references_created"] = len(
        [p for p, v in posts.items() if (v.get("visual_reference") or {}).get("accepted")]
    )
    pilot = state.setdefault("pilot_batch", {})
    planned = pilot.get("planned_posts") or len(pilot.get("post_ids", []))
    pilot["remaining_cards_to_create"] = max(0, planned - len(created))
    pilot["cards_created"] = len(created)
    pilot["descriptions_saved"] = len(desc_ok)
    return {"trello_created": len(created), "descriptions_saved": len(desc_ok),
            "remaining": pilot["remaining_cards_to_create"]}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--post")
    ap.add_argument("--status")
    ap.add_argument("--card-id")
    ap.add_argument("--card-url")
    ap.add_argument("--desc-saved", choices=["true", "false"])
    ap.add_argument("--desc-len", type=int)
    ap.add_argument("--desc-standard")
    ap.add_argument("--native-due")
    ap.add_argument("--reconciliation")
    ap.add_argument("--note", action="append", default=[])
    ap.add_argument("--next-action", action="append", default=[])
    ap.add_argument("--due-pending")
    ap.add_argument("--recount", action="store_true")
    args = ap.parse_args()

    state = load_state()

    if args.due_pending is not None:
        state["native_due_pending"] = {
            "value_expected": args.due_pending,
            "reason": "O controle nativo de vencimento do Trello não pôde ser gravado com "
                      "segurança; o campo personalizado 'Data de publicação' não substitui o due.",
            "recorded_at": now_iso(),
        }

    if args.post:
        post = ensure_post(state, args.post)
        trello = post.setdefault("trello", {})
        if args.status:
            post["status"] = args.status
        if args.card_id:
            trello["card_object_id"] = args.card_id
        if args.card_url:
            trello["card_url"] = args.card_url
            trello["list_id"] = state.get("trello", {}).get("list_id")
        if args.desc_saved:
            trello["description_saved"] = args.desc_saved == "true"
        if args.desc_len is not None:
            trello["description_length"] = args.desc_len
        if args.desc_standard:
            trello["description_standard"] = args.desc_standard
        if args.native_due is not None:
            trello["native_due"] = None if args.native_due == "null" else args.native_due
        if args.reconciliation:
            post["reconciliation"] = args.reconciliation
        for n in args.note:
            post.setdefault("notes", []).append(n)
        if args.next_action:
            post["next_actions"] = args.next_action
        post["updated_at"] = now_iso()

    info = recount(state)
    save_state(state)
    print(json.dumps({"saved": STATE_PATH, **info}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
