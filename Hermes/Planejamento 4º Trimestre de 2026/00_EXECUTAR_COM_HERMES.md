# EXECUTAR COM HERMES — Social Media ACIRV Q4 2026

## Missão
Executar **60 publicações estáticas** entre 16/09 e 31/12/2026 para a designer **Samara**, com rastreabilidade, retomada segura, alta qualidade de briefing e sem duplicação.

## Fontes canônicas obrigatórias
Plano editorial:
`01-planejamento/v2/README.md`

Padrão de briefing de produção:
`01-planejamento/v2/PADRAO_BRIEFING_PRODUCAO.md`

Estado operacional ativo:
`02-estado/execution_state_v2.json`

Padrão da descrição no Trello:
`03-integracoes/PADRAO_DESCRICAO_CARTOES_TRELLO.md`

Moodboard ativo:
`04-moodboard/MOODBOARD.md` — `ACIRV-MOOD-v1`, status `READY`.

## Escopo imutável
- Não criar, solicitar ou atribuir Reels/vídeos à Samara.
- IDs 001–044 foram preservados.
- IDs 045–060 têm **exatamente 2 slides: capa + CTA**.
- Todas as 60 pautas têm legenda.
- Reels serão definidos separadamente pelo usuário.

## Regra editorial crítica

O Hermes não deve apenas copiar a síntese existente nos arquivos mensais para o Trello.

Antes de criar ou atualizar qualquer card, deve **expandir a pauta para um briefing de produção completo**.

A Samara precisa receber:
- texto exato que entra em cada slide;
- hierarquia textual por slide;
- direção visual específica por slide;
- formato e dimensões;
- CTA final;
- assets/referências;
- restrições;
- legenda final pronta para copiar;
- dados pendentes claramente marcados.

É proibido considerar como briefing pronto frases genéricas como:
- `mostrar pessoas, negócios e conexões`;
- `uma situação por card`;
- `rede, representação, consultorias...`;
- `slide 2: explicar benefícios`;
- `fotografia humana + frase principal` sem escrever a frase.

A designer não deve precisar escrever nenhuma frase nova para conseguir produzir a peça.

## Quality Gate obrigatório

Antes de escrever no Trello, o Hermes deve confirmar internamente:
1. texto exato de todos os slides;
2. quantidade de slides coerente com o entregável;
3. hierarquia textual clara;
4. direção visual por slide;
5. capa com gancho e hierarquia definidos;
6. CTA exato;
7. legenda final pronta ou explicitamente bloqueada;
8. assets críticos identificados;
9. dados voláteis validados ou marcados;
10. nenhuma decisão editorial central transferida para a designer.

Se faltar item essencial, o briefing não está `PRODUÇÃO_PRONTA`.

## Trello
Destino obrigatório:
- Board `622e83218d717e4a16d7856c` — Calendário Editorial.
- List `69370019555b10bb6ad19e30` — ORDEM DE SERVIÇO - SAMARA.

Antes da primeira mutação de cada sessão, validar IDs e estado externo dos cartões já registrados.

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

A descrição do cartão deve seguir:
`03-integracoes/PADRAO_DESCRICAO_CARTOES_TRELLO.md`

E o conteúdo editorial deve ter sido gerado conforme:
`01-planejamento/v2/PADRAO_BRIEFING_PRODUCAO.md`

A descrição da Samara deve conter conteúdo suficiente para produção, não metadados internos.

## Procedimento de escrita via navegador
1. No composer da lista, preencher **somente o título**.
2. Criar o cartão.
3. Abrir o cartão.
4. Editar a descrição no campo próprio.
5. Inserir o briefing completo já aprovado no quality gate.
6. Clicar explicitamente em **Salvar** (`description-save-button`).
7. Confirmar persistência antes de avançar.

Nunca usar `list-name-textarea` como composer: esse campo renomeia a lista.

Um post = um card.

## Regra crítica 045–060
Não expandir para mais de 2 slides sem decisão editorial registrada no Git.

Mesmo nessas peças leves, entregar:
- texto exato do slide 1;
- texto exato do slide 2;
- direção visual do slide 1;
- direção visual do slide 2;
- legenda final.

## Revisão obrigatória do lote piloto

Antes de seguir para posts posteriores a 05/10, revisar os 12 cards do lote de 16/09 a 05/10 segundo o padrão de produção v2.1.

A criação anterior dos cards **não significa** que estão prontos para design.

Para cada card existente:
- não recriar;
- preservar ID/URL/histórico;
- substituir a descrição genérica por briefing completo;
- fornecer copy exata slide a slide;
- fornecer direção visual slide a slide;
- salvar;
- verificar persistência;
- atualizar o estado.

## Moodboard e referência visual
Versão obrigatória:
`ACIRV-MOOD-v1`

Regras:
- ler `04-moodboard/MOODBOARD.md`;
- peças maiores do moodboard têm peso maior;
- usar as peças âncora como principal fonte de hierarquia, contraste, composição e tratamento fotográfico;
- adaptar ao briefing sem copiar literalmente;
- a referência visual deve refletir o **texto exato** e a **direção visual por slide** definidos no briefing;
- registrar cada referência no estado e vincular ao card quando possível.

## Estado e retomada
Após cada mutação externa bem-sucedida:
1. persistir card ID/URL, classificação e status;
2. registrar qualidade do briefing (`BRIEFING_INCOMPLETO` ou `PRODUÇÃO_PRONTA`);
3. atualizar imediatamente `02-estado/execution_state_v2.json` ou estado materializado por post;
4. nunca esperar o fim de um lote para salvar progresso.

Ao retomar, confirmar primeiro o estado real do Trello e continuar do primeiro passo realmente incompleto.

## Auditoria final
Confirmar:
- 60 IDs únicos;
- 0 Reels no escopo;
- 16 extras com exatamente 2 slides;
- 1 card por post;
- texto exato em todos os slides de todos os briefings liberados;
- direção visual por slide;
- dimensões/entregáveis definidos;
- CTA exato;
- legenda final pronta;
- assets críticos identificados;
- descrições Trello no padrão da Samara;
- referências visuais coerentes com `ACIRV-MOOD-v1`;
- nenhuma duplicação silenciosa.
