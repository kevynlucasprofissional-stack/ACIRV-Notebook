"""Upgrade dos 22 JSONs 'schema A' (coleta antiga) para o schema unificado:
adiciona melhores_metricas / metricas_ausentes e normaliza status.
Fonte dos dados: insights_raw (20) ou secoes (2). Nenhuma invencao de dados.
"""
import json, os, sys, shutil, datetime

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)
from _insights_builder import NORM, parse, normalize, num

SCHEMA_A = ['Db-7_-OOxRu','DcbJmepx1nq','DccD4y_m_vZ','DccDC3EG62U','Dcg2HcQm08f','Dcg571dmzBL',
 'DchIji9m9Ac','Dcjs2R4G_fX','DcjUaHrjhxv','Dcl1hMpDirN','DcliQzRDjNM','DclREC4m2H4',
 'DclSk4fG8C1','DclTCCwm8ff','DcmHJv_G-0A','DcmSbnuG9E-','DcmUAaAG3Pi','DcO_l7tAO80',
 'DcrgQC6gknC','DcUEyDAgrbq','DcUJGqJG3tO','DcUSK-YAmSq']

def rows_from_secoes(secoes):
    rows = []
    for s in secoes:
        for pair in s.get('metricas', []):
            if len(pair) == 2:
                rows.append({'secao': s.get('secao',''), 'nome_original': pair[0], 'valor_original': str(pair[1])})
    return rows

def text_of(d):
    """texto para deteccao de anuncio"""
    if d.get('insights_raw'):
        return d['insights_raw']
    parts = []
    for s in d.get('secoes', []) or []:
        parts.append(s.get('secao',''))
        for p in s.get('metricas', []):
            parts.extend([str(x) for x in p])
    if d.get('observacao'): parts.append(d['observacao'])
    if d.get('nota'): parts.append(d['nota'])
    return '\n'.join(parts)

def upgrade(sc, payload, old):
    raw = old.get('insights_raw') or ''
    if raw:
        rows = parse(raw.split('\n'))
    else:
        rows = rows_from_secoes(old.get('secoes') or [])
    m, a, _ = normalize(rows)
    txt = text_of(old).lower()
    ad = ('dados de anúncios' in txt) or ('dados de anuncios' in txt) or \
         ('anúncio' in txt and 'turbine' not in txt) or ('anuncio' in txt and 'turbine' not in txt)
    if ad: m['promovido'] = True
    out = dict(old)
    out['tipo_midia'] = (old.get('tipo_midia') or '').lower()
    out['status_insights'] = 'ok'
    if old.get('status_data') in ('CONFIRMADA',):
        out['status_data'] = 'ok'
    out['metricas_ausentes'] = a if a else []
    out['melhores_metricas'] = m
    return out

def main():
    bkp = os.path.join(BASE, '_backup_schemaA')
    os.makedirs(bkp, exist_ok=True)
    ok = 0; bad = []
    for sc in SCHEMA_A:
        p = os.path.join(BASE, sc + '.json')
        old = json.load(open(p, encoding='utf-8'))
        shutil.copy2(p, os.path.join(bkp, sc + '.json'))
        new = upgrade(sc, None, old)
        if not new['melhores_metricas'].get('visualizacoes'):
            bad.append(sc)
        with open(p, 'w', encoding='utf-8') as f:
            json.dump(new, f, ensure_ascii=False, indent=1)
        ok += 1
        print(f"{sc:16s} -> metricas={len(new['melhores_metricas']):2d} viz={new['melhores_metricas'].get('visualizacoes')} prom={new['melhores_metricas'].get('promovido')} ausentes={new['metricas_ausentes']}")
    print(f"\nUpgraded: {ok}/22 | sem visualizacoes: {bad}")

if __name__ == '__main__':
    main()
