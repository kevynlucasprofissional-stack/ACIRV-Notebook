#!/usr/bin/env python3
"""
Gera os payloads dos cartões do lote piloto (16/09 a 05/10/2026) para o Trello.

Fonte de verdade:
- pilot_batch.json  (extraído dos arquivos canônicos v2 por extract_pilot_batch.py)
- RECONC abaixo (classificação de reconciliação + referências históricas
  encontradas na varredura ao vivo do quadro Calendário Editorial)

Padrão de descrição: 03-integracoes/PADRAO_DESCRICAO_CARTOES_TRELLO.md
- a string enviada ao campo `desc` do Trello é ENXUTA e voltada à designer;
- metadados internos (prioridade, pilar, campanha, serviço, métrica,
  reconciliação, referências históricas) NÃO vão para a descrição;
- eles são preservados em `_meta/<NNN>.json` e no payload interno, para
  auditoria e idempotência.

Nada é inventado: campos ausentes na v2 simplesmente não geram linha.
"""
import json
import os
import sys
import unicodedata

sys.stdout.reconfigure(encoding="utf-8")

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
TMP = os.path.join(os.environ["LOCALAPPDATA"], "Temp")
PILOT = os.path.join(TMP, "pilot_batch.json")
OUTDIR = os.path.join(ROOT, "06-referencias-visuais", "cartoes")
METADIR = os.path.join(OUTDIR, "_meta")

TRELLO = "https://trello.com"
LIST_ID = "69370019555b10bb6ad19e30"

