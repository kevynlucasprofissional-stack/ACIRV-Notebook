---
id: processo-gestao-de-capacidade-e-wip
titulo: Gestao-de-Capacidade-e-WIP
aliases: []
tipo: processo
status: auditado
profundidade: avancada
versao_schema: '1.0'
versao_conteudo: '1.3'
idioma: pt-BR
data_criacao: '2026-06-17'
ultima_revisao: '2026-09-23'
grau_confianca: medio_alto
camadas_evidencia:
- fato_documentado
- interpretacao_operacional
- hipotese_de_trabalho
tags:
- operacao
fontes_documentais:
- '[[Fonte - Reunioes de Junho 2026]]'
- '[[Fonte - Notas Operacionais]]'
- '000-Arquivos-originais/HD-ACIRV/03-Metricas-e-Relatorios/KEVYN-DADOS-ACIRV/Documentos/Relatório de métrica Março parte 2 de 2.txt'
- '000-Arquivos-originais/SCRUM da ACIRV + Vcom/GDM8ZE3r - acirv-vcom-scrum (6).json'
notas_relacionadas:
- '[[Criterios-de-Priorizacao-de-Marketing]]'
- '[[Quadro-Operacional-Kanban]]'
- '[[Ritual-Semanal-de-Priorizacao]]'
- '[[Evolucao-da-Operacao-de-Marketing-2026]]'
- '[[Evolucao-do-Sistema-de-Priorizacao-e-Execucao]]'
confidencialidade: interno
subtipo: processo
---

# Gestao-de-Capacidade-e-WIP

> [!summary] Síntese
> Política para proteger a equipe de sobrecarga e tornar explícito o custo de inserir novas urgências.

## Sinal observado

A série preservada no SCRUM mostra semanas com listas de finalizados variando de **8 a 52 cards** entre abril e setembro. A variação é compatível com mistura de granularidade, sazonalidade e pressão operacional — especialmente no ciclo da SudoExpo. O número de cards, sozinho, **não mede produtividade**.

A leitura longitudinal e seus limites estão em [[Evolucao-do-Sistema-de-Priorizacao-e-Execucao]].

## Evidência longitudinal do SCRUM

O snapshot mais recente do board **ACIRV + VCOM: SCRUM** registra **23 listas semanais de finalização entre 13/04 e 19/09**, somando **644 cards**. A variação semanal vai de **8 a 52 cards**, com média simples de 28.

Essa série confirma que o volume de cards varia muito ao longo do calendário, mas **não autoriza usar quantidade de cards como produtividade**: as unidades têm granularidades diferentes.

O valor do board é principalmente tornar fluxo, temas e ciclos de fechamento observáveis.

A narrativa completa está em [[Evolucao-da-Operacao-de-Marketing-2026]].

> Fonte: 000-Arquivos-originais/SCRUM da ACIRV + Vcom/GDM8ZE3r - acirv-vcom-scrum (6).json — blob 4997fef9b93dcd1fd751ac7817bdf09bbf384b89.

## Limites propostos

Por responsável: até 3 itens em produção, 2 em revisão e 1 urgência. Eventos próximos podem reservar capacidade própria. Mudança de limite precisa ser registrada.

## Capacidade não é contagem de entregas

A transcrição de março registra uma tentativa de resolver uma distorção recorrente: **dez tarefas pequenas não são diretamente comparáveis a uma implementação grande**, e dificuldade, duração e importância são dimensões diferentes.

Naquele momento foi cogitado um sistema de pontos dado por stakeholders. O número e a fórmula não foram promovidos porque eram exploração, não regra aprovada.

O aprendizado canônico é manter três perguntas separadas:

1. **prioridade:** quão importante/urgente é o resultado?
2. **esforço:** quanto trabalho e complexidade exige?
3. **capacidade:** quanto espaço real existe no período?

Isso evita usar volume de cards como produtividade e evita prometer mais trabalho apenas porque os itens têm nomes igualmente curtos.

> Fonte: `000-Arquivos-originais/HD-ACIRV/03-Metricas-e-Relatorios/KEVYN-DADOS-ACIRV/Documentos/Relatório de métrica Março parte 2 de 2.txt` — blob `96d0b18ae5f7f8d9259ae11608c252f65d73742b`.

## Classes de tamanho

S: até 2 horas; M: até 1 dia; L: 2–3 dias; XL: quebrar antes de entrar. Tamanho mede esforço aproximado, não importância.

## Replanejamento

Ao entrar um P0/P1 não previsto, escolher explicitamente qual item será pausado. Itens bloqueados saem do WIP ativo e recebem causa e próximo acompanhamento.

## Relações justificadas

- [[Criterios-de-Priorizacao-de-Marketing]] — define prioridade.
- [[Quadro-Operacional-Kanban]] — visualiza WIP.
- [[Ritual-Semanal-de-Priorizacao]] — revisa capacidade.

## Fontes e rastreabilidade

- [[Fonte - Reunioes de Junho 2026]]
- [[Fonte - Notas Operacionais]]

## Limitações e revisão

Esta nota deve ser revisada quando a fonte, o responsável, a data, a metodologia ou o estado operacional mudar.

## Dados disponíveis nas fontes

Esta nota possui informações complementares nos seguintes arquivos-fonte:

- `Dados ACIRV/Notas\(RELATÓRIO MÉTRICAS) - Fevereiro.md`
- `Dados ACIRV/Notas\(RELATÓRIO MÉTRICAS) - Janeiro.md`
- `Dados ACIRV/Notas\(RELATÓRIO MÉTRICAS) - Março.md`
- `Dados ACIRV/Notas\Como fazer o relatório de março ser de alto nível.md`
- `Dados ACIRV/Notas\Como melhorar o relatório mensal.md`

> **Status da integração**: Dados identificados. Aguardando extração e incorporação dirigida.
