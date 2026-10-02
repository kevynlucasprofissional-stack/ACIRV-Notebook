---
id: fonte-fonte-instagram-insights
titulo: Fonte - Instagram Insights
aliases: []
tipo: fonte
subtipo: fonte_dados
status: revisado
profundidade: intermediaria
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
- dominio/fontes
fontes_documentais: []
notas_relacionadas:
- '[[LEIA-ME-Instagram-Insights]]'
- '[[Base-Instagram-Setembro-2026]]'
- '[[Instagram]]'
confidencialidade: interno
---

# Fonte - Instagram Insights

> [!summary] Síntese
> Índice da fonte que origina as métricas de publicação do Instagram institucional `@acirvoficial`: o painel de insights post a post. A captura é feita pelo agente e o dado consolidado vive na camada canônica.

## O que esta fonte produz

O painel `instagram.com/insights/media/<media_id>/` entrega, por publicação: visualizações, visualizadores, contas Meta alcançadas, interações (e a quebra entre posts e reels), curtidas, comentários, compartilhamentos, salvamentos, contas com engajamento, novos seguidores, atividade do perfil, visitas ao perfil, toques em links externos e a divisão percentual entre seguidores e não seguidores.

O grão é **uma linha por publicação**. Totais de conta (seguidores do perfil, alcance do período) não saem daqui e continuam vindo de [[Fonte - Dados Marketing]] e do export histórico da Meta.

## Onde a fonte bruta está

- Export manual (XLSX), camada original, somente leitura para IA:
  - `000-Arquivos-originais/Dados para mega-relatório pós Sudoexpo/Redes sociais/instagram_acirvoficial_insights_agosto_2026.xlsx`;
  - `.../instagram_acirvoficial_insights_agosto_2026_MASTER(1).xlsx`;
  - `.../instagram_acirvoficial_insights_setembro_2026.xlsx`.
- Captura crua do agente (JSONL, camada 3): `Hermes/instagram-insights/captura/<mes>-<ano>/`.
- Export histórico da Meta: `000-Arquivos-originais/DADOS ACIRV - HD EXTERNO/Dados instagram - 100425 até 100426/logged_information/past_instagram_insights/posts.json`.

## Regra de uso

O painel é a fonte do grão por publicação; o XLSX é o recorte que o humano salvou. Divergência entre os dois não é corrigida em silêncio: entra em [[Qualidade-dos-Dados-de-Marketing]].

Métricas ausentes no painel (rótulo sem valor numérico, ou `--`) são registradas como ausentes, nunca como zero.

## Relações justificadas

- [[LEIA-ME-Instagram-Insights]] — dicionário da base derivada.
- [[Base-Instagram-Setembro-2026]] — primeira aplicação completa desta fonte.
- [[Instagram]] — canal que consome o dado.

## Fontes e rastreabilidade

- Painel: `https://www.instagram.com/insights/media/<media_id>/` (sessão autenticada do `@acirvoficial`).
- API pública de apoio (quando o painel não expõe o dado): `https://www.instagram.com/api/v1/media/<media_id>/info/`.
- Captura crua: `Hermes/instagram-insights/captura/`.
- Base derivada: `85-Bases-e-Consultas/Instagram-Publicacoes-<AAAA-MM>.csv`.

## Limitações e revisão

Esta nota deve ser revisada quando a fonte, o responsável, a data, a metodologia ou o estado operacional mudar.
