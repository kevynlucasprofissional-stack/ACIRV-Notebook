"""Testes da contagem de publicacoes do feed da ACIRV (agosto e setembro/2026).

Trava o numero e as invariantes que impedem o erro de voltar. Roda sem instalar nada:

    python test_publicacoes_feed.py

Tambem funciona sob pytest, se estiver instalado (pytest test_publicacoes_feed.py).

O que estes testes protegem:
 - a contagem e um CONJUNTO, nao um total (mesma contagem com posts trocados reprova);
 - nada pode aparecer numa fonte sem estar na varredura do feed;
 - a data vale pela decodificacao do shortcode, nao pelo rotulo da fonte;
 - um defeito conhecido fica travado como teste: quando for corrigido, o teste
   falha de proposito e obriga a atualizar a expectativa.
"""
import csv
import datetime
import json
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import publicacoes_feed as pf  # noqa: E402

FONTES = pf.registro_fontes()

def _grid():
    return pf.fonte_grid(FONTES["grid"][1])

def _src(nome):
    leitor, caminho = FONTES[nome][0], FONTES[nome][1]
    return leitor(caminho)

def _do_mes(itens, mes):
    return {sc for sc in itens if pf.mes_de(sc) == mes}

# ------------------------------------------------------------- a referencia
def test_01_grid_carrega_com_204_itens():
    g = _grid()
    assert len(g) == 204, "a varredura do feed tem %d itens, esperado 204" % len(g)

def test_02_shortcode_e_media_id_sao_coerentes():
    """O id que veio na captura tem que reproduzir o shortcode. Pega id trocado/copiado errado."""
    itens = json.load(open(FONTES["grid"][1], encoding="utf-8"))["itens"]
    ruins = [x["sc"] for x in itens if x.get("media_id") and pf.mid2sc(x["media_id"])[:11] != x["sc"][:11]]
    assert not ruins, "media_id nao corresponde ao shortcode em: %s" % ruins

def test_03_data_decodificada_confere_com_a_data_do_grid():
    """Se o decodificador errasse, todo o resto do teste estaria medindo a coisa errada."""
    itens = json.load(open(FONTES["grid"][1], encoding="utf-8"))["itens"]
    ruins = []
    for x in itens:
        esperada = str(x["publicado_brt"])[:16]
        obtida = pf.sc_para_data(x["sc"]).strftime("%Y-%m-%d %H:%M")
        if esperada != obtida:
            ruins.append((x["sc"], esperada, obtida))
    assert not ruins, "data decodificada != data da varredura em: %s" % ruins[:5]

# ---------------------------------------------------------------- contagens
def test_04_setembro_tem_exatamente_116_posts_no_feed():
    n = len(_do_mes(_grid(), "2026-09"))
    assert n == 116, "setembro tem %d posts na varredura do feed, esperado 116" % n

def test_05_agosto_tem_exatamente_62_posts_no_feed():
    n = len(_do_mes(_grid(), "2026-08"))
    assert n == 62, "agosto tem %d posts na varredura do feed, esperado 62" % n

def test_06_borda_de_mes_em_brt():
    """01/10 pertence a outubro e nao pode vazar para setembro."""
    g = _do_mes(_grid(), "2026-10")
    assert len(g) == 1, "outubro tem %d posts na varredura, esperado 1" % len(g)
    assert len(_do_mes(_grid(), "2026-09")) == 116, "o post de 01/10 vazou para setembro"

def test_07_cada_post_pertence_a_um_unico_mes():
    itens = json.load(open(FONTES["grid"][1], encoding="utf-8"))["itens"]
    meses = {}
    for x in itens:
        meses.setdefault(pf.mes_de(x["sc"]), []).append(x["sc"])
    total = sum(len(v) for v in meses.values())
    assert total == len(itens), "post contado em dois meses"
    assert set(meses) == {"2026-06", "2026-07", "2026-08", "2026-09", "2026-10"}, sorted(meses)

# ------------------------------------------------------------ base canonica
def test_08_base_de_setembro_e_o_mesmo_conjunto_do_grid():
    """Nao basta 116 = 116: tem que ser os MESMOS posts."""
    base = set(_src("base_set"))
    grid = _do_mes(_grid(), "2026-09")
    so_base, so_grid = base - grid, grid - base
    assert not so_base, "a base tem post que o feed nao tem: %s" % sorted(so_base)
    assert not so_grid, "o feed tem post que a base nao tem: %s" % sorted(so_grid)
    assert len(base) == len(grid) == 116

def test_09_base_de_setembro_nao_tem_shortcode_repetido():
    scs = [r["shortcode"][:11] for r in csv.DictReader(open(FONTES["base_set"][1], encoding="utf-8"), delimiter=";")]
    assert len(scs) == len(set(scs)) == 116

def test_10_xlsx_da_base_confere_com_o_csv():
    import openpyxl
    x = FONTES["base_set"][1].replace(".csv", ".xlsx")
    ws = openpyxl.load_workbook(x, read_only=True).active
    assert ws.max_row == 117, "xlsx tem %d linhas (1 cabecalho + 116), esperado 117" % ws.max_row

# --------------------------------------------------- uniao: nada de fora
def test_11_nenhuma_fonte_traz_post_que_o_feed_nao_tem():
    """O teste que pega o caso 'o sweep perdeu um post'."""
    for periodo in ("2026-09", "2026-08"):
        r = pf.auditar(periodo)
        for nome, f in r["fontes"].items():
            if "erro" in f:
                continue
            assert not f["fora_da_referencia"], "%s (periodo %s) traz post fora do feed: %s" % (
                nome, periodo, f["fora_da_referencia"])

def test_12_varreduras_antigas_sao_subconjunto_do_sweep_final():
    full = set(_grid())
    for nome in ("grid_v1", "grid_v2"):
        antigos = set(_src(nome))
        assert not (antigos - full), "%s tem post que o sweep final perdeu: %s" % (nome, sorted(antigos - full))

def test_13_brutos_e_export_de_agosto_cabem_no_grid():
    g = set(_grid())
    for nome in ("brutos_ago", "export_ago"):
        fora = set(_src(nome)) - g
        assert not fora, "%s tem post fora do feed: %s" % (nome, sorted(fora))

def test_14_export_oficial_de_agosto_rotula_4_posts_com_data_errada():
    """Export ja trouxe 4 posts de 31/07 como se fossem de agosto. A data do shortcode manda."""
    esperados = {"Dbd6DYGA0y3", "DbdvooJOi2n", "DbdvwQLu4_o", "DbdwBOBOVJt"}
    exp = _src("export_ago")
    julho = {sc for sc in exp if pf.mes_de(sc) == "2026-07"}
    assert julho == esperados, "posts de julho no export de agosto mudaram: %s" % sorted(julho)
    agosto = {sc for sc in exp if pf.mes_de(sc) == "2026-08"}
    assert len(agosto) == 48
    assert not (agosto - set(_grid())), "export de agosto tem post que o feed nao tem"

# -------------------------------------------------- divida conhecida de agosto
def test_15_base_de_agosto_esta_incompleta_14_posts():
    """DEFEITO CONHECIDO: a base 08-09 cobre 48 dos 62 posts de agosto.

    Quando alguem completar a base, este teste FALHA de proposito: e o sinal para
    atualizar a expectativa e apagar a divida.
    """
    faltando = sorted(_do_mes(_grid(), "2026-08") - _do_mes(_src("base_08_09"), "2026-08"))
    assert len(faltando) == 14, "a base de agosto agora cobre %d de 62 (antes: 48)" % (62 - len(faltando))

def test_16_base_de_agosto_tem_4_datas_publicadas_erradas():
    base = _src("base_08_09")
    errados = sorted(sc for sc in base if pf.mes_de(sc) == "2026-07" and str(base[sc].get("rotulo", ""))[:7] == "2026-08")
    assert errados == ["Dbd6DYGA0y3", "DbdvooJOi2n", "DbdvwQLu4_o", "DbdwBOBOVJt"], errados

# ------------------------------------------------------------------- buracos
def test_17_keniasleite_entra_na_contagem_mas_sem_views():
    """Reel colaborativo: lacuna do painel. Ausencia de metrica nunca vira zero."""
    base = _src("base_set")
    linha = None
    for r in csv.DictReader(open(FONTES["base_set"][1], encoding="utf-8"), delimiter=";"):
        if r["shortcode"][:11] == "DdFXhdwp0L9":
            linha = r
    assert linha is not None, "o reel colaborativo sumiu da base de setembro"
    assert linha.get("visualizacoes", "").strip() == "", "views do keniasleite veio preenchida: %r" % linha.get("visualizacoes")
    assert linha.get("status_validacao") == "colab_metricas_principais_indisponiveis_no_painel"

# ------------------------------------------------------- o auditor morde
def test_18_bateria_negativa_do_auditor_passa():
    ok, falhas = pf.autoteste()
    assert not falhas, "a bateria negativa falhou: %s" % falhas
    assert ok == 7, "esperava 7 casos na bateria negativa, rodou %d" % ok

def test_19_auditoria_reprova_quando_injetam_defeito():
    import tempfile
    tmp = tempfile.mkdtemp(prefix="teste_audit_")
    scs = sorted(_do_mes(_grid(), "2026-09"))[:3]
    gp = os.path.join(tmp, "grid.json")
    json.dump({"itens": [{"sc": s, "publicado_brt": pf.sc_para_data(s).strftime("%Y-%m-%d %H:%M:%S"),
                          "dono_grid": "acirvoficial", "tipo_grid": "p"} for s in scs]}, open(gp, "w", encoding="utf-8"))
    bp = os.path.join(tmp, "base.csv")
    with open(bp, "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, delimiter=";")
        w.writerow(["shortcode", "data_publicacao", "vinculo"])
        for s in scs[:2]:
            w.writerow([s, pf.sc_para_data(s).strftime("%Y-%m-%d"), "proprio"])
    r = pf.auditar("2026-09", fontes={
        "grid": (pf.fonte_grid, gp, "grid de teste", "referencia", set()),
        "base": (pf.fonte_csv, bp, "base de teste", "base", {"2026-09"})})
    assert r["veredito"] == "REPROVADO", "o auditor aprovou uma base com 1 post faltando"

def test_20_veredito_limpo_quando_nada_falta():
    r = pf.auditar("2026-09")
    assert not r["divergencias"], "a auditoria de setembro acusou: %s" % r["divergencias"]
    assert r["veredito"] == "COMPLETO"

# ------------------------------------------------------------------- runner
def main():
    testes = [(n, f) for n, f in sorted(globals().items()) if n.startswith("test_") and callable(f)]
    ok, falhas = 0, []
    for nome, f in testes:
        try:
            f()
            print("  PASSOU  %s" % nome)
            ok += 1
        except AssertionError as e:
            print("  FALHOU  %s\n          %s" % (nome, e))
            falhas.append(nome)
        except Exception as e:
            print("  ERRO    %s\n          %r" % (nome, e))
            falhas.append(nome)
    print("\n%d/%d testes passaram" % (ok, len(testes)))
    return 0 if not falhas else 1

if __name__ == "__main__":
    sys.exit(main())
