import json, re, os

base = r'C:\Github\ACIRV-Notebook\Hermes\Planejamento 4º Trimestre de 2026'
src = json.load(open(os.path.join(base, 'scratch', 'posts_sem_canonica.json'), encoding='utf-8'))

def br(iso):
    return iso[8:10] + '/' + iso[5:7] + '/' + iso[0:4]

out = []
for p in src:
    corpo = p['corpo']
    linhas = corpo.split('\n')
    # remove a linha de cabecalho "## ACIRV-SM-2026-XXX | data | titulo"
    if linhas and linhas[0].startswith('## '):
        linhas = linhas[1:]
    texto = '\n'.join(linhas).strip()
    # remove separador final "---"
    texto = re.sub(r'\n*-{3,}\s*$', '', texto).strip()
    out.append({
        'key': p['key'],
        'titulo': p['titulo'],
        'pub_iso': p['pub_iso'],
        'entrega_iso': p['entrega_iso'],
        'nome_cartao': 'ACIRV — %s — %s' % (p['titulo'], br(p['pub_iso'])),
        'due': p['entrega_iso'],
        'desc': texto,
    })

out.sort(key=lambda x: x['pub_iso'])
dest = os.path.join(base, 'scratch', 'cards_payload.json')
json.dump(out, open(dest, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

print('cartoes:', len(out))
print('periodo:', out[0]['pub_iso'], '->', out[-1]['pub_iso'])
print('tamanho json:', len(json.dumps(out, ensure_ascii=False)), 'chars')
print('primeiro nome:', out[0]['nome_cartao'])
print('--- desc[0] (repr 300) ---')
print(repr(out[0]['desc'][:300]))
print('--- ultimo ---')
print(out[-1]['nome_cartao'], '| due', out[-1]['due'], '| desc', len(out[-1]['desc']), 'chars')
