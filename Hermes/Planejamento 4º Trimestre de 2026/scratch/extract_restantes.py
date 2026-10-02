import re, os, json

base = r'C:\Github\ACIRV-Notebook\Hermes\Planejamento 4º Trimestre de 2026\01-planejamento\v2'
posts = []
for f in sorted(os.listdir(base)):
    if not f.endswith('.md'):
        continue
    txt = open(os.path.join(base, f), encoding='utf-8').read()
    marks = [(m.start(), m.group(1), m.group(2), m.group(3)) for m in re.finditer(r'^##\s+(ACIRV-SM-2026-\d{3})\s*\|\s*([0-9]{4}-[0-9]{2}-[0-9]{2})\s*\|\s*(.*)$', txt, re.M)]
    for idx, (pos, key, data_iso, titulo) in enumerate(marks):
        end = marks[idx+1][0] if idx+1 < len(marks) else len(txt)
        bloco = txt[pos:end]
        tem_canon = 'DESCRIÇÃO CANÔNICA PARA O TRELLO' in bloco
        ent = re.search(r'\*\*Entrega:\*\*\s*([0-9]{4}-[0-9]{2}-[0-9]{2})', bloco)
        fmt = re.search(r'\*\*Formato:\*\*\s*([^·\n]+)', bloco)
        camps = re.search(r'\*\*Campanha:\*\*\s*([^·\n]+)', bloco)
        posts.append({
            'arquivo': f, 'key': key, 'pub_iso': data_iso, 'titulo': titulo.strip(),
            'tem_canonica': tem_canon,
            'entrega_iso': ent.group(1) if ent else None,
            'formato': (fmt.group(1).strip() if fmt else None),
            'campanha': (camps.group(1).strip() if camps else None),
            'corpo': bloco,
        })

sem = [p for p in posts if not p['tem_canonica']]
print('TOTAL %d | com canonica %d | SEM canonica %d' % (len(posts), len(posts)-len(sem), len(sem)))
faltando_ent = [p['key'] for p in sem if not p['entrega_iso']]
print('SEM campo Entrega:', faltando_ent if faltando_ent else 'nenhum')
print('periodo:', sem[0]['pub_iso'], '->', sem[-1]['pub_iso'])
print()
for p in sem:
    d = p['pub_iso'][8:10] + '/' + p['pub_iso'][5:7] + '/' + p['pub_iso'][0:4]
    e = p['entrega_iso']
    e = (e[8:10] + '/' + e[5:7] + '/' + e[0:4]) if e else '---'
    print('%-6s pub=%s ent=%s %-12s %s' % (p['key'], d, e, (p['formato'] or '?')[:12], p['titulo'][:58]))

json.dump(sem, open(r'C:\Github\ACIRV-Notebook\Hermes\Planejamento 4º Trimestre de 2026\scratch\posts_sem_canonica.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('\nsalvo posts_sem_canonica.json (%d posts)' % len(sem))