# ---------------------------------------------------------------- reconciliação
# `obs`      = observações internas completas (NUNCA vão para o cartão)
# `obs_pub`  = observações que ALTERAM DIRETAMENTE A PRODUÇÃO da designer
#              (padrão canônico, regra de redação). Condensadas e sem
#              referência a arquivos internos, IDs internos ou classificação.
# `validar`  = DADOS A VALIDAR, redigidos para a designer (sem jargão interno).
RECONC = {
    "ACIRV-SM-2026-001": {
        "classe": "REFERENCE_ONLY",
        "refs": [
            ("[ACIRV] Criativos de agradecimento", "/c/Kit1KpSE/4535-acirv-criativos-de-agradecimento"),
            ("[ACIRV] Carrossel manifesto estande", "/c/JJjqWakW/4420-acirv-carrossel-manifesto-estande"),
            ("[ACIRV] Destaque: SudoExpo", "/c/fxqxET3B/4371-acirv-destaque-sudoexpo"),
        ],
        "obs": [
            "Nenhum cartão existente corresponde a esta pauta: o pedido é novo (pesquisa de avaliação do estande).",
            "Coordenação obrigatória com '[ACIRV] Criativos de agradecimento' (EM PRODUÇÃO), que já cobre peças de fechamento da SudoExpo, para evitar encerramento redundante.",
        ],
        # Exemplo aprovado no padrão canônico: mantidas verbatim.
        "obs_pub": [
            "Nenhum cartão existente corresponde a esta pauta: o pedido é novo (pesquisa de avaliação do estande).",
            "Coordenação obrigatória com '[ACIRV] Criativos de agradecimento' (EM PRODUÇÃO), que já cobre peças de fechamento da SudoExpo, para evitar encerramento redundante.",
        ],
        "validar": [
            "Link/QR do formulário de avaliação (pesquisa de 1 minuto) precisa ser fornecido antes da arte final.",
        ],
    },
    "ACIRV-SM-2026-045": {
        "classe": "REFERENCE_ONLY",
        "refs": [
            ("[ACIRV] Criativos de agradecimento", "/c/Kit1KpSE/4535-acirv-criativos-de-agradecimento"),
        ],
        "obs": [
            "RISCO DE REDUNDÂNCIA — confirmar com o editorial antes de produzir.",
            "'[ACIRV] Criativos de agradecimento' (EM PRODUÇÃO) já trata o encerramento da SudoExpo; a reconciliação inicial pede coordenar os posts pós-evento para não repetir fechamentos.",
            "Esta pauta é pós-evento com ângulo próprio (continuidade das conexões), mas a sobreposição de intenção precisa de decisão humana.",
        ],
        "obs_pub": [
            "Risco de redundância: '[ACIRV] Criativos de agradecimento' (EM PRODUÇÃO) já trata o encerramento da SudoExpo. Confirmar com o editorial antes de produzir.",
        ],
        "validar": [
            "Definir se esta peça substitui, complementa ou convive com o fechamento existente.",
        ],
    },
    "ACIRV-SM-2026-002": {
        "classe": "NO_MATCH",
        "refs": [
            ("[ACIRV] Criativos de agradecimento", "/c/Kit1KpSE/4535-acirv-criativos-de-agradecimento"),
            ("[ACIRV] Destaque: SudoExpo", "/c/fxqxET3B/4371-acirv-destaque-sudoexpo"),
        ],
        "obs": [
            "Sem cartão equivalente no quadro; conteúdo novo.",
            "Pertence à mesma família pós-SudoExpo de 001/003/045/006 — alinhar a narrativa entre elas antes de produzir.",
        ],
        "obs_pub": [
            "Alinhar a narrativa com as demais peças pós-SudoExpo do lote antes de produzir.",
        ],
        "validar": [
            "Números, resultados e alcance da SudoExpo não podem ser publicados sem validação atual.",
        ],
    },
    "ACIRV-SM-2026-003": {
        "classe": "NO_MATCH",
        "refs": [
            ("CARROSSEL - ACIRV SUDOEXPO", "/c/7TZtBxSU/4458-carrossel-acirv-sudoexpo"),
            ("CARROSSEL - ACIRV SUDOEXPO", "/c/7DqvlWkJ/4459-carrossel-acirv-sudoexpo"),
        ],
        "obs": [
            "Conceito próximo ao card histórico 'CARROSSEL - ACIRV SUDOEXPO' (o mesmo caso que motivou o ajuste da pauta 016), porém o ângulo 'do Match à conversa' é distinto e não repete o conceito.",
        ],
        "obs_pub": [],
        "validar": [
            "Confirmar se o Match da SudoExpo realmente aconteceu e se pode ser citado como caso.",
        ],
    },
    "ACIRV-SM-2026-004": {
        "classe": "REFERENCE_ONLY",
        "refs": [
            ("[ACIRV] Certificado digital", "/c/7ybgzAj1/4447-acirv-certificado-digital"),
            ("[ACIRV] Certificado Digital em uma página", "/c/v30MvsQC/4257-acirv-certificado-digital-em-uma-p%C3%A1gina"),
            ("[ACIRV] Carrossel Certificado Digital", "/c/4qWNPqWt/4095-acirv-carrossel-certificado-digital"),
        ],
        "obs": [
            "Há três peças históricas de Certificado Digital. O ângulo desta pauta (5 situações de necessidade) é distinto; reaproveitar apenas informações e visuais ainda válidos.",
        ],
        "obs_pub": [],
        "validar": [
            "Produtos de certificado digital, prazos, tipos e condições exigem validação atual.",
        ],
    },
    "ACIRV-SM-2026-046": {
        "classe": "REFERENCE_ONLY",
        "refs": [
            ("CARD - HAPPY HOUR DOS ASSOCIADOS", "/c/zfB5vaSM/4091-card-happy-hour-dos-associados"),
            ("CARDS - HAPPY HOUR ASSOCIADOS ACIRV", None),
        ],
        "obs": [
            "Os cartões históricos tratam de happy hour de associados — conteúdo diferente. Servem apenas como precedente de linguagem para público associado, sem repetir a sequência textual.",
        ],
        "obs_pub": [],
        "validar": [
            "Canais e serviços citados precisam refletir a operação atual da ACIRV.",
        ],
    },
    "ACIRV-SM-2026-005": {
        "classe": "REFERENCE_ONLY",
        "refs": [
            ("[ACIRV] Destaque: Benefícios", "/c/VHIrq9YP/4384-acirv-destaque-benef%C3%ADcios"),
        ],
        "obs": [
            "Usar como referência para NÃO repetir a mesma sequência textual sobre rede, representação, networking e capacitação.",
            "Mesma frente da campanha 'Eu Faço Parte do Movimento' (evergreen de pertencimento e prova social).",
        ],
        "obs_pub": [
            "Evitar repetir a sequência textual sobre rede, representação, networking e capacitação já usada em peças anteriores.",
        ],
        "validar": [
            "Benefícios, depoimentos e prova social exigem evidência e autorização de uso.",
        ],
    },
    "ACIRV-SM-2026-006": {
        "classe": "REFERENCE_ONLY",
        "refs": [
            ("REELS - BASTIDORES DO PALCO", "/c/bxBu9Ja0/3305-reels-bastidores-do-palco"),
        ],
        "obs": [
            "O card histórico é REEL — fora do escopo da Samara. Usar apenas como referência de ideia fotográfica; esta pauta é carrossel estático.",
        ],
        "obs_pub": [
            "Peça estática: não produzir vídeo/Reel.",
        ],
        "validar": [
            "Uso de imagem de pessoas e de bastidores exige autorização de imagem.",
        ],
    },
    "ACIRV-SM-2026-007": {
        "classe": "REFERENCE_ONLY",
        "refs": [
            ("[ACIRV] Auditório + Sala de Treinamento", "/c/KnsGllBd/3761-acirv-audit%C3%B3rio-sala-de-treinamento"),
            ("[ACIRV] - Catálogo de locação", "/c/9Dv9izeA/3853-acirv-cat%C3%A1logo-de-loca%C3%A7%C3%A3o"),
        ],
        "obs": [
            "Há material histórico de espaços/locação. Usar como referência, sem repetir o mesmo recorte.",
        ],
        "obs_pub": [],
        "validar": [
            "Capacidades, estrutura, preços/descontos e disponibilidade dos espaços precisam ser revalidados antes de virar arte ou legenda.",
        ],
    },
    "ACIRV-SM-2026-008": {
        "classe": "REFERENCE_ONLY",
        "refs": [
            ("[ACIRV] Card do dia do comerciante", "/c/Xhgv3MmC/4342-acirv-card-do-dia-do-comerciante"),
        ],
        "obs": [
            "Precedente de data comemorativa com fotografia humana e frase principal; não repetir o mesmo layout.",
            "Critério do plano para datas comemorativas: relevância estratégica e utilidade; rejeitar homenagem protocolar sem função clara.",
        ],
        "obs_pub": [
            "Não repetir o layout de peças de data comemorativa anteriores (fotografia humana + frase principal).",
        ],
        "validar": [
            "Se houver foto ou nome de vendedor associado, é necessária autorização de imagem.",
        ],
    },
    "ACIRV-SM-2026-047": {
        "classe": "NO_MATCH",
        "refs": [],
        "obs": [
            "Sem cartão equivalente no quadro. O único candidato encontrado ('Apresentação Canais - Néctar') é de OUTRO cliente e não serve de referência.",
        ],
        "obs_pub": [],
        "validar": [
            "Lista de canais oficiais de atendimento e eventuais horários exigem validação atual.",
        ],
    },
    "ACIRV-SM-2026-009": {
        "classe": "NO_MATCH",
        "refs": [],
        "obs": [
            "Sem cartão equivalente no quadro; conteúdo novo.",
            "Data comemorativa: aplicar o critério do plano (função clara, conexão com público empresarial) em vez de homenagem protocolar.",
        ],
        "obs_pub": [],
        "validar": [
            "Não usar números ou estatísticas sobre micro e pequenas empresas sem validação atual.",
        ],
    },
}

