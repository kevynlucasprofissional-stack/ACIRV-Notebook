---
id: consulta-leia-me-instagram-insights
titulo: LEIA-ME-Instagram-Insights
aliases: []
tipo: consulta
subtipo: guia_tecnico
status: revisado
profundidade: avancada
versao_schema: '1.0'
versao_conteudo: '1.5'
idioma: pt-BR
data_criacao: '2026-10-02'
ultima_revisao: '2026-10-02'
grau_confianca: alto
camadas_evidencia:
- fato_documentado
- interpretacao_operacional
tags:
- infraestrutura
- dominio/metricas
fontes_documentais:
- '97-Fontes-Brutas/01-Indices/Fonte - Instagram Insights.md'
- '85-Bases-e-Consultas/Instagram-Publicacoes-2026-09.csv'
notas_relacionadas:
- '[[Fonte - Instagram Insights]]'
- '[[Base-Instagram-Setembro-2026]]'
- '[[Metricas-Consolidadas-por-Fonte]]'
- '[[Qualidade-dos-Dados-de-Marketing]]'
confidencialidade: interno
---

# LEIA-ME-Instagram-Insights

> [!summary] Síntese
> Define o **local canônico** dos dados de publicação do Instagram institucional e o contrato das bases derivadas `Instagram-Publicacoes-<AAAA-MM>.csv`, para que a coleta pare de se espalhar em pastas diversas.

## Onde o dado canônico mora

`85-Bases-e-Consultas/` é o local único e canônico da família. Não existe pasta paralela para métricas de rede social.

Contrato de nome: `Instagram-Publicacoes-<AAAA-MM>.csv` — um arquivo por mês fechado, uma linha por publicação.

Contrato de nome dos stories: `Instagram-Stories-<AAAA-MM>.csv` — um arquivo por mês fechado, uma linha por story publicado. Story expirado não volta do painel: esta base é a única cópia durável dele.

Espalhamento anterior a esta nota: os mesmos números viviam dentro de `Instagram-Publicacoes-2026-08-09.csv` misturados (52 linhas de agosto + 86 de setembro parcial) e em JSONL de trabalho na camada original. A unificação separou o que era agosto do que era setembro.

## Contrato da base

Separador `;`, codificação UTF-8 sem BOM, quebra de linha CRLF, 34 colunas, ordenação por `data_publicacao` e `hora_publicacao` decrescentes.

| Coluna | Semântica |
|---|---|
| `periodo_fonte` | mês coberto, `AAAA-MM` |
| `data_publicacao`, `hora_publicacao` | publicação em BRT (UTC-3) |
| `shortcode`, `media_id` | identificadores da publicação |
| `tipo_midia` | `p` (imagem), `reel`, `carrossel` |
| `vinculo` | `proprio` (autoria ACIRV) ou `colaboracao` |
| `parceiro_coautores` | conta parceira da colaboração |
| `promovido` | `sim`, `nao`, `nao_informado` |
| `visualizacoes`, `visualizadores`, `contas_meta_alcancadas` | alcance |
| `interacoes_raw`, `interacoes_posts_raw`, `interacoes_reels_raw` | interações |
| `curtidas_raw`, `comentarios_raw`, `compartilhamentos_raw`, `salvamentos_raw` | engajamento |
| `contas_com_engajamento_raw` | contas únicas que engajaram |
| `novos_seguidores_raw`, `novos_seguidores_normalizado` | seguidores ganhos |
| `atividade_do_perfil_raw`, `visitas_ao_perfil_raw`, `toques_em_links_externos_raw` | tráfego para o perfil |
| `pct_seguidores_alcance_raw`, `pct_nao_seguidores_alcance_raw` | divisão do alcance |
| `taxa_interacao_pct_raw` | `interacoes_raw / visualizacoes` em % |
| `metricas_ausentes` | rótulos sem valor no painel, separados por `;` |
| `notas` | observações de coleta (não é métrica) |
| `source_path`, `source_blob_sha` | rastreabilidade até a captura crua |
| `status_validacao` | estado de validação da linha |

