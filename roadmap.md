# Roadmap de Endurecimento da Ingestão e Paridade — ACIRV Notebook

Este documento é o backlog canônico da frente de hardening da infraestrutura de ingestão, proveniência e paridade.

---

## Fases de Endurecimento

### Fase 1: Correção do Core e Idempotência Real
- [ ] **1.1** Corrigir idempotência de `inventariar_fontes.py` (blob conhecido não altera `inventoried_at`, não contabiliza `new_entries`, não gera diff no JSONL; diferenciar "já inventariado" de "já processado").
- [ ] **1.2** Adicionar suporte ao estado `existing_unprocessed` na contagem de inventário.
- [ ] **1.3** Garantir que a segunda execução sem alterações no repositório produza 0 novos blobs, 0 edições no ledger e 0 diffs.
- [ ] **1.4** Criar suíte de testes de integração com repositório Git temporário real.

### Fase 2: Fechamento do Ciclo Fonte → Claims → Ledger
- [ ] **2.1** Expandir schema do `Ledger-de-Ingestao.jsonl` com `processing_status` (`unprocessed`, `in_progress`, `partially_processed`, `processed`, `error`), `last_processed`, `processor_version`, `claims_detected` e `claims_by_disposition`.
- [ ] **2.2** Exigir que uma fonte só fique `processed` quando todos os seus claims materiais tiverem disposition explícita.
- [ ] **2.3** Implementar validação cruzada: erro se existir claim promovido para fonte `unprocessed` ou se fonte estiver `processed` sem evidência.
- [ ] **2.4** Atualizar o estado no ledger das fontes utilizadas pelo Golden Set de claims.

### Fase 3: Parsing Estrito, Schemas e Integridade Referencial
- [ ] **3.1** Substituir captura silenciosa de erros de JSON por exceção/falha explícita com indicação de arquivo e número de linha.
- [ ] **3.2** Validar enums, formato de SHA (40 hex chars), prefixos de caminho e tipos em `claims.py` e `inventariar_fontes.py`.
- [ ] **3.3** Normalizar todos os `claim_id` para ASCII puro (ex.: `orcamento` em vez de `orçamento`).
- [ ] **3.4** Implementar checagem de integridade referencial em `claims.py`: unicidade de `claim_id`, existência de `source_path + blob_sha` no ledger, existência de `canonical_destination` no disk, e existência de alvos de `supersedes`, `contradicts` e `duplicates`.
- [ ] **3.5** Implementar verificação determinística de anchors (headings ou block IDs) nos arquivos canônicos.

### Fase 4: Desacoplamento Fonte vs. Validação Humana & Semântica de Estados
- [ ] **4.1** Reformular a estrutura de proveniência de claims para separar `supporting_sources` (documentos primários) de `validation_source` / `validation_record` (validação humana).
- [ ] **4.2** Definir a semântica de `validation_status`: `validated`, `not_required`, `pending_validation`.
- [ ] **4.3** Adicionar invariante: se um claim for `pending_validation`, a nota canônica de destino deve contê-lo marcado como provisório.

### Fase 5: Refatoração do Golden Set de 12 Claims
- [ ] **5.1** Refatorar os 12 claims atuais em unidades atômicas com IDs ASCII, anchors verificáveis e metadados de proveniência atualizados.
- [ ] **5.2** Ajustar inconsistências canônicas conhecidas (`SudoExpo-2026.md`, `Validacoes-Humanas-Necessarias.md`, `Lacunas-de-Cobertura.md`).

### Fase 6: Relatório de Cobertura e Imutabilidade Runtime
- [ ] **6.1** Substituir métrica tautológica por `git_tracked_source_accounting_coverage`, `processable_source_coverage`, `material_claim_disposition_coverage`, `provenance_coverage` e `validation_coverage`.
- [ ] **6.2** Substituir a afirmação genérica `0_secrets_lidos` por `known_sensitive_paths_blocked` com prova observável.
- [ ] **6.3** Implementar snapshot pré e pós-execução no `validar_invariantes.py` para detectar se os scripts modificaram `000-Arquivos-originais/`.

### Fase 7: CI e Piloto Controlado (10–20 fontes)
- [ ] **7.1** Criar `.github/workflows/ci.yml` estritamente seguro (`permissions: contents: read`, sem escrita, sem secrets).
- [ ] **7.2** Executar piloto de ingestão com 10–20 fontes representativas de diferentes domínios.
- [ ] **7.3** Executar re-inventariação pós-piloto e comprovar 100% de idempotência (zero diffs no ledger).
- [ ] **7.4** Executar suíte completa de testes e validadores.
