---
id: consulta-leia-me-instagram-insights
titulo: LEIA-ME-Instagram-Insights
aliases: []
tipo: consulta
subtipo: guia_tecnico
status: revisado
profundidade: avancada
versao_schema: '1.0'
versao_conteudo: '1.0'
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

## Bases existentes

- `Instagram-Publicacoes-2026-09.csv` — **116 linhas**, setembro/2026 completo. Ver [[Base-Instagram-Setembro-2026]].
- `Instagram-Publicacoes-2026-08-09.csv` — 138 linhas, agosto (52) + setembro parcial (86). O bloco de setembro está **superado** pela base de setembro completa; ver [[Qualidade-dos-Dados-de-Marketing]].
- `Instagram-Publicacoes-Export-Meta-2025-2026.csv` — 200 linhas do export histórico da Meta. Ver [[Diagnostico-Longitudinal-Instagram-2025-2026]].

## Regras

1. Métrica ausente no painel é registrada como ausente (`metricas_ausentes`), nunca como zero.
2. Número que o painel não expõe não é substituído por estimativa; se houver um número de outra fonte, ele vai em `notas` com a fonte declarada.
3. Base mensal fechada é imutável; correção entra como nova versão com `status_validacao` explícito.
4. Toda linha aponta para a captura crua em `source_path`.
5. Script e captura crua ficam na camada 3 (`Hermes/instagram-insights/`), nunca em `000-Arquivos-originais/`.

## Relações justificadas

- [[Fonte - Instagram Insights]] — define a origem.
- [[Base-Instagram-Setembro-2026]] — nota de métrica do mês fechado.
- [[Metricas-Consolidadas-por-Fonte]] — consolida as bases por fonte.
- [[Qualidade-dos-Dados-de-Marketing]] — registra inconsistências, inclusive a supersessão.

## Fontes e rastreabilidade

- `97-Fontes-Brutas/01-Indices/Fonte - Instagram Insights.md`.
- `85-Bases-e-Consultas/Instagram-Publicacoes-2026-09.csv`.
- Pipeline: `Hermes/instagram-insights/README.md`.

## Limitações e revisão

Esta nota deve ser revisada quando a fonte, o responsável, a data, a metodologia ou o estado operacional mudar.
