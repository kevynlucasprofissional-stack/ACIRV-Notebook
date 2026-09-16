---
id: infraestrutura-schema-de-propriedades
titulo: Schema-de-Propriedades
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
- '[[Ontologia-do-Vault]]'
- '[[Convencoes-de-Nomenclatura]]'
- '[[Auditoria-de-Links-e-Metadados]]'
confidencialidade: interno
subtipo: schema
---

# Schema-de-Propriedades

> [!summary] Síntese
> Contrato YAML comum e campos condicionais do vault.

## Universais

`id`, `titulo`, `aliases`, `tipo`, `subtipo`, `status`, `profundidade`, `versao_schema`, `versao_conteudo`, `idioma`, `data_criacao`, `ultima_revisao`, `grau_confianca`, `camadas_evidencia`, `tags`, `fontes_documentais`, `notas_relacionadas`, `confidencialidade`.

## Tipos controlados

`documentacao`, `estrategia`, `processo`, `projeto`, `canal`, `metrica`, `stakeholder`, `reuniao`, `operacao`, `moc`, `trilha`, `consulta`, `template`, `auditoria`, `fonte`, `infraestrutura`, `pendencia`.

## Condicionais

`data_reuniao` para reunião; `prioridade`, `responsavel`, `prazo` para trabalho; `kanban-plugin` no quadro; campos de projeto podem ser adicionados quando governados.

## Vocabulários

Status: rascunho, em_pesquisa, em_revisao, revisado, auditado, arquivado, concluida. Profundidade: indice, introdutoria, intermediaria, avancada, dossie. Confiança: alto, medio_alto, medio, medio_baixo, baixo, nao_avaliado.

## Compatibilidade

Campos planos e listas, adequados a Properties, Bases e Dataview. Links em propriedades usam strings de wikilinks para notas existentes.

## Versão

Schema 1.0. Alterações exigem migração, auditoria e changelog.

## Relações justificadas

- [[Ontologia-do-Vault]] — define tipos.
- [[Convencoes-de-Nomenclatura]] — define nomes.
- [[Auditoria-de-Links-e-Metadados]] — valida contrato.

## Fontes e rastreabilidade

- [[Fonte - Briefing do projeto]]

## Limitações e revisão

Esta nota deve ser revisada quando a fonte, o responsável, a data, a metodologia ou o estado operacional mudar.
