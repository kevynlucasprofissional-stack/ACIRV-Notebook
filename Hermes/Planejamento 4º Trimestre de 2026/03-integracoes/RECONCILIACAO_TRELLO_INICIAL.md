# Reconciliação inicial com o Trello

Fonte: export do quadro `Calendário Editorial` fornecido em 16/09/2026.

## Destino confirmado
- Quadro: `Calendário Editorial`
- Board ID: `622e83218d717e4a16d7856c`
- URL: `https://trello.com/b/Edq32SNp/calend%C3%A1rio-editorial`
- Lista de entrada: `ORDEM DE SERVIÇO - SAMARA`
- List ID: `69370019555b10bb6ad19e30`

Fluxo observado da designer:
`ORDEM DE SERVIÇO - SAMARA` → `EM PRODUÇÃO - SAMARA` → `PARA APROVAÇÃO - SAMARA` → `ALTERAÇÕES SAMARA` quando necessário.

## Regra crítica: Trello não é prova de publicação
O quadro possui cartões históricos da ACIRV ainda abertos em produção/aprovação. Portanto:
- cartão aberto ≠ conteúdo ainda não publicado;
- cartão em aprovação ≠ conteúdo não aprovado atualmente;
- vencimento antigo ≠ publicação confirmada;
- semelhança de título ≠ duplicata automática.

Antes de criar, reutilizar ou cancelar um card, reconciliar **POST ID + tema + briefing + status do Trello + evidência de publicação**.

## Candidatos históricos que merecem verificação

### SudoExpo / pós-evento
Existe `[ACIRV] Criativos de agradecimento` em produção, com peças de fechamento da SudoExpo. Coordenar com os posts pós-evento para evitar fechamentos redundantes.

### Representação institucional
Existe `CARROSSEL - ACIRV SUDOEXPO` com conceito próximo a “o que uma associação empresarial faz quando não está realizando eventos?”. Por isso `ACIRV-SM-2026-016` foi ajustado para **“Como uma demanda empresarial vira pauta coletiva na ACIRV”**, com foco em escuta → identificação de interesse coletivo → consolidação → articulação → acompanhamento/devolutiva.

### Certificado Digital
Há referências anteriores como `[ACIRV] Certificado digital`, `[ACIRV] Carrossel Certificado Digital` e `[ACIRV] Certificado Digital em uma página`. Os novos posts usam ângulos distintos, mas o Hermes deve verificar o que já foi publicado e reaproveitar apenas informações/visuais ainda válidos.

### Consultorias
Existem `[ACIRV] Carrossel sobre consultorias` e `[ACIRV] Card serviço de consultoria gratuita`. Podem servir como referência, mas áreas, condições e eventual gratuidade precisam de confirmação atual.

### Auditório / espaços
Existe `[ACIRV] Auditório + Sala de Treinamento`. Pode servir de referência, mas capacidades, estrutura, preços/descontos e disponibilidade devem ser revalidados.

### Benefícios / associação
Existe `[ACIRV] Destaque: Benefícios`, com narrativa sobre rede, representação, networking e capacitação. Usar como referência para não repetir a mesma sequência textual.

## Classificação de reconciliação
Para cada `post_id`, classificar candidatos como:
- `NO_MATCH`: não é o mesmo conteúdo;
- `REFERENCE_ONLY`: serve de fonte/referência, mas a nova publicação é diferente;
- `REUSE_CARD`: o card existente representa exatamente a publicação planejada;
- `ALREADY_PUBLISHED`: a ideia já foi executada/publicada e exige decisão antes de repetir;
- `DUPLICATE_BLOCKED`: há ambiguidade ou mais de um candidato; bloquear e não criar novo card.

## Nomenclatura corrigida
`ACIRV + VCOM: SCRUM` e `ACIRV + AVECON` referem-se ao mesmo quadro interno segundo correção do usuário. Eles **não são o destino** dos cartões deste planejamento.

## Privacidade operacional
O export bruto do Trello não deve ser versionado neste repositório. Ele contém informações de outros clientes, membros e projetos que não são necessárias para executar o planejamento da ACIRV.
