# EXECUTAR COM HERMES — Social Media ACIRV Q4 2026

## Missão
Executar **60 publicações estáticas** entre 16/09 e 31/12/2026 para a designer **Samara**, com rastreabilidade, retomada segura e sem duplicação.

## Fonte canônica obrigatória
Plano editorial:
`01-planejamento/v2/README.md`

Estado operacional ativo:
`02-estado/execution_state_v2.json`

Padrão canônico das descrições no Trello:
`03-integracoes/PADRAO_DESCRICAO_CARTOES_TRELLO.md`

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

Antes da primeira mutação de cada sessão, validar os IDs e confirmar o estado externo dos cartões já registrados.

## Reconciliação antes de criar card
Para cada `post_id`:
1. buscar POST ID internamente e no estado;
2. buscar título exato no Trello;
3. buscar assunto/serviço semelhante;
4. verificar evidência de publicação quando houver conteúdo histórico parecido;
5. classificar internamente como `NO_MATCH`, `REFERENCE_ONLY`, `REUSE_CARD`, `ALREADY_PUBLISHED` ou `DUPLICATE_BLOCKED`;
6. criar somente quando seguro.

Card antigo aberto não prova que o conteúdo não foi publicado.

A classificação de reconciliação e as referências históricas pertencem ao **estado/Git**, não à descrição visível para a Samara, salvo quando uma observação histórica altera diretamente a produção.

## Criação do card
Título:
`ACIRV — [Título] — [DD/MM/AAAA]`

Vencimento planejado = data de entrega. Se a interface não permitir gravar o vencimento nativo com segurança, registrar o bloqueio e **não usar um campo personalizado por engano**.

A descrição do cartão deve seguir exatamente:
`03-integracoes/PADRAO_DESCRICAO_CARTOES_TRELLO.md`

A descrição visível para a Samara contém somente:
- publicação;
- data de entrega para Samara;
- objetivo/racional;
- formato;
- número de slides;
- conteúdo/estrutura dos slides;
- CTA;
- direção visual;
- legenda sugerida completa;
- dados a validar, quando existirem;
- observações úteis à produção, quando existirem.

Não colocar no cartão: POST ID, prioridade, pilar, campanha, serviço, métrica, classificação de reconciliação, lista de referências históricas, nomes de arquivos internos ou textos como `não especificado no plano`.

Esses metadados continuam registrados internamente para auditoria e idempotência.

### Procedimento de escrita via navegador
1. No composer da lista, preencher **somente o título**.
2. Criar o cartão.
3. Abrir o cartão.
4. Editar a descrição no campo próprio.
5. Clicar explicitamente em **Salvar** (`description-save-button`).
6. Confirmar que a descrição persistiu antes de avançar.

Nunca usar `list-name-textarea` como composer: esse campo renomeia a lista.

Um post = um card.

### Regra crítica 045–060
Não expandir para mais de 2 slides sem decisão editorial registrada no Git. A legenda é o aprofundamento.

## Cartões já criados com padrão antigo
Se houver cartão já criado com descrição verbosa:
- não recriar;
- preservar ID, URL, posição, comentários, anexos e histórico;
- atualizar apenas a descrição para o padrão canônico;
- salvar explicitamente;
- verificar a persistência.

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

Ao retomar uma execução interrompida, confirmar primeiro o estado real do Trello e continuar do primeiro passo realmente incompleto. Nunca recriar um cartão apenas porque o estado local está atrasado.

## Auditoria final
Confirmar:
- 60 IDs únicos;
- 0 Reels no escopo;
- 16 extras com exatamente 2 slides;
- 60 legendas;
- 1 card por post ativo;
- datas corretas;
- descrições Trello no padrão enxuto da Samara;
- briefings completos;
- referências visuais usando `ACIRV-MOOD-v1`;
- nenhuma duplicação silenciosa.
