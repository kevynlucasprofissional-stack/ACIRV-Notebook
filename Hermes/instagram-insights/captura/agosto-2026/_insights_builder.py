import json, re, datetime, sys

SECS = {'Visualizações','Interações','Perfil','Anúncio','Respostas','Publicações','Recursos'}

# colunas normalizadas em snake_case (idênticas aos JSon existentes)
NORM = {
 'Visualizações':'visualizacoes','Visualizadores':'visualizadores','Alcance':'alcance',
 'Contas alcançadas':'contas_alcancadas','Interações':'interacoes','Interações com posts':'interacoes_posts',
 'Curtidas':'curtidas','Comentários':'comentarios','Compartilhamentos':'compartilhamentos',
 'Salvamentos':'salvamentos','Contas com engajamento':'contas_com_engajamento',
 'Atividade do perfil':'atividade_do_perfil','Visitas ao perfil':'visitas_ao_perfil',
 'Toques em links externos':'toques_em_links_externos','Toques no endereço comercial':'toques_no_endereco_comercial',
 'Seguidores':'novos_seguidores','Novos seguidores':'novos_seguidores','Respostas':'respostas',
 'Turbine este post':'','Promover':'','Impulsionar':'',
 'Na página inicial':'na_pagina_inicial','No perfil':'no_perfil','De outra pessoa':'de_outra_pessoa',
 'Contas Meta alcançadas':'contas_meta_alcancadas','Contas alcançadas':'contas_meta_alcancadas','Alcance':'alcance',
}

def num(v):
    v=v.replace('.','').replace(',','.')
    try: return int(v)
    except: return None

def parse(dados):
    """dados: lista de linhas já limpas do body.innerText da página de insights."""
    ls=[l.strip() for l in dados if l.strip()]
    sec=None; rows=[]; i=0
    while i<len(ls):
        l=ls[i]
        nxt=ls[i+1] if i+1<len(ls) else None
        # seção somente se NÃO for seguida de valor numérico (senão é métrica)
        if l in SECS and not (nxt and re.fullmatch(r'[\d.,%+\s\-]+', nxt)):
            sec=l; i+=1; continue
        if nxt and re.fullmatch(r'[\d.,%+\s\-]+', nxt):
            rows.append({'secao':sec or '','nome_original':l,'valor_original':nxt})
            i+=2; continue
        if re.fullmatch(r'[\d.,%+\s\-]+', l):
            if rows and rows[-1]['valor_original']=='':
                rows[-1]['valor_original']=l
            i+=1; continue
        rows.append({'secao':sec or '','nome_original':l,'valor_original':''})
        i+=1
    return rows

def normalize(rows):
    metricas={}; ausentes=[]
    for r in rows:
        v=r['valor_original'].strip()
        n=NORM.get(r['nome_original'])
        # match inexato
        if n is None:
            for k,c in NORM.items():
                if k.lower() in r['nome_original'].lower() or r['nome_original'].lower() in k.lower():
                    n=c; break
        if not v:
            ausentes.append(r['nome_original']); continue
        if n:
            numv=num(v)
            metricas[n]=numv if numv is not None else v
    return metricas, ausentes, rows

def build(shortcode, url, tipo, datetime_iso, legenda, autor, coautores, colaborativo,
          insights_raw, coletado_em, fonte, promovido=False, obs=None):
    rows=parse(insights_raw.split('\n'))
    m, a, bruta = normalize(rows)
    # promovido: SOMENTE se houver o aviso real "dados de anúncios".
    # O botao "Turbine este post"/"Turbinar este reel" existe em TODOS os posts -> nunca sinaliza.
    tl = insights_raw.lower()
    AD_HINT = ('dados de anúncios' in tl) or ('dados de anuncios' in tl)
    prom = promovido or AD_HINT
    if prom: m['promovido']=True
    else: m.pop('promovido',None)

    dp=None; hp=None; status_data='ok'
    try:
        dt=datetime.datetime.fromisoformat(datetime_iso.replace('Z','+00:00')).astimezone(datetime.timezone(datetime.timedelta(hours=-3)))
        dp=dt.strftime('%Y-%m-%d'); hp=dt.strftime('%H:%M:%S')
    except Exception:
        status_data='NAO_CONFIRMADA'
    base={
      'shortcode':shortcode,'url':url,'data_publicacao':dp,'hora_publicacao':hp,
      'tipo_midia':tipo.lower(),'autor':autor,'colaborativo':colaborativo,'coautores':coautores,
      'legenda':legenda,'status_data':status_data,'status_insights':'ok','erro':'',
      'metricas_ausentes':a if a else [],'insights_raw':insights_raw,'melhores_metricas':m,
      'evidencia_data':f"time datetime={datetime_iso}",
      'coletado_em':coletado_em,'fonte':fonte,
    }
    if obs: base['observacao']=obs
    return base

if __name__=='__main__':
    import json as j
    # CLI: python _insights_builder.py '<json del passos pela stdin>' -- recebe dict de metadados
    data=j.load(sys.stdin)
    out=build(**data)
    print(j.dumps(out,ensure_ascii=False))