---
id: metrica-base-instagram-setembro-2026
titulo: Base-Instagram-Setembro-2026
aliases:
- Setembro 2026 no Instagram
tipo: metrica
subtipo: base_derivada
status: revisado
profundidade: avancada
versao_schema: '1.0'
versao_conteudo: '1.1'
idioma: pt-BR
data_criacao: '2026-10-02'
ultima_revisao: '2026-10-02'
grau_confianca: alto
camadas_evidencia:
- fato_documentado
- interpretacao_operacional
tags:
- dominio/metricas
- dominio/canais
fontes_documentais:
- '85-Bases-e-Consultas/Instagram-Publicacoes-2026-09.csv'
- 'Hermes/instagram-insights/captura/setembro-2026/_painel_conta_2026-10-02_30.json'
- '97-Fontes-Brutas/01-Indices/Fonte - Instagram Insights.md'
- 'Hermes/instagram-insights/captura/setembro-2026/_setembro_2026_116.jsonl'
notas_relacionadas:
- '[[Instagram]]'
- '[[Metricas-Consolidadas-por-Fonte]]'
- '[[Qualidade-dos-Dados-de-Marketing]]'
- '[[LEIA-ME-Instagram-Insights]]'
- '[[Diagnostico-Instagram-Agosto-Setembro-2026]]'
confidencialidade: interno
---

# Base-Instagram-Setembro-2026

> [!summary] Síntese
> Setembro/2026 fechado no grão por publicação: **116 publicações** do grid do `@acirvoficial` entre 01/09 e 30/09, sendo 60 de autoria própria e 56 em colaboração. Soma de **497.290 visualizações** e **18.414 interações**. Base canônica em `85-Bases-e-Consultas/Instagram-Publicacoes-2026-09.csv`.

## Cobertura

A varredura do grid institucional foi feita em 02/10/2026 e retornou 204 itens entre 22/06 e 01/10/2026, dos quais **116 são de setembro**. A coleta foi feita em duas runs (01–14 e 15–30) e depois unificada; o resultado fecha **116 de 116** posts do inventário, em 25 dias com publicação.

| Corte | Posts | Visualizações | Interações |
|---|---:|---:|---:|
| Próprios | 60 | 273.917 | — |
| Em colaboração | 56 | 223.373 | — |
| Reels | 52 | 275.519 | 12.028 |
| Imagem | 64 | 221.771 | 6.386 |
| **Total** | **116** | **497.290** | **18.414** |

Distribuição por década do mês:

| Período | Posts | Visualizações | Interações |
|---|---:|---:|---:|
| 01 a 10/09 | 60 | 253.476 | 6.683 |
| 11 a 20/09 | 40 | 210.753 | 11.029 |
| 21 a 30/09 | 16 | 33.061 | 702 |

O terço final do mês concentra menos publicações e menos resultado: 16 posts e 33 mil visualizações, contra 60 posts e 253 mil na primeira década.

## Engajamento

| Métrica | Soma | Posts com valor | Mediana |
|---|---:|---:|---:|
| Curtidas | 14.797 | 116 | 39,5 |
| Comentários | 1.534 | 116 | 1 |
| Compartilhamentos | 1.969 | 116 | 3 |
| Salvamentos | 255 | 116 | 0 |
| Contas com engajamento | 15.762 | 114 | 42 |
| Visualizadores | 226.371 | 111 | 1.115 |
| Interações | 18.414 | 114 | 52 |

Relação agregada interações/visualizações: **3,70%**.

## Destaques do mês

| Data | Tipo | Vínculo | Visualizações | Interações | Curtidas |
|---|---|---:|---:|---:|---:|
| 12/09 | reel | colaboração `sarahdaotica` | 115.839 | 8.380 | 7.842 |
| 07/09 | reel | próprio | 53.845 | 97 | 76 |
| 01/09 | imagem | próprio | 16.473 | 755 | 369 |

O reel de 12/09 com `sarahdaotica` responde por **23,3%** de todas as visualizações do mês. O reel próprio de 07/09 tem volume alto e interação desproporcionalmente baixa, o que separa os dois casos: alcance e engajamento não andaram juntos em setembro.

Parceiros por visualizações somadas: `sarahdaotica` 115.839, `sudoexpo.oficial` 36.939, `gruposalus.rh` 7.043, `brenoalves.92` 5.557, `inovarioverde` 4.700, `raphael_valongo` 4.535.

## Qualidade da base