OBJETIVO_CAMPANHA = {
    "SUDOEXPO-POS": "Frente Pós-SudoExpo: transformar o evento em evidência, conexão, aprendizado e continuidade",
    "SERVICOS-SEMPRE-PRESENTES": "Frente 'Serviços sempre presentes': alternar serviços e informações institucionais por ângulos diversos, sem repetir o mesmo recorte",
    "EU-FACO-PARTE-REPRISE": "Campanha 'Eu Faço Parte do Movimento': evergreen de pertencimento e prova social",
    "DATAS-ESTRATEGICAS": "Data comemorativa sob critério do plano: relevância estratégica, conexão com o público empresarial e utilidade real; homenagem protocolar sem função clara deve ser rejeitada",
}

# Regra de produção obrigatória para os IDs 045-060 (padrão canônico).
OBS_2_SLIDES = (
    "Exatamente 2 slides (capa + CTA): não criar slides intermediários; "
    "o aprofundamento fica na legenda."
)

# Exemplo aprovado no padrão canônico — teste de contrato do gerador.
EXPECTED_001 = """PUBLICAÇÃO: 16/09/2026
DATA DE ENTREGA PARA SAMARA: 16/09/2026

OBJETIVO/RACIONAL:
Frente Pós-SudoExpo: transformar o evento em evidência, conexão, aprendizado e continuidade

FORMATO: Carrossel 2 slides — 2 slide(s)
NÚMERO DE SLIDES: 2 (EXATO)

CONTEÚDO/ESTRUTURA DOS SLIDES:

Slide 1: convite para avaliar o estande. Slide 2: por que a resposta importa + QR Code.
CTA: Responder à pesquisa de 1 minuto

DIREÇÃO VISUAL: Visual direto, pouco texto, QR em destaque e foto/ilustração real do estande.

LEGENDA SUGERIDA (completa):
A SudoExpo terminou, mas a nossa escuta continua. Se você passou pelo estande da ACIRV, sua percepção ajuda a entender o que funcionou e o que pode evoluir nas próximas experiências. A pesquisa leva cerca de 1 minuto e transforma opinião em melhoria prática.
Responder à pesquisa de 1 minuto.
#ACIRV #ConectarParaCrescer

DADOS A VALIDAR:

- Link/QR do formulário de avaliação (pesquisa de 1 minuto) precisa ser fornecido antes da arte final.

OBSERVAÇÕES:

- Nenhum cartão existente corresponde a esta pauta: o pedido é novo (pesquisa de avaliação do estande).
- Coordenação obrigatória com '[ACIRV] Criativos de agradecimento' (EM PRODUÇÃO), que já cobre peças de fechamento da SudoExpo, para evitar encerramento redundante."""

