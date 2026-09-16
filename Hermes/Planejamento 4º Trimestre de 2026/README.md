# Hermes — Planejamento 4º Trimestre de 2026

Este diretório é o workspace operacional do Hermes para executar o Social Media da ACIRV entre 16/09 e 31/12/2026.

## Ordem de leitura
1. `00_EXECUTAR_COM_HERMES.md`
2. `01-planejamento/PLANEJAMENTO_ESTRATEGICO.md`
3. `01-planejamento/CALENDARIO_EDITORIAL.csv`
4. `02-estado/execution_state.json`
5. `03-integracoes/trello_destination.json`
6. `04-moodboard/README.md`
7. `05-auditoria/README.md`

## Fonte canônica
Para automação, a fonte canônica é:
- plano editorial: `01-planejamento/CALENDARIO_EDITORIAL.csv`;
- estado mutável: `02-estado/execution_state.json`.

O XLSX existe como visão humana/gerencial no pacote entregue ao usuário, mas o Hermes deve preferir CSV + JSON para execução.

## Trello
Destino:
- `Calendário Editorial` — `622e83218d717e4a16d7856c`
- `ORDEM DE SERVIÇO - SAMARA` — `69370019555b10bb6ad19e30`

## Regra de separação
- **Planejamento** = intenção aprovada, muda apenas por replanejamento explícito.
- **Estado** = progresso da execução, muda a cada ação.
- **Integrações** = IDs e contratos externos.
- **Moodboard** = referências visuais versionadas.
- **Auditoria** = evidência e reconciliação.

Essa separação evita que o Hermes reescreva o plano ao atualizar o próprio progresso.