- 115 de 116 linhas com `status_validacao = completo_2026-09_insights_dom`.
- 1 linha com `colab_metricas_principais_indisponiveis_no_painel` (`media_id 3982692900246340349`, reel com `keniasleite` em 09/09): o painel da ACIRV não expõe visualizações, visualizadores nem interações para essa publicação. Os rótulos estão em `metricas_ausentes` e o número bruto da API pública ficou em `notas` — não é o mesmo metro do painel e não deve ser somado. **Prova da reverificação (02/10/2026):** `Hermes/instagram-insights/captura/setembro-2026/_verificacao_keniasleite_2026-10-02.json` — o painel entrega curtidas (210), comentários (28), salvamentos (2) e compartilhamentos (2) e devolve `--` para visualizações, visualizadores, interações, alcance e visitas ao perfil. É limitação do painel para reel colaborativo, não lacuna de coleta.
- Ausências recorrentes no rodapé do painel: `atividade_do_perfil` (56 linhas) e `novos_seguidores` (54). Ausência registrada, nunca convertida em zero.
- Sem duplicidade de `media_id` e sem linha sem curtidas.

## Conferência com o painel da conta (camada 2)

Esta base é a **camada 1** (post a post). O painel **Insights** da conta mede outra coisa e não fecha com a soma dos posts — leitura de 02/10/2026 com `timeframe=30` (janela móvel ~03/09 a 02/10):

| Métrica | Painel (30 dias) | Esta base (01–30/09) | Leitura |
|---|---:|---:|---|
| Visualizações | 1.315.639 | 497.290 | não comparável |
| Visualizadores | 260.569 | 226.371 (soma por post) | não comparável |
| Interações | 17.779 | 18.414 | **≈ igual (−3,5%)** |
| Contas com engajamento | 6.588 | 15.762 (soma por post) | não comparável |

Por que as visualizações divergem (2,6×), em ordem de peso: (1) o painel é janela móvel de 30 dias, não período calendário; (2) o escopo inclui **Stories** (31,2% das visualizações do painel), Vídeos e o split Instagram/Facebook (1.783); (3) o painel conta visualização pela **data em que ela ocorreu** — conteúdo de meses anteriores conta, e a run 01–14/09 foi lida em 14/09, antes das visualizações posteriores; (4) visualizadores e contas com engajamento são únicos por conteúdo no painel, enquanto aqui estão somados.

Onde as camadas conversam: **interações** (92% vêm de feed + reels) e as **magnitudes por conteúdo** da lista ranqueada do painel (`99 mil`, `49,9 mil`, `18,8 mil`, `14,2 mil`… contra 115.839 / 53.845 / 16.473 / 14.153 desta base) — mesma ordem, valores próximos, nunca idênticos.

Foto da camada 2: `Hermes/instagram-insights/captura/setembro-2026/_painel_conta_2026-10-02_30.json`.

## Superação

O bloco de setembro (86 linhas, `periodo_fonte = 2026-09-01_a_2026-09-14`) que existe dentro de `Instagram-Publicacoes-2026-08-09.csv` fica **superado** por esta base: cobria só 01–14/09 e omitia o post de 09/09 da `keniasleite`. Para análise de setembro, usar `Instagram-Publicacoes-2026-09.csv`.

## Relações justificadas

- [[Instagram]] — canal de origem.
- [[Metricas-Consolidadas-por-Fonte]] — consolida a base entre fontes.
- [[Qualidade-dos-Dados-de-Marketing]] — registra a supersessão e as ausências.
- [[LEIA-ME-Instagram-Insights]] — contrato do esquema de 34 colunas.
- [[Diagnostico-Instagram-Agosto-Setembro-2026]] — leitura de agosto em contraste.

## Fontes e rastreabilidade

- Base canônica: `85-Bases-e-Consultas/Instagram-Publicacoes-2026-09.csv` (116 linhas, 34 colunas, `;`, CRLF).
- Registros normalizados: `Hermes/instagram-insights/captura/setembro-2026/_setembro_2026_116.jsonl`.
- Captura crua por post: `Hermes/instagram-insights/captura/setembro-2026/_raw*.jsonl` (apontada em `source_path` de cada linha).
- Inventário do grid: `Hermes/instagram-insights/captura/setembro-2026/_grid_inventario2.json` (204 itens, 116 de setembro).
- Índice de fonte: [[Fonte - Instagram Insights]].
- Painel da conta (camada 2): `Hermes/instagram-insights/captura/setembro-2026/_painel_conta_2026-10-02_30.json`.

## Limitações e revisão

Esta nota deve ser revisada quando a fonte, o responsável, a data, a metodologia ou o estado operacional mudar.
