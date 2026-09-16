# Reconciliação inicial com o Trello

## Destino confirmado

- Quadro: `Calendário Editorial`
- Board ID: `622e83218d717e4a16d7856c`
- URL: `https://trello.com/b/Edq32SNp/calend%C3%A1rio-editorial`
- Lista de criação: `ORDEM DE SERVIÇO - SAMARA`
- List ID: `69370019555b10bb6ad19e30`

Fluxo observado da designer:
`ORDEM DE SERVIÇO - SAMARA` → `EM PRODUÇÃO - SAMARA` → `PARA APROVAÇÃO - SAMARA` → `ALTERAÇÕES SAMARA` quando necessário.

No snapshot fornecido, a lista `ORDEM DE SERVIÇO - SAMARA` tinha quatro cartões ativos e nenhum deles era claramente uma demanda ACIRV. Não há, portanto, uma duplicação óbvia dentro da lista de entrada naquele snapshot.

## Regra importante: Trello não é prova de publicação

O quadro possui muitos cartões históricos da ACIRV ainda abertos em listas de produção/aprovação, inclusive com vencimentos antigos. Portanto:

- cartão aberto ≠ conteúdo ainda não publicado;
- cartão em aprovação ≠ conteúdo não aprovado atualmente;
- data de vencimento antiga ≠ publicação confirmada.

Antes de decidir criar, reutilizar ou cancelar um card, reconciliar **tema + briefing + status do Trello + evidência de publicação**.

## Candidatos que merecem verificação

### SudoExpo / pós-evento
Existe `[ACIRV] Criativos de agradecimento` em `EM PRODUÇÃO - SAMARA`, com três peças de fechamento da SudoExpo. Não é automaticamente duplicado de `ACIRV-SM-2026-002`, mas as mensagens precisam ser coordenadas para evitar dois fechamentos redundantes.

### Representação institucional
Existe `CARROSSEL - ACIRV SUDOEXPO` cujo gancho é: “Afinal, o que uma associação empresarial faz quando não está realizando eventos?”. Isso sobrepunha fortemente o antigo `ACIRV-SM-2026-016`. O plano foi corrigido: o post de 21/10 agora é **“Como uma demanda empresarial vira pauta coletiva na ACIRV”**, com foco no processo de representação.

### Certificado Digital
Há referências anteriores como `[ACIRV] Certificado digital`, `[ACIRV] Carrossel Certificado Digital` e `[ACIRV] Certificado Digital em uma página`. Os novos posts podem permanecer porque usam ângulos distintos, mas verificar o que foi efetivamente publicado e reaproveitar somente informações/visuais ainda válidos.

### Consultorias
Existem `[ACIRV] Carrossel sobre consultorias` e `[ACIRV] Card serviço de consultoria gratuita`. Usar como fonte operacional/visual, mas confirmar se áreas, condições e eventual gratuidade continuam vigentes.

### Auditório / espaços
Existe `[ACIRV] Auditório + Sala de Treinamento`. Pode servir de referência, mas capacidades, estrutura, preços/descontos e disponibilidade devem ser revalidados.

### Benefícios / associação
Existe `[ACIRV] Destaque: Benefícios`, com narrativa sobre rede, representação, networking e capacitação. Usar como base para evitar repetir a mesma sequência textual.

## Classificação de reconciliação

Para cada `post_id`, classificar qualquer candidato como:

- `NO_MATCH`: não é o mesmo conteúdo.
- `REFERENCE_ONLY`: serve como fonte/referência, mas o novo conteúdo é diferente.
- `REUSE_CARD`: o card existente representa a mesma publicação e deve ser vinculado ao `post_id`.
- `ALREADY_PUBLISHED`: o conteúdo já foi publicado; decidir se o planejado é uma nova abordagem ou se deve ser substituído.
- `DUPLICATE_BLOCKED`: duplicação não resolvida; não criar novo card.

## Privacidade operacional

O export bruto do Trello não deve ser versionado neste repositório. Ele contém informações de outros clientes, membros e projetos que não são necessárias para executar o planejamento ACIRV. Este documento preserva apenas os fatos operacionais necessários ao Hermes.
