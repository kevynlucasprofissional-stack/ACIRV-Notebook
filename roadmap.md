# Roadmap de Ingestão Semântica Narrativa — ACIRV Notebook

Este documento é o backlog canônico da frente de ingestão, paridade e governança epistemológica do ACIRV Notebook.

---

## Fases do Roadmap

### Fase A — Preservação e Transição Arquitetural
- [x] **A.1** Backup remoto do `main` publicado e verificado no GitHub (`backup/main-pre-chatgpt-semantic-ingestion-2026-09-17` e tag correspondente, ambos no SHA `c485e72d7243b07ccc2f9f5751dabbdca6724fee`).
- [x] **A.2** Preservação da branch histórica `fix/ingestion-pipeline-hardening` no `origin`.
- [x] **A.3** Transição arquitetural documentada: *claim-centric / script-centric* → **AI-semantic / narrative-centric com verificação determinística** (`Decisao-Arquitetural-Ingestao-Narrativa.md`).
- [x] **A.4** Matriz de auditoria de componentes concluída (manter, adaptar, remover, arquivar).

### Fase B — Fundação Determinística Mínima
- [x] **B.1** Inventário SHA idempotente (`inventariar_fontes.py`) separando *já inventariado* de *já revisado semântica/editorialmente* (`review_status`).
- [x] **B.2** Safety gate pré-leitura (`safety_gate.py`) bloqueando credenciais confirmadas/suspeitas por metadados sem abrir conteúdo.
- [x] **B.3** Schema expandido no ledger (`Ledger-de-Ingestao.jsonl`) com `review_status`, `last_reviewed_at`, `reviewed_by`.
- [x] **B.4** Parsing estrito de JSONL e schema com exceção/erro explícito contendo arquivo e número de linha.
- [x] **B.5** CI estritamente seguro (`.github/workflows/ci.yml`) com `permissions: contents: read` e dupla verificação de imutabilidade (PR diff vs Base SHA e Runtime status).

### Fase C — Contrato de Nota Canônica Narrativa
- [x] **C.1** Formalização do [[Contrato-de-Nota-Canonica-Narrativa]] definindo o padrão de memória institucional.
- [x] **C.2** Diretrizes de storytelling orientado a dados (números integrados na prosa explicativa).
- [x] **C.3** Separação transparente de fatos documentados, interpretações operacionais e incertezas/pendências.
- [x] **C.4** Regra de distinção temporal (`planejado` → `aprovado` → `agendado` → `executado` → `observado`).

### Fase D — Protocolo do ChatGPT Agendado (GitHub-First)
- [x] **D.1** Protocolo detalhado em [[ChatGPT-Protocolo-de-Ingestao-Agendada]] (18 passos operacionais no paradigma **GitHub-First**).
- [x] **D.2** Definição estrita do papel do ChatGPT como interpretador editorial (sem depender de shell/Python local) e do Python como validador determinístico.
- [x] **D.3** Definição do fluxo de silêncio sem novidade material (sem PRs ruidosos).

### Fase E — Refatoração dos Claims de Evidência
- [x] **E.1** Claims redefinidos como âncoras de evidência atômicas (KPIs, datas, decisões, valores), não como representação integral do conhecimento.
- [x] **E.2** Normalização de todos os IDs de máquina para ASCII puro (`^[a-z0-9_.-]+$`).
- [x] **E.3** Desacoplamento entre fontes primárias (`supporting_sources`) e validação humana (`validation_source` / `validation_record`).
- [x] **E.4** Verificação determinística opcional de anchors (headings e block IDs).

### Fase F — Golden Set Piloto (10–20 fontes)
- [ ] **F.1** Seleção e ingestão do piloto de 10–20 fontes representativas de diferentes domínios.
- [ ] **F.2** Validação da narrativa canônica e dos claims do piloto.
- [ ] **F.3** Verificação de re-inventariação pós-piloto com 100% de idempotência (zero diffs no ledger).

### Fase G — Execução Agendada em Modo Diagnóstico
- [ ] **G.1** Validação da primeira execução periódica do ChatGPT Agendado via GitHub.
- [ ] **G.2** Ajuste fino de prompts e formatos de PR.

### Fase H — Processamento do Corpus em Ondas
- [ ] **H.1** Ingestão incremental das ~389 fontes restantes organizadas por domínio.
- [ ] **H.2** Auditorias periódicas de paridade e integridade.

### Fase I — Manutenção Incremental Contínua
- [ ] **I.1** Monitoramento diário de novas fontes em `000-Arquivos-originais/`.
- [ ] **I.2** Preservação contínua da imutabilidade da camada original.