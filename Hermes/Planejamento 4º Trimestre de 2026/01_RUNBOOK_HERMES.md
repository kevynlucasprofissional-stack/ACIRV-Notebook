# Runbook do Hermes — Social Media ACIRV Q4 2026

## Missão
Executar o planejamento vigente entre 16/09/2026 e 31/12/2026 com rastreabilidade, idempotência, baixa possibilidade de duplicação e briefings realmente prontos para produção.

## Fontes operacionais
Plano editorial:
`01-planejamento/v2/README.md`

Padrão de briefing de produção:
`01-planejamento/v2/PADRAO_BRIEFING_PRODUCAO.md`

Estado:
`02-estado/execution_state_v2.json`

Integração Trello:
`03-integracoes/trello_destination.json`

Padrão das descrições dos cartões:
`03-integracoes/PADRAO_DESCRICAO_CARTOES_TRELLO.md`

Reconciliação:
`03-integracoes/RECONCILIACAO_TRELLO_INICIAL.md`

Moodboard:
`04-moodboard/MOODBOARD.md` — `ACIRV-MOOD-v1`, status `READY`.

## Invariantes
1. Direção: **Conectar para Crescer**.
2. Plano da Samara = **somente peças estáticas**.
3. Reels/vídeos ficam fora do escopo.
4. Total ativo = **60 posts**.
5. IDs 001–044 permanecem imutáveis.
6. IDs 045–060 = **2 slides exatos, capa + CTA**, com profundidade na legenda.
7. Toda pauta tem legenda.
8. Não publicar números, condições comerciais, capacidades, horários, nomes ou promessas sem validação atual.
9. Prova social exige evidência e autorização quando aplicável.
10. Um post = um card.
11. Toda referência visual usa `ACIRV-MOOD-v1` e dá mais peso às peças maiores do moodboard.
12. A descrição do Trello é uma interface para a designer, não um dump dos metadados do Hermes.
13. A designer não deve precisar escrever a copy para conseguir executar a peça.

## Inicialização
1. Ler `00_README.md`.
2. Ler `00_EXECUTAR_COM_HERMES.md`.
3. Ler `01-planejamento/v2/README.md`.
4. Ler `01-planejamento/v2/PADRAO_BRIEFING_PRODUCAO.md`.
5. Ler estratégia e arquivos mensais aplicáveis.
6. Ler `05_DECISOES_ESTRATEGICAS.md`.
7. Ler `02-estado/execution_state_v2.json`.
8. Ler destino, padrão de descrição e reconciliação do Trello.
9. Ler `04-moodboard/MOODBOARD.md`.
10. Antes de escrever externamente, validar board/list pelos IDs exatos e conferir cartões já registrados no estado.

## Estados
Fluxo principal:
`BRIEFING_CRIADO -> BRIEFING_INCOMPLETO/PRODUÇÃO_PRONTA -> CARTAO_CRIADO -> REFERENCIA_VISUAL_CRIADA -> REVISAO_PENDENTE -> CONCLUIDA`

Auxiliares:
- `BLOCKED_TRELLO_ACCESS`
- `BLOCKED_DUPLICATE_CARD`
- `BLOCKED_DATA_VALIDATION`
- `BLOCKED_TRELLO_DESTINATION_DRIFT`
- `CANCELADA`

## Quality Gate editorial

Antes de qualquer briefing chegar à Samara, o Hermes deve verificar:

1. texto exato de todos os slides;
2. quantidade de slides coerente;
3. hierarquia textual clara (`TÍTULO`, `SUBTÍTULO`, `CORPO`, `DESTAQUE`, `CTA`, quando útil);
4. direção visual por slide;
5. capa com gancho e prioridade visual definidos;
6. CTA final escrito;
7. legenda final pronta para copiar ou explicitamente bloqueada;
8. assets/referências identificados;
9. dados voláteis validados ou marcados;
10. nenhuma decisão editorial central transferida para a designer.

Se qualquer item essencial falhar, marcar `BRIEFING_INCOMPLETO` e melhorar antes de considerar a pauta pronta.

Frases como `mostrar pessoas`, `explicar benefícios`, `uma situação por card`, `rede + representação + consultorias` não atendem ao padrão de produção.

## Reconciliação antes do card
1. Pesquisar POST ID no estado/Git.
2. Pesquisar título exato no Trello.
3. Pesquisar conceitos/serviços próximos.
4. Consultar a reconciliação inicial.
5. Verificar evidência de publicação quando houver card histórico semelhante.
6. Classificar internamente como `NO_MATCH`, `REFERENCE_ONLY`, `REUSE_CARD`, `ALREADY_PUBLISHED` ou `DUPLICATE_BLOCKED`.
7. Só criar quando a classificação permitir.

