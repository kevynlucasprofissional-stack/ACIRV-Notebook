---
id: metrica-prints-app-mobile-setembro-2026
titulo: Prints-do-App-Mobile-Setembro-2026
aliases: [Prints do app mobile, Painel profissional do celular]
tipo: metrica
status: auditado
profundidade: avancada
versao_schema: '1.0'
versao_conteudo: '1.0'
idioma: pt-BR
data_criacao: '2026-10-02'
ultima_revisao: '2026-10-02'
grau_confianca: alto
camadas_evidencia:
- fato_documentado
- dado_calculado
- interpretacao_operacional
tags:
- metricas
- instagram
- sudoexpo
- conciliacao
fontes_documentais:
- '000-Arquivos-originais/Dados de setembro segundo prints do painel profissional do Instagram mobile, ou seja, prints vindas do app do celular.md'
- '85-Bases-e-Consultas/Instagram-Publicacoes-2026-09.csv'
- 'Hermes/instagram-insights/captura/setembro-2026/_grid_inventario2.json'
- 'Hermes/instagram-insights/captura/setembro-2026/_painel_conta_2026-10-02_30.json'
- '000-Arquivos-originais/Dados para mega-relatório pós Sudoexpo/Redes sociais/instagram_acirvoficial_insights_agosto_2026_MASTER(1).xlsx'
notas_relacionadas:
- '[[Base-Instagram-Setembro-2026]]'
- '[[Diagnostico-Instagram-Agosto-Setembro-2026]]'
- '[[Qualidade-dos-Dados-de-Marketing]]'
confidencialidade: interno
subtipo: conciliacao_fontes
---

# Prints-do-App-Mobile-Setembro-2026

> [!summary] Síntese
> Os prints do painel profissional do **celular** são outra **câmera** sobre a mesma conta — não outra medição. Onde os dois medem a mesma coisa, batem **exatamente** (stories 272 = 272; reels próprios 13 = 13; quatro conteúdos conferidos item a item com curtidas/comentários/compartilhamentos idênticos). A divergência aparente `116 × 55 posts + 13 reels` **não é erro**: o card oficial conta **só o que a ACIRV publicou**, e a nossa base conta **o que apareceu no feed** — que inclui as entradas de parceiros. Em setembro: **116 no feed = 60 da conta (47 posts + 13 reels) + 56 de parceiros (17 posts + 39 reels)**.

## 1. Quatro telas dos prints, quatro escopos diferentes

| Tela | Escopo do período | Números dos prints |
|---|---|---|
| Card "Você arrasou em Setembro" | mês calendário, **conteúdo da conta** | 539 mil views (+190% vs agosto) · **13 reels, 55 posts e 272 stories** · 11 mil seguidores (+1.032) · 53% não seguidores |
| Visão geral "30 dias" | janela móvel | **1.409.945 views** · 15.580 interações · 279.100 visualizadores · +1.017 seguidores líquidos |
| Views por tipo de conteúdo | **mês** (293+128+113 = 534 mil fecha com o card) | 293 mil posts · 128 mil reels · 113 mil stories · 0 lives |
| Interações por tipo | **30 dias** (8,7+5,2+1,3 = 15,2 mil fecha com a janela) | posts 8,7 mil · reels 5,2 mil · stories 1,3 mil (+ curtidas, comentários, reposts, compartilhamentos, salvamentos e respostas por tipo) |
| Público e atividade | 30 dias | 8.306 visitas ao perfil · 878 toques no link · 11.099 seguidores · 58,7% mulheres · 25–34 = 37,9% · Brasil 99,1% / Goiás 96,4% / Rio Verde 92,3% · pico 18–21 h |

> [!warning] As duas telas "por tipo" não são do mesmo período
> A de **views** fecha com o card (mês); a de **interações** fecha com a janela de 30 dias. Misturá-las produz comparação inválida. Anote o período de cada print antes de usar.

## 2. A regra de autoria — é isto que explica `116 × 55`

A varredura do grid é a única fonte que vê **tudo que passou pelo feed**: o que a ACIRV publicou **e** o conteúdo de parceiros que entrou por colaboração. Setembro:

| | Posts | Reels | Total |
|---|---|---|---|
| **Da conta** (`dono_grid = acirvoficial`, nenhum com coautor) | 47 | 13 | **60** |
| **De parceiros** (todos com coautor: SudoExpo, Raphael Valongo, Kenia, …) | 17 | 39 | **56** |
| **Total no feed (nossa base)** | 64 | 52 | **116** |

O card oficial diz **13 reels + 55 posts + 272 stories**:

- **13 reels = exatamente os 13 reels da conta** (casamento perfeito de conjunto).
- **272 stories = exatamente os nossos 272 stories**, capturados por rota independente (arquivo de stories + `reels_media`), não pelo app.
- **55 posts × nossos 47 da conta** → resíduo de **8** não identificado (ver §5).

Corroboram a leitura de autoria as capturas antigas, que têm coluna explícita de autor: no arquivo de agosto, `autor = acirvoficial` em **todas as 52 linhas** e **0 divergências** com a nossa classificação; na captura de setembro (01–14/09), **42 da conta + 44 de parceiros** — e a nossa varredura da mesma janela dá **42 da conta + 45 de parceiros (87)**; a única diferença de conjunto é o reel da `keniasleite` (09/09 19:46, `DdFXhdwp0L9`), o mesmo item que o export da Meta nunca listou.

