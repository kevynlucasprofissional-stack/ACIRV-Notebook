---
id: base-relatorio-de-cobertura
titulo: Relatorio-de-Cobertura
tipo: auditoria
subtipo: cobertura
ultima_revisao: '2026-09-17'
confidencialidade: interno
---

# Relatório de Cobertura e Paridade — ACIRV Notebook

> Gerado em: `2026-09-17T18:44:30.060993+00:00`

## 1. Cobertura de Fontes (000-Arquivos-originais/)

| Métrica | Valor |
|---|---:|
| Total de blobs no repositório Git | 394 |
| Blobs indexados no Ledger | 394 |
| **Accounting Coverage (Git → Ledger)** | **100.0%** |
| Fontes Ativas | 394 |
| Fontes Deletadas por Humano | 0 |
| Fontes Sensíveis (Safety Gate Bloqueado) | 3 |
| Formato Não Suportado | 2 |
| Com Erro | 0 |
| Total de Fontes Processáveis | 389 |
| Fontes Semanticamente Revisadas | 0 |
| **Processable Source Coverage** | **0.0%** |

### Cobertura por Domínio Temático

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

## 2. Paridade e Cobertura de Evidências (Claims)

| Métrica de Claims | Valor |
|---|---:|
| Total de Claims Registrados | 14 |
| Disposition Coverage | 100.0% |
| Claims Promovidos com Proveniência Completa | 14 / 14 |
| **Provenance Coverage** | **100.0%** |
| Claims Validados | 3 / 14 |
| **Validation Coverage** | **21.43%** |

### Claims por Disposition

| Disposition | Quantidade |
|---|---:|
| promoted | 14 |

## 3. Isolamento Observável de Segurança

- **Caminhos Sensíveis Confirmados Bloqueados Pré-Leitura:** `SIM`

| Caminho Sensível | Bloqueado Pré-Leitura | Motivo do Safety Gate |
|---|:---:|---|
| `000-Arquivos-originais/Minha Chave API Antropic.md` | SIM | caminho confirmado sensível na auditoria de segurança: 000-Arquivos-originais/Minha Chave API Antropic.md |
| `000-Arquivos-originais/Contas e Senhas.md` | SIM | caminho confirmado sensível na auditoria de segurança: 000-Arquivos-originais/Contas e Senhas.md |
