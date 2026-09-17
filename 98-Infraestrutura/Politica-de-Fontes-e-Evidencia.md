---
id: infraestrutura-politica-de-fontes-e-evidencia
titulo: Politica-de-Fontes-e-Evidencia
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
- evidencia
fontes_documentais:
- '[[Fonte - Briefing do projeto]]'
notas_relacionadas:
- '[[Metodologia]]'
- '[[Manifesto-de-Preservacao-de-Fontes]]'
- '[[Fonte - Notas Operacionais]]'
- '[[Politica-Editorial-de-Evidencia]]'
confidencialidade: interno
subtipo: politica
---

# Politica-de-Fontes-e-Evidencia

> [!summary] Síntese
> Define como fontes entram no ACIRV Notebook, como sua autoridade é avaliada e como conhecimento é promovido de `000-Arquivos-originais/` para a camada canônica sem modificar a origem.

## Arquitetura de fonte

### Origem primária — `000-Arquivos-originais/`

É o corpus humano permanente: notas, diários, documentos recebidos, arquivos de trabalho e registros livres. Não precisa obedecer ao schema da camada estruturada.

Para IAs e automações, essa pasta é somente leitura. Sua função é preservar o registro original e permitir reinterpretação futura.

### Evidência técnica — `97-Fontes-Brutas/`

É uma camada derivada de suporte: índices, hashes, seleção, manifestos, quarentena, referências e artefatos históricos de preservação. Não substitui a fonte primária e não deve competir com ela como origem canônica.

### Conhecimento canônico — `00-*` a `99-*`

É onde fatos, interpretações, processos, projetos, métricas e decisões são consolidados em formas estáveis e reutilizáveis.

## Hierarquia de autoridade

A autoridade depende da natureza da afirmação, não apenas da pasta em que o arquivo está.

Como regra geral:

1. registro primário contemporâneo ao fato, dado ou decisão;
2. documento institucional ou registro formal de decisão;
3. dado estruturado ou relatório especializado com período e metodologia identificáveis;
4. nota operacional humana;
5. síntese derivada previamente auditada;
6. conversa, conteúdo gerado por IA ou inferência como indício, nunca como autoridade automática.

Quando duas fontes divergem, não escolher silenciosamente uma versão. Registrar período, autoria/contexto e conflito, e buscar evidência adicional quando necessário.

## Camadas de evidência

- `fato_documentado`: afirmação explícita sustentada por fonte identificável;
- `dado_calculado`: cálculo reproduzível a partir de dados rastreáveis;
- `interpretacao_operacional`: síntese aplicada ao trabalho, distinguida do fato bruto;
- `hipotese_de_trabalho`: explicação ou proposta ainda não confirmada;
- `recurso_pedagogico`: reorganização destinada à compreensão ou uso;
- `representacao_visual`: mapa, Canvas, grafo ou visualização; não constitui prova por si só.

## Regra de promoção

Antes de criar ou atualizar uma nota canônica a partir de `000-Arquivos-originais/`:

1. verificar se o conhecimento já está representado no vault;
2. identificar a nota canônica mais específica e estável;
3. comparar a nova fonte com o estado atual;
4. promover somente informação nova, corrigida ou materialmente mais precisa;
5. preservar a proveniência da afirmação;
6. manter datas e períodos quando a informação for temporal;
7. registrar contradições e incertezas;
8. evitar cópia extensa quando uma síntese fiel for suficiente;
9. nunca editar a fonte para fazê-la concordar com a síntese.

## Atualidade

Informação mais recente não é automaticamente mais verdadeira, mas pode substituir o estado operacional anterior quando houver evidência clara de mudança.

Quando uma nota canônica consolidar estados ao longo do tempo, preservar histórico útil em vez de sobrescrever contexto necessário para auditoria.

## Conteúdo de agentes

Resultados produzidos por Hermes, ChatGPT ou outras IAs podem sugerir sínteses, relações, hipóteses e atualizações. Eles só se tornam conhecimento canônico quando estão sustentados por evidência apropriada ou claramente identificados como interpretação/hipótese.

Estado interno de agente, execução de tarefa e raciocínio operacional não devem ser tratados como fato institucional.

## Rastreabilidade

Notas canônicas devem indicar fonte nominal ou caminho quando relevante; dados voláteis devem indicar período; divergências devem permanecer visíveis até resolução.

A referência a `000-Arquivos-originais/` deve ser suficiente para localizar novamente o material sem exigir que o arquivo seja renomeado ou adaptado à ontologia.

## Web

Fontes públicas externas podem complementar ou verificar fatos externos quando necessário, mas não devem preencher lacunas institucionais da ACIRV por suposição. Informação interna deve continuar apoiada em fontes internas identificáveis.

## Limite

Toda fonte pode estar incompleta, desatualizada ou errada. Prioridade documental não elimina crítica, comparação temporal ou validação humana.

## Relações justificadas

- [[Metodologia]] — aplica a política.
- [[Manifesto-de-Preservacao-de-Fontes]] — protege a origem.
- [[Fonte - Notas Operacionais]] — representa parte do corpus histórico.
- [[Politica-Editorial-de-Evidencia]] — aplica evidência à publicação.

## Fontes e rastreabilidade

- [[Fonte - Briefing do projeto]]
- `000-Arquivos-originais/` — corpus primário vivo.

## Limitações e revisão

Esta nota deve ser revisada quando a arquitetura de fontes, os critérios de autoridade, os mecanismos de ingestão ou o processo de validação mudarem.
