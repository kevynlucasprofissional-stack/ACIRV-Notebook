# Planejamento 4º Trimestre de 2026 — ACIRV Social Media

Período operacional: **16/09/2026 a 31/12/2026**.

## Plano atual

Este workspace contém somente o planejamento vigente para execução:

`01-planejamento/v2/README.md`

Escopo:
- **60 publicações estáticas** para a designer Samara;
- **0 Reels/vídeos** no escopo da designer;
- IDs `001–044` preservados;
- IDs `045–060` = 16 peças leves de **2 slides exatos: capa + CTA**;
- aprofundamento das peças extras na legenda;
- briefing de produção completo antes do Trello;
- legenda final pronta quando não houver bloqueio editorial.

## Fontes de verdade

- **Plano editorial:** `01-planejamento/v2/README.md` e arquivos mensais da mesma pasta.
- **Padrão de briefing de produção:** `01-planejamento/v2/PADRAO_BRIEFING_PRODUCAO.md`.
- **Estratégia:** `01-planejamento/v2/PLANEJAMENTO_ESTRATEGICO.md` e `05_DECISOES_ESTRATEGICAS.md`.
- **Execução:** `02-estado/execution_state_v2.json`.
- **Destino Trello:** `03-integracoes/trello_destination.json`.
- **Padrão das descrições Trello:** `03-integracoes/PADRAO_DESCRICAO_CARTOES_TRELLO.md`.
- **Reconciliação:** `03-integracoes/RECONCILIACAO_TRELLO_INICIAL.md`.
- **Moodboard:** `04-moodboard/MOODBOARD.md` — versão ativa `ACIRV-MOOD-v1`, status `READY`.
- **Auditoria:** `05-auditoria/`.

## Ordem de leitura do Hermes

1. `00_README.md`
2. `00_EXECUTAR_COM_HERMES.md`
3. `01_RUNBOOK_HERMES.md`
4. `01-planejamento/v2/README.md`
5. `01-planejamento/v2/PADRAO_BRIEFING_PRODUCAO.md`
6. `01-planejamento/v2/PLANEJAMENTO_ESTRATEGICO.md`
7. arquivos mensais aplicáveis em `01-planejamento/v2/`
8. `05_DECISOES_ESTRATEGICAS.md`
9. `02-estado/execution_state_v2.json`
10. `03-integracoes/trello_destination.json`
11. `03-integracoes/PADRAO_DESCRICAO_CARTOES_TRELLO.md`
12. `03-integracoes/RECONCILIACAO_TRELLO_INICIAL.md`
13. `04-moodboard/MOODBOARD.md`.

## Invariantes

- Samara recebe somente peças estáticas.
- Reels serão planejados separadamente pelo usuário.
- Todo post ativo deve ter um único card reconciliado no Trello.
- A descrição do cartão deve ser enxuta em metadados, mas completa em conteúdo de produção.
- **Todo slide deve ter texto exato e direção visual específica antes da liberação para design.**
- A designer não deve precisar escrever, completar ou decidir a copy da peça.
- Um briefing só é considerado pronto quando passa pelo gate `PRODUÇÃO_PRONTA` descrito em `PADRAO_BRIEFING_PRODUCAO.md`.
- O Hermes deve salvar o estado imediatamente após cada mutação externa.
- Dados, cases, depoimentos, horários, capacidades, preços e resultados voláteis precisam de validação antes da publicação.
- Toda referência visual deve usar `ACIRV-MOOD-v1` e respeitar a regra: **peças maiores do moodboard têm peso maior como referência**.
- Os 12 cards do lote piloto de 16/09 a 05/10 devem ser revisados para o padrão de produção antes de avançar para o restante do trimestre.
