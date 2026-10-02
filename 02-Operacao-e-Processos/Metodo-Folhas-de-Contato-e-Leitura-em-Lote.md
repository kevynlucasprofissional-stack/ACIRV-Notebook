---
id: processo-metodo-folhas-de-contato-e-leitura-em-lote
titulo: Metodo-Folhas-de-Contato-e-Leitura-em-Lote
aliases: [folhas-de-contato, leitura-em-lote-de-imagens, descricao-em-bloco]
tipo: processo
subtipo: metodo
status: ativo
profundidade: avancada
versao_schema: '1.0'
versao_conteudo: '1.0'
idioma: pt-BR
data_criacao: '2026-10-02'
ultima_revisao: '2026-10-02'
grau_confianca: alto
camadas_evidencia:
- fato_documentado
- interpretacao_operacional
tags:
- operacao
- metodo
- conteudo
- ia
fontes_documentais:
- '85-Bases-e-Consultas/Instagram-Stories-2026-09.csv'
- 'Hermes/instagram-insights/captura/stories-setembro-2026/_descricoes_stories.json'
notas_relacionadas:
- '[[Stories-Instagram-Setembro-2026]]'
- '[[Base-Instagram-Setembro-2026]]'
- '[[Diagnostico-Instagram-Agosto-Setembro-2026]]'
- '[[Qualidade-dos-Dados-de-Marketing]]'
confidencialidade: interno
---

# Metodo-Folhas-de-Contato-e-Leitura-em-Lote

> [!summary] Síntese
> Método para produzir descrição de **grandes lotes de imagem** sem olhar uma imagem por vez: monta-se uma folha de contato (grade 3×3) e a leitura acontece **nove por folha**. Foi o que tornou viável descrever os 273 stories de setembro/2026 — e o que transformou uma tarefa inviável em uma tarefa de 31 passos.

## O que é isso

É um **método de leitura**, não um script. A ideia central: quando existem centenas de imagens para descrever, o gargalo não é a capacidade de descrever — é o número de vezes que se precisa *abrir* uma imagem. Então reduz-se o número de aberturas, e não a qualidade da descrição.

A regra operacional que define o método: **uma folha de contato 3×3 = 9 imagens lidas numa única passada**, com o resultado gravado por item.

## Como nasceu

Em setembro/2026 o Instagram da ACIRV produziu **273 stories**. Cada story expira em 24 horas e não volta do painel: sem descrição registrada, o conteúdo desaparece como conteúdo — resta o número. A base de stories precisa de três colunas que só existem se alguém *olhar*: `descricao_visao` (o que a imagem mostra), `texto_sobreposto` (o texto escrito sobre ela) e `natureza` (foto, arte, vídeo ou print).

O caminho ingênuo era abrir story por story: 273 aberturas, 273 idas e voltas. O caminho adotado foi compor **31 folhas de contato de 3×3** e ler cada folha como uma unidade — 9 imagens por decisão de leitura.

## O método, passo a passo

1. **Materializar o índice primeiro.** A lista dos 273 stories vem da captura oficial (`day_shells` + `reels_media`), não do olho. O índice é a fonte da verdade; a imagem é anexo.
2. **Cortar as capas** de cada story e montar as folhas em grade fixa (3 colunas × 3 linhas), numeradas `folha_01` a `folha_31`.
3. **Ler uma folha por vez** e gravar um JSON por folha — nunca um JSON só no fim. Se algo falhar no meio, o que já foi lido está preservado.
4. **Mapear o tile para o item de forma determinística:** a folha `NN` cobre os índices `(NN-1)*9+1` até `(NN-1)*9+9`; a última folha cobre o resto (`folha_31` = 271, 272, 273).
5. **Unificar** os 31 JSONs num só e conferir a contagem contra o índice antes de escrever na base.

Formato de cada arquivo: `{"folha":"folha_NN","ids":[...],"itens":{"<índice>":{"descricao","texto_sobreposto","natureza"}}}`.

## Os números reais

| Medida | Valor |
|---|---|
| Stories descritos | **273** |
| Folhas de contato | **31** (3×3) |
| Imagens por folha | **9** (a última com 3) |
| Itens sem descrição depois da unificação | **0** |
| Com texto sobreposto identificado | **236** |
| Natureza apurada | 176 vídeos, 61 fotos, 32 artes, 4 prints |

