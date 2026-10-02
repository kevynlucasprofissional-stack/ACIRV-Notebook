---
id: infraestrutura-sistema-ingestao
titulo: Sistema-de-Ingestao-e-Paridade
aliases: [ingestao, ledger, claims]
tipo: infraestrutura
status: ativo
profundidade: avancada
versao_schema: '2.0'
versao_conteudo: '2.0'
idioma: pt-BR
data_criacao: '2026-09-17'
ultima_revisao: '2026-09-17'
grau_confianca: alto
camadas_evidencia:
- fato_documentado
tags:
- infraestrutura
- ingestao
- proveniencia
fontes_documentais:
- '[[Politica-de-Fontes-e-Evidencia]]'
- '[[Manifesto-de-Preservacao-de-Fontes]]'
- '[[Decisao-Arquitetural-Ingestao-Narrativa]]'
notas_relacionadas:
- '[[Metodologia]]'
- '[[Ontologia-do-Vault]]'
- '[[Contrato-de-Nota-Canonica-Narrativa]]'
confidencialidade: interno
subtipo: documentacao
---

# Sistema de Ingestão e Paridade — ACIRV Notebook

> [!summary] Síntese
> Documentação da infraestrutura determinística de apoio à ingestão semântica e paridade entre fontes humanas (`000-Arquivos-originais/`) e conhecimento canônico (`00-*` a `99-*`).

## Arquitetura da Solução

```text
fontes humanas imutáveis (000-Arquivos-originais/)
        ↓ (git ls-files --format)
inventariar_fontes.py
        → Ledger-de-Ingestao.jsonl (identidade: source_path + blob_sha)
        ↓ (safety gate pré-leitura)
safety_gate.py
        → classificação de sensibilidade SEM abertura de conteúdo
        ↓
ChatGPT Agendado (Camada Cognitiva & Editorial)
        → lê deltas elegíveis, compreende contexto e evolução temporal
        → escreve/atualiza NOTAS CANÔNICAS NARRATIVAS (00-* a 99-*)
        → registra claims de evidência atômicos em Claims-Canonicos.jsonl
        ↓
scripts Python de garantia
        → claims.py (sintaxe, IDs ASCII, integridade referencial, anchors)
        → validar_invariantes.py (segurança, imutabilidade runtime, idempotência)
        → relatorio_cobertura.py (métricas de cobertura real)
        ↓
PR auditável no GitHub (sem auto-merge)
```

## Scripts (em `98-Infraestrutura/ingestao/`)

| Script | Função |
|---|---|
| `safety_gate.py` | Classifica sensibilidade por nome/caminho — bloqueia credenciais sem abrir conteúdo |
| `inventariar_fontes.py` | Popula/atualiza `Ledger-de-Ingestao.jsonl` por `blob_sha` (idempotência absoluta) |
| `claims.py` | Valida schema estrito, IDs ASCII, integridade referencial e âncoras de evidência |
| `validar_invariantes.py` | Verifica invariantes do vault, incluindo snapshot runtime de imutabilidade |
| `relatorio_cobertura.py` | Gera relatório de cobertura de accounting Git, revisão e evidências |
| `test_invariantes.py` | Suíte de testes unitários e de integração (28+ testes com repo Git temporário) |

## Arquivos de dados (em `85-Bases-e-Consultas/`)

| Arquivo | Conteúdo |
|---|---|
| `Ledger-de-Ingestao.jsonl` | Registro por `(source_path, blob_sha)` com `review_status` editorial |
| `Claims-Canonicos.jsonl` | Âncoras de evidência atômicas (KPIs, datas, decisões, valores) |
| `Relatorio-de-Cobertura.md` | Relatório gerado reproduzível de cobertura real do vault |

## Conceito do Ledger: `review_status`

Separamos categoricamente a inventariação determinística da revisão editorial semântica. Uma fonte possui um dos seguintes estados de revisão em `Ledger-de-Ingestao.jsonl`:

- `unreviewed`: Inventariada, aguarda leitura pelo ChatGPT Agendado.
- `reviewed`: Revisada pelo ChatGPT com alterações/sínteses promovidas para o canônico.
- `reviewed_no_material_change`: Revisada pelo ChatGPT, mas sem novidade material (redundante, rascunho histórico, ou já coberta integralmente pelo canônico).
- `partially_reviewed`: Análise em andamento ou parcial.
- `sensitive_do_not_read`: Bloqueada pelo safety gate (credenciais/segredos).
- `unsupported`: Formato binário não suportado para extração direta de texto.
- `error`: Erro durante o processamento.

*Regra:* Uma fonte pode ficar em `reviewed_no_material_change` com **0 claims novos**. Isso é um estado perfeitamente válido e esperado.

## Claims como Âncoras de Evidência

Claims não tentam reconstruir a nota canônica nem representar 100% do texto. Eles atuam como âncoras para afirmações materiais que exigem auditabilidade estrita.

Exemplos de propriedades que geram claims:
- Data / cronograma formal;
- Valor financeiro / remanejamento de verba;
- KPI / métrica observada;
- Decisão formal de diretoria;
- Regra ou alteração de política institucional.

## Imutabilidade Runtime

O validador `validar_invariantes.py` realiza snapshots dos hashes dos arquivos em `000-Arquivos-originais/` antes e depois da execução dos scripts para garantir que a própria automação nunca modifique a camada de origem.
