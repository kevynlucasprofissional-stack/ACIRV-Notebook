import json, sys
from _insights_builder import build

def save(meta, verbose=True):
    out = build(**meta)
    path = f"{meta['shortcode']}.json"
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    if verbose:
        print(path, 'OK', json.dumps(out['melhores_metricas'], ensure_ascii=False))
    return path

if __name__ == '__main__':
    meta = json.load(open(sys.argv[1], encoding='utf-8'))
    save(meta)