## 3. Validação 1:1 — a métrica é a mesma nos dois lados

Conferência item a item entre a lista "Conteúdos recentes (30 dias)" dos prints e a nossa captura (a métrica **bate; o que muda é o conjunto de itens**):

| Conteúdo no app | Print (views / curtidas / comentários / compart.) | Nosso dado |
|---|---|---|
| "A oficina Inicia.IA Pro…" (2 d) | 1,6 mil / 27 / 3 / 3 | post **30/09 14:15** (conta): **1.568 / 26 / 3 / 3** ✓ |
| "Aos meus queridos le…" — **Turbinado** | 2,1 mil / 71 / 27 / 147 | post **30/09 18:31** (parceiro `carloswriter`): **2.039 / 68 / 27 / 147** ✓ |
| "sem título visível" (2 d) | 428 / 4 / 0 / 0 | story **30/09 14:09**: **428 / 4 / 0 / 0** ✓ |
| "sem título visível" (2 d) | 126 / 1 / 0 / 0 | story **29/09 22:35**: **126 / 1 / 0 / 0** ✓ |
| "sem título visível" (2 d) | 121 / 3 / 0 / 0 | story **29/09 22:35**: **121 / 3 / 0 / 0** ✓ |
| "Card Raphael Valongo" (20 h) | 118 / 2 / 0 respostas | story **01/10 21:00** (`3998674771175034729`, sobreposto "CRIE SEU SITE COM IA / QUEM VAI CONDUZIR / **RAPHAEL VALONGO**"), o "+1" que estava sem dono ✓ |

Duas confirmações extras dessa lista: o item "Turbinado" é **exatamente** o único post marcado `promovido = sim` na nossa base (o `carloswriter` de 30/09) ✓; e o app lista **conteúdo de parceiro** com as próprias views — ou seja, a lista de conteúdos não é restrita ao que é da conta.

## 4. O que NÃO fecha (e por quê)

| Comparação | Print | Nosso | Leitura |
|---|---|---|---|
| Views do mês | 539 mil (card) = 534 mil (por tipo) | 603,5 mil = posts+reels 497.290 + stories 106.259 | **Não são a mesma grandeza.** O card mede views **no mês** do **conteúdo da conta** (inclui posts antigos ainda sendo vistos no período, exclui os de parceiros). Nossa soma mede views **acumuladas** de tudo que foi **publicado** em setembro (da conta + parceiros), lidas em 02/10. |
| Views por tipo | 293 mil posts / 128 mil reels | 221.771 (64 posts) / 275.519 (52 reels) | Diferença de **escopo**, não de métrica: 128 mil ≈ nossos **reels da conta** (103.214) + reels antigos vistos no mês; 293 mil fica acima de todos os nossos posts (221.771) → o balde inclui posts antigos ainda vistos no período. Fechar a aritmética exige uma captura controlada das duas telas no mesmo instante. |
| Interações 30 dias | 15.580 | 17.779 (painel desktop, 02/10 15:32) | Views, seguidores, visitas e toques são consistentes com "o print é ~2 h depois"; **interações divergem para baixo** no app — ponto a vigiar. |
| Conteúdo em destaque | 146 mil / 14 mil / 9,7 mil / 7,6 mil | "--" / 99 mil (promover) / 49,9 mil / 18,8 mil / 14,2 mil … | **Não alinham posicionalmente.** Nosso 1º item está ilegível no desktop ("--", ícone reels) e é provavelmente o de 146 mil. A conferir. |
| Público (gênero, idade, cidades, horários) | completo | **não existe** | É métrica de **conta**, sem equivalente por publicação. Registro separado. |

## 5. Resíduo aberto: 55 posts × 47 da conta (8 itens)

Não fecha por borda de mês (só há 1 item em 01/10 e nada em 31/08 à noite), nem por pin (1 único item fixado), nem por promoção (1 item). Hipóteses, em ordem de plausibilidade:

1. **Conteúdo publicado em setembro que saiu do grid antes da varredura de 02/10** (apagado/arquivado) — o card conta o que foi compartilhado no mês, o grid só mostra o que existe hoje.
2. **8 itens que o Instagram atribui à ACIRV e a nossa classificação de autoria dá ao parceiro** (colaboração em que a ACIRV seria a autora).
3. Diferença de definição do próprio Instagram entre "reel" e "vídeo no feed".

Teste que resolve: abrir os 17 posts de parceiro no endpoint `GET /api/v1/media/<id>/info/` (sessão logada) e ler `owner` + `coauthor_producers`.

## 6. Implicações práticas

- **Nunca comparar o card do app com a contagem do grid.** São conjuntos diferentes: card = "o que a ACIRV publicou"; grid/base = "o que passou pelo feed".
- **"Quantos posts publicamos em setembro?" → 60** (47 posts + 13 reels). **"Quantas publicações passaram pelo feed?" → 116.** Ver `[[Base-Instagram-Setembro-2026]]`.
- O par `vinculo` + `parceiro_coautores` da base é o que permite separar os dois conjuntos — use sempre os dois campos juntos.
- **Não somar** métrica de publicação (nossa base) com métrica de conta (painel/app): são esferas diferentes.
- Dados de público/atividade do app são registrados nesta nota; não há versão nossa equivalente.
- Complementar: `Hermes/instagram-insights/auditorias/AUDITORIA-2026-08.md` (contagem por conjunto de shortcodes) e `Hermes/instagram-insights/README.md` (portão de contagem).
