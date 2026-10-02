---
id: infraestrutura-convencoes-de-nomenclatura
titulo: Convencoes-de-Nomenclatura
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
- '[[Manifesto-de-Preservacao-de-Fontes]]'
- '[[Auditoria-de-Links-e-Metadados]]'
confidencialidade: interno
subtipo: convencao
---

# Convencoes-de-Nomenclatura

> [!summary] Síntese
> Padrão de nomes para estabilidade de links e manutenção.

## Arquivos

Basenames únicos; sem barras, dois-pontos ou caracteres reservados; nomes legíveis; datas ISO em registros; versão explícita quando necessária.

## Títulos

Podem usar linguagem natural no YAML; o basename permanece estável.

## IDs

Minúsculos, derivados de tipo e basename, únicos no vault.

## Pastas

Numeração por função, não por decoração. Nenhuma pasta vazia.

## Arquivos operacionais

`AAAA-MM-DD - Projeto - Entrega - Status`. Evitar “final-final”.

## Fontes brutas

Manter nome original quando preservado; cópias selecionadas recebem nome normalizado e hash no manifesto.

## Relações justificadas

- [[Schema-de-Propriedades]] — define IDs.
- [[Manifesto-de-Preservacao-de-Fontes]] — governa cópias.
- [[Auditoria-de-Links-e-Metadados]] — detecta duplicidade.

## Fontes e rastreabilidade

- [[Fonte - Briefing do projeto]]

## Limitações e revisão

Esta nota deve ser revisada quando a fonte, o responsável, a data, a metodologia ou o estado operacional mudar.
