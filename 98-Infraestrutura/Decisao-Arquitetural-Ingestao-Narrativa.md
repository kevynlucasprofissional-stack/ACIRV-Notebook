---
id: infraestrutura-decisao-arquitetural-ingestao-narrativa
titulo: Decisao-Arquitetural-Ingestao-Narrativa
aliases: [ADR-ingestao-narrativa]
tipo: infraestrutura
status: ativo
profundidade: avancada
versao_schema: '1.0'
versao_conteudo: '1.0'
idioma: pt-BR
data_criacao: '2026-09-17'
ultima_revisao: '2026-09-17'
grau_confianca: alto
camadas_evidencia:
- fato_documentado
tags:
- infraestrutura
- arquitetura
- adr
- ingestao
fontes_documentais:
- '[[Politica-de-Fontes-e-Evidencia]]'
- '[[Manifesto-de-Preservacao-de-Fontes]]'
notas_relacionadas:
- '[[Sistema-de-Ingestao]]'
- '[[Metodologia]]'
- '[[Contrato-de-Nota-Canonica-Narrativa]]'
confidencialidade: interno
subtipo: decisao_arquitetural
---

# Registro de Decisão Arquitetural (ADR) — Transição para Ingestão Semântica Narrativa

> [!summary] Síntese
> Decisão de transição da pipeline de ingestão: do modelo preliminar *claim-centric / script-centric* para o modelo canônico **AI-semantic / narrative-centric com verificação determinística**.

## Contexto

A implementação inicial do sistema de ingestão explorou um modelo no qual scripts Python e arquivos JSONL de claims formavam o centro do processamento de conhecimento. Naquele desenho preliminar, pretendia-se que a extração de claims fosse exaustiva e que notas canônicas pudessem ser derivadas mecanicamente dos dados estruturados.

## Problema

1. O propósito principal do ACIRV Notebook não é atuar como banco de dados relacional de fatos atômicos isolados, mas como **memória institucional narrativa**, contextualizada, orientada a dados e evidências.
2. Scripts Python determinísticos não possuem capacidade cognitiva para interpretar causa e efeito, avaliar a evolução temporal de um projeto, sintetizar reuniões com nuanced context ou construir storytelling institucional útil.
3. Exigir claims para 100% das frases ou tentar reconstruir notas canônicas a partir de listas de claims gera burocracia excessiva, duplicidade e perda de legibilidade humana.

## Decisão

Mudança deliberada da arquitetura de ingestão para o modelo de papéis desemparelhados:

```text
fontes humanas imutáveis (000-Arquivos-originais/)
        ↓
detecção determinística de mudança (Python / git ls-files / blob SHA)
        ↓
ChatGPT Agendado (Camada Cognitiva & Editorial)
        ↓
ChatGPT identifica informação material, contexto e evolução temporal
        ↓
ChatGPT escreve/atualiza NOTAS CANÔNICAS NARRATIVAS (00-* a 99-*)
        ↓
claims/evidências materiais sustentam afirmações importantes (Claims-Canonicos.jsonl)
        ↓
scripts Python verificam integridade, proveniência e segurança (Safety Gate / Invariantes)
        ↓
PR auditável no GitHub (sem auto-merge)
```

### Divisão estrita de papéis:

- **ChatGPT Agendado = Camada Cognitiva e Editorial:** Responsável por ler deltas, compreender a história, sintetizar narrativas canônicas, distinguir fatos de interpretações e temporalidades (`planejado` vs `executado`), e atualizar o repositório.
- **Scripts Python = Infraestrutura de Garantia:** Responsáveis por inventory determinístico, detecção de mudanças por SHA, safety gate pré-leitura, parsing estrito de JSONL, integridade referencial e verificação de imutabilidade da camada de origem.
- **Git = Versionamento e Memória Imutável:** Rastreia o histórico e garante auditabilidade completa.
- **Claims = Âncoras de Evidência:** Registram afirmações materiais críticas (datas, valores, KPIs, decisões formais) como suporte à narrativa, e **não como substituto do texto canônico**.
- **Notas Markdown Narrativas = Conhecimento Canônico Principal:** Onde a memória da ACIRV reside e é consumida por humanos e automações.

## Consequências

1. **Idempotência Real:** O inventário diferencia *já inventariado* de *já revisado sematicamente* (`review_status`). Fontes revisadas sem novidade material ficam em `reviewed_no_material_change` com 0 claims sem gerar erro.
2. **Desacoplamento de Validação Humana:** Claims distinguem documentos originais de suporte (`supporting_sources`) de confirmações humanas posteriores (`validation_source` / `validation_record`).
3. **Qualidade Editorial:** As notas canônicas passam a seguir o [[Contrato-de-Nota-Canonica-Narrativa]], unindo storytelling institucional, dados e evidências rastreáveis.