A variante `_raw` marca coluna que preserva o valor como veio da fonte, sem arredondamento ou conversão.

### Contrato da base de stories

Separador `;`, UTF-8 sem BOM, CRLF, **30 colunas**, ordenação por `data_story` e `hora_story` decrescentes. Uma linha por story; o grão é o story, não o dia.

| Coluna | Semântica |
|---|---|
| `periodo_fonte` | mês coberto, `AAAA-MM` |
| `data_story`, `hora_story` | publicação do story em BRT (UTC-3) |
| `media_id` | identificador do story |
| `tipo_midia` | `imagem` ou `video` |
| `visualizacoes`, `visualizadores`, `alcance` | alcance do story |
| `views_seguidores`, `views_nao_seguidores` | abertura de `visualizacoes` por vínculo |
| `interacoes` | interações totais do story |
| `contas_com_engajamento` | contas únicas que engajaram |
| `curtidas_story`, `respostas`, `compartilhamentos`, `salvamentos` | engajamento próprio de story |
| `cliques_link` | toques na figurinha de link |
| `visitas_perfil`, `novos_seguidores` | tráfego gerado pelo story |
| `navegacoes`, `navegacoes_quebra` | navegação total e a quebra crua por tipo de ação |
| `descricao_visao`, `texto_sobreposto`, `natureza` | leitura por visão da capa (não é métrica do painel) |
| `metricas_ausentes` | rótulos sem valor no painel, separados por `;` |
| `formato_metricas` | `lista` ou `umapi` — de qual superfície o registro veio |
| `notas` | observações de coleta (não é métrica) |
| `source_path`, `source_blob_sha` | rastreabilidade até a captura crua |
| `status_validacao` | estado de validação da linha |

`descricao_visao`, `texto_sobreposto` e `natureza` não vêm do painel: são leitura assistida da capa e ficam marcadas como interpretação. `natureza` ∈ `foto`, `arte`, `video`, `print`. A distinção imagem × `video` é **conferida contra o tipo de mídia da captura** (`idx` -> `tipo`), não contra a tarja da folha de contato: em 273 células a tarja errou 7 vezes, e a coluna precisa concordar com o dado, não com a leitura.

## Bases existentes

- `Instagram-Publicacoes-2026-09.csv` — **116 linhas**, setembro/2026 completo. Ver [[Base-Instagram-Setembro-2026]].
- `Instagram-Stories-2026-09.csv` — **272 linhas**, stories de setembro/2026 (19 dias com story). Ver [[Stories-Instagram-Setembro-2026]].
- `Instagram-Publicacoes-2026-08-09.csv` — 138 linhas = **48 de agosto + 4 de julho mal-rotulados + 86 de setembro parcial**. O bloco de setembro está **superado** pela base de setembro completa; o bloco de **agosto está incompleto e com 4 datas erradas** — o feed de agosto tem **62** publicações (faltam 14: oito próprias de 24 e 28/08 e seis de colaboração). Laudo: `Hermes/instagram-insights/auditorias/AUDITORIA-2026-08.md`; ver [[Qualidade-dos-Dados-de-Marketing]].
- `Instagram-Publicacoes-Export-Meta-2025-2026.csv` — 200 linhas do export histórico da Meta. Ver [[Diagnostico-Longitudinal-Instagram-2025-2026]].

## Regras

1. Métrica ausente no painel é registrada como ausente (`metricas_ausentes`), nunca como zero.
2. Número que o painel não expõe não é substituído por estimativa; se houver um número de outra fonte, ele vai em `notas` com a fonte declarada.
3. Base mensal fechada é imutável; correção entra como nova versão com `status_validacao` explícito.
4. Toda linha aponta para a captura crua em `source_path`.
5. Script e captura crua ficam na camada 3 (`Hermes/instagram-insights/`), nunca em `000-Arquivos-originais/`.
6-bis. A **contagem** de publicações de um período é o conjunto de shortcodes da varredura do grid, nunca o total de um export ou de uma planilha: rode o portão (`Hermes/instagram-insights/ferramentas/publicacoes_feed.py auditar --periodo <AAAA-MM>` + `test_publicacoes_feed.py`) antes de publicar número. Export oficial é fonte **secundária de métricas** — pode estar incompleto e pode ter data publicada errada.
7. A base canônica é a **camada 1** da medição (post a post). Os totais do **painel da conta** (camada 2) ficam em captura própria e **nunca** entram nas colunas da base, nem são usados para ajustar o número de um post.

