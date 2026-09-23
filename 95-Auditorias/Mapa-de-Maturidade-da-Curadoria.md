---
id: mapa-maturidade-curadoria
titulo: Mapa de Maturidade da Curadoria
tipo: auditoria
status: ativo
profundidade: avancada
versao_schema: '1.0'
versao_conteudo: '1.0'
idioma: pt-BR
data_criacao: '2026-09-23'
ultima_revisao: '2026-09-23'
grau_confianca: medio_alto
tags: [auditoria, curadoria, maturidade, antirregressao]
confidencialidade: interno
---

# Mapa de Maturidade da Curadoria

> [!summary] Função
> Controle persistente para orientar auditorias futuras. `excelente` significa proteger de retrabalho cosmético; não significa que o domínio nunca mais possa mudar. Uma área só deve ser reaberta quando houver fonte nova material, contradição, desatualização, erro ou melhoria semanticamente superior.

## Critérios

A maturidade considera em conjunto: cobertura das fontes relevantes, qualidade semântica, qualidade narrativa, utilidade operacional, proveniência, separação entre fato e interpretação, tratamento de contradições, atualidade, conectividade e redundância.

| Domínio / nota | Estado | Evidência da avaliação | Próximo gatilho legítimo |
|---|---|---|---|
| [[SudoExpo-Match]] + [[SudoExpo-Match-Metodologia-de-Avaliacao]] | `bom` | A narrativa já reconstrói origem, renomeação, Café, escala na SudoExpo, próximo ciclo e limites epistemológicos. A metodologia separa comportamento interno de resultado econômico. Ainda faltam recomputação da base, pesquisas e follow-up. | Resultados recalculados; reconciliação das pesquisas; evidência do próximo Café; follow-up das conexões. |
| [[Plano-Operacional-21-22-09-2026]] | `bom` | Converte reunião em direções, ações, lacunas e dependências sem confundir intenção com execução. | Reconciliação com SCRUM/Trello e evidência de execução posterior. |
| [[Backlog-Canonico-ACIRV]] | `em_evolucao` | O próprio arquivo declara 405 itens históricos não reconciliados e registra que o Trello não havia sido consultado. O commit `9f3c9a55df6cb268035d5b60ae497a21750601ee` adicionou sete exports do SCRUM, abrindo uma nova fonte primária para reconciliação. | Parse confiável dos exports do SCRUM, deduplicação entre snapshots e cruzamento com backlog histórico. |
| Curadoria do delta do HD externo | `bom` | A auditoria de 22/09 deduplicou por SHA, preservou versões superiores, aplicou Safety Gate e promoveu conhecimento material; também registrou explicitamente que não leu os 3.020 arquivos integralmente. | Novos lotes, conversões de formatos pendentes ou execução determinística que revele lacunas. |

## Regra antirregressão

1. Não reescrever áreas `bom`/`excelente` apenas para mudar estilo.
2. Preferir fechar lacunas explicitamente registradas a aumentar volume de texto.
3. Uma nova fonte não invalida automaticamente o cânone: primeiro verificar se é nova evidência, snapshot histórico, duplicata ou versão inferior.
4. Narrativas transversais devem separar fatos documentados, dados calculados e inferências.

## Auditoria 2026-09-23 — chegada do SCRUM

O `main` recebeu o commit `9f3c9a55df6cb268035d5b60ae497a21750601ee` (`Dados do SCRUM da ACIRV`), com sete exports JSON sob `000-Arquivos-originais/SCRUM da ACIRV + Vcom/`. Isso altera materialmente a maturidade do domínio de backlog porque [[Backlog-Canonico-ACIRV]] havia sido construído, de propósito, sem consultar o Trello/SCRUM.

A história que as fontes passam a contar é prudente, mas importante: primeiro foi criado um inventário histórico amplo de ações potenciais; depois surgiu uma fonte operacional capaz de ajudar a distinguir memória de trabalho de estado recente. **Ainda não é correto afirmar quais tarefas estão abertas ou concluídas**, porque os sete arquivos precisam ser interpretados como snapshots/exportações, deduplicados e reconciliados antes de promover estado operacional.

Essa lacuna tem prioridade maior que reescrever [[SudoExpo-Match]], que já está semanticamente bem estruturado e explicita as próprias pendências quantitativas.

### Fontes

- `08-Agenda-e-Execucao/Backlog-Canonico-ACIRV.md` — registra 405 itens não reconciliados e ausência de consulta ao Trello na etapa inicial.
- commit `9f3c9a55df6cb268035d5b60ae497a21750601ee` — adiciona os exports do SCRUM em `000-Arquivos-originais/SCRUM da ACIRV + Vcom/`.
- `95-Auditorias/Curadoria-Delta-HD-Externo-2026-09-22.md` — estabelece o ponto de corte e o método de deduplicação/Safety Gate da auditoria anterior.
- `03-Projetos-Campanhas-e-Eventos/SudoExpo-Match.md` e `05-Metricas-e-Decisao/SudoExpo-Match-Metodologia-de-Avaliacao.md` — amostra antirregressão usada nesta sessão.
