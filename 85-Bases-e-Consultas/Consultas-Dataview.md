---
id: consulta-consultas-dataview
titulo: Consultas-Dataview
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
- consulta
- dataview
fontes_documentais:
- '[[Fonte - Briefing do projeto]]'
notas_relacionadas:
- '[[LEIA-ME-Bases-e-Consultas]]'
- '[[MOC-Metricas-e-Decisao]]'
confidencialidade: interno
subtipo: consulta
---

# Consultas-Dataview

> [!summary] Síntese
> Coleção de consultas opcionais testadas quanto a campos e caminhos, mas não executadas no aplicativo.

## Projetos ativos

```dataview
TABLE status, prioridade, responsavel, proxima_revisao
FROM "03-Projetos-Campanhas-e-Eventos"
WHERE status != "arquivado"
SORT prioridade ASC, file.name ASC
```

## Pendências

```dataview
TABLE prioridade, responsavel, prazo
FROM "99-Pendencias" OR "08-Agenda-e-Execucao"
WHERE tipo = "pendencia" AND status != "concluida"
SORT prioridade ASC, prazo ASC
```

## Notas com baixa confiança

```dataview
TABLE tipo, grau_confianca, ultima_revisao
FROM ""
WHERE grau_confianca = "baixo" OR grau_confianca = "medio"
WHERE !contains(file.path, "90-Templates") AND !contains(file.path, "97-Fontes-Brutas/00-Original")
SORT file.path ASC
```

## Reuniões recentes

```dataview
TABLE data_reuniao, status
FROM "07-Reunioes-e-Decisoes"
WHERE tipo = "reuniao"
SORT data_reuniao DESC
```

## Relações justificadas

- [[LEIA-ME-Bases-e-Consultas]] — explica dependência.
- [[MOC-Metricas-e-Decisao]] — é alternativa manual.

## Fontes e rastreabilidade

- [[Fonte - Briefing do projeto]]

## Limitações e revisão

Esta nota deve ser revisada quando a fonte, o responsável, a data, a metodologia ou o estado operacional mudar.