8. O **card mensal do app** e a nossa base contam conjuntos **diferentes**: o card conta o que a ACIRV publicou (setembro/2026: **13 reels + 55 posts + 272 stories**) e a base conta o que passou pelo feed (**116 = 60 da conta + 56 de parceiros**). Comparar um com o outro só faz sentido depois de separar por autoria (`vinculo` + `parceiro_coautores`). Ver [[Prints-do-App-Mobile-Setembro-2026]].

## As duas camadas (post a post × painel da conta)

A página **Insights** da conta mede outra coisa, e o número dela não é a soma dos posts:

| | Camada 1 — base canônica | Camada 2 — painel da conta |
|---|---|---|
| Fonte | `https://www.instagram.com/insights/media/<media_id>/` | `https://www.instagram.com/accounts/insights/?timeframe=30` |
| Unidade | a publicação | a conta, na janela móvel |
| Escopo | feed + reels do grid | Posts, Reels, **Stories**, Vídeos, split Instagram/Facebook |
| Contagem | visualizações acumuladas pelo post até a coleta | visualizações **ocorridas** na janela, em todo conteúdo |

Leitura verificada em 02/10/2026 (`timeframe=30`, janela ~03/09 a 02/10): painel **1.315.639** visualizações contra **497.290** somadas dos 116 posts de setembro. As causas, em ordem de peso: (1) janela móvel de 30 dias × período calendário; (2) Stories, Vídeos e Facebook fora do escopo dos posts; (3) o painel conta visualização por data em que ocorreu — conteúdo de meses anteriores conta, e uma coleta feita no meio do mês (a run 01–14/09 foi lida em 14/09) não tem as visualizações posteriores; (4) únicos por conteúdo não se somam.

Onde as camadas conversam: **interações** (painel 17.779 × base 18.414, −3,5%), porque 92% delas vêm de feed+reels; e as **magnitudes por conteúdo** da lista ranqueada. Visualizações nunca fecham — e não devem ser forçadas a fechar.

Lista ranqueada do painel (mesma origem, útil para conferência de magnitudes): `/accounts/insights/content/?media_type=all&metric=views&sort_by=highest&timeframe=30&view_type=card` — valores vêm abreviados (`99 mil`, `5,1 mil`) e `--` quando o painel não expõe o número.

Uma **terceira câmera** existe: o painel profissional do **celular** (prints). Ele mostra rótulos iguais com **escopos diferentes** — o card e a tela de views por tipo são do mês, a de interações por tipo é de 30 dias — e o card conta **só o conteúdo da conta**. Conciliação completa em [[Prints-do-App-Mobile-Setembro-2026]].

## Relações justificadas

- [[Fonte - Instagram Insights]] — define a origem.
- [[Base-Instagram-Setembro-2026]] — nota de métrica do mês fechado.
- [[Metricas-Consolidadas-por-Fonte]] — consolida as bases por fonte.
- [[Qualidade-dos-Dados-de-Marketing]] — registra inconsistências, inclusive a supersessão.
- [[Prints-do-App-Mobile-Setembro-2026]] — concilia os prints do app do celular com a base: autoria (116 × 55), validação 1:1 e resíduos.

## Fontes e rastreabilidade

- `97-Fontes-Brutas/01-Indices/Fonte - Instagram Insights.md`.
- `85-Bases-e-Consultas/Instagram-Publicacoes-2026-09.csv`.
- Pipeline: `Hermes/instagram-insights/README.md`.

## Limitações e revisão

Esta nota deve ser revisada quando a fonte, o responsável, a data, a metodologia ou o estado operacional mudar.
