---
id: metrica-riscos-operacionais
titulo: Riscos-Operacionais
aliases: []
tipo: metrica
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
- risco
- operacao
fontes_documentais:
- '[[Fonte - Notas Operacionais]]'
- '[[Fonte - Dados Marketing]]'
- '[[Fonte - Conversas WhatsApp]]'
notas_relacionadas:
- '[[Privacidade-e-Seguranca]]'
- '[[Qualidade-dos-Dados-de-Marketing]]'
- '[[Gestao-de-Capacidade-e-WIP]]'
confidencialidade: interno
subtipo: registro_risco
---

# Riscos-Operacionais

> [!summary] Síntese
> Registro consolidado de riscos observados no corpus e no processo de construção.

## R1 — credenciais

Arquivos com senhas/chaves e `.env` em ZIPs internos. Ação: restringir, rotacionar, inventariar e migrar para gerenciador.

## R2 — versão

Múltiplas versões de tom de voz, processos e artefatos. Ação: declarar vigente e arquivar histórico.

## R3 — canal informal

Demandas e decisões em WhatsApp. Ação: converter em card/registro.

## R4 — dados

Tipos e períodos inconsistentes. Ação: tabela canônica e fechamento.

## R5 — capacidade

Oscilação e sobrecarga. Ação: WIP, prioridade e trade-off explícito.

## R6 — privacidade

Conversas, contatos e dossiês pessoais. Ação: minimização, controle de acesso e política.

## R7 — software experimental

Protótipos com dependências/segredos. Ação: revisão técnica antes de execução.

## Relações justificadas

- [[Privacidade-e-Seguranca]] — trata R1/R6.
- [[Qualidade-dos-Dados-de-Marketing]] — trata R4.
- [[Gestao-de-Capacidade-e-WIP]] — trata R5.

## Fontes e rastreabilidade

- [[Fonte - Notas Operacionais]]
- [[Fonte - Dados Marketing]]
- [[Fonte - Conversas WhatsApp]]

## Limitações e revisão

Esta nota deve ser revisada quando a fonte, o responsável, a data, a metodologia ou o estado operacional mudar.
