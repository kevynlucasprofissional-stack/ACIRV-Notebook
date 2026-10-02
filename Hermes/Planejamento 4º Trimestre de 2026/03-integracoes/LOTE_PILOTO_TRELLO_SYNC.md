# Lote piloto — mapa de sincronização Trello

**Escopo:** publicações de 16/09/2026 a 05/10/2026.  
**Objetivo:** deixar o Hermes apenas com a tarefa mecânica de sincronizar no Trello os briefings já escritos no GitHub.

## Regras

- Todos os 12 cards canônicos abaixo já existem.
- **Não criar novos cards para o lote piloto.**
- A descrição final vem do bloco `DESCRIÇÃO CANÔNICA PARA O TRELLO` no arquivo mensal indicado.
- Não reescrever, resumir ou complementar copy.
- O vencimento nativo desejado é a data de entrega indicada no briefing.
- No snapshot auditado, os 12 cards canônicos estavam com `due = null`; portanto, o Hermes pode tentar preencher o vencimento nativo com segurança pela UI.
- O campo personalizado `Data de publicação` não substitui o vencimento nativo.

## Cards canônicos

| Post ID | Publicação | Entrega | Fonte canônica | Card ID | URL |
|---|---:|---:|---|---|---|
| ACIRV-SM-2026-001 | 16/09/2026 | 16/09/2026 | `../01-planejamento/v2/2026-09.md` | `6aaadd7ab17c112faab2ffad` | https://trello.com/c/SUXu5o63 |
| ACIRV-SM-2026-045 | 17/09/2026 | 16/09/2026 | `../01-planejamento/v2/2026-09.md` | `6aaae33bc6b94da53dd48656` | https://trello.com/c/YgUcrpAM |
| ACIRV-SM-2026-002 | 18/09/2026 | 16/09/2026 | `../01-planejamento/v2/2026-09.md` | `6aaae36664ae41c101f1cbd9` | https://trello.com/c/vQA88NJ0 |
| ACIRV-SM-2026-003 | 21/09/2026 | 16/09/2026 | `../01-planejamento/v2/2026-09.md` | `6aaae36960696fadef29705f` | https://trello.com/c/IaKmvPz7 |
| ACIRV-SM-2026-004 | 23/09/2026 | 18/09/2026 | `../01-planejamento/v2/2026-09.md` | `6aaae36cd20909f93b51ae3a` | https://trello.com/c/b5DCNeqw |
| ACIRV-SM-2026-046 | 24/09/2026 | 22/09/2026 | `../01-planejamento/v2/2026-09.md` | `6aaae36f466385ab176fdd97` | https://trello.com/c/hVRma9lN |
| ACIRV-SM-2026-005 | 25/09/2026 | 22/09/2026 | `../01-planejamento/v2/2026-09.md` | `6aaae372ed3904fb709c751b` | https://trello.com/c/8K8TPekj |
| ACIRV-SM-2026-006 | 28/09/2026 | 23/09/2026 | `../01-planejamento/v2/2026-09.md` | `6aaae37e1cd356158b810378` | https://trello.com/c/UvcwnAFK |
| ACIRV-SM-2026-007 | 30/09/2026 | 25/09/2026 | `../01-planejamento/v2/2026-09.md` | `6aaae381f06b16b952801039` | https://trello.com/c/6PVVFLwt |
| ACIRV-SM-2026-008 | 01/10/2026 | 28/09/2026 | `../01-planejamento/v2/2026-10-1.md` | `6aaae3cb1eb71dc68df8bb2f` | https://trello.com/c/i4MUHERX |
| ACIRV-SM-2026-047 | 02/10/2026 | 30/09/2026 | `../01-planejamento/v2/2026-10-1.md` | `6aaae3cd864963c0e5965586` | https://trello.com/c/01E2Oicn |
| ACIRV-SM-2026-009 | 05/10/2026 | 28/09/2026 | `../01-planejamento/v2/2026-10-1.md` | `6aaae3cfe012d4bd9e1c2435` | https://trello.com/c/1B3pbnDG |

## Duplicidade conhecida

Foi identificado e arquivado um segundo card para `ACIRV-SM-2026-005`:

- Card ID: `6aaae37bd2bf0a8c4ef4edad`
- URL: https://trello.com/c/umA9RkpT
- Estado no snapshot: `closed = true`

**Não reabrir, não reutilizar e não sincronizar esse card.**

O card canônico de `ACIRV-SM-2026-005` é:

https://trello.com/c/8K8TPekj

## Estado observado no snapshot do Trello

- 12 cards canônicos presentes na lista `ORDEM DE SERVIÇO - SAMARA`.
- 1 duplicado arquivado do post 005.
- `due` nativo estava vazio nos 12 cards canônicos.
- O card 001 já possuía o campo personalizado `Data de publicação = 16/09/2026`.
- Os briefings existentes no snapshot ainda eram versões anteriores e devem ser substituídos pelos blocos canônicos v2.1/v2.2 do planejamento.

## Tarefa restante para o Hermes

Para cada linha da tabela:
1. abrir a fonte canônica;
2. localizar o post ID;
3. copiar integralmente o conteúdo de `DESCRIÇÃO CANÔNICA PARA O TRELLO`;
4. abrir a URL canônica;
5. substituir a descrição;
6. salvar e verificar;
7. tentar preencher o vencimento nativo com a data de entrega;
8. registrar o resultado em `execution_state_v2.json`.

Nada de autoria editorial permanece para o Hermes neste lote.