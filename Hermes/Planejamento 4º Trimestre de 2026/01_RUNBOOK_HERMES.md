# Runbook do Hermes — Social Media ACIRV Q4 2026

## Missão
Executar o planejamento vigente entre 16/09/2026 e 31/12/2026 com rastreabilidade, idempotência e baixa possibilidade de duplicação.

## Fontes operacionais
Plano editorial:
`01-planejamento/v2/README.md`

Estado:
`02-estado/execution_state_v2.json`

Integração Trello:
`03-integracoes/trello_destination.json`

Reconciliação:
`03-integracoes/RECONCILIACAO_TRELLO_INICIAL.md`

Moodboard:
`04-moodboard/MOODBOARD.md` — `ACIRV-MOOD-v1`, status `READY`.

## Invariantes
1. Direção: **Conectar para Crescer**.
2. Plano da Samara = **somente peças estáticas**.
3. Reels/vídeos ficam fora do escopo e serão definidos pelo usuário separadamente.
4. Total ativo = **60 posts**.
5. IDs 001–044 permanecem imutáveis.
6. IDs 045–060 = **2 slides exatos, capa + CTA**, com profundidade na legenda.
7. Toda pauta tem legenda sugerida.
8. Não publicar números, condições comerciais, capacidades, horários, nomes ou promessas sem validação atual.
9. Prova social exige evidência e autorização quando aplicável.
10. Um post = um card.
11. Toda referência visual usa `ACIRV-MOOD-v1` e dá mais peso às peças maiores do moodboard.

## Inicialização
1. Ler `00_README.md`.
2. Ler `00_EXECUTAR_COM_HERMES.md`.
3. Ler `01-planejamento/v2/README.md`.
4. Ler a estratégia e os arquivos mensais aplicáveis.
5. Ler `05_DECISOES_ESTRATEGICAS.md`.
6. Ler `02-estado/execution_state_v2.json`.
7. Ler destino e reconciliação do Trello.
8. Ler `04-moodboard/MOODBOARD.md`.
9. Antes de escrever externamente, validar board/list pelos IDs exatos.

## Estados
Fluxo principal:
`BRIEFING_CRIADO -> CARTAO_CRIADO -> REFERENCIA_VISUAL_CRIADA -> REVISAO_PENDENTE -> CONCLUIDA`

Auxiliares:
- `BLOCKED_TRELLO_ACCESS`
- `BLOCKED_DUPLICATE_CARD`
- `BLOCKED_DATA_VALIDATION`
- `CANCELADA`

## Reconciliação antes do card
1. Pesquisar POST ID.
2. Pesquisar título exato.
3. Pesquisar conceitos/serviços próximos.
4. Consultar a reconciliação inicial.
5. Verificar evidência de publicação quando houver card histórico semelhante.
6. Classificar como `NO_MATCH`, `REFERENCE_ONLY`, `REUSE_CARD`, `ALREADY_PUBLISHED` ou `DUPLICATE_BLOCKED`.
7. Só criar quando a classificação permitir.

Se houver candidatos ambíguos, bloquear; não criar um terceiro card.

## Criação do cartão
Destino:
- Board `622e83218d717e4a16d7856c` — Calendário Editorial.
- List `69370019555b10bb6ad19e30` — ORDEM DE SERVIÇO - SAMARA.

Título:
`ACIRV — [title] — [DD/MM/AAAA]`

Vencimento = `delivery_date`.

Descrição mínima:
- POST ID;
- publicação/entrega/prioridade;
- objetivo;
- formato + número de slides;
- estrutura/conteúdo;
- CTA;
- métrica;
- pilar/campanha/serviço;
- direção visual;
- legenda sugerida completa;
- observações e validações.

Para IDs 045–060, a instrução de 2 slides é obrigatória.

## Moodboard
O moodboard está `READY`.

Antes de gerar referência visual:
1. ler `04-moodboard/MOODBOARD.md`;
2. aplicar a ponderação `PESO 4 / PESO 2 / PESO 1` definida no documento;
3. preservar principalmente os padrões das referências âncora;
4. não copiar literalmente uma peça existente;
5. gerar somente referência conceitual para orientar a designer;
6. registrar a referência no estado do `post_id` e no card correspondente.

## Persistência
Depois de cada mutação externa bem-sucedida, salvar imediatamente no estado: card ID, URL, reconciliação, referência visual e status.

## Auditoria
Checar:
- 60 IDs e dedupe keys únicos;
- 0 Reels no escopo;
- 16 extras de 2 slides;
- 60 legendas;
- 1 post = 1 card;
- board/list corretos;
- vencimento = entrega;
- dados voláteis validados;
- referências visuais coerentes com `ACIRV-MOOD-v1`;
- nenhum duplicado ignorado.
