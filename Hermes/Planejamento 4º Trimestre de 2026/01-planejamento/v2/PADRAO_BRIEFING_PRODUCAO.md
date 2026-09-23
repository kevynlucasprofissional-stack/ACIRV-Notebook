# Padrão canônico de briefing de produção — ACIRV Social Media

**Versão:** 2.2  
**Status:** ATIVO  
**Aplicação:** todas as peças destinadas à designer Samara.

## Princípio

O planejamento editorial define **o que comunicar e por quê**. O briefing de produção precisa ir além: deve entregar à designer **o texto exato que entra na arte e a direção visual de cada slide**.

A designer não deve receber apenas temas como `rede + representação + consultorias` ou instruções genéricas como `uma situação por card`. Esse nível é apenas um rascunho editorial. Antes de uma pauta chegar ao Trello, ela deve estar expandida para um briefing executável.

## Separação de responsabilidades

### Autoria editorial

A copy, a estrutura slide a slide, a direção visual, a legenda, os assets e as restrições são definidos **nos arquivos canônicos do planejamento no GitHub**.

Quando um post estiver marcado como `PRODUÇÃO_PRONTA` ou `PRODUÇÃO_PRONTA_COM_ASSET_PENDENTE`, o bloco `DESCRIÇÃO CANÔNICA PARA O TRELLO` passa a ser a fonte editorial final daquela pauta.

### Papel do Hermes

Para briefings já fechados no planejamento, o Hermes é **executor de transferência**, não autor editorial.

O Hermes deve:
- localizar o card correto no Trello;
- copiar integralmente a descrição canônica do planejamento;
- preservar formatação e conteúdo;
- salvar;
- verificar persistência;
- registrar o estado externo.

O Hermes **não deve**:
- reescrever a copy;
- resumir o briefing;
- criar títulos, subtítulos ou CTAs alternativos;
- trocar palavras para “melhorar” o texto;
- transformar direção visual específica em orientação genérica;
- preencher lacunas editoriais por conta própria;
- alterar o número de slides.

Se o planejamento ainda estiver em estado de pauta editorial e não possuir briefing canônico fechado, o Hermes deve **parar aquele item e registrar `BLOCKED_EDITORIAL_BRIEFING`**, em vez de escrever o briefing sozinho.

## Definição de PRODUÇÃO_PRONTA

Uma pauta só pode ser enviada para `ORDEM DE SERVIÇO - SAMARA` quando possuir:

1. objetivo editorial curto e compreensível;
2. formato e dimensões;
3. número exato de slides;
4. **texto exato de cada slide**;
5. hierarquia do texto quando útil: `TÍTULO`, `SUBTÍTULO`, `CORPO`, `DESTAQUE`, `RODAPÉ`, `CTA`;
6. **direção visual por slide**;
7. assets/referências necessários ou indicação clara de onde obtê-los;
8. restrições / `NÃO FAZER` quando houver risco de interpretação errada;
9. legenda final pronta para copiar, salvo pendência editorial explícita;
10. dados pendentes claramente marcados sem transferir para a designer a responsabilidade de pesquisar ou inventar conteúdo.

Se faltar copy de um slide ou a designer ainda precisar decidir `o que escrever`, a pauta **não está pronta para produção**.

## Regra de autoridade do texto

Todo texto dentro de `TEXTO EXATO DA ARTE` é a copy editorial que deve ser diagramada.

A designer pode ajustar:
- quebra de linha;
- hierarquia tipográfica;
- tamanho e composição;
- elementos visuais.

A designer **não deve precisar reescrever, completar ou inventar a mensagem**.

Se o texto precisar mudar por motivo editorial, a alteração deve ser feita primeiro no briefing canônico do GitHub e depois refletida no Trello.

## Template canônico

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

[DESTAQUE / CTA / RODAPÉ, quando houver]
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
- [Somente fatos que realmente precisam de confirmação.]

