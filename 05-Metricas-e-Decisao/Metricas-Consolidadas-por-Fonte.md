---
id: metrica-consolidada-por-fonte
titulo: Metricas-Consolidadas-por-Fonte
aliases: []
tipo: metrica
status: auditado
profundidade: avancada
versao_schema: '1.0'
versao_conteudo: '1.1'
idioma: pt-BR
data_criacao: '2026-06-18'
ultima_revisao: '2026-09-22'
grau_confianca: medio_alto
tags:
- metricas
- consolidacao
fontes_documentais:
- '[[Fonte - Dados Marketing]]'
- '[[Fonte - Fontes Especificas da Retomada]]'
notas_relacionadas:
- '[[Historico-de-KPIs-Mensais]]'
- '[[Qualidade-dos-Dados-de-Marketing]]'
confidencialidade: interno
subtipo: consolidacao
---

# Métricas Consolidadas por Fonte

> [!summary] Índice de fontes quantitativas e do estado de sua promoção. A lista histórica por regex continua preservada, mas Instagram agora possui fontes estruturadas e bases derivadas rastreáveis.

## Instagram — fontes estruturadas atuais

| Fonte | Grão / período | Estado |
|---|---|---|
| `past_instagram_insights/audience_insights.json` | audiência, 10/01–09/04/2026 | curado |
| `content_interactions.json` | interações, 10/01–09/04/2026 | curado |
| `profiles_reached.json` | alcance/funil, 10/01–09/04/2026 | curado |
| `past_instagram_insights/posts.json` | 200 publicações, 22/04/2025–10/04/2026 | normalizado |
| `instagram_acirvoficial_insights_agosto_2026.xlsx` | 52 publicações, agosto | fonte preservada |
| `instagram_acirvoficial_insights_agosto_2026_MASTER(1).xlsx` | 52 publicações, agosto | **fonte preferida por publicação** |
| `instagram_acirvoficial_insights_setembro_2026.xlsx` | 86 publicações, 01–14/09 | curado como parcial |

## Bases derivadas de Instagram

- `85-Bases-e-Consultas/Instagram-Publicacoes-Export-Meta-2025-2026.csv` — 200 linhas;
- `85-Bases-e-Consultas/Instagram-Publicacoes-2026-08-09.csv` — 138 linhas;
- [[Perfil-da-Audiencia-Instagram]];
- [[Diagnostico-Longitudinal-Instagram-2025-2026]];
- [[Diagnostico-Instagram-Agosto-Setembro-2026]].

## Fontes de métricas identificadas em Dados ACIRV

- `Notas\(MÉTRICAS) - 2025.md` — 10 valores numéricos identificados
- `Notas\(RELATÓRIO MÉTRICAS) - Fevereiro.md` — 3 valores numéricos identificados
- `Notas\(RELATÓRIO MÉTRICAS) - Janeiro.md` — 3 valores numéricos identificados
- `Notas\(RELATÓRIO MÉTRICAS) - Março.md` — 4 valores numéricos identificados
- `Notas\00_DASHBOARD ACIRV.md` — 1 valores numéricos identificados
- `Notas\Como fazer o relatório de março ser de alto nível.md` — 1 valores numéricos identificados
- `Notas\Como melhorar o relatório mensal.md` — 1 valores numéricos identificados
- `Notas\Como é realizado a reunião de apresentação de Métricas de todo dia 30 - Modelo da Vivi.md` — 3 valores numéricos identificados
- `Notas\Contraproposta para o relatório de abril.md` — 1 valores numéricos identificados
- `Notas\Dados sobre o Conecta Saúde 2º ed..md` — 7 valores numéricos identificados
- `Notas\Todos os dados para relatório de métricas.md` — 10 valores numéricos identificados
- `Notas\Todos os relatórios de tráfego de 161025 até 100426.md` — 4 valores numéricos identificados
- `TODAS AS NOTAS DA ACIRV\(RELATÓRIO MÉTRICAS) - 2025.md` — 10 valores numéricos identificados
- `TODAS AS NOTAS DA ACIRV\(RELATÓRIO MÉTRICAS) - Janeiro.md` — 3 valores numéricos identificados
- `TODAS AS NOTAS DA ACIRV\Como é realizado a reunião de apresentação de Métricas de todo dia 30 - Modelo da Vivi.md` — 3 valores numéricos identificados

## Fontes de métricas no vault (legado)

- `000 - Notas/(MÉTRICAS) - 2025.md`
- `000 - Notas/(RELATÓRIO MÉTRICAS) - Janeiro.md` a `Maio.md`
- `000 - Notas/00_DASHBOARD ACIRV.md`
- `000 - Notas/(DADOS RELATÓRIO MÉTRICAS) - Março.md`

## Status da extração

15 fontes legadas continuam inventariadas por regex. Para Instagram, a extração estruturada foi promovida e reconciliada com preservação de grão, período, valor bruto, fonte e SHA. Validação humana continua necessária quando a semântica da própria fonte é ambígua.

## Relações justificadas

- [[Historico-de-KPIs-Mensais]] — série oficial.
- [[Qualidade-dos-Dados-de-Marketing]] — avalia confiabilidade.
- [[Diagnostico-Instagram-Agosto-Setembro-2026]] — documenta a reconciliação atual.

## Limitações e revisão

A seção legada continua sujeita às limitações da extração por regex. As novas bases de Instagram têm schema explícito, mas ainda exigem leitura de período, unidade, disponibilidade de campo e mudança metodológica antes de comparação.
