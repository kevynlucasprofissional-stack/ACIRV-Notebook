# EXECUTAR COM HERMES — Social Media ACIRV Q4 2026

## Missão
Executar **60 publicações estáticas** entre 16/09 e 31/12/2026 para a designer **Samara**, com rastreabilidade, retomada segura e sem duplicação.

## Fonte canônica obrigatória
Plano editorial:
`01-planejamento/v2/README.md`

Estado operacional ativo:
`02-estado/execution_state_v2.json`

Moodboard ativo:
`04-moodboard/MOODBOARD.md` — `ACIRV-MOOD-v1`, status `READY`.

## Escopo imutável
- Não criar, solicitar ou atribuir Reels/vídeos à Samara.
- Reels serão definidos separadamente pelo usuário.
- IDs 001–044 foram preservados.
- IDs 045–060 são novas peças de baixa complexidade.
- IDs 045–060 têm **exatamente 2 slides: capa + CTA**; o aprofundamento está na legenda.
- Todas as 60 pautas têm legenda sugerida.

## Trello
Destino obrigatório:
- Board `622e83218d717e4a16d7856c` — Calendário Editorial.
- List `69370019555b10bb6ad19e30` — ORDEM DE SERVIÇO - SAMARA.

Antes da primeira mutação, fazer preflight dos IDs.

## Reconciliação antes de criar card
Para cada `post_id`:
1. buscar POST ID;
2. buscar título exato;
3. buscar assunto/serviço semelhante;
4. verificar evidência de publicação quando houver conteúdo histórico parecido;
5. classificar `NO_MATCH`, `REFERENCE_ONLY`, `REUSE_CARD`, `ALREADY_PUBLISHED` ou `DUPLICATE_BLOCKED`;
6. criar somente quando seguro.

Card antigo aberto não prova que o conteúdo não foi publicado.

## Criação do card
Título:
`ACIRV — [Título] — [DD/MM/AAAA]`

Vencimento = data de entrega.

Descrição obrigatória:
- POST ID;
- publicação e entrega;
- objetivo/racional;
- formato e **número de slides**;
- estrutura/conteúdo;
- CTA;
- métrica;
- pilar/campanha/serviço;
- direção visual;
- **legenda sugerida completa**;
- observações de validação.

Um post = um card.

### Regra crítica 045–060
Não expandir para mais de 2 slides sem decisão editorial registrada no Git. A legenda é o aprofundamento.

## Moodboard e referência visual
O moodboard está liberado para execução.

Versão obrigatória:
`ACIRV-MOOD-v1`

Regras:
- ler `04-moodboard/MOODBOARD.md` antes de gerar qualquer referência;
- respeitar a ponderação definida pelo usuário: **peças maiores do moodboard têm peso maior como referência**;
- usar as peças âncora como principal fonte de hierarquia, contraste, composição e tratamento fotográfico;
- adaptar a linguagem ao briefing sem copiar literalmente uma composição existente;
- gerar referências apenas para peças estáticas;
- registrar cada referência no estado do respectivo `post_id` e vinculá-la ao card correspondente quando possível.

## Estado e retomada
Após cada mutação externa bem-sucedida:
1. persistir card ID/URL, classificação e status;
2. atualizar imediatamente `02-estado/execution_state_v2.json` ou o estado materializado por post derivado dele;
3. nunca esperar o fim de um lote para salvar progresso.

## Auditoria final
Confirmar:
- 60 IDs únicos;
- 0 Reels no escopo;
- 16 extras com exatamente 2 slides;
- 60 legendas;
- 1 card por post ativo;
- datas corretas;
- briefings completos;
- referências visuais usando `ACIRV-MOOD-v1`;
- nenhuma duplicação silenciosa.