Se houver candidatos ambíguos, bloquear; não criar um terceiro card.

## Criação / atualização do cartão
Destino:
- Board `622e83218d717e4a16d7856c` — Calendário Editorial.
- List `69370019555b10bb6ad19e30` — ORDEM DE SERVIÇO - SAMARA.

Título:
`ACIRV — [title] — [DD/MM/AAAA]`

Vencimento planejado = `delivery_date`.

Se não for possível gravar o vencimento nativo com segurança, registrar a pendência no estado. **Não reutilizar um campo personalizado apenas porque ele abre um seletor de data.**

A descrição deve seguir:
`03-integracoes/PADRAO_DESCRICAO_CARTOES_TRELLO.md`

e o conteúdo deve cumprir:
`01-planejamento/v2/PADRAO_BRIEFING_PRODUCAO.md`

### Conteúdo mínimo de produção

Para cada slide:
- função do slide;
- texto exato;
- hierarquia textual;
- direção visual própria.

Além disso:
- formato e dimensões;
- assets/referências;
- restrições;
- legenda final;
- dados a validar;
- observações úteis.

## Procedimento validado de escrita no Trello via navegador
1. Abrir a lista correta pelo ID validado.
2. No composer, inserir **somente o título** do card.
3. Criar o card.
4. Abrir o card criado.
5. Entrar no editor de descrição.
6. Substituir/preencher a descrição com o briefing que já passou no Quality Gate.
7. Clicar explicitamente em `Salvar` / `description-save-button`.
8. Confirmar a persistência antes de avançar.

Armadilhas conhecidas:
- `list-name-textarea` é o campo de renomear a lista; não usar como composer.
- O composer correto é `list-card-composer-textarea` e funciona como `contenteditable`.
- Não tentar inserir título + descrição de uma vez no composer.
- Escrita direta por API encontrou bloqueio CSRF durante o lote piloto; preferir a UI autenticada para mutações enquanto esse comportamento persistir.

## Migração dos cards do lote piloto

Os 12 cards do período 16/09 a 05/10 devem ser reavaliados segundo o padrão v2.1 antes de avançar para o restante do trimestre.

Quando um card já existir:
1. não criar outro;
2. preservar card ID/URL e histórico;
3. expandir a pauta para copy exata slide a slide;
4. criar direção visual slide a slide;
5. substituir somente a descrição;
6. clicar em Salvar;
7. verificar persistência;
8. marcar internamente `PRODUÇÃO_PRONTA` somente se passar no gate.

## Regra 045–060

Continuam com exatamente 2 slides:
- Slide 1 = capa/gancho;
- Slide 2 = CTA.

Mesmo assim, fornecer texto exato e direção visual dos dois slides. O aprofundamento ficar na legenda não elimina a obrigação de resolver a copy da arte.

## Moodboard
O moodboard está `READY`.

Antes de gerar referência visual:
1. ler `04-moodboard/MOODBOARD.md`;
2. aplicar a ponderação `PESO 4 / PESO 2 / PESO 1`;
3. preservar principalmente os padrões das referências âncora;
4. não copiar literalmente uma peça existente;
5. usar o briefing completo como fonte da composição;
6. registrar a referência no estado do `post_id` e no card correspondente.

Quando uma publicação for carrossel, a referência visual deve seguir a regra vigente: **uma única geração contendo o conjunto de slides da peça**, salvo decisão editorial posterior registrada.

## Persistência
Depois de cada mutação externa bem-sucedida, salvar imediatamente no estado: card ID, URL, reconciliação, qualidade do briefing, referência visual e status.

Ao retomar:
1. ler o estado;
2. verificar o Trello ao vivo;
3. reconciliar diferenças;
4. continuar do primeiro passo realmente incompleto;
5. nunca recriar um card só porque o arquivo local está atrasado.

## Auditoria
Checar:
- 60 IDs e dedupe keys únicos;
- 0 Reels no escopo;
- 16 extras de 2 slides;
- 1 post = 1 card;
- todos os cards liberados têm texto exato por slide;
- todos têm direção visual por slide;
- entregável e dimensões definidos;
- CTA final escrito;
- legenda final pronta;
- assets críticos identificados;
- descrições conforme o padrão da Samara;
- vencimento = entrega ou pendência registrada;
- dados voláteis validados;
- referências visuais coerentes com `ACIRV-MOOD-v1`;
- nenhum duplicado ignorado.
