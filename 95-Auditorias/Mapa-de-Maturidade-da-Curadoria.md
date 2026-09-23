---
id: auditoria-mapa-maturidade-curadoria
titulo: Mapa-de-Maturidade-da-Curadoria
tipo: auditoria
status: ativo
versao_conteudo: '1.0'
idioma: pt-BR
data_criacao: '2026-09-23'
ultima_revisao: '2026-09-23'
grau_confianca: medio_alto
camadas_evidencia:
- interpretacao_operacional
tags:
- auditoria
- maturidade
- curadoria
- antirregressao
confidencialidade: interno
---

# Mapa-de-Maturidade-da-Curadoria

> [!summary] Função
> Controle de qualidade para orientar as auditorias diárias. O estado indica **quanto valor marginal ainda existe em nova curadoria**, não uma nota estética. Áreas excelentes devem permanecer estáveis até surgir evidência material que justifique reabertura.

## Estados

- **insuficiente** — fontes relevantes ainda não foram transformadas em inteligência utilizável.
- **em_evolucao** — existe estrutura, mas faltam cobertura, reconciliação ou narrativa importantes.
- **bom** — conhecimento já é útil e confiável; melhorias devem ser focais.
- **excelente** — cobertura e narrativa estão maduras para o escopo atual; proteger contra retrabalho cosmético.

## Baseline de 23/09/2026

| Área | Estado | Justificativa | Próximo gatilho legítimo |
|---|---|---|---|
| Priorização, capacidade e SCRUM | **bom** | Há diagnóstico de origem, regras de prioridade/capacidade, evidência de ritual semanal e agora narrativa longitudinal março→setembro. | Reconciliar backlog canônico com semântica real do Trello; validar limites/SLA propostos. |
| SudoExpo Match | **bom** | Projeto, trajetória, metodologia e próximo ciclo estão bem separados entre fato, hipótese e resultado. | Recomputação do JSON, pesquisas e follow-up comercial. |
| SudoExpo 2026 | **bom** | Planejamento, execução e pós-evento já formam narrativa forte com guardrails. | Fechar matriz Planejado×Entregue e resultados das pesquisas. |
| Instagram agosto 2026 | **bom** | Há série mensal, diagnóstico executivo e leitura Pago×Orgânico. | Reconciliar original×MASTER e regenerar gráfico inconsistente. |
| Tom de voz | **excelente** | Estado vigente V4.5/V5 versus V6 futura está validado; regras de legibilidade, limites e proveniência estão claros. | Nova versão formal aprovada ou evidência de mudança real de uso. |
| Backlog canônico | **em_evolucao** | A captura histórica é ampla, mas os 405 itens continuam não reconciliados e o Trello só agora entrou como fonte de estado. | Criar metodologia de reconciliação e fazer primeiro lote backlog×SCRUM. |
| Dados de associados/captação | **em_evolucao** | Meta existe, mas ainda falta definição e número canônico de novos associados de 2026. | Fonte institucional confirmada e definição da métrica. |
| Check-in inteligente | **em_evolucao** | Projeto e guardrails foram estruturados, porém ainda não existe piloto executado. | Primeiro Café com MVP e dados de operação. |

## Proteção antirregressão

### Tom de voz — excelente

Não reescrever por preferência estilística. Só reabrir se houver:

- nova versão formal do manual;
- mudança humana confirmada sobre V4.5/V5/V6;
- contradição documental;
- erro factual/proveniência.

### Áreas boas

Antes de editar, responder:

1. há fonte material nova?
2. existe lacuna semântica concreta?
3. a mudança adiciona entendimento ou apenas palavras?
4. a nova versão preserva as distinções epistemológicas já alcançadas?

Se a resposta for “não”, deixar intacta.

## Sessão de 23/09/2026

### Área aprofundada

**Priorização, capacidade e SCRUM.**

### Descoberta narrativa

O cruzamento entre transcrições de março, snapshots do SCRUM de agosto–setembro e reunião de 21/09 sustenta a história:

**prioridades concorrentes informais → quadro visível → ritual semanal → memória de execução → regras de capacidade e escalonamento.**

Promovido para [[Evolucao-do-Sistema-de-Priorizacao-e-Execucao]].

### Área preservada

**Tom de voz** foi classificado como excelente e não recebeu nova reescrita nesta sessão.

### Nova lacuna

O [[Backlog-Canonico-ACIRV]] precisa agora de reconciliação específica com o SCRUM; não é seguro usar apenas o atributo closed ou o nome da lista como verdade do estado atual.

## Regra de atualização

Este mapa muda quando a **qualidade do conhecimento** muda, não porque uma auditoria diária aconteceu. Não promover uma área de estado apenas por volume de texto produzido.
