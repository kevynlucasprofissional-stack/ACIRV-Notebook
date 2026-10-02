import re, os, json, sys

base = r'C:\Github\ACIRV-Notebook\Hermes\Planejamento 4º Trimestre de 2026\01-planejamento\v2'
rows = []
for f in sorted(os.listdir(base)):
    if not f.endswith('.md'):
        continue
    p = os.path.join(base, f)
    txt = open(p, encoding='utf-8').read()
    heads = re.findall(r'^##\s+(ACIRV-SM-2026-\d{3})\s*(.*)$', txt, re.M)
    for key, resto in heads:
        i = txt.find('## ' + key)
        j = len(txt)
        for m in re.finditer(r'^##\s', txt[i+3:], re.M):
            j = i + 3 + m.start()
            break
        bloco = txt[i:j]
        tem = 'DESCRICAO CANONICA' in bloco.upper().replace('\u00c7', 'C').replace('\u00c3', 'A') and True or ('DESCRIÇÃO CANÔNICA' in bloco)
        tem = 'DESCRIÇÃO CANÔNICA PARA O TRELLO' in bloco
        pub = re.search(r'PUBLICA[ÇC][ÃA]O[:\s]*([0-9]{2}/[0-9]{2}/[0-9]{4})', bloco.upper())
        ent = re.search(r'DATA DE ENTREGA PARA SAMARA[:\s]*([0-9]{2}/[0-9]{2}/[0-9]{4})', bloco.upper())
        rows.append({
            'arquivo': f,
            'key': key,
            'titulo': resto.strip(' —-–:')[:80],
            'bloco_chars': len(bloco),
            'tem_canonica': tem,
            'pub': pub.group(1) if pub else None,
            'entrega': ent.group(1) if ent else None,
        })

print('TOTAL POSTS:', len(rows))
print('COM bloco canonico:', sum(1 for r in rows if r['tem_canonica']))
print('SEM bloco canonico:', sum(1 for r in rows if not r['tem_canonica']))
print()
for r in rows:
    print('%-28s %-6s %5d %s pub=%-10s ent=%-10s %s' % (
        r['key'], r['arquivo'].replace('2026-', '').replace('.md', ''),
        r['bloco_chars'], 'CANON' if r['tem_canonica'] else '-----',
        r['pub'], r['entrega'], r['titulo'][:60]))

json.dump(rows, open(r'C:\Github\ACIRV-Notebook\Hermes\Planejamento 4º Trimestre de 2026\scratch\posts_inventory.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('\nsalvo posts_inventory.json')
