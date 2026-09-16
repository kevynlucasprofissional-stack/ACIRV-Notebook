# Padrão de descrição dos cartões Trello — Samara

Este documento define o **padrão canônico** das descrições dos cartões de Social Media da ACIRV destinados à designer Samara.

## Fonte editorial obrigatória

Antes de escrever qualquer descrição no Trello, localizar o briefing fechado nos arquivos canônicos de:

`../01-planejamento/v2/`

O padrão editorial que governa esses briefings está em:

`../01-planejamento/v2/PADRAO_BRIEFING_PRODUCAO.md`

## Regra principal: copiar, não redigir

Quando um post estiver marcado como `PRODUÇÃO_PRONTA` ou `PRODUÇÃO_PRONTA_COM_ASSET_PENDENTE`, o arquivo mensal contém um bloco:

`DESCRIÇÃO CANÔNICA PARA O TRELLO`

Esse bloco é a descrição final aprovada para a Samara.

O Hermes deve **copiar integralmente esse bloco para o card correspondente**.

O Hermes não deve:
- reescrever;
- resumir;
- melhorar estilo;
- trocar CTA;
- criar copy faltante;
- remover seções;
- transformar direção slide a slide em instrução genérica;
- alterar número de slides;
- mudar legenda final.

Se não existir bloco canônico fechado para a pauta, registrar `BLOCKED_EDITORIAL_BRIEFING` e não escrever uma versão própria.

## Princípio

O Trello é a interface operacional da designer. A descrição deve ser enxuta em metadados, mas **completa em conteúdo de produção**.

A Samara não deve receber somente tema, estrutura genérica ou intenção editorial. O cartão deve entregar o que ela precisa para desenhar a peça sem assumir o trabalho de copywriter.

## O que a descrição canônica contém

Quando aplicável:
- publicação;
- data de entrega;
- objetivo;
- entregável, número de slides e dimensões;
- texto exato da arte, slide a slide;
- hierarquia textual;
- direção visual por slide;
- assets/referências;
- restrições / `NÃO FAZER`;
- legenda final pronta;
- dados a validar;
- observações úteis à produção.

## Não colocar na descrição do cartão

Não incluir metadados internos que não estejam no bloco canônico:
- `POST ID`;
- `PRIORIDADE`;
- `PILAR ESTRATÉGICO`;
- `CAMPANHA/FRENTE`;
- `SERVIÇO/BENEFÍCIO RELACIONADO`;
- `MÉTRICA PRINCIPAL`;
- `RECONCILIAÇÃO TRELLO`;
- `REFERÊNCIAS HISTÓRICAS`;
- nomes de arquivos internos do repositório;
- justificativas técnicas sobre de qual arquivo uma informação foi extraída;
- frases como `não especificado no plano` ou `não definido no plano`.

Esses dados continuam registrados no estado/Git.

## Template de referência

A estrutura editorial típica é:

```text
PUBLICAÇÃO: DD/MM/AAAA
DATA DE ENTREGA PARA SAMARA: DD/MM/AAAA

OBJETIVO:
[objetivo]

ENTREGÁVEL:
[formato]
[quantidade] slide(s)
Formato: 4:5 — 1080 × 1350 px

TEXTO EXATO DA ARTE:

SLIDE 1 — [FUNÇÃO]
[TÍTULO]
Texto exato

...

DIREÇÃO VISUAL POR SLIDE:
...

ASSETS / REFERÊNCIAS:
...

NÃO FAZER:
...

LEGENDA FINAL — PRONTA PARA COPIAR:
...

DADOS A VALIDAR:
...
```

O Hermes não preenche esse template a partir do zero quando o briefing editorial já está fechado; ele transfere o bloco existente.

## IDs 045–060

Para os posts `ACIRV-SM-2026-045` a `060`:
- exatamente 2 slides;
- Slide 1 = capa/gancho;
- Slide 2 = CTA;
- aprofundamento na legenda;
- sem slides intermediários.

A copy e a direção dos dois slides vêm do planejamento canônico.

## Atualização de cartões já criados

Se um cartão deste planejamento já existir com briefing antigo, genérico ou incompleto:
1. **não recriar o cartão**;
2. preservar ID, URL, posição, anexos, comentários e histórico;
3. localizar o bloco `DESCRIÇÃO CANÔNICA PARA O TRELLO` no arquivo mensal;
4. substituir a descrição atual pelo bloco canônico;
5. clicar explicitamente em **Salvar**;
6. verificar depois da gravação que o texto está persistido no Trello;
7. registrar a sincronização no estado.

## Procedimento de escrita no Trello via navegador

1. Abrir o card correto já reconciliado.
2. Entrar no campo de descrição.
3. Copiar integralmente o bloco canônico do GitHub.
4. Colar sem alterações editoriais.
5. Clicar em `Salvar` / `description-save-button`.
6. Reabrir/verificar o conteúdo persistido.
7. Registrar sucesso ou erro no estado.

Se um card novo precisar ser criado no futuro:
- no composer da lista, inserir somente o título;
- criar o card;
- abrir;
- colar a descrição canônica;
- salvar e verificar.

Atenção: `list-name-textarea` renomeia a lista e não é o composer do cartão.