---
id: infraestrutura-manifesto-de-preservacao-de-fontes
titulo: Manifesto-de-Preservacao-de-Fontes
aliases: []
tipo: infraestrutura
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
- infraestrutura
- fontes
fontes_documentais:
- '[[Fonte - Briefing do projeto]]'
notas_relacionadas:
- '[[Privacidade-e-Seguranca]]'
- '[[MOC-Fontes-e-Auditoria]]'
- '[[Relatorio-de-Auditoria-do-Vault]]'
- '[[Politica-de-Fontes-e-Evidencia]]'
confidencialidade: interno
subtipo: infraestrutura
---

# Manifesto-de-Preservacao-de-Fontes

> [!summary] Síntese
> `000-Arquivos-originais/` é a camada permanente de captura humana e de fontes primárias do ACIRV Notebook. Para IAs e automações, ela é estritamente somente leitura. `97-Fontes-Brutas/` permanece como camada derivada de evidência, seleção, indexação, auditoria e proveniência — nunca como substituta da origem.

## Fonte primária permanente

Todo material depositado em `000-Arquivos-originais/` deve ser preservado no estado em que foi produzido ou recebido pelo usuário.

A pasta aceita deliberadamente heterogeneidade: notas rápidas, diários, ideias incompletas, documentos, planilhas, arquivos recebidos, versões históricas e outros materiais sem obrigação de seguir a ontologia ou as convenções da camada canônica.

Para agentes de IA, automações e scripts autônomos, `000-Arquivos-originais/` é **imutável**. É proibido alterar, excluir, mover, renomear, corrigir, normalizar, acrescentar frontmatter ou reescrever qualquer conteúdo dentro dela.

A única direção autorizada de transformação automatizada é para fora da pasta:

`000-Arquivos-originais/` → leitura/análise → síntese derivada → camada canônica `00-*` a `99-*`.

## Papel de `97-Fontes-Brutas/`

`97-Fontes-Brutas/` não é a origem primária corrente. É uma camada técnica derivada para facilitar rastreabilidade e auditoria.

Pode conter:

- índices e notas de fonte;
- manifestos e hashes;
- referências a caminhos em `000-Arquivos-originais/`;
- cópias selecionadas quando houver justificativa operacional;
- anexos derivados necessários à consulta;
- quarentena e registros de risco;
- artefatos históricos de preservação anteriores à adoção de `000-Arquivos-originais/`.

Uma cópia em `97-Fontes-Brutas/` nunca autoriza alterar ou substituir o arquivo correspondente em `000-Arquivos-originais/`.

## Artefatos históricos de preservação

O ZIP original e demais artefatos preservados em versões anteriores do vault continuam válidos como evidência histórica. Eles documentam a origem de parte do corpus inicial, mas não definem mais sozinhos a arquitetura de ingestão contínua.

A partir de 17 de setembro de 2026, a camada de captura humana contínua é `000-Arquivos-originais/`.

## Promoção de conhecimento

Promover conhecimento não significa mover a fonte. Significa:

1. ler o original sem modificá-lo;
2. identificar informação nova ou mais atual;
3. localizar a nota canônica correspondente;
4. sintetizar ou atualizar a nota derivada;
5. registrar proveniência suficiente para retornar ao original;
6. preservar divergências, datas, contexto e grau de confiança;
7. não criar duplicata quando uma nota canônica já puder receber a atualização.

## Detecção de mudanças

A rotina diária pode usar histórico do Git, hashes, caminhos e datas para identificar arquivos novos ou alterados. Esse estado de ingestão deve ser mantido fora de `000-Arquivos-originais/`.

A mudança em uma fonte não implica automaticamente que a versão mais nova esteja correta; ela apenas dispara nova análise.

## Quarentena e segurança

Materiais sensíveis ou potencialmente perigosos devem ser lidos conforme [[Privacidade-e-Seguranca]]. A quarentena pode registrar riscos e referências, sem editar a origem para “sanear” o documento.

## Proveniência

Sempre que material de `000-Arquivos-originais/` sustentar uma afirmação canônica, a camada estruturada deve manter referência suficiente à fonte, ao período e, quando relevante, ao trecho ou dado utilizado.

## Relações justificadas

- [[Privacidade-e-Seguranca]] — define proteção.
- [[MOC-Fontes-e-Auditoria]] — navega fontes e evidências.
- [[Relatorio-de-Auditoria-do-Vault]] — valida integridade estrutural.
- [[Politica-de-Fontes-e-Evidencia]] — define autoridade e promoção.

## Fontes e rastreabilidade

- [[Fonte - Briefing do projeto]]
- `000-Arquivos-originais/` — corpus primário vivo e imutável para agentes.

## Limitações e revisão

Esta política deve ser revisada quando mudar a arquitetura de ingestão, preservação, segurança, proveniência ou automação do repositório.
