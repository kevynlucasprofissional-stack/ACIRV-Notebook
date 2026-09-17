---
id: pendencia-validacoes-humanas-necessarias
titulo: Validacoes-Humanas-Necessarias
aliases: []
tipo: pendencia
status: auditado
profundidade: avancada
versao_schema: '1.0'
versao_conteudo: '1.1'
idioma: pt-BR
data_criacao: '2026-06-17'
ultima_revisao: '2026-09-17'
grau_confianca: alto
camadas_evidencia:
- fato_documentado
- interpretacao_operacional
tags:
- pendencia
fontes_documentais:
- '[[Fonte - Briefing do projeto]]'
notas_relacionadas:
- '[[Pendencias-Assumidas]]'
- '[[Riscos-Operacionais]]'
- '[[Registro-de-Decisoes]]'
- '[[Triagem-Inicial-000-Arquivos-Originais-2026-09-17]]'
confidencialidade: interno
subtipo: pendencia
---

# Validacoes-Humanas-Necessarias

> [!summary] Síntese
> Lista de confirmações que dependem de responsáveis da ACIRV ou de decisão humana consciente antes de serem tratadas como estado canônico.

## Estratégia

- Confirmar metas, linhas de base, proprietários e campanhas vigentes.
- Confirmar se a Campanha de Pertencimento deve ser tratada oficialmente como **maio/2026**; o planejamento anual contém conflito interno entre abril e maio, enquanto dossiê posterior sustenta maio.

## Governança

Confirmar cargos, alçadas, SLA, RACI e canal oficial de aprovação.

## Calendário

Confirmar datas, escopo e status de eventos e campanhas quando houver divergência entre planejamento e execução real.

## Conecta ACIRV

- Confirmar o valor oficial da **Cota Diamante** do Conecta 2026: uma mesma fonte registra R$ 20.000 e R$ 18.000.
- Validar a origem e a metodologia da cifra de **R$ 4 milhões** associada ao Conecta, distinguindo resultado histórico alegado de meta anual.

## Dados

Aprovar dicionário, tabela canônica e tratamento das divergências. Valores públicos de impacto devem registrar período, fonte e método.

## Marca

Confirmar V5 como manual vigente e política de submarcas.

## Segurança

- Rotacionar/revogar qualquer credencial real potencialmente versionada no repositório.
- Revisar `.env` e artefatos de protótipos sem expor valores em notas, issues ou PRs.
- Migrar credenciais ativas para gerenciador de segredos.
- Avaliar remoção humana segura de segredos do Git e, quando necessário, reescrita de histórico após rotação.
- Manter a regra de que agentes **não abrem** arquivos suspeitos de conter credenciais e **não alteram** `000-Arquivos-originais/`.

## Tecnologia

Decidir arquivar, revisar ou pilotar protótipos de SaaS e separar claramente experimento técnico de conhecimento institucional.

## Relações justificadas

- [[Pendencias-Assumidas]] — explica origem.
- [[Riscos-Operacionais]] — prioriza risco.
- [[Registro-de-Decisoes]] — deve receber confirmações.
- [[Triagem-Inicial-000-Arquivos-Originais-2026-09-17]] — registra evidências da ingestão inicial.

## Fontes e rastreabilidade

- [[Fonte - Briefing do projeto]]
- [[Triagem-Inicial-000-Arquivos-Originais-2026-09-17]]

## Limitações e revisão

Esta nota deve ser revisada quando uma validação for resolvida, quando novas divergências forem encontradas ou quando o estado operacional mudar.
