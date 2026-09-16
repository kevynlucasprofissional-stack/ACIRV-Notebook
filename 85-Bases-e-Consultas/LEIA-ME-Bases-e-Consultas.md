---
id: consulta-leia-me-bases-e-consultas
titulo: LEIA-ME-Bases-e-Consultas
aliases: []
tipo: consulta
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
- '[[Dependencias-e-Compatibilidade]]'
- '[[MOC-Geral]]'
confidencialidade: interno
subtipo: guia_tecnico
---

# LEIA-ME-Bases-e-Consultas

> [!summary] Síntese
> Explica as vistas nativas e consultas opcionais incluídas no vault.

## Bases

Arquivos `.base` são vistas nativas sobre propriedades: Projetos e Eventos, Indicadores, Reuniões e Stakeholders. Use-as para filtrar e editar metadados.

## Dataview

Consultas em [[Consultas-Dataview]] são opcionais e somente leitura. Instale o plugin comunitário para renderizá-las.

## Modo degradado

Todos os itens essenciais aparecem também em MOCs manuais; a navegação não depende de plugin.

## Teste

A sintaxe YAML dos `.base` foi validada estaticamente. A renderização no aplicativo Obsidian não foi executada neste ambiente.

## Relações justificadas

- [[Dependencias-e-Compatibilidade]] — documenta requisitos.
- [[MOC-Geral]] — oferece alternativa manual.

## Fontes e rastreabilidade

- [[Fonte - Briefing do projeto]]

## Limitações e revisão

Esta nota deve ser revisada quando a fonte, o responsável, a data, a metodologia ou o estado operacional mudar.
