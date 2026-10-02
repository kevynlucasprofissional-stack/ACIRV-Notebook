---
id: metrica-diagnostico-longitudinal-instagram-2025-2026
titulo: Diagnostico-Longitudinal-Instagram-2025-2026
aliases: [Base longitudinal Instagram 2025-2026]
tipo: metrica
status: auditado
profundidade: avancada
versao_schema: '1.0'
versao_conteudo: '1.0'
idioma: pt-BR
data_criacao: '2026-09-22'
ultima_revisao: '2026-09-22'
grau_confianca: alto
camadas_evidencia:
- fato_documentado
- dado_calculado
- interpretacao_operacional
tags:
- metricas
- instagram
- conteudo
- longitudinal
fontes_documentais:
- '000-Arquivos-originais/DADOS ACIRV - HD EXTERNO/Dados instagram - 100425 até 100426/logged_information/past_instagram_insights/posts.json'
- '85-Bases-e-Consultas/Instagram-Publicacoes-Export-Meta-2025-2026.csv'
notas_relacionadas:
- '[[Instagram]]'
- '[[Diagnostico-de-84-Posts]]'
- '[[Resumo-Instagram-90-Dias]]'
confidencialidade: interno
subtipo: analise_longitudinal
---

# Diagnostico-Longitudinal-Instagram-2025-2026

> [!summary] Síntese
> O export histórico da Meta contém **200 registros de publicação entre 22/04/2025 e 10/04/2026**. A base foi normalizada em `85-Bases-e-Consultas/Instagram-Publicacoes-Export-Meta-2025-2026.csv`. Esta análise é descritiva e mantém o grão por publicação separado dos totais da conta.

## Cobertura

- registros: **200**;
- primeira publicação encontrada: **22/04/2025**;
- última: **10/04/2026**;
- origem: `past_instagram_insights/posts.json`;
- blob da fonte: `32e452c2d6101cea98aaccf47bb39ea37d0836bc`.

O nome da pasta da exportação indica 10/04/2025–10/04/2026, mas os registros de post efetivamente encontrados começam em 22/04/2025.

## Somas no grão publicação

Somando apenas os campos de cada uma das 200 linhas:

- impressões: **275.393**;
- alcance: **210.171** em 198 registros com valor;
- curtidas: **5.621**;
- comentários: **566**;
- compartilhamentos: **982**;
- salvamentos: **136**;
- interações calculadas (curtidas + comentários + compartilhamentos + salvamentos): **7.305**;
- visitas ao perfil atribuídas às linhas: **1.126**;
- seguidores gerados atribuídos às linhas: **160**;
- toques em link externo: **223** em 43 registros com valor.

Essas somas **não são totais oficiais da conta** e não devem ser reconciliadas por igualdade com janelas agregadas de Insights.

## Concentração temporal observada

Por soma de interações calculadas nas linhas:

- set/2025: **1.839** em 31 posts;
- out/2025: **1.271** em 32 posts;
- mai/2025: **1.031** em 20 posts;
- jun/2025: **602** em 18 posts.

Totais brutos por mês misturam quantidade de publicações, distribuição, tema e possíveis diferenças de disponibilidade de métricas. Eles servem para localizar períodos a investigar, não para declarar “melhor mês”.

## Publicações que se destacam na base

### Alcance

- 29/07/2025 — conteúdo Pirulito & Violão: **27.132** contas alcançadas;
- 16/12/2025 — ACIRV na 96 FM: **20.017**.

### Seguidores atribuídos

- 04/08/2025 — chamada do Festival Barzinho e Violão: **35** seguidores e **275** visitas ao perfil;
- 16/12/2025 — ACIRV na 96 FM: **15** seguidores.

### Compartilhamentos

- 15/09/2025 — Café Entre Amigos: **57**;
- 30/05/2025 — Assembleia Geral: **44**;
- 24/10/2025 — Grupo Futura: **36**.

Esses casos são candidatos a análise qualitativa de tema, CTA, distribuição e contexto. Não provam causalidade de formato.

## Relação com o diagnóstico de 84 posts

`[[Diagnostico-de-84-Posts]]` permanece como **amostra histórica com metodologia própria**. Ele não deve ser sobrescrito pela nova base. A série de 200 registros amplia a cobertura e passa a ser a referência longitudinal para consultas compatíveis com seu schema.

## Base derivada

`85-Bases-e-Consultas/Instagram-Publicacoes-Export-Meta-2025-2026.csv` preserva:

- linha de origem;
- data/hora em BRT;
- id de mídia quando disponível;
- legenda;
- métricas individuais;
- interação calculada;
- caminho e SHA da fonte;
- status de validação.

## Limitações

- o JSON não oferece um campo de formato suficientemente confiável para classificar todas as linhas como feed, carrossel ou reel;
- duas linhas não trazem alcance;
- alguns registros não expõem id de mídia na miniatura;
- disponibilidade de campos varia;
- a soma de posts não equivale ao total da conta;
- mídia paga e coautoria não estão normalizadas com a mesma riqueza dos workbooks de ago/set 2026.

## Fontes e rastreabilidade

- fonte primária: `000-Arquivos-originais/DADOS ACIRV - HD EXTERNO/Dados instagram - 100425 até 100426/logged_information/past_instagram_insights/posts.json`;
- blob: `32e452c2d6101cea98aaccf47bb39ea37d0836bc`;
- base derivada: `85-Bases-e-Consultas/Instagram-Publicacoes-Export-Meta-2025-2026.csv`.
