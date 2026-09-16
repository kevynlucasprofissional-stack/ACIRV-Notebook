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

Padrão das descrições dos cartões:
`03-integracoes/PADRAO_DESCRICAO_CARTOES_TRELLO.md`

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
12. A descrição do Trello é uma interface para a designer, não um dump dos metadados do Hermes.

## Inicialização
1. Ler `00_README.md`.
2. Ler `00_EXECUTAR_COM_HERMES.md`.
3. Ler `01-planejamento/v2/README.md`.
4. Ler a estratégia e os arquivos mensais aplicáveis.
5. Ler `05_DECISOES_ESTRATEGICAS.md`.
6. Ler `02-estado/execution_state_v2.json`.
7. Ler destino, padrão de descrição e reconciliação do Trello.
8. Ler `04-moodboard/MOODBOARD.md`.
9. Antes de escrever externamente, validar board/list pelos IDs exatos e conferir cartões já registrados no estado.

## Estados
Fluxo principal:
`BRIEFING_CRIADO -> CARTAO_CRIADO -> REFERENCIA_VISUAL_CRIADA -> REVISAO_PENDENTE -> CONCLUIDA`

Auxiliares:
- `BLOCKED_TRELLO_ACCESS`
- `BLOCKED_DUPLICATE_CARD`
- `BLOCKED_DATA_VALIDATION`
- `BLOCKED_TRELLO_DESTINATION_DRIFT`
- `CANCELADA`

## Reconciliação antes do card
1. Pesquisar POST ID no estado/Git.
2. Pesquisar título exato no Trello.
3. Pesquisar conceitos/serviços próximos.
4. Consultar a reconciliação inicial.
5. Verificar evidência de publicação quando houver card histórico semelhante.
6. Classificar internamente como `NO_MATCH`, `REFERENCE_ONLY`, `REUSE_CARD`, `ALREADY_PUBLISHED` ou `DUPLICATE_BLOCKED`.
7. Só criar quando a classificação permitir.

Se houver candidatos ambíguos, bloquear; não criar um terceiro card.

A classificação e as referências históricas ficam no estado/Git. Na descrição do cartão entram apenas observações históricas que alterem diretamente o trabalho da Samara.

## Criação do cartão
Destino:
- Board `622e83218d717e4a16d7856c` — Calendário Editorial.
- List `69370019555b10bb6ad19e30` — ORDEM DE SERVIÇO - SAMARA.

Título:
`ACIRV — [title] — [DD/MM/AAAA]`

Vencimento planejado = `delivery_date`.

Se não for possível gravar o vencimento nativo com segurança, registrar a pendência no estado. **Não reutilizar um campo personalizado apenas porque ele abre um seletor de data.**

### Descrição canônica
Seguir obrigatoriamente:
`03-integracoes/PADRAO_DESCRICAO_CARTOES_TRELLO.md`

Campos visíveis para Samara:
- publicação;
- data de entrega;
- objetivo/racional;
- formato;
- número de slides;
- estrutura/conteúdo;
- CTA;
- direção visual;
- legenda sugerida completa;
- dados a validar, quando houver;
- observações úteis à produção, quando houver.

Não colocar na descrição:
- POST ID;
- prioridade;
- pilar;
- campanha;
- serviço/benefício;
- métrica;
- classificação de reconciliação;
- bloco de referências históricas;
- nomes de arquivos internos;
- placeholders como `não especificado no plano`.

Esses dados continuam obrigatórios quando úteis para a operação, mas pertencem ao estado/Git.

Para IDs 045–060, a instrução de 2 slides é obrigatória e deve aparecer de maneira inequívoca no briefing.

## Procedimento validado de escrita no Trello via navegador
1. Abrir a lista correta pelo ID validado.
2. No composer, inserir **somente o título** do card.
3. Criar o card.
4. Abrir o card criado.
5. Entrar no editor de descrição.
6. Substituir/preencher a descrição com o template canônico.
7. Clicar explicitamente em `Salvar` / `description-save-button`.
8. Confirmar a persistência antes de avançar.

Armadilhas conhecidas:
- `list-name-textarea` é o campo de renomear a lista; não usar como composer.
- O composer correto é `list-card-composer-textarea` e funciona como `contenteditable`.
- Não tentar inserir título + descrição de uma vez no composer.
- Escrita direta por API encontrou bloqueio CSRF durante o lote piloto; preferir a UI autenticada para mutações enquanto esse comportamento persistir.

## Migração de cartões já existentes
Quando um card deste planejamento já tiver sido criado com o padrão antigo:
1. não criar outro;
2. preservar card ID/URL e histórico;
3. atualizar apenas a descrição;
4. clicar em Salvar;
5. verificar a persistência;
6. registrar a migração no estado.

## Moodboard
O moodboard está `READY`.

Antes de gerar referência visual:
1. ler `04-moodboard/MOODBOARD.md`;
2. aplicar a ponderação `PESO 4 / PESO 2 / PESO 1` definida no documento;
3. preservar principalmente os padrões das referências âncora;
4. não copiar literalmente uma peça existente;
5. gerar somente referência conceitual para orientar a designer;
6. registrar a referência no estado do `post_id` e no card correspondente.

Quando uma publicação for um carrossel, a referência visual deve seguir a regra operacional vigente no repositório: **uma única geração contendo o conjunto de slides da peça**, e não uma geração isolada por slide, salvo decisão editorial posterior registrada.

## Persistência
Depois de cada mutação externa bem-sucedida, salvar imediatamente no estado: card ID, URL, reconciliação, referência visual e status.

Ao retomar:
1. ler o estado;
2. verificar o Trello ao vivo;
3. reconciliar diferenças entre estado e realidade externa;
4. continuar do primeiro passo realmente incompleto;
5. nunca recriar um card só porque o arquivo local está atrasado.

## Auditoria
Checar:
- 60 IDs e dedupe keys únicos;
- 0 Reels no escopo;
- 16 extras de 2 slides;
- 60 legendas;
- 1 post = 1 card;
- board/list corretos;
- descrições conforme o padrão enxuto da Samara;
- vencimento = entrega ou pendência explicitamente registrada;
- dados voláteis validados;
- referências visuais coerentes com `ACIRV-MOOD-v1`;
- nenhum duplicado ignorado.
