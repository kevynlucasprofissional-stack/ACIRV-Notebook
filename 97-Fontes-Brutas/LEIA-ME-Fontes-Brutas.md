---
id: fonte-leia-me-fontes-brutas
titulo: LEIA-ME-Fontes-Brutas
aliases: []
tipo: fonte
status: auditado
profundidade: avancada
versao_schema: '1.0'
versao_conteudo: '2.0'
idioma: pt-BR
data_criacao: '2026-06-17'
ultima_revisao: '2026-09-17'
grau_confianca: alto
camadas_evidencia:
- fato_documentado
- interpretacao_operacional
tags:
- fontes
- proveniencia
fontes_documentais:
- '[[Fonte - Briefing do projeto]]'
notas_relacionadas:
- '[[Manifesto-de-Preservacao-de-Fontes]]'
- '[[Politica-de-Fontes-e-Evidencia]]'
- '[[MOC-Fontes-e-Auditoria]]'
confidencialidade: interno
subtipo: guia
---

# LEIA-ME-Fontes-Brutas

> [!summary] Síntese
> `97-Fontes-Brutas/` é uma camada derivada de evidência, proveniência, seleção e auditoria. A origem primária viva do repositório é `000-Arquivos-originais/`, que deve permanecer imutável para IAs e automações.

## O que esta pasta é

Esta pasta organiza mecanismos que tornam as fontes mais fáceis de verificar e auditar sem exigir que os arquivos originais sejam modificados.

Pode conter:

- índices e notas de fonte em `01-Indices`;
- documentos selecionados em `02-Selecionadas` quando uma cópia operacional for útil;
- registros de risco e quarentena em `03-Quarentena`;
- anexos derivados em `04-Anexos`;
- manifestos, hashes, referências e artefatos históricos do processo inicial de preservação.

## O que esta pasta não é

`97-Fontes-Brutas/` não é a caixa de entrada humana do vault e não substitui `000-Arquivos-originais/`.

Uma cópia selecionada ou indexada aqui é evidência derivada. O registro de origem continua sendo o arquivo localizado em `000-Arquivos-originais/` ou, para partes históricas do corpus, o artefato primário preservado e identificado no manifesto correspondente.

## Originais atuais

Novas notas manuais, ideias, documentos e demais materiais livres devem ser depositados pelo usuário em `000-Arquivos-originais/`.

Agentes podem ler essa pasta, detectar mudanças e derivar conhecimento, porém nunca alterar, excluir, mover, renomear ou normalizar seus arquivos.

## Acesso rápido

Use [[MOC-Fontes-e-Auditoria]], as notas de fonte em `01-Indices` e os manifestos disponíveis nesta camada para localizar a evidência relacionada a uma nota canônica.

## Artefatos históricos

O ZIP original e outras estruturas de preservação criadas no release inicial continuam sendo evidência válida do corpus histórico. Eles não precisam ser apagados ou migrados apenas porque a arquitetura passou a adotar `000-Arquivos-originais/` como camada contínua de captura.

## Princípio de síntese

As notas canônicas devem resumir e consolidar apenas o necessário. Preservar o original permite revisitar contexto, corrigir interpretações futuras e produzir novas sínteses sem perda da fonte.

## Segurança

Leia [[Privacidade-e-Seguranca]] e a documentação de quarentena antes de abrir ou redistribuir material sensível. O saneamento ocorre em derivados apropriados; nunca por edição do original.

## Relações justificadas

- [[Manifesto-de-Preservacao-de-Fontes]] — define imutabilidade e preservação.
- [[Politica-de-Fontes-e-Evidencia]] — define autoridade e promoção.
- [[MOC-Fontes-e-Auditoria]] — navega índices e evidências.

## Fontes e rastreabilidade

- [[Fonte - Briefing do projeto]]
- `000-Arquivos-originais/` — corpus primário vivo.

## Limitações e revisão

Esta nota deve ser revisada sempre que mudar o papel de `97-Fontes-Brutas/`, a estrutura de proveniência ou o mecanismo de ingestão do vault.