# Termos que NUNCA podem aparecer na descrição visível para a designer.
FORBIDDEN = [
    "POST ID",
    "PRIORIDADE",
    "PILAR ESTRATÉGICO",
    "CAMPANHA/FRENTE",
    "SERVIÇO/BENEFÍCIO",
    "MÉTRICA PRINCIPAL",
    "RECONCILIAÇÃO TRELLO",
    "REFERÊNCIAS HISTÓRICAS",
    "não especificado",
    "não definido",
    "plano v2",
    ".md",
    "trello.com/c",
    "_meta",
    "ACIRV-SM-2026-",
    "invariante",
]

SECTIONS = [
    "OBJETIVO/RACIONAL:",
    "FORMATO: ",
    "NÚMERO DE SLIDES: ",
    "CONTEÚDO/ESTRUTURA DOS SLIDES:",
    "CTA: ",
    "DIREÇÃO VISUAL: ",
    "LEGENDA SUGERIDA (completa):",
]


def br(iso: str) -> str:
    a, m, d = iso.split("-")
    return f"{d}/{m}/{a}"


def slug(s: str) -> str:
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return "".join(c if c.isalnum() else "-" for c in s.lower()).strip("-")


def normalize_legend(text: str) -> str:
    """Colapsa as linhas vazias internas da legenda.

    O padrão canônico aprovado apresenta a legenda em linhas consecutivas.
    Nenhum texto é removido — apenas as quebras de linha vazias.
    """
    return "\n".join(ln.rstrip() for ln in (text or "").split("\n") if ln.strip())


