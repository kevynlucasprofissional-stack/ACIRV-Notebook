# Padrão de descrição dos cartões Trello — Samara

Este documento define o **padrão canônico** das descrições dos cartões de Social Media da ACIRV destinados à designer Samara.

## Fonte editorial obrigatória

Antes de escrever qualquer descrição no Trello, o briefing deve cumprir:

`../01-planejamento/v2/PADRAO_BRIEFING_PRODUCAO.md`

O Trello é a interface operacional da designer. A descrição deve ser enxuta em metadados, mas **completa em conteúdo de produção**.

## Princípio

A Samara não deve receber somente tema, estrutura genérica ou intenção editorial. O cartão deve entregar o que ela precisa para desenhar a peça sem assumir o trabalho de copywriter.

Portanto, a descrição deve conter:
- texto exato da arte, slide a slide;
- hierarquia textual quando aplicável;
- direção visual por slide;
- formato e dimensões;
- assets/referências;
- restrições relevantes;
- legenda final pronta;
- pendências claramente marcadas.

Metadados de rastreabilidade continuam importantes para o Hermes, mas ficam no estado/Git e **não** na descrição visível para a Samara.

## Não colocar na descrição do cartão

Não incluir:
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

Esses dados, quando úteis, devem continuar registrados no estado operacional, auditoria ou arquivos internos do Hermes.

## Template canônico da descrição

```text
PUBLICAÇÃO: DD/MM/AAAA
DATA DE ENTREGA PARA SAMARA: DD/MM/AAAA

OBJETIVO:
[Uma frase curta dizendo o que a peça deve fazer.]

ENTREGÁVEL:
[Post / Carrossel / Carrossel fotográfico]
[Quantidade] slide(s)
Formato: 4:5 — 1080 × 1350 px, salvo exceção documentada

TEXTO EXATO DA ARTE:

SLIDE 1 — [FUNÇÃO]
[TÍTULO]
Texto exato

[SUBTÍTULO, se houver]
Texto exato

[CORPO / DESTAQUE / CTA / RODAPÉ, quando houver]
Texto exato

SLIDE 2 — [FUNÇÃO]
...

DIREÇÃO VISUAL POR SLIDE:

SLIDE 1:
[Composição, fotografia, hierarquia, cor, elementos, destaque principal.]

SLIDE 2:
[...]

ASSETS / REFERÊNCIAS:
- [...]

NÃO FAZER:
- [...]

LEGENDA FINAL — PRONTA PARA COPIAR:
[Legenda completa]

DADOS A VALIDAR:
- [...]

OBSERVAÇÕES:
- [...]
```

Se uma seção não tiver conteúdo real, ela pode ser omitida.

## Regras de redação

- Escrever para a Samara, não para o sistema de auditoria.
- Ser claro, humano, escaneável e orientado à execução.
- Não repetir a mesma informação em campos diferentes.
- Não colocar caminhos de arquivos, classificação interna ou explicações de reconciliação na descrição.
- Uma observação de reconciliação pode permanecer **somente quando altera diretamente a produção da designer**.
- Não inventar dados para preencher seções vazias.
- Não usar uma legenda bem escrita como desculpa para deixar a copy da arte vaga.

## Regra obrigatória — texto exato

É proibido enviar para produção descrições como:
- `Slide 2: explicar benefícios`;
- `mostrar pessoas e conexões`;
- `rede, representação, consultorias, certificado...`;
- `uma situação por card`;
- `fotografia humana + frase principal` sem fornecer a frase.

A designer precisa receber o texto final que entra em cada slide.

Quando útil, indicar explicitamente:
- `[TÍTULO]`;
- `[SUBTÍTULO]`;
- `[CORPO]`;
- `[DESTAQUE]`;
- `[RODAPÉ]`;
- `[CTA]`.

Tudo que estiver nesses campos é copy editorial pronta para diagramar, salvo placeholder explicitamente marcado como pendente.

## Direção visual por slide

Carrosséis com 2+ slides precisam de orientação visual específica para cada slide. Uma única frase global não é suficiente quando os slides possuem funções diferentes.

A direção pode indicar:
- tipo de fotografia/elemento;
- composição;
- hierarquia;
- cor de destaque;
- densidade;
- relação com outros slides;
- elemento dominante;
- continuidade visual.

Usar `ACIRV-MOOD-v1` como linguagem-base sem copiar literalmente uma peça existente.

## IDs 045–060

Para os posts `ACIRV-SM-2026-045` a `060`:
- exatamente 2 slides;
- Slide 1 = capa/gancho;
- Slide 2 = CTA;
- aprofundamento na legenda;
- sem slides intermediários.

Mesmo assim, ambos os slides precisam de **texto exato** e **direção visual específica**.

## Quality Gate antes de mover para produção

Antes de considerar um card pronto para a Samara, o Hermes deve confirmar:
1. há texto exato para todos os slides;
2. a quantidade de slides bate com o entregável;
3. a hierarquia textual está clara;
4. existe direção visual por slide;
5. o CTA está escrito exatamente;
6. a legenda está pronta para copiar ou explicitamente bloqueada;
7. assets críticos estão identificados;
8. dados voláteis estão validados ou claramente marcados;
9. a designer consegue criar a peça sem escrever nenhuma frase nova.

Se faltar qualquer item estrutural, o briefing ainda não está pronto para produção.

## Metadados internos do Hermes

Registrar internamente, fora da descrição do Trello, quando aplicável:
- `post_id`;
- prioridade;
- pilar estratégico;
- campanha/frente;
- serviço/benefício;
- métrica;
- classificação de reconciliação;
- referências históricas;
- dedupe key;
- fontes internas;
- card ID/URL;
- estado de execução;
- referência visual e versão do moodboard;
- validações e bloqueios.

## Atualização de cartões já criados

Se um cartão deste planejamento já existir com briefing antigo, genérico ou incompleto:
1. **não recriar o cartão**;
2. preservar ID, URL, posição, anexos, comentários e histórico;
3. atualizar a descrição para o padrão de produção;
4. clicar explicitamente em **Salvar**;
5. verificar depois da gravação que o texto está persistido no Trello;
6. marcar internamente a revisão de qualidade.

## Procedimento de escrita no Trello via navegador

1. No composer da lista, inserir **somente o título do cartão**.
2. Criar o cartão.
3. Abrir o cartão criado.
4. Entrar no campo de descrição.
5. Preencher o briefing completo.
6. Clicar no botão `Salvar` (`description-save-button`).
7. Verificar que a descrição ficou persistida antes de seguir para o próximo cartão.

Atenção: não usar o primeiro `textarea` encontrado na lista. O campo `list-name-textarea` renomeia a lista e não é o composer do cartão.