OBSERVAÇÕES:
- [Somente orientações úteis à produção.]
```

Se uma seção não tiver conteúdo real, ela pode ser omitida.

## Direção visual por slide

Não basta escrever `usar fotos humanas` para um carrossel inteiro. Sempre que houver 2+ slides, indicar, quando possível:

- qual tipo de imagem/composição cabe naquele slide;
- qual informação deve dominar visualmente;
- o que deve receber maior contraste;
- se o slide é fotográfico, tipográfico, comparativo, diagrama, mosaico ou CTA;
- como preservar continuidade visual com os slides anteriores.

A direção deve reduzir ambiguidades, não engessar a criatividade da designer.

## Capa

A capa merece direção específica. Deve deixar claro:

- gancho principal;
- qual palavra/frase recebe maior destaque;
- fotografia ou conceito principal;
- densidade desejada;
- relação com `ACIRV-MOOD-v1`.

Em peças estratégicas, priorizar a qualidade da capa sobre elementos decorativos dos slides internos.

## Assets

Quando o briefing depender de foto real, logo de parceiro, QR Code, print, números, depoimento, nome de pessoa ou material de evento, informar explicitamente o asset necessário e, quando conhecido, sua fonte/localização.

Não pedir à Samara para `procurar alguma foto`, `pesquisar um dado` ou decidir qual informação institucional é verdadeira.

## Dados a validar

Dados voláteis não devem virar copy definitiva sem validação. Exemplos: preço, desconto, capacidade de sala, horários, números de evento, estatísticas, produtos/condições comerciais, depoimentos, nomes e autorizações de imagem.

Quando um dado pendente afetar apenas um detalhe, usar placeholder editorial inequívoco ou registrar a pendência de asset sem bloquear a copy.

Quando o dado mudar a mensagem central, marcar a pauta como `BLOCKED_DATA_VALIDATION` e não enviá-la para produção ainda.

## Legenda

O padrão é `LEGENDA FINAL — PRONTA PARA COPIAR`.

Usar `LEGENDA SUGERIDA` somente quando existir uma pendência editorial real que impeça tratá-la como final.

A legenda pode aprofundar a peça, especialmente nos IDs `045–060`, mas não deve ser usada como desculpa para deixar o texto da arte indefinido.

## Regra especial — IDs 045–060

Continuam sendo peças de baixa complexidade com **exatamente 2 slides**:

- Slide 1 = capa/gancho;
- Slide 2 = CTA;
- sem slides intermediários;
- aprofundamento na legenda.

Mesmo assim, os dois slides precisam ter **copy exata** e **direção visual própria**.

## Relação com o sistema visual

A autoridade visual é `../../../01-Estrategia-e-Marca/Design-System-ACIRV.md`.

Para execução pelo Hermes, toda direção visual usa `ACIRV-MOOD-v1` em `../../04-moodboard/MOODBOARD.md`, que é uma projeção operacional sincronizada do Design System canônico.

Regra de ponderação já estabelecida:

**quanto maior a peça no moodboard original, maior o peso dela como referência.**

O briefing pode indicar qual linguagem do moodboard faz mais sentido para a peça, mas não deve pedir cópia literal de uma referência. Nenhum briefing deve introduzir regra permanente de identidade visual que contradiga o Design System canônico.

## Quality Gate editorial

O gate é aplicado **no planejamento**, antes de liberar o briefing para execução.

Um briefing só recebe `PRODUÇÃO_PRONTA` quando:
- existe texto exato para todos os slides;
- a quantidade de slides bate com o entregável;
- existe direção visual por slide;
- a capa tem hierarquia clara;
- o CTA está escrito exatamente;
- a legenda está pronta para copiar ou explicitamente bloqueada;
- assets críticos estão identificados;
- dados voláteis estão validados ou claramente marcados;
- a designer consegue produzir a peça sem precisar escrever a copy.

O Hermes não refaz esse julgamento editorial quando o status já está fechado; ele apenas verifica se está usando o arquivo/versão correta.

## Regra de migração

Briefings já criados no Trello com descrições genéricas devem ser atualizados **no card existente**, sem recriação.

Preservar ID, URL, histórico, comentários e anexos. Substituir apenas a descrição pelo bloco canônico correspondente, salvar e verificar persistência.