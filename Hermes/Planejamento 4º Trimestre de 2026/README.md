# Hermes — Planejamento 4º Trimestre de 2026

Este diretório é o workspace operacional do Hermes para executar o Social Media da ACIRV entre 16/09 e 31/12/2026.

## Ordem de leitura
1. `00_EXECUTAR_COM_HERMES.md`
2. `01-planejamento/PLANEJAMENTO_ESTRATEGICO.md`
3. `01-planejamento/calendario/CALENDARIO_CANONICO.json`
4. `02-estado/execution_state.json`
5. `03-integracoes/trello_destination.json`
6. `03-integracoes/RECONCILIACAO_TRELLO_INICIAL.md`
7. `04-moodboard/README.md`
8. `05-auditoria/README.md`

## Fonte canônica
Para automação:
- plano editorial: `01-planejamento/calendario/CALENDARIO_CANONICO.json`;
- estado mutável: `02-estado/execution_state.json`.

A versão completa com todos os briefings, planilha XLSX, CSV e arquivos auxiliares também foi entregue ao usuário no pacote corrigido. O JSON no repositório funciona como índice canônico e idempotente das 44 publicações; o Hermes deve cruzá-lo com o planejamento estratégico e as fontes do Notebook antes de escrever no Trello.

## Trello
Destino confirmado:
- `Calendário Editorial` — `622e83218d717e4a16d7856c`
- `ORDEM DE SERVIÇO - SAMARA` — `69370019555b10bb6ad19e30`

Antes da primeira escrita, fazer preflight dos IDs. Não substituir automaticamente por outro quadro/lista.

## Regra de separação
- **Planejamento** = intenção aprovada, muda apenas por replanejamento explícito.
- **Estado** = progresso da execução, muda a cada ação.
- **Integrações** = IDs, contratos externos e reconciliação com legado.
- **Moodboard** = referências visuais versionadas.
- **Auditoria** = evidência e reconciliação.

Essa separação evita que o Hermes reescreva o plano ao atualizar o próprio progresso.
