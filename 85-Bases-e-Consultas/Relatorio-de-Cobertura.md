---
id: base-relatorio-de-cobertura
titulo: Relatorio-de-Cobertura
tipo: auditoria
subtipo: cobertura
ultima_revisao: '2026-09-17'
confidencialidade: interno
---

# Relatório de Cobertura — ACIRV Notebook

> Gerado em: `2026-09-17T17:10:49.115456+00:00`

## Fontes (000-Arquivos-originais/)

| Métrica | Valor |
|---|---:|
| Total de blobs no ledger | 394 |
| Ativas | 394 |
| Deletadas por humano | 0 |
| `sensitive_do_not_read` | 3 |
| Formato não suportado | 2 |
| Com erro | 0 |
| Processadas | 0 |
| Não processadas | 394 |
| Processáveis (não sensíveis, suportadas) | 389 |

### Por domínio

| Domínio | Fontes |
|---|---:|
| campanhas | 5 |
| conecta | 29 |
| geral | 214 |
| imprensa | 14 |
| marca | 15 |
| metricas | 52 |
| reunioes | 19 |
| servicos | 5 |
| stakeholders | 6 |
| sudoexpo | 19 |
| tecnologia | 16 |

### Por formato

| Extensão | Fontes |
|---|---:|
| `.md` | 390 |
| `.pdf` | 2 |
| `.zip` | 2 |

## Claims Canônicos

| Métrica | Valor |
|---|---:|
| Total de claims | 11 |
| Pending validation | 11 |
| Contradições | 0 |
| Contradições silenciosas (**erro**) | 0 |
| Promovidos | 10 |
| Promovidos com proveniência completa | 10 |

### Por disposition

| Disposition | Claims |
|---|---:|
| `pending_validation` | 1 |
| `promoted` | 10 |

## Métricas de Cobertura

> [!important]
> Denominadores diferentes — não somar como se fossem a mesma métrica.

| Métrica | Valor | Denominador |
|---|---:|---|
| `source_accounting_coverage` | 100.0% | blobs atuais no Git |
| `processable_source_coverage` | 0.0% | fontes processáveis (não sensíveis/unsupported) |
| `material_claim_disposition_coverage` | 90.9% | claims com disposition definida |
| `provenance_coverage` | 100.0% | claims promovidos com blob_sha + destino |

## Critério de Paridade

- ✅ PASS  `100pct_blobs_contabilizados`: 394/394 blobs contabilizados
- ❌ FAIL  `100pct_processaveis_processados_ou_classificados`: 0/389 processáveis processados (0.0%)
- ✅ PASS  `0_contradicoes_silenciosas`: 0 contradição(ões) silenciosamente validada(s)
- ✅ PASS  `0_secrets_lidos`: safety gate ativo — secrets classificados sem abertura
- ✅ PASS  `claims_promovidos_com_proveniencia`: 10/10 claims promovidos com proveniência completa

> [!warning]
> Paridade incompleta. Critérios não satisfeitos: `100pct_processaveis_processados_ou_classificados`
