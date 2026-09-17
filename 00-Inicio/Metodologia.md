---
id: documentacao-metodologia
titulo: Metodologia
aliases: []
tipo: documentacao
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
- metodologia
fontes_documentais:
- '[[Fonte - Briefing do projeto]]'
- '[[Fonte - Notas Operacionais]]'
notas_relacionadas:
- '[[Ontologia-do-Vault]]'
- '[[Politica-de-Fontes-e-Evidencia]]'
- '[[Manifesto-de-Preservacao-de-Fontes]]'
- '[[Relatorio-de-Auditoria-do-Vault]]'
confidencialidade: interno
subtipo: metodologia
---

# Metodologia

> [!summary] Síntese
> Método contínuo de transformação de registros humanos e documentos primários em conhecimento operacional estruturado, rastreável e reutilizável, sem alterar a fonte original.

## Arquitetura de trabalho

O ACIRV Notebook opera em três camadas:

1. `000-Arquivos-originais/`: captura humana e fontes primárias, livre na forma e imutável para IAs;
2. `00-*` a `99-*`: conhecimento estruturado e canônico;
3. áreas de agentes e automações, como `Hermes/`: execução, estado e artefatos operacionais.

`.obsidian/` contém configuração do ambiente e não é uma camada de conhecimento.

## Fluxo metodológico

O fluxo de conhecimento é predominantemente unidirecional:

`captura humana → 000-Arquivos-originais → inspeção → comparação → síntese → camada canônica → uso operacional/agentes`.

A fonte original permanece intacta. Corrigir ou consolidar conhecimento significa atualizar a camada derivada apropriada, não reescrever o registro de origem.

## Ingestão contínua

A ingestão pode ocorrer manualmente ou por rotina automatizada. Em cada ciclo:

1. detectar arquivos novos ou modificados em `000-Arquivos-originais/`;
2. ler apenas o necessário para compreender a mudança;
3. localizar conhecimento canônico relacionado;
4. comparar a informação nova com o estado existente;
5. classificar cada descoberta por camada de evidência;
6. promover apenas novidade material ou correção comprovada;
7. registrar proveniência, período, conflitos e grau de confiança;
8. sinalizar o que depende de validação humana;
9. manter o estado de ingestão fora da pasta de originais.

A ausência de novidade não justifica alterações cosméticas na camada canônica.

## Seleção

Fontes primárias ou operacionais recebem prioridade conforme a natureza da afirmação. Versões antigas, documentos históricos e conteúdo gerado por IA permanecem úteis como contexto, mas não devem ser confundidos com estado atual sem evidência temporal.

Duplicatas e contradições devem ser registradas ou consolidadas; nunca ocultadas por edição da fonte original.

## Camadas de evidência

- `fato_documentado`: registro explícito em documento ou dado;
- `dado_calculado`: cálculo reproduzível a partir de fonte;
- `interpretacao_operacional`: síntese aplicada ao fluxo de trabalho;
- `hipotese_de_trabalho`: proposta ainda não confirmada;
- `recurso_pedagogico`: organização para facilitar uso;
- `representacao_visual`: Canvas ou grafo, nunca usado como prova.

## Profundidade

Notas de estratégia, processo e decisão são avançadas. Projetos recebem profundidade proporcional à evidência. Fontes e índices priorizam rastreabilidade. Itens periféricos ficam como pendências qualificadas em vez de verbetes fictícios.

## Deduplicação e promoção

Quando uma fonte trouxer conhecimento já existente, atualizar a nota canônica adequada em vez de criar uma nova nota paralela. Uma nova nota só deve surgir quando representar uma entidade, processo, projeto, decisão ou conjunto de conhecimento com identidade própria.

A promoção deve preservar a diferença entre:

- o que a fonte afirma;
- o que pode ser calculado;
- o que foi interpretado;
- o que ainda é hipótese.

## Auditoria

Devem ser testados, quando aplicáveis: YAML, IDs, basenames, wikilinks, cabeçalhos/blocos, JSON Canvas, referências de Canvas, arquivos `.base`, JSON de configuração, vocabulários, densidade, duplicação textual, inventário, checksums e integridade das fontes/evidências.

Auditorias da camada estruturada não autorizam normalização retroativa de `000-Arquivos-originais/`.

## Relações justificadas

- [[Ontologia-do-Vault]] — define tipos e relações.
- [[Politica-de-Fontes-e-Evidencia]] — formaliza autoridade e promoção.
- [[Manifesto-de-Preservacao-de-Fontes]] — protege a camada de origem.
- [[Relatorio-de-Auditoria-do-Vault]] — registra testes reais.

## Fontes e rastreabilidade

- [[Fonte - Briefing do projeto]]
- [[Fonte - Notas Operacionais]]
- `000-Arquivos-originais/` — corpus primário contínuo.

## Limitações e revisão

Esta nota deve ser revisada quando a fonte, o responsável, a metodologia, a ontologia, o mecanismo de ingestão ou o estado operacional mudar.
