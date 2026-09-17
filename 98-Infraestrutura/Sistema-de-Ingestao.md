---
id: infraestrutura-sistema-ingestao
titulo: Sistema-de-Ingestao-e-Paridade
aliases: [ingestao, ledger, claims]
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
- ingestao
- proveniencia
fontes_documentais:
- '[[Politica-de-Fontes-e-Evidencia]]'
- '[[Manifesto-de-Preservacao-de-Fontes]]'
notas_relacionadas:
- '[[Metodologia]]'
- '[[Ontologia-do-Vault]]'
- '[[Schema-de-Propriedades]]'
confidencialidade: interno
subtipo: documentacao
---

# Sistema de Ingestão e Paridade — ACIRV Notebook

> [!summary] Síntese
> Documentação operacional do sistema determinístico de ingestão, proveniência e paridade entre fontes humanas (`000-Arquivos-originais/`) e conhecimento canônico (`00-*` a `99-*`). Implementado em setembro de 2026.

## Arquitetura

```
000-Arquivos-originais/
    ↓ (git ls-files --format)
inventariar_fontes.py
    → Ledger-de-Ingestao.jsonl (identidade: source_path + blob_sha)
    ↓ (safety gate primeiro)
safety_gate.py
    → classificação de sensibilidade SEM abertura de conteúdo
    ↓ (leitura somente se read_status = unread)
[processamento manual ou Hermes]
    → Claims-Canonicos.jsonl (unit: source → versão → claim → disposition)
    ↓ (promoção quando evidence suficiente)
notas canônicas (00-* a 99-*)
    ↓ (auditoria)
validar_invariantes.py + relatorio_cobertura.py
```

## Scripts (em `98-Infraestrutura/ingestao/`)

| Script | Função |
|---|---|
| `safety_gate.py` | Classifica sensibilidade por nome/caminho — nunca abre o arquivo |
| `inventariar_fontes.py` | Popula/atualiza `Ledger-de-Ingestao.jsonl` com blob SHAs do Git |
| `claims.py` | Schema, validação e persistência de claims canônicos |
| `validar_invariantes.py` | Verifica todos os invariantes do sistema |
| `relatorio_cobertura.py` | Gera relatório reproduzível de cobertura |
| `test_invariantes.py` | Suite de testes unitários (28 testes) |

## Arquivos de dados (em `85-Bases-e-Consultas/`)

| Arquivo | Conteúdo |
|---|---|
| `Ledger-de-Ingestao.jsonl` | Uma entrada por (source_path, blob_sha) — identidade de versão |
| `Claims-Canonicos.jsonl` | Claims materiais com disposition e rastreabilidade |
| `Relatorio-de-Cobertura.md` | Relatório gerado pelo `relatorio_cobertura.py` |

## Identidade de versão

A identidade mínima de uma fonte é:

```
source_path + blob_sha (Git object SHA)
```

**Não use timestamp de filesystem** — o Git blob SHA é determinístico e imutável por conteúdo.

## Safety gate

O safety gate opera **antes** de qualquer leitura:

```python
result = classify(path)
if result.read_status == "sensitive_do_not_read":
    # NÃO ABRIR
```

Caminhos confirmados sensíveis:
- `000-Arquivos-originais/Contas e Senhas.md` → `confirmed_secret`
- `000-Arquivos-originais/Minha Chave API Antropic.md` → `confirmed_secret`

Qualquer arquivo com padrão suspeito no nome (senha, token, apikey, chave, etc.) é classificado como `secret_suspected` e não é aberto.

## Estados do ledger

| Campo | Valores possíveis |
|---|---|
| `sensitivity` | `normal`, `personal_data`, `confidential_process`, `secret_suspected`, `confirmed_secret`, `technical_quarantine` |
| `read_status` | `unread`, `processed`, `sensitive_do_not_read`, `unsupported`, `error` |
| `processing_status` | `unprocessed`, `processed`, `error` |
| `source_status` | `active`, `deleted_by_human` |

## Dispositions de claims

| Disposition | Semântica |
|---|---|
| `promoted` | Promovido para nota canônica com destino explícito |
| `duplicate` | Duplicata de claim já registrado |
| `superseded` | Substituído por fonte ou claim mais recente |
| `contradiction` | Contradição registrada — aguarda resolução |
| `pending_validation` | Aguarda validação humana |
| `not_material` | Não material — não promovido |
| `sensitive_skip` | Pulado por conteúdo sensível |
| `unsupported` | Formato não suportado |
| `error` | Erro durante processamento |

## Idempotência

Se `(source_path, blob_sha)` já está no ledger com `processing_status != unprocessed/error`, o script pula sem reprocessar.

Se o arquivo foi modificado (novo blob_sha), a nova entrada é criada com `is_version_update=true` e `supersedes_sha` apontando para a versão anterior.

## Triagem diária (rotina incremental)

```bash
# 1. Inventariar novas fontes e detectar mudanças
python inventariar_fontes.py <vault_root>

# 2. Validar invariantes
python validar_invariantes.py <vault_root>

# 3. Gerar relatório de cobertura
python relatorio_cobertura.py <vault_root>
```

A rotina processa apenas o delta — fontes sem mudança de blob_sha são puladas (`unchanged_skip`).

## Testes

```bash
# Executar suite completa (28 testes)
cd 98-Infraestrutura/ingestao
python -m pytest test_invariantes.py -v
```

Cobre: imutabilidade de fontes, safety gate, idempotência, versionamento, remoção, claims, proveniência, contradições, divergência de validação, schema.

## Invariantes verificados automaticamente

1. `000-Arquivos-originais/` nunca é modificado por scripts
2. Os dois caminhos sensíveis confirmados são bloqueados sem abertura
3. Ledger não contém duplicatas `(source_path, blob_sha)`
4. Claims promovidos têm `source_blob_sha` e `canonical_destination`
5. Contradições não aparecem como `validated`
6. `pending_validation` não aparece como `validated` em campos diferentes

## Decisão arquitetural: JSONL vs SQLite vs Markdown

**JSONL** foi escolhido por:
- Diff Git legível linha a linha
- Sem dependência de banco de dados
- Consumível pelo Hermes e por qualquer ferramenta que leia JSON
- Sem conflitos de merge em inserções ao final do arquivo
- Append-only natural para o ledger

**SQLite** foi descartado por requerer ferramenta adicional para diff e por ser um formato binário.

**Markdown puro** foi descartado por ser difícil de parsear deterministicamente para claims granulares.

## Limitações atuais

- Processing de conteúdo textual (extração de claims) é manual nesta versão
- PDFs e outros formatos binários precisam de processamento externo antes da extração de claims
- Ledger de ingestão cobre apenas `000-Arquivos-originais/` — não inclui `97-Fontes-Brutas/`

## Relações justificadas

- [[Politica-de-Fontes-e-Evidencia]] — orienta regras de promoção
- [[Manifesto-de-Preservacao-de-Fontes]] — protege a camada original
- [[Metodologia]] — contexto do processo geral