def build(post: dict) -> dict:
    pid = post["post_id"]
    r = RECONC[pid]
    slides = post["slides"]
    pub = br(post["publication_date"])
    deliv = br(post["delivery_date"])

    L = []
    L.append(f"PUBLICAÇÃO: {pub}")
    L.append(f"DATA DE ENTREGA PARA SAMARA: {deliv}")
    L.append("")
    L.append("OBJETIVO/RACIONAL:")
    L.append(OBJETIVO_CAMPANHA[post["campanha"]])
    L.append("")
    L.append(f"FORMATO: {post['formato']}")
    L.append(f"NÚMERO DE SLIDES: {slides} (EXATO)")
    L.append("")
    L.append("CONTEÚDO/ESTRUTURA DOS SLIDES:")
    L.append("")
    L.append(post["estrutura"])
    L.append(f"CTA: {post['cta']}")
    L.append("")
    L.append(f"DIREÇÃO VISUAL: {post['direcao_visual']}")
    L.append("")
    L.append("LEGENDA SUGERIDA (completa):")
    L.append(normalize_legend(post["legend"]))

    if r["validar"]:
        L.append("")
        L.append("DADOS A VALIDAR:")
        L.append("")
        for v in r["validar"]:
            L.append(f"- {v}")

    obs_pub = list(r["obs_pub"])
    if post["requer_2_slides"]:
        obs_pub.append(OBS_2_SLIDES)
    if obs_pub:
        L.append("")
        L.append("OBSERVAÇÕES:")
        L.append("")
        for o in obs_pub:
            L.append(f"- {o}")

    internal = {
        "post_id": pid,
        "publication_date": post["publication_date"],
        "delivery_date": post["delivery_date"],
        "prioridade": post.get("prioridade"),
        "pilar_estrategico": post.get("pilar"),
        "campanha_frente": post["campanha"],
        "servico_beneficio": post.get("servico"),
        "metrica_principal": post.get("metrica"),
        "reconciliacao_trello": r["classe"],
        "referencias_historicas": [
            {"nome": n, "url": (TRELLO + h) if h else None} for n, h in r["refs"]
        ],
        "observacoes_internas": r["obs"],
        "dados_a_validar": r["validar"],
        "dedupe_key": f"{pid}|{post['publication_date']}|{slug(post['title'])}",
        "fontes_internas": post.get("source_file"),
        "formato": post["formato"],
        "slides": slides,
        "requer_2_slides": post["requer_2_slides"],
        "extra_leve": post.get("extra_leve"),
        "legend_len": len(post.get("legend") or ""),
    }

    return {
        "post_id": pid,
        "title": f"ACIRV — {post['title']} — {pub}",
        "publication_date": post["publication_date"],
        "due": post["delivery_date"],
        "list_id": LIST_ID,
        "desc": "\n".join(L),
        "internal": internal,
    }


def load_posts() -> list:
    raw = json.load(open(PILOT, encoding="utf-8"))
    if isinstance(raw, dict):
        for k in ("pilot", "posts"):
            if k in raw:
                raw = raw[k]
                break
        else:
            cands = [v for v in raw.values()
                     if isinstance(v, list) and v and isinstance(v[0], dict)]
            raw = cands[0] if cands else []
    posts = [p for p in raw if isinstance(p, dict) and "post_id" in p]
    posts.sort(key=lambda p: (p["publication_date"], p["post_id"]))
    return posts