## Correção de registro: foram 9 por folha, não 4

O método ficou conhecido na operação como "juntar os stories em blocos de 4". O registro correto, conferido nos artefatos, é **3×3 = 9 por folha**. A diferença importa: com 9 por folha, 273 stories fecham em 31 leituras; com 4, seriam 69. A versão real é a mais eficiente das duas — e é a que está implementada. Nenhum artefato usou blocos de 4.

## Por que funciona

- **Diminui o número de rodadas, não o cuidado por item.** A descrição continua individual; o que cai é o custo fixo de abrir, enquadrar e gravar.
- **A grade dá contexto visual comparativo.** Nove stories do mesmo dia, lado a lado, revelam a campanha que os une — algo que nove leituras isoladas não mostram.
- **O índice fixo torna o erro detectável.** Se o item 45 sai na folha 5, é posição 9: a conta erra sozinha quando o mapeamento quebra.
- **A leitura por folha é paralelizável sem perder rastro.** Cada folha é uma unidade independente e verificável.

## As quatro regras que tornaram o método confiável

1. **`natureza` vem do dado da captura, nunca da aparência da imagem.** A leitura visual errou **7 vezes em 273** ao classificar; o dado de origem não. Aparência é indício, não prova.
2. **Um JSON por folha, validado antes de unificar.** Nada entra na base sem casar com o índice.
3. **Autorrelato não vale como prova.** A conferência é programática: contagem, casamento de conjunto e campos vazios, sempre contra o índice — nunca contra a memória de quem leu.
4. **O que não aparece na imagem não é inventado.** Story sem texto sobreposto legível fica sem valor, não com um valor plausível.

## Onde o método já está implementado

- **Base:** `85-Bases-e-Consultas/Instagram-Stories-2026-09.csv` (30 colunas, com `descricao_visao`, `texto_sobreposto` e `natureza`).
- **Descrições unificadas:** `Hermes/instagram-insights/captura/stories-setembro-2026/_descricoes_stories.json`.
- **Procedimento:** `references/descricao-visual-das-capas.md` da skill `instagram-post-metrics-reporting` (camada 3, onde o método é executado).
- **Registro de capacidade:** `operational_capabilities` do Hermes Workstation (ver abaixo).

## Primo deste método: a legenda

Para o **feed**, existe um atalho que dispensa imagem: a **legenda** do post diz do que ele trata em texto. Desde 02/10/2026 a legenda é campo obrigatório da medição (`Instagram-Legendas-<AAAA-MM>.csv`), capturada por `GET /api/v1/media/<media_id>/info/`.

Os dois métodos são complementares e não competem: **legenda resolve o post** (onde o texto explica); **folha de contato resolve a imagem** (onde só o olhar explica — story, capa, arte, print).

## Reuso além do Instagram

O método é geral para **lote de imagens que precisa de descrição**: fotos de evento para o acervo, capturas de tela de relatórios, peças gráficas de campanha, quadros de vídeo. O que ele exige é só isto: um índice confiável, uma grade fixa e um arquivo de saída por folha.

## Relações justificadas

- [[Stories-Instagram-Setembro-2026]] — o resultado produzido por este método.
- [[Base-Instagram-Setembro-2026]] — a base de publicações irmã, que usa a legenda como descritor.
- [[Diagnostico-Instagram-Agosto-Setembro-2026]] — o diagnóstico que motivou descrever o conteúdo, não só contá-lo.
- [[Qualidade-dos-Dados-de-Marketing]] — registra a divergência entre a natureza aparente e a natureza real (7 em 273).

## Fontes e rastreabilidade

- `85-Bases-e-Consultas/Instagram-Stories-2026-09.csv` (272 stories + 1 de 01/10).
- `Hermes/instagram-insights/captura/stories-setembro-2026/_descricoes_stories.json` (273 itens).
- Folhas e capas: `Hermes/instagram-insights/captura/stories-setembro-2026/` e pasta de trabalho do método.

## Limitações e revisão

A grade 3×3 é o que está validado em produção. Grades maiores reduzem o número de leituras, mas degradam a legibilidade de texto sobreposto pequeno — o limite não foi medido. Esta nota deve ser revisada se o método for aplicado a outro acervo, se a grade mudar ou se o número de imagens por folha for reavaliado.
