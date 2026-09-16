---
id: documentacao-metodologia
titulo: Metodologia
aliases: []
tipo: documentacao
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
- metodologia
fontes_documentais:
- '[[Fonte - Briefing do projeto]]'
- '[[Fonte - Notas Operacionais]]'
notas_relacionadas:
- '[[Ontologia-do-Vault]]'
- '[[Politica-de-Fontes-e-Evidencia]]'
- '[[Relatorio-de-Auditoria-do-Vault]]'
confidencialidade: interno
subtipo: metodologia
---

# Metodologia

> [!summary] Síntese
> Método de transformação do arquivo bruto em conhecimento operacional: inspeção, delimitação, autoridade, ontologia, inventário, arquitetura, produção, links semânticos, navegação, recursos Obsidian, auditoria e release.

## Seleção

O corpus foi inventariado por formato, tamanho, hash e caminho. Fontes primárias ou operacionais receberam prioridade; versões antigas e conteúdo gerado em conversas com IA foram tratados como contexto. Duplicatas e arquivos vazios foram registrados, não ocultados.

## Camadas de evidência

- `fato_documentado`: registro explícito em documento ou dado;
- `dado_calculado`: cálculo reproduzível a partir de fonte;
- `interpretacao_operacional`: síntese aplicada ao fluxo de trabalho;
- `hipotese_de_trabalho`: proposta ainda não confirmada;
- `recurso_pedagogico`: organização para facilitar uso;
- `representacao_visual`: Canvas ou grafo, nunca usado como prova.

## Profundidade

Notas de estratégia, processo e decisão são avançadas. Projetos recebem profundidade proporcional à evidência. Fontes e índices priorizam rastreabilidade. Itens periféricos ficam como pendências qualificadas em vez de verbetes fictícios.

## Auditoria

Foram testados YAML, IDs, basenames, wikilinks, cabeçalhos/blocos, JSON Canvas, referências de Canvas, arquivos `.base`, JSON de configuração, vocabulários, densidade, duplicação textual, inventário, checksums, ZIP e equivalência após extração.

## Relações justificadas

- [[Ontologia-do-Vault]] — define tipos e relações.
- [[Politica-de-Fontes-e-Evidencia]] — formaliza autoridade.
- [[Relatorio-de-Auditoria-do-Vault]] — registra testes reais.

## Fontes e rastreabilidade

- [[Fonte - Briefing do projeto]]
- [[Fonte - Notas Operacionais]]

## Limitações e revisão

Esta nota deve ser revisada quando a fonte, o responsável, a data, a metodologia ou o estado operacional mudar.