def validate(cards: list) -> list:
    """Retorna a lista de erros. Vazia = conforme o padrão canônico."""
    errs = []
    by_id = {c["post_id"]: c for c in cards}

    if len(cards) != 12:
        errs.append(f"esperado 12 cartões, gerado {len(cards)}")

    for c in cards:
        pid = c["post_id"]
        d = c["desc"]
        it = c["internal"]
        pub = br(it["publication_date"])

        # título: "ACIRV — <título> — DD/MM/AAAA" com a data de publicação
        if not c["title"].startswith("ACIRV — "):
            errs.append(f"{pid}: título sem o prefixo canônico")
        if not c["title"].endswith(f" — {pub}"):
            errs.append(f"{pid}: título não termina com a data de publicação ({c['title']!r})")

        # datas na descrição
        if f"PUBLICAÇÃO: {pub}" not in d:
            errs.append(f"{pid}: falta PUBLICAÇÃO correta")
        if f"DATA DE ENTREGA PARA SAMARA: {br(it['delivery_date'])}" not in d:
            errs.append(f"{pid}: falta DATA DE ENTREGA PARA SAMARA correta")

        # seções obrigatórias, presentes e em ordem
        pos = -1
        for sec in SECTIONS:
            i = d.find(sec)
            if i < 0:
                errs.append(f"{pid}: seção ausente {sec!r}")
            elif i < pos:
                errs.append(f"{pid}: seção fora de ordem {sec!r}")
            else:
                pos = i

        # legenda completa presente
        if it["legend_len"] <= 0:
            errs.append(f"{pid}: legenda vazia")

        # nenhum metadado interno vazando
        for bad in FORBIDDEN:
            if bad in d:
                errs.append(f"{pid}: string interna vazando na descrição -> {bad!r}")

        # slides
        n = it["slides"]
        if f"NÚMERO DE SLIDES: {n} (EXATO)" not in d:
            errs.append(f"{pid}: NÚMERO DE SLIDES divergente (esperado {n})")

        # IDs 045-060: exatamente 2 slides + regra explícita na descrição
        if it["requer_2_slides"]:
            if n != 2:
                errs.append(f"{pid}: ID 045-060 com {n} slides (deve ser exatamente 2)")
            if OBS_2_SLIDES not in d:
                errs.append(f"{pid}: falta a regra explícita de 2 slides na descrição")

        # metadados internos preservados (não podem ter sido descartados)
        if not it["observacoes_internas"]:
            errs.append(f"{pid}: observações internas perdidas")
        if it["reconciliacao_trello"] not in (
            "NO_MATCH", "REFERENCE_ONLY", "REUSE_CARD",
            "ALREADY_PUBLISHED", "DUPLICATE_BLOCKED",
        ):
            errs.append(f"{pid}: classificação de reconciliação inválida")
        if not it["dedupe_key"]:
            errs.append(f"{pid}: dedupe_key ausente")

    # contrato do exemplo aprovado
    if "ACIRV-SM-2026-001" in by_id:
        if by_id["ACIRV-SM-2026-001"]["desc"] != EXPECTED_001:
            errs.append("ACIRV-SM-2026-001: descrição difere do exemplo aprovado no padrão canônico")

    return errs


def main() -> int:
    posts = load_posts()
    os.makedirs(OUTDIR, exist_ok=True)
    os.makedirs(METADIR, exist_ok=True)

    cards = [build(p) for p in posts]

    for c in cards:
        nnn = c["post_id"].replace("ACIRV-SM-2026-", "")
        with open(os.path.join(OUTDIR, nnn + ".md"), "w", encoding="utf-8") as fh:
            fh.write(c["title"] + "\n\n" + c["desc"] + "\n")
        with open(os.path.join(METADIR, nnn + ".json"), "w", encoding="utf-8") as fh:
            json.dump(c["internal"], fh, ensure_ascii=False, indent=2)

    payload = os.path.join(TMP, "cards_payload.json")
    with open(payload, "w", encoding="utf-8") as fh:
        json.dump(cards, fh, ensure_ascii=False, indent=2)

    errs = validate(cards)

    print(f"cartoes gerados : {len(cards)}")
    print(f"descricoes      : {OUTDIR}")
    print(f"meta interno    : {METADIR}")
    print(f"payload         : {payload}")
    print()
    for c in cards:
        print(f"{c['post_id']} | pub={br(c['publication_date'])} | venc={c['due']} | "
              f"slides={c['internal']['slides']} | {len(c['desc']):4d} chars | {c['title']}")
    print()
    if errs:
        print("VALIDACAO: FALHOU")
        for e in errs:
            print("  ! " + e)
        return 1
    print("VALIDACAO: OK (12/12 conforme PADRAO_DESCRICAO_CARTOES_TRELLO.md)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
