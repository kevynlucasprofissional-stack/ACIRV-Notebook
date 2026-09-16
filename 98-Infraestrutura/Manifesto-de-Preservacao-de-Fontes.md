---
id: infraestrutura-manifesto-de-preservacao-de-fontes
titulo: Manifesto-de-Preservacao-de-Fontes
aliases: []
tipo: infraestrutura
status: auditado
profundidade: avancada
versao_schema: '1.0'
versao_conteudo: '1.0'
idioma: pt-BR
data_criacao: '2026-06-17'
ultima_revisao: '2026-06-17'
grau_confianca: alto
camadas_evidencia:
- fato_documentado
- interpretacao_operacional
tags:
- infraestrutura
- fontes
fontes_documentais:
- '[[Fonte - Briefing do projeto]]'
notas_relacionadas:
- '[[Privacidade-e-Seguranca]]'
- '[[MOC-Fontes-e-Auditoria]]'
- '[[Relatorio-de-Auditoria-do-Vault]]'
confidencialidade: interno
subtipo: infraestrutura
---

# Manifesto-de-Preservacao-de-Fontes

> [!summary] Síntese
> Registro de como os anexos originais foram preservados sem misturar material bruto ao conhecimento curado.

## Original

`97-Fontes-Brutas/00-Original/Dados ACIRV.zip` é cópia byte a byte do upload; o briefing também foi copiado sem modificação.

## Selecionadas

Documentos centrais foram copiados para `02-Selecionadas` para acesso rápido. Os hashes permitem verificar identidade com a origem extraída.

## Não importado em massa

Markdowns, conversas e protótipos permanecem no ZIP original para evitar duplicidade, vazamento e poluição do grafo.

## Quarentena

`03-Quarentena` documenta riscos e não contém valores de credenciais.

## Proveniência

`manifesto-fontes.csv` registra caminho, tamanho e SHA-256.

## Relações justificadas

- [[Privacidade-e-Seguranca]] — define proteção.
- [[MOC-Fontes-e-Auditoria]] — navega fontes.
- [[Relatorio-de-Auditoria-do-Vault]] — valida hashes.

## Fontes e rastreabilidade

- [[Fonte - Briefing do projeto]]

## Limitações e revisão

Esta nota deve ser revisada quando a fonte, o responsável, a data, a metodologia ou o estado operacional mudar.
