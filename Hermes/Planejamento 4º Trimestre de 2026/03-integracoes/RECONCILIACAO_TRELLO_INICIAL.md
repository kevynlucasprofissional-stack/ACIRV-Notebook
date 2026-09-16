# Reconciliação inicial com o Trello

Fonte: export do quadro `Calendário Editorial` fornecido em 16/09/2026.

## Destino confirmado
- Board: `Calendário Editorial`
- Board ID: `622e83218d717e4a16d7856c`
- Lista de entrada: `ORDEM DE SERVIÇO - SAMARA`
- List ID: `69370019555b10bb6ad19e30`

O histórico do export comprova criação de cartões diretamente nessa lista. O fluxo posterior da Samara inclui `EM PRODUÇÃO - SAMARA` e `PARA APROVAÇÃO - SAMARA`.

## Risco identificado
Há cartões históricos da ACIRV que permanecem abertos em listas de produção/aprovação. Portanto:
- card aberto != conteúdo ainda não publicado;
- semelhança de título != duplicata automática;
- ausência de Post ID em cards antigos não autoriza criar novo card sem checagem semântica.

## Procedimento antes de criar cada cartão
1. Buscar o `POST ID`.
2. Buscar o título exato.
3. Buscar termos centrais do assunto, serviço e campanha.
4. Examinar cards candidatos e, quando possível, evidência de publicação.
5. Classificar o resultado como:
   - `NO_MATCH`: nenhuma publicação equivalente encontrada;
   - `REFERENCE_ONLY`: existe conteúdo anterior semelhante, mas não é a mesma publicação;
   - `REUSE_CARD`: existe card que representa exatamente a publicação planejada;
   - `ALREADY_PUBLISHED`: a ideia já foi executada e publicada; replanejar antes de duplicar;
   - `DUPLICATE_BLOCKED`: há ambiguidade/mais de um candidato; bloquear para revisão.

## Regra especial de 21/10
Durante a auditoria do export foi encontrado conceito anterior próximo a “o que uma associação empresarial faz quando não está realizando eventos”. Para evitar repetição, o planejamento de 21/10 foi ajustado para `Como uma demanda empresarial vira pauta coletiva na ACIRV`, focando escuta -> consolidação de pauta -> articulação -> acompanhamento/devolutiva.

## Nomenclatura corrigida
`ACIRV + VCOM: SCRUM` e `ACIRV + AVECON` referem-se ao mesmo quadro interno segundo correção do usuário. Eles não são o destino dos cartões de design deste planejamento.
