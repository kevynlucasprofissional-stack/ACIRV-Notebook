---
id: infraestrutura-ontologia-do-vault
titulo: Ontologia-do-Vault
aliases: []
tipo: infraestrutura
status: auditado
profundidade: avancada
versao_schema: '1.0'
versao_conteudo: '1.0'
idioma: pt-BR
data_criacao: '2026-06-17'
ultima_revisao: '2026-06-17'
grau_confianca: alto
camadas_evidencia:
- fato_documentado
- interpretacao_operacional
tags:
- infraestrutura
fontes_documentais:
- '[[Fonte - Briefing do projeto]]'
notas_relacionadas:
- '[[Schema-de-Propriedades]]'
- '[[MOC-Geral]]'
- '[[Politica-de-Links-Semanticos]]'
confidencialidade: interno
subtipo: ontologia
---

# Ontologia-do-Vault

> [!summary] Síntese
> Modelo dos tipos de nota e relações permitidas.

## Tipos principais

`documentacao`, `estrategia`, `processo`, `projeto`, `canal`, `metrica`, `stakeholder`, `reuniao`, `operacao`, `moc`, `trilha`, `consulta`, `template`, `auditoria`, `fonte`, `infraestrutura` e `pendencia`. O campo `subtipo` preserva distinções como evento, campanha, pessoa, manual, indicador ou ritual.

## Relações

`orienta`, `desdobra`, `aplica`, `depende_de`, `documenta`, `evidencia`, `governa`, `mede`, `participa_de`, `contextualiza`, `sucede`, `contrasta_com`, `integra`.

## Direção

Estratégia orienta processo; processo governa projeto; projeto usa canal; métrica mede objetivo; fonte documenta afirmação; decisão altera estado. Relações simétricas, como contraste, devem ser explicitadas nos dois contextos quando úteis.

## Nota de relação própria

Criar quando a relação possui evidência, controvérsia, risco, data ou decisão que não cabe em uma frase contextual.

## Contraexemplo

Duas notas mencionarem “evento” não justifica link. O link deve afirmar uso, dependência, evidência ou participação.

## Relações justificadas

- [[Schema-de-Propriedades]] — implementa a ontologia.
- [[MOC-Geral]] — oferece navegação.
- [[Politica-de-Links-Semanticos]] — define links.

## Fontes e rastreabilidade

- [[Fonte - Briefing do projeto]]

## Limitações e revisão

Esta nota deve ser revisada quando a fonte, o responsável, a data, a metodologia ou o estado operacional mudar.
