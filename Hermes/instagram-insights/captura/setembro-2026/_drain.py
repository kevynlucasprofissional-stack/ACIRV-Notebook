"""Drena o download do navegador (Electron grava o blob como <uuid>.tmp em Downloads).

Uso:
    python _drain.py <destino>
Le o usuario do Windows atual via USERPROFILE, acha o arquivo *.tmp mais recente
em Downloads que ainda nao foi drenado (estado em .drain_state.json) e o move
(os.replace) para <destino>.
"""
import json
import os
import sys
import time

DL = os.path.join(os.environ.get("USERPROFILE", r"C:\Users\Kevyn Lucas"), "Downloads")
STATE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".drain_state.json")


def load_state():
    try:
        return set(json.load(open(STATE, encoding="utf-8")))
    except Exception:
        return set()


def save_state(s):
    json.dump(sorted(s)[-400:], open(STATE, "w", encoding="utf-8"))


def main():
    dest = sys.argv[1]
    if not os.path.isabs(dest):
        dest = os.path.join(os.path.dirname(os.path.abspath(__file__)), dest)
    done = load_state()
    deadline = time.time() + float(sys.argv[2] if len(sys.argv) > 2 else 20)
    picked = None
    while time.time() < deadline:
        cands = [
            (os.path.getmtime(os.path.join(DL, f)), f)
            for f in os.listdir(DL)
            if f.endswith(".tmp") and f not in done
        ]
        cands.sort(reverse=True)
        if cands:
            picked = cands[0][1]
            break
        time.sleep(0.5)
    if not picked:
        print("DRAIN_FAIL: nenhum .tmp novo em", DL)
        sys.exit(3)
    src = os.path.join(DL, picked)
    size = os.path.getsize(src)
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    if os.path.exists(dest):
        os.remove(dest)
    os.replace(src, dest)
    done.add(picked)
    save_state(done)
    print(f"DRAIN_OK {picked} -> {dest} ({size} bytes)")


if __name__ == "__main__":
    main()
