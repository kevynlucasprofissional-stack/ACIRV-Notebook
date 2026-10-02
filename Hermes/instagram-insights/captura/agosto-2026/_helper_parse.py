import json, re, datetime, os, sys

SECS = {'Visualizações','Interações','Perfil','Anúncio','Respostas','Publicações','Recursos'}

def parse_insights(txt):
    ls=[l.strip() for l in txt.split('\n') if l.strip()]
    sec=None
    seq=[]
    i=0
    while i<len(ls):
        l=ls[i]
        if l in SECS:
            sec=l
            seq.append(('_SECAO_',sec,''))
            i+=1
            continue
        # valor é a próxima linha se for numérica/%
        nxt=ls[i+1] if i+1<len(ls) else None
        if nxt and re.fullmatch(r'[\d.,%+\s\-]+', nxt):
            seq.append((sec or '', l, nxt))
            i+=2
        else:
            seq.append((sec or '', l, ''))
            i+=1
    return seq

if __name__=='__main__':
    raw=open(sys.argv[1],encoding='utf-8').read()
    for a,b,c in parse_insights(raw):
        print(repr(a), '|', repr(b), '|', repr(c))