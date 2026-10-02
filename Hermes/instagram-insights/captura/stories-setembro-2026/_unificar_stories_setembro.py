#!/usr/bin/env python3
"""_unificar_stories_setembro.py — monta a base de stories de 2026-09.

Le os artefatos brutos desta pasta de captura e escreve a base consolidada na
camada 1 do cofre, no MESMO contrato do Instagram-Publicacoes-2026-09.csv:
separador ';', CRLF, UTF-8 sem BOM, ordenado por data/hora decrescente.

PORTAO: nao escreve nada se VERIFICACAO-2026-09.json nao trouxer veredito
COMPLETO. Sem veredito nao existe base — e a regra que evita canonizar captura
duvidosa.

Uso:
    python _unificar_stories_setembro.py            # escreve
    python _unificar_stories_setembro.py --simular  # so relata, nao escreve

Insumos (mesma pasta):
    midias_2026-09.json          inventario (pk, taken_at, tipo, img, vid)
    insights_2026-09.json        metricas por media_id (BaseSurface)
    day_shells_2026-09.json      contagem oficial por dia (a expectativa)
    _descricoes_stories.json     descricao por visao, por media_id
    VERIFICACAO-2026-09.json     veredito + sha256 das fontes

Dependencia externa: metricas_stories.py (scripts da skill) — unico lugar que
sabe ler os dois formatos de metrica. Sobrescreva o caminho com a variavel de
ambiente HERMES_SKILL_SCRIPTS se a skill mudar de lugar.
"""
import argparse
import csv
import datetime as dt
import hashlib
import json
import os
import sys

PERIODO = "2026-09"
OFFSET_BRT = -10800
STATUS_OK = f"completo_{PERIODO}_stories_basesurface"


def achar_skill():
    candidatos = []
    if os.environ.get("HERMES_SKILL_SCRIPTS"):
        candidatos.append(os.environ["HERMES_SKILL_SCRIPTS"])
    base = os.environ.get("LOCALAPPDATA") or os.path.expanduser("~/.local/share")
    candidatos.append(os.path.join(base, "hermes", "skills", "productivity",
                                   "instagram-post-metrics-reporting", "scripts"))
    candidatos.append(os.path.expanduser("~/AppData/Local/hermes/skills/productivity/"
                                         "instagram-post-metrics-reporting/scripts"))
    for c in candidatos:
        if os.path.isfile(os.path.join(c, "metricas_stories.py")):
            return c
    raise SystemExit("metricas_stories.py nao encontrado. Defina HERMES_SKILL_SCRIPTS.")


sys.path.insert(0, achar_skill())
from metricas_stories import (  # noqa: E402
    COLUNAS_CSV,
    ausentes_em,
    formato_de,
    json_compacto,
    quebra_de,
    valor_coluna,
)

AQUI = os.path.dirname(os.path.abspath(__file__))


def achar_cofre(inicio):
    """Sobe a arvore ate achar a raiz do cofre (a que tem 85-Bases-e-Consultas)."""
    atual = inicio
    for _ in range(8):
        if os.path.isdir(os.path.join(atual, "85-Bases-e-Consultas")):
            return atual
        pai = os.path.dirname(atual)
        if pai == atual:
            break
        atual = pai
    raise SystemExit("raiz do cofre nao encontrada (procurei 85-Bases-e-Consultas acima).")


def ler_json(nome):
    caminho = os.path.join(AQUI, nome)
    if not os.path.isfile(caminho):
        raise SystemExit(f"insumo ausente: {nome} (rode a coleta e o verificador antes).")
    with open(caminho, encoding="utf-8") as f:
        return json.load(f)


def sha256(caminho):
    h = hashlib.sha256()
    with open(caminho, "rb") as f:
        for bloco in iter(lambda: f.read(1 << 16), b""):
            h.update(bloco)
    return h.hexdigest()


def valor_de_quebra(registro, campo):
    """Total de uma metrica quebrada por dimensao (ex.: navegacoes)."""
    itens = quebra_de(registro, campo) if callable(quebra_de) else None
    if isinstance(itens, dict):
        return sum(v for v in itens.values() if isinstance(v, (int, float)))
    if isinstance(itens, list):
        return sum(i.get("total_value", 0) for i in itens if isinstance(i, dict))
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--simular", action="store_true", help="relata sem escrever")
    args = ap.parse_args()

    cofre = achar_cofre(AQUI)
    verif = ler_json(f"VERIFICACAO-{PERIODO}.json")
    veredito = str(verif.get("veredito") or "").upper()
    if veredito != "COMPLETO":
        raise SystemExit(f"PORTAO FECHADO: veredito={veredito or 'ausente'} "
                         f"(rode verificar_completude.py e conserte antes de canonizar).")
    print(f"portao aberto: veredito {veredito}")

    midias = ler_json(f"midias_{PERIODO}.json")
    insights = ler_json(f"insights_{PERIODO}.json")
    try:
        descricoes = ler_json("_descricoes_stories.json")
    except SystemExit:
        descricoes = {}
        print("AVISO: _descricoes_stories.json ausente — a coluna descricao_visao vai vazia.")

    por_midia = insights.get("por_midia") if isinstance(insights, dict) else None
    if por_midia is None:
        por_midia = insights if isinstance(insights, dict) else {}
    registros = {str(k): v for k, v in por_midia.items()}

    caminho_insights = os.path.join(AQUI, f"insights_{PERIODO}.json")
    sha_insights = sha256(caminho_insights)
    pasta_captura = f"Hermes/instagram-insights/captura/stories-setembro-2026"
    source_path = f"{pasta_captura}/insights_{PERIODO}.json"

    linhas = []
    for dia_utc, lista in (midias.get("por_dia") or {}).items():
        for m in lista:
            pk = str(m.get("pk"))
            taken = m.get("taken_at")
            if not pk or not taken:
                continue
            local = dt.datetime.fromtimestamp(taken + OFFSET_BRT, dt.timezone.utc)
            if local.strftime("%Y-%m") != PERIODO:
                continue  # a borda (01/10) fica fora da base do mes
            reg = registros.get(pk)
            if not reg:
                raise SystemExit(f"midia {pk} sem registro de insights — veredito nao cobre isto")
            desc = descricoes.get(pk) or {}
            linha = {
                "periodo_fonte": PERIODO,
                "data_story": local.strftime("%Y-%m-%d"),
                "hora_story": local.strftime("%H:%M:%S"),
                "media_id": pk,
                "tipo_midia": {1: "imagem", 2: "video"}.get(m.get("tipo"), f"tipo_{m.get('tipo')}"),
            }
            for campo, referencia in COLUNAS_CSV:
                if campo in linha or not referencia:
                    continue
                if referencia.endswith("|bruto"):
                    linha[campo] = ""
                    continue
                linha[campo] = valor_coluna(reg, referencia)
            # navegacoes_quebra: codigos de acao lado a lado, sem inventar rotulo
            linha["navegacoes_quebra"] = json_compacto(
                quebra_de(reg, "story_navigations_count_story_navigation_action_type_breakdowns")
                if callable(quebra_de) else {}
            )
            linha["descricao_visao"] = desc.get("descricao", "")
            linha["texto_sobreposto"] = desc.get("texto_sobreposto", "")
            linha["natureza"] = desc.get("natureza", "")
            linha["metricas_ausentes"] = ";".join(ausentes_em(reg) or [])
            linha["formato_metricas"] = formato_de(reg)
            notas = []
            if not linha["descricao_visao"]:
                notas.append("descricao_visao_ausente")
            if linha["visualizacoes"] is None:
                notas.append("visualizacoes_ausentes_no_painel")
            linha["notas"] = "; ".join(notas)
            linha["source_path"] = source_path
            linha["source_blob_sha"] = sha_insights
            linha["status_validacao"] = (STATUS_OK if linha["visualizacoes"] is not None
                                         else f"incompleto_{PERIODO}_stories_sem_visualizacoes")
            linhas.append(linha)

    linhas.sort(key=lambda r: (r["data_story"], r["hora_story"]), reverse=True)
    campos = [c for c, _ in COLUNAS_CSV]
    sem_desc = sum(1 for r in linhas if not r["descricao_visao"])
    print(f"linhas: {len(linhas)} | sem descricao: {sem_desc} | "
          f"sem visualizacoes: {sum(1 for r in linhas if r['visualizacoes'] is None)}")

    # resumo por dia (ascendente, para a nota de decisao)
    resumo = {}
    for r in linhas:
        d = resumo.setdefault(r["data_story"], {"stories": 0, "visualizacoes": 0, "visualizadores": 0,
                                                "alcance": 0, "interacoes": 0, "curtidas_story": 0,
                                                "respostas": 0, "compartilhamentos": 0,
                                                "navegacoes": 0, "cliques_link": 0,
                                                "visitas_perfil": 0, "novos_seguidores": 0,
                                                "com_descricao": 0})
        d["stories"] += 1
        for k in ("visualizacoes", "visualizadores", "alcance", "interacoes", "curtidas_story",
                  "respostas", "compartilhamentos", "navegacoes", "cliques_link",
                  "visitas_perfil", "novos_seguidores"):
            v = r.get(k)
            d[k] += int(v) if isinstance(v, (int, float)) else 0
        if r["descricao_visao"]:
            d["com_descricao"] += 1

    if args.simular:
        print("--simular: nada foi escrito.")
        return

    destino_csv = os.path.join(cofre, "85-Bases-e-Consultas", f"Instagram-Stories-{PERIODO}.csv")
    with open(destino_csv, "w", encoding="utf-8", newline="\r\n") as f:
        w = csv.DictWriter(f, fieldnames=campos, delimiter=";", quoting=csv.QUOTE_MINIMAL)
        w.writeheader()
        for r in linhas:
            w.writerow({c: ("" if r.get(c) is None else r.get(c)) for c in campos})
    print(f"escrito: {os.path.relpath(destino_csv, cofre)}")

    destino_xlsx = destino_csv.replace(".csv", ".xlsx")
    try:
        from openpyxl import Workbook
        wb = Workbook()
        ws = wb.active
        ws.title = f"Stories {PERIODO}"
        ws.append(campos)
        for r in linhas:
            ws.append(["" if r.get(c) is None else r.get(c) for c in campos])
        ws.freeze_panes = "A2"
        wb.save(destino_xlsx)
        print(f"escrito: {os.path.relpath(destino_xlsx, cofre)}")
    except ImportError:
        print("AVISO: openpyxl ausente — .xlsx nao gerado")

    destino_jsonl = os.path.join(AQUI, f"_stories_{PERIODO}.jsonl")
    with open(destino_jsonl, "w", encoding="utf-8") as f:
        for r in linhas:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    destino_resumo = os.path.join(AQUI, f"_resumo_por_dia_{PERIODO}.json")
    with open(destino_resumo, "w", encoding="utf-8") as f:
        json.dump({"periodo": PERIODO, "gerado_em": dt.datetime.now(dt.timezone.utc).isoformat(),
                   "por_dia": dict(sorted(resumo.items())),
                   "totais": {k: sum(d[k] for d in resumo.values())
                              for k in ("stories", "visualizacoes", "visualizadores", "alcance",
                                        "interacoes", "curtidas_story", "respostas",
                                        "compartilhamentos", "navegacoes", "cliques_link",
                                        "visitas_perfil", "novos_seguidores", "com_descricao")}},
                  f, ensure_ascii=False, indent=1)
    print(f"escrito: {os.path.relpath(destino_jsonl, cofre)}")
    print(f"escrito: {os.path.relpath(destino_resumo, cofre)}")
    t = json.load(open(destino_resumo, encoding="utf-8"))["totais"]
    print(f"totais: {t['stories']} stories | {t['visualizacoes']} views | "
          f"{t['interacoes']} interacoes | {t['com_descricao']} descritos")


if __name__ == "__main__":
    main()
