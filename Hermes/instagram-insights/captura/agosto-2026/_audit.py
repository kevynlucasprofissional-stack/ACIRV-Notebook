import json, glob, os, re

master = json.load(open('../_acirv_agosto_progresso.json', encoding='utf-8'))
cands = master['candidatos'] if isinstance(master, dict) else master
def code_of(c):
    if isinstance(c, dict): return c.get('shortcode') or c.get('code')
    return c if isinstance(c, str) else None
codes = [code_of(c) for c in cands]

saved = sorted(os.path.basename(f)[:-5] for f in glob.glob('*.json') if not os.path.basename(f).startswith('_'))
missing = [c for c in codes if c not in saved]
orphan = [c for c in saved if c not in codes]
print('MASTER:', len(codes), '| SAVED:', len(saved))
print('MISSING:', missing)
print('ORPHAN:', orphan)

def find_viz(o):
    if isinstance(o, dict):
        for k, v in o.items():
            if k.lower() == 'visualizacoes':
                try: return int(v)
                except Exception: pass
            r = find_viz(v)
            if r is not None: return r
    elif isinstance(o, list):
        for it in o:
            r = find_viz(it)
            if r is not None: return r
    return None

def viz(d):
    v = find_viz(d.get('melhores_metricas') or {})
    if v is not None: return v, 'melhores_metricas'
    v = find_viz(d.get('secoes') or [])
    if v is not None: return v, 'secoes'
    raw = d.get('insights_raw') or ''
    m = re.search(r'Visualiza\u00e7\u00f5es\s*\n\s*([\d.]+)', raw)
    if m: return int(m.group(1).replace('.', '')), 'regex_raw'
    return None, 'none'

noviz, promo = [], []
tot = 0
for c in saved:
    d = json.load(open(c + '.json', encoding='utf-8'))
    v, src = viz(d)
    raw = (d.get('insights_raw') or '').lower()
    banner = 'dados de an\u00fancios' in raw
    mm = d.get('melhores_metricas') or {}
    pm = mm.get('promovido')
    if v is None: noviz.append(c)
    else: tot += v
    if banner or pm:
        promo.append((c, v, 'banner_real' if banner else 'FLAG_SEM_BANNER', pm))
print('SEM VISUALIZACOES:', noviz)
print('SOMA VISUALIZACOES (todos):', tot)
print('PROMOVIDOS / FLAGS:')
for p in promo: print('  ', p)
