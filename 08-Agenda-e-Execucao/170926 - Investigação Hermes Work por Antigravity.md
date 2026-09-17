Viewed contracts.py:1-268
Viewed kanban.py:1-340
Viewed durable_tasks.py:1-800
Viewed task_compiler.py:1-737
Viewed task_compiler.py:690-737
Viewed task_compiler.py:690-737
Viewed runtime.py:1-150
Viewed runtime.py:151-350
Viewed runtime.py:351-550
Viewed runtime.py:551-747
Viewed kanban_db.py:1-200
Searched for "task_acceptance_contracts"
Searched for "task_acceptance_contracts"
Viewed kanban_db.py:1325-1350
Viewed kanban_db.py:5605-5670
Viewed hybrid_kanban.py:1-150
Searched for "def delegate_card"
Searched for "delegat"
Searched for "hybrid_card_delegations"
Viewed hybrid_kanban.py:430-520
Viewed hybrid_kanban.py:400-435
Viewed browser_readiness.py:1-174
Viewed journal.py:1-240
Viewed cockpit.py:1-64
Viewed work100.py:1-92
Viewed evaluation.py:1-180
Viewed tool_guardrails.py:1-160
Searched for "ExperimentKey"
Searched for "ExperimentKey"
Viewed tool_guardrails.py:265-315
Viewed verification_evidence.py:1-800
Viewed jobs.py:150-250
Searched for "NEEDS_MIGRATION"
Viewed jobs.py:2360-2400
Viewed jobs.py:2640-2675
Viewed hermes_state_search.py:1-160
Searched for "compacted"
Ran command: `git diff HEAD -- hermes_state_search.py`
Ran command: `git status -s`
Ran command: `git diff HEAD -- run_agent.py cli.py gateway/run.py agent/conversation_loop.py agent/turn_finalizer.py`
Viewed work_intent.py:1-69
Viewed test_canonical_work_loop.py:1-160
Viewed test_canonical_work_loop.py:161-309
Viewed test_canonical_continuity.py:1-226
Viewed memory.py:1-150
Viewed routines.py:1-160
Viewed HERMES_WORKSTATION_INTELLIGENCE.md:1-150
Viewed HERMES_WORKSTATION_INTELLIGENCE.md:2400-2515
Viewed CURRENT.md:3242-3242
Viewed CURRENT.md:3242-3242
Viewed CURRENT.md:3150-3242
Viewed UPSTREAM_DELTA.md:1-169
Ran command: `pytest workstation/tests/test_canonical_work_loop.py workstation/tests/test_canonical_continuity.py -v`
Ran command: `.venv\Scripts\python.exe -m pytest workstation/tests/test_canonical_work_loop.py workstation/tests/test_canonical_continuity.py`

I have launched the automated test execution of the canonical work loop and continuity test suites using `.venv` Python to inspect current test passes, coverage, and any failures. I will review the results as soon as the run finishes.

Viewed task-140.log:1-9

I am waiting for the pytest execution to finish and notify me.

Viewed task-140.log:1-52
Viewed kanban_db.py:2500-2520
Ran command: `.venv\Scripts\python.exe -m workstation.work100`
Viewed workstation-browser-runtime.ts:1-120
Viewed preview.ts:1-100
Viewed workers.py:1-140
Viewed events.py:1-140
Viewed events.py:135-147
Viewed policy.py:1-140

# Relatório de Investigação Profunda e Rigorosa: Hermes Work

> **Objetivo:** Estabelecer a transformação do Hermes Work em uma camada operacional contínua, confiável e verificável sobre o computador e o trabalho do usuário, orientada pelo fluxo:
> 
> $$\text{Intenção} \longrightarrow \text{Trabalho Canônico} \longrightarrow \text{Execução} \longrightarrow \text{Evidência} \longrightarrow \text{Verificação} \longrightarrow \text{Resultado} \longrightarrow \text{Aprendizado} \longrightarrow \text{Rotina}$$
> 
> e superando definitivamente o paradigma ingênuo $\text{Prompt} \to \text{Ferramentas} \to \text{Resposta}$.

---

## 1. Executive Synthesis

O que realmente limita o Hermes hoje não é inteligência linguística nem falta de ferramentas adicionais. O limite central decorre de uma **fronteira de execução originalmente herdada do paradigma conversacional**:

1. **Equiparação errônea entre Raciocínio e Execução Mecânica:**
   Quando uma tarefa envolve 50 abas, 20 arquivos ou 100 mutações repetitivas em lote, delegar cada passo ao loop conversacional do LLM resulta em consumo descontrolado de tokens de entrada e cache, saturação de contexto, latência multiplicada e alta vulnerabilidade a falhas estocásticas do modelo. O LLM deve ser o **planejador e o árbitro de exceções**, enquanto o runtime deve ser o **motor determinístico de execução com checkpointing atômico**.
2. **Ausência Histórica de Contratos de Aceitação e Falsa Conclusão (*False Completion*):**
   No modelo clássico, a tarefa era considerada concluída quando o modelo emitia um texto afirmando que terminou (`"Tarefa finalizada com sucesso"`). Se ocorresse um timeout ou erro silencioso, a tarefa frequentemente recebia status `done` sem que nenhuma evidência estruturada comprovasse o resultado.
3. **Contaminação de Intenção e Criação de Tarefas Fantasma:**
   Eventos internos do sistema (notificações de término de processo, cron alerts, erros de background) eram injetados no contexto conversacional como mensagens comuns, fazendo com que o agente interpretasse uma notificação do sistema como uma nova ordem de trabalho humana, poluindo o Kanban com tarefas duplicadas ou cíclicas.
4. **Desconexão de Lifecycles e Estado Zumbi:**
   A interrupção de um plano ou cancelamento de uma tarefa pai deixava filhos (`WorkItems`, abas de browser ou subprocessos) rodando em background sem supervisão. Bancos de dados registravam tarefas como `running` simplesmente porque um processo morreu antes de atualizar o registro, sem que houvesse prova de vida (*Live Handle*) ativa.
5. **A Fragilidade da Percepção Web e Drift de DOM:**
   A automação de browser baseada em delays arbitrários (`sleep(5)`) ou seletores CSS voláteis quebra facilmente em Single Page Applications (SPAs) modernas devido a hidratação atrasada, re-renderizações e telas de login/CAPTCHA.

A evolução recente no branch `main` e na árvore de trabalho (especialmente as iniciativas V3 e *Canonical Work Loop* consolidadas em setembro de 2026) já implementou contratos fundamentais para fechar essas brechas. No entanto, o sistema encontra-se exatamente no limiar entre a **existência dos contratos nos módulos de runtime** e a sua **imposição universal e infalível em todos os ingressos, conectores e clientes**.

---

## 2. Current Architecture (Reconstrução a partir do Código Real)

O Hermes Work não possui múltiplos sistemas operacionais paralelos; ele implementa uma hierarquia rigorosa com **uma única autoridade canônica por domínio** (*One Hermes State*):

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                             CLIENT SURFACES                                 │
│      Hermes Desktop (Electron)  │  TUI (Ink/React)  │  CLI / Gateway API    │
└─────────────────────────────────────┬───────────────────────────────────────┘
                                      │ Ingress: MessageEnvelope (Human/Agent/Runtime)
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                            INTENT & ORCHESTRATION                           │
│  workstation.work_intent.prepare_turn_work() ──► IntentAuthority Gate       │
│  AIAgent.run_conversation() (run_agent.py / agent/conversation_loop.py)     │
└──────────┬──────────────────────────────────────────────────────┬───────────┘
           │                                                      │
           ▼                                                      ▼
┌───────────────────────────────┐              ┌───────────────────────────────┐
│     CONVERSATIONAL DOMAIN     │              │    CANONICAL WORK DOMAIN      │
│ SessionDB (~/.hermes/state.db)│              │ KanbanDB (~/.hermes/kanban.db)│
│ - Messages (active/compacted) │              │ - tasks & task_runs           │
│ - FTS5 / Trigram / CJK        │              │ - task_acceptance_contracts   │
│ - Compacted Snapshots Dedup   │              │ - hybrid_boards/cards/activity│
│ - Session Metadata            │              │ - hybrid_card_delegations     │
└───────────────────────────────┘              │ - work_plans & work_items     │
                                               └───────────────┬───────────────┘
                                                               │
                                                               ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                          DURABLE EXECUTION PLANE                            │
│  TaskCompiler (task_compiler.py) ──► DurableBatchRunner (batch_runner.py)   │
│  - DAG Execution: Setup ──► Fan-Out (Canary Gate) ──► Finalize              │
│  - Checkpoints Atômicos: capture ──► persist ──► validate ──► complete       │
│  - Reference-First Data Plane: ArtifactStore (artifact://tasks/...)         │
│  - Systemic Failure Circuit Breaker: ExperimentKey (3 consecutive stops)    │
└──────────┬──────────────────────────────────────────────────────┬───────────┘
           │                                                      │
           ▼                                                      ▼
┌───────────────────────────────┐              ┌───────────────────────────────┐
│        HOST & BROWSER         │              │     EVIDENCE & AUDIT TRAIL    │
│ BrowserRuntime (Electron CDP) │              │ ExecutionJournal (journal.py) │
│ - WebContentsView (1:1 Task)  │              │ - Hash-Chained JSONL v2       │
│ - BrowserReadinessContract    │              │ - Writer Lock & fsync         │
│ - BrowserHumanControlLease    │              │ VerificationEvidenceDB        │
│ - ProceduralMemory (Anchors)  │              │ - outcome_verification_events │
└───────────────────────────────┘              └───────────────────────────────┘
```

### Fontes Canônicas e Stores

1. **KanbanDB (`hermes_cli/kanban_db.py` em `~/.hermes/kanban.db`):**
   - **Autoridade Única sobre Tarefas e Trabalho:** Contém a tabela central [`tasks`](file:///c:/Github/hermes-agent/hermes_cli/kanban_db.py#L1337-L1370) e [`task_runs`](file:///c:/Github/hermes-agent/hermes_cli/kanban_db.py#L1371-L1410).
   - **Contratos de Aceitação:** Tabela [`task_acceptance_contracts`](file:///c:/Github/hermes-agent/hermes_cli/kanban_db.py#L1333-L1336) vinculada por chave estrangeira em cascata.
   - **Workspace Híbrido Humano-Agente:** Tabelas `hybrid_boards`, `hybrid_columns`, `hybrid_cards`, `hybrid_checklists`, `hybrid_checklist_items`, `hybrid_activity` e [`hybrid_card_delegations`](file:///c:/Github/hermes-agent/hermes_cli/kanban_db.py#L1621-L1640).
   - **Execução Durável:** Tabelas [`work_plans`](file:///c:/Github/hermes-agent/workstation/durable_tasks.py#L193-L206) e [`work_items`](file:///c:/Github/hermes-agent/workstation/durable_tasks.py#L208-L228).
2. **SessionDB (`hermes_state.py` / `hermes_state_search.py` em `~/.hermes/state.db`):**
   - Autoridade sobre histórico conversacional, mensagens brutas e ativas, tokens acumulados e busca semântica/FTS5.
3. **ExecutionJournal (`workstation/journal.py` em `~/.hermes/workstation/journals/<task_id>.jsonl`):**
   - Trilha de auditoria append-only à prova de adulteração com encadeamento de hash SHA-256 (`previous_event_hash`, `event_hash`), trava de arquivo entre processos (`_writer_lock` via `msvcrt.locking` no Windows e `fcntl.flock` no POSIX) e `fsync` em marcos críticos.
4. **ArtifactStore (`workstation/artifacts.py` em `~/.hermes/artifacts/`):**
   - Repositório de dados e entregáveis indexados por conteúdo (`artifact://tasks/<id>/<name>`), evitando o trânsito de blobs pesados pelo contexto do modelo.
5. **VerificationEvidenceDB (`agent/verification_evidence.py` em `~/.hermes/verification_evidence.db`):**
   - Ledger passivo de testes de compilação, suites executadas e verificadores estruturados na tabela `outcome_verification_events`.
6. **ProceduralMemory (`workstation/memory.py` em `~/.hermes/workstation/memory/procedures.json`):**
   - Procedimentos web ancorados multi-facetados com ciclo de vida explícito (`discovered` $\to$ `validated` $\to$ `promoted` $\to$ `retired`).
7. **BrowserSessionState (`apps/desktop/electron/workstation-browser-session-state.ts` em `%LOCALAPPDATA%/HermesWorkstation/Runtime/browser-session.json`):**
   - Projeção de abas lógicas, URL restorable segura e snapshots de `BrowserTask` mantidos pelo Electron.

---

## 3. Evidence Map

As conclusões desta investigação estão fundamentadas em verificações diretas no código, testes e execuções:

| Componente Auditado | Arquivo / Linha | Evidência Direta | Status no Código |
| :--- | :--- | :--- | :--- |
| **Acceptance Gate** | [`hermes_cli/kanban_db.py:L5618-5635`](file:///c:/Github/hermes-agent/hermes_cli/kanban_db.py#L5618-L5635) | `complete_task` rejeita status `done` se `AcceptanceEvaluator().evaluate(outcome, contract)` falhar ou verifiers faltarem. | **CONFIRMADO** |
| **Intent Authority** | [`workstation/contracts.py:L38-56`](file:///c:/Github/hermes-agent/workstation/contracts.py#L38-L56) | `MessageEnvelope.can_create_work` exige `HUMAN + CREATE_WORK` ou `AGENT + DELEGATE_WORK + parent_task_id`. | **CONFIRMADO** |
| **Ingress Binding** | [`agent/conversation_loop.py:L1890-1894`](file:///c:/Github/hermes-agent/agent/conversation_loop.py#L1890-L1894) | `prepare_turn_work(agent, user_message, message_envelope)` chamado no prólogo de cada turno. | **CONFIRMADO** |
| **Turn Outcome Finalizer**| [`agent/turn_finalizer.py:L837-845`](file:///c:/Github/hermes-agent/agent/turn_finalizer.py#L837-L845) | `finalize_turn` submete candidato de resultado do turno a `finalize_turn_candidate`. | **CONFIRMADO** |
| **Parent Reconciliation** | [`workstation/durable_tasks.py:L730-735`](file:///c:/Github/hermes-agent/workstation/durable_tasks.py#L730-L735) | `update_plan_state` transiciona atomicamente filhos `running` para `blocked` em caso de parada do pai. | **CONFIRMADO** |
| **Live vs Durable Proof** | [`workstation/runtime.py:L74-80`](file:///c:/Github/hermes-agent/workstation/runtime.py#L74-L80) | `EvidenceClass.LIVE_HANDLE` exige `expires_at > now`; `DURABLE_PROOF` nunca promove estado para `RUNNING`. | **CONFIRMADO** |
| **Canary & Batch Guard** | [`workstation/task_compiler.py:L563-569`](file:///c:/Github/hermes-agent/workstation/task_compiler.py#L563-L569) | Primeiro item mutável exige `canary_verified` com evidência externa antes de liberar fan-out. | **CONFIRMADO** |
| **Circuit Breaker** | [`agent/tool_guardrails.py:L268-292`](file:///c:/Github/hermes-agent/agent/tool_guardrails.py#L268-L292) | `ExperimentKey` agrupa falhas estruturais idênticas independentemente dos valores dos itens. | **CONFIRMADO** |
| **Journal Hash Chain** | [`workstation/journal.py:L103-119`](file:///c:/Github/hermes-agent/workstation/journal.py#L103-L119) | Schema v2, encadeamento de SHA-256 e fsync em marcos de aceitação/recovery. | **CONFIRMADO** |
| **Compacted Search Dedup**| [`hermes_state_search.py:L1378-1382`](file:///c:/Github/hermes-agent/hermes_state_search.py#L1378-L1382) | Subquery `NOT EXISTS` impede que snapshots compactados idênticos enviesem o FTS5. | **CONFIRMADO** |
| **Cron Drift & Migration**| [`cron/jobs.py:L2649-2663`](file:///c:/Github/hermes-agent/cron/jobs.py#L2649-L2663) | Detecção de drift de modelo transiciona job para `NEEDS_MIGRATION` com `enabled = False`. | **CONFIRMADO** |
| **Bug de Caminho Windows**| [`hermes_cli/kanban_db.py:L2510`](file:///c:/Github/hermes-agent/hermes_cli/kanban_db.py#L2510) | Chamada `path.parent.mkdir()` lança `AttributeError` se `db_path` for passado como `str`. | **CONFIRMADO (REPRODUZIDO)** |

---

## 4. Behavioral Evolution

A evolução temporal do Hermes através das etapas do projeto reflete um aprendizado contínuo:

```
[Etapa 1: Conversacional Legado]
   Falha em ferramenta ──► Retry cego no prompt ──► Esgota limite de turnos ──► Emite "Concluído!" falso
   (Não havia Acceptance Gate; o modelo auto-atestava seu sucesso)

[Etapa 2: Workstation V1 & V2]
   Browser isolado + Kanban adicionado ──► Operações repetitivas no loop LLM ──► Inunda contexto com 2.5MB
   (Poluía histórico, re-lia arquivos, colidia com abas, gerava tarefas a partir de system events)

[Etapa 3: TaskCompiler & Durable Tasks (HW-020 a HW-022)]
   Compilação de lote ──► Executa 100 itens via DurableBatchRunner ──► 2 chamadas LLM vs 100
   Mas: se o item 1 falhasse por seletor errado, repetia a falha nos outros 99 (amplificação sistêmica)

[Etapa 4: Canonical Work Loop (Atual - 2026-09-17)]
   Canary obrigatório no item 1 ──► Se falhar, bloqueia fan-out ──► Circuit Breaker abre
   MessageEnvelope filtra notificações ──► Acceptance Gate exige prova gravada ──► Resultado verificado
```

- **O que foi corrigido de verdade:** Falsa conclusão por exaustão de turnos eliminada nos fluxos Workstation; tarefas fantasma criadas por eventos de sistema filtradas por `MessageEnvelope`; explosão de tokens em loops repetitivos controlada pelo `TaskCompiler`.
- **O que mudou de forma:** Em vez de o agente entrar em loop conversacional infinito tentando consertar um erro, o `TaskCompiler` executava o erro em todos os 100 itens. Isso levou à criação do `ExperimentKey` e do `Canary-before-fan-out`.
- **O que ainda persiste como gap:** O bug de inicialização de caminho string no `kanban_db.py` no Windows; e conectores legados de chat (ex.: certas integrações de mensageria direta) que ainda não embrulham a mensagem em `MessageEnvelope(HUMAN, CREATE_WORK)`.

---

## 5. Failure Taxonomy (Famílias de Falhas e Causas-Raiz)

### Família 1: Falsa Conclusão (*False Completion*)
- **Sintoma:** O agente declara que o relatório foi extraído, os dados foram salvos ou o deploy foi feito, mas o arquivo de destino não existe ou o banco está vazio.
- **Causa-Raiz:** Ausência de vínculo obrigatório entre a transição de estado no Kanban e um contrato de aceitação avaliado deterministicamente.
- **Mecanismo de Defesa Atual:** [`AcceptanceEvaluator`](file:///c:/Github/hermes-agent/workstation/contracts.py#L99-L126) + checagem de [`outcome_verifiers_recorded`](file:///c:/Github/hermes-agent/agent/verification_evidence.py#L178-L189).

### Família 2: Estado Fantasma e Contaminação de Intenção (*Phantom Tasks*)
- **Sintoma:** Kanban subitamente preenchido com tarefas como `"Background process completed normally"` ou `"Process exited with code 0"`.
- **Causa-Raiz:** O canal de mensageria tratava qualquer string que entrava na fila do turno como intenção humana de alto nível.
- **Mecanismo de Defesa Atual:** [`MessageEnvelope`](file:///c:/Github/hermes-agent/workstation/contracts.py#L38-L56) classifica a origem como `SYSTEM_EVENT` e autoridade como `OBSERVATION_ONLY`, bloqueando `promote_request_if_multistep`.

### Família 3: Mutação Incerta e Retry Perigoso (*Uncertain Mutation Storm*)
- **Sintoma:** O agente envia uma requisição de pagamento, clique de submissão de formulário ou escrita em banco. Ocorre timeout de rede aos 30 segundos. O agente tenta novamente e processa a transação em duplicidade.
- **Causa-Raiz:** Tratar erro de timeout em mutações com o mesmo protocolo de retry de operações somente-leitura.
- **Mecanismo de Defesa Atual:** [`task_compiler.py:L465-466`](file:///c:/Github/hermes-agent/workstation/task_compiler.py#L465-L466) detecta que o checkpoint de despacho ocorreu e interrompe com `uncertain_mutation_requires_review`.

### Família 4: Filhos Órfãos e Tarefas Zumbis (*Zombie Execution*)
- **Sintoma:** Usuário cancela uma tarefa na interface ou a máquina reinicia; o banco SQLite continua mostrando `running` infinitamente ou um worker delegado continua gastando recursos em background.
- **Causa-Raiz:** Falta de conciliação atômica no encerramento do pai e confiar no status armazenado sem exigir verificação de handle de processo vivo.
- **Mecanismo de Defesa Atual:** [`reconcile_running_items`](file:///c:/Github/hermes-agent/workstation/durable_tasks.py#L737-L753) e [`EvidenceState.reconcile`](file:///c:/Github/hermes-agent/workstation/runtime.py#L168-L184).

### Família 5: Amplificação de Falha Sistêmica em Lote (*Systemic Failure Amplification*)
- **Sintoma:** Em um lote de 50 registros, uma mudança de layout quebra o seletor. O sistema executa todos os 50 registros e gera 50 erros consecutivos idênticos.
- **Causa-Raiz:** Falta de canary e falta de circuit breaker estrutural entre itens de lote.
- **Mecanismo de Defesa Atual:** [`canary_required`](file:///c:/Github/hermes-agent/workstation/task_compiler.py#L563-L569) e `ExperimentKey` abrindo `SYSTEMIC_FAILURE_SUSPECTED`.

### Família 6: Drift de DOM e Ilusão de Prontidão (*Semantic Readiness Failure*)
- **Sintoma:** O navegador carrega a página HTML básica, o agente executa o clique, mas o framework React/Vue ainda não hidratou os listeners. O clique não tem efeito.
- **Causa-Raiz:** Usar apenas `document.readyState === 'complete'` em vez de esperar predicados semânticos do elemento alvo.
- **Mecanismo de Defesa Atual:** [`BrowserReadinessContract`](file:///c:/Github/hermes-agent/workstation/browser_readiness.py#L132-L161).

---

## 6. Invariant Audit

| Invariante Arquitetural | Onde está definido | Como é garantido no código | Risco Residual / Brecha Atual |
| :--- | :--- | :--- | :--- |
| **I-1: Conclusão Exige Verificação** | `contracts.py`, `kanban_db.py` | `complete_task` falha se `workstation` metadata não contiver verifiers válidos registrados no banco. | Tarefas legadas sem tag `workstation` ou `hybrid` ainda podem ser completadas manualmente. |
| **I-2: Stored Running não é Prova de Vida** | `runtime.py`, `durable_tasks.py` | `reconcile_running_items` e `EvidenceState.reconcile` exigem `LIVE_HANDLE` válido com TTL. | Tarefas em `kanban.db` dependem de gatilho de conciliação explícito; não há daemon contínuo em background para todos os boards. |
| **I-3: Notificação não Cria Trabalho** | `contracts.py`, `work_intent.py` | `MessageEnvelope.can_create_work` retorna `False` para origens de sistema/runtime. | Conectores externos de terceiros que não instanciam `MessageEnvelope` podem passar strings sem autoridade. |
| **I-4: Mutação Incerta Não Tem Replay** | `task_compiler.py`, `durable_tasks.py` | Step despachado sem retorno marca `uncertain_mutation_requires_review` e bloqueia retry. | Aplicações fora do `TaskCompiler` (loop de tools direto do LLM) dependem de disciplina do modelo. |
| **I-5: 1 Tarefa = 1 Página de Browser** | `workstation-browser-runtime.ts` | Map de abas indexado por `ownerTaskId`; nova aba substitui ou vincula exclusivamente. | Abas órfãs por crash de processo necessitam de restauração preguiçosa no startup. |
| **I-6: Integridade do Journal** | `journal.py` | Hash encadeado SHA-256 e fsync; `read_events` lança `JournalIntegrityError` em adulteração. | Custo computacional de verificar toda a cadeia em arquivos com milhares de eventos. |
| **I-7: Isolamento de Profiles** | `hermes_constants.py`, `kanban_db.py` | `get_hermes_home()` resolve paths por profile; boards isolam bancos e workspaces. | Subprocessos precisam sempre receber `HERMES_HOME` e `HERMES_KANBAN_DB` via env explícito. |

---

## 7. State & Identity Audit

Mapeamento rigoroso das entidades de estado e suas relações:

```
[Human Board] (hybrid_boards)
     │
     └──► [Human Card] (hybrid_cards: hcard_*)
               │
               ├──► [Delegation Link] (hybrid_card_delegations: attempt 1, 2...)
               │         │
               │         ▼
               │    [Agent Task] (tasks: task_* ou uuid)
               │         │
               │         ├──► [Task Runs] (task_runs: run_id incremental)
               │         │
               │         ├──► [Acceptance Contract] (task_acceptance_contracts)
               │         │
               │         ├──► [WorkPlan] (work_plans: plan_*)
               │         │         │
               │         │         └──► [WorkItems] (work_items: plan_*_0001, 0002...)
               │         │
               │         ├──► [BrowserTask] (BrowserTask: id vinculado a 1 WebContentsView)
               │         │
               │         ├──► [ExecutionJournal] (~/journals/<task_id>.jsonl encadeado)
               │         │
               │         └──► [Artifacts] (~/artifacts/tasks/<task_id>/...)
               │
               └──► [Human Checklists] (hybrid_checklists / items)
```

### Análise de Contradições e Riscos de Identidade:
1. **Divergência entre Plan e Item:**
   Se um `WorkPlan` for cancelado ou interrompido pelo usuário, [`update_plan_state`](file:///c:/Github/hermes-agent/workstation/durable_tasks.py#L726-L735) executa:
   ```sql
   UPDATE work_items SET status='blocked', last_error='parent stopped; reconcile dispatched effects before resume' 
   WHERE plan_id=? AND status='running'
   ```
   Isso elimina o risco de `Plan = interrupted` enquanto `WorkItem = running`.
2. **Duplicação de Delegação:**
   [`delegate_card`](file:///c:/Github/hermes-agent/hermes_cli/hybrid_kanban.py#L413-L463) gera chave de idempotência `hybrid-card:{card_id}:attempt:{attempt}` dentro de uma transação `kanban_db.write_txn`. Clicks múltiplos rápidos no botão "Entregar ao Hermes" retornam o registro existente sem criar tasks zumbis.
3. **Identidade de Ambiente:**
   Telemetria e testes geram eventos com `environment="test"`, os quais são estritamente excluídos do cálculo das métricas de produção pelo [`EvaluationHarness.outcome_metrics`](file:///c:/Github/hermes-agent/workstation/evaluation.py#L55-L58).

---

## 8. Execution Audit (Durable Execution,

Error: The stream was interrupted. Please continue the task you were working on. (Error ID: ba782570-990b-4010-8ba8-4fb22095df94-163)

Continuando a investigação profunda exatamente a partir da **Seção 8 (Execution Audit)**:

---

## 8. Execution Audit (Durable Execution, Retries, Cancellation e Recovery)

A durabilidade no Hermes Work é implementada em duas camadas complementares: o [`DurableTaskStore`](file:///c:/Github/hermes-agent/workstation/durable_tasks.py#L179-L270) (camada transacional SQLite via KanbanDB) e o [`TaskCompiler`](file:///c:/Github/hermes-agent/workstation/task_compiler.py#L195-L235) / [`DurableBatchRunner`](file:///c:/Github/hermes-agent/workstation/batch_runner.py).

### Análise Adversarial de Cenários Críticos

#### 1. A operação mutável termina após o timeout
- **Cenário:** O agente executa uma ferramenta mutável (ex: `browser_click` em botão de pagamento ou submissão de formulário, ou `patch`/`write_file`). A chamada de dispatch leva 35s, mas o timeout da ferramenta é de 30s. A chamada levanta `TimeoutError`.
- **Comportamento no Código:** No [`task_compiler.py:L465-466`](file:///c:/Github/hermes-agent/workstation/task_compiler.py#L465-L466), antes de despachar, o sistema grava o checkpoint `step_{index}_dispatch`. Quando a exceção é capturada, se a ferramenta pertencer a `WRITE_EFFECTS`, o compilador recusa-se a avançar ou tentar de novo cegamente e retorna:
  ```python
  {"valid": False, "code": "uncertain_mutation_requires_review", "results": results}
  ```
  Na retoma subsequente, ao verificar que `step_{index}_dispatch` está presente sem um `result_ref` verificado, o runner bloqueia o item com `uncertain_mutation_requires_review`.
- **Invariante Garantida:** **Zero retries cegos em mutações com estado incerto.**

#### 2. O runtime reinicia entre dispatch e checkpoint de escrita
- **Cenário:** O processo morre (SIGKILL, crash de energia, reinicialização do Windows) exatamente após o envio do comando ao sistema operacional/browser, antes de salvar o commit no SQLite.
- **Comportamento no Código:** O `WorkItem` permanece gravado como `status = 'running'` ou com `step_{index}_dispatch` marcado. Ao reiniciar, o [`reconcile_running_items`](file:///c:/Github/hermes-agent/workstation/durable_tasks.py#L737-L753) inspeciona os itens:
  ```python
  for row in conn.execute("SELECT id FROM work_items WHERE plan_id=? AND status='running'"):
      if row[0] not in live_item_ids:
          conn.execute("UPDATE work_items SET status='blocked', last_error=? WHERE id=?",
                       ("recovery-required: no live handle; reconcile effect", row[0]))
  ```
  O item **não é re-executado automaticamente**. Ele é transicionado para `blocked` com necessidade de verificação por probe de leitura antes de qualquer retry.

#### 3. O site/sistema aplica a mudança, mas o verifier falha
- **Cenário:** O clique de criação de um card/registro ocorreu no backend do serviço, mas o verifier subsequente não encontrou o elemento de confirmação ou ocorreu erro de DOM drift.
- **Comportamento no Código:** O `TaskCompiler` marca o passo como não verificado (`verified = False`). O item transiciona para `failed` ou `blocked`. Caso o procedimento venha de uma receita previamente promovida, o [`TaskCompiler:L541-544`](file:///c:/Github/hermes-agent/workstation/task_compiler.py#L541-L544) imediatamente invalida a receita:
  ```python
  self.recipes.invalidate(recipe_key, "QUARANTINED")
  self.store.update_plan_metadata(item.plan_id, {"recipe": {"status": "QUARANTINED"}})
  ```
  O plano não tenta repetir a mutação, impedindo criações duplicadas no serviço externo.

#### 4. Falhas correlacionadas em lote (Amplificação Sistêmica)
- **Cenário:** Uma lista de 50 itens é enviada para processamento. Uma mudança de seletor quebra o segundo passo em todos os itens.
- **Comportamento no Código:** 
  1. O **Canary Gate** ([`task_compiler.py:L563-568`](file:///c:/Github/hermes-agent/workstation/task_compiler.py#L563-L568)) executa apenas o item 0 com verificação obrigatória. Se o item 0 falhar, nenhum outro item é despachado.
  2. Caso a receita já existisse e o Canary fosse dispensado, o **Circuit Breaker** baseado em [`ExperimentKey`](file:///c:/Github/hermes-agent/agent/tool_guardrails.py#L268-L292) detecta 3 falhas consecutivas com a mesma assinatura estrutural (mesma ferramenta + mesmo formato de argumento + mesmo erro/seletor) e ativa `SYSTEMIC_FAILURE_SUSPECTED`. Os 47 itens restantes permanecem intocados em `pending`.

---

## 9. Context Efficiency Audit (Tokens, Compressão, Duplicação e Sobrecarga de Reconstrução)

### 1. Mensagens Ativas vs. Compactadas no SessionDB
- **Mecanismo:** A tabela `messages` possui as colunas `active` (0 ou 1) e `compacted` (0 ou 1).
- **Problema Histórico Identificado:** Quando uma sessão longa sofria múltiplas compressões de contexto sucessivas, cada snapshot compactado gerava mensagens de resumo e histórico arquivado que continuavam indexadas pelo motor FTS5 (`messages_fts`). Ao rodar `session_search`, a busca retornava múltiplos trechos idênticos de resumos antigos, distorcendo o ranking do BM25 e inflando o contexto com ruído repetitivo.
- **Correção Confirmada no Código Atual:** Em [`hermes_state_search.py:L1378-1382`](file:///c:/Github/hermes-agent/hermes_state_search.py#L1378-L1382), a query de busca nos índices FTS, Trigram, CJK e LIKE agora usa uma projeção de leitura dedupada:
  ```sql
  (m.active = 1 OR (m.compacted = 1 AND NOT EXISTS (
      SELECT 1 FROM messages d WHERE d.session_id=m.session_id 
      AND d.role=m.role AND d.content=m.content 
      AND (d.active=1 OR (d.compacted=1 AND d.id<m.id)))))
  ```
  O histórico de auditoria no SQLite permanece 100% intacto, mas a projeção de leitura suprime duplicatas idênticas.

### 2. Reference-First Architecture vs. Injeção de Blobs no Contexto
- **O desperdício anterior:** O modelo executava um comando terminal ou extração web que retornava 500 KB de JSON. Esse JSON era colocado inteiro no histórico da conversa como mensagem de resposta da ferramenta (`tool`). No turno seguinte, o modelo pagava 125.000 tokens de entrada apenas para reler aquele output.
- **A solução atual:**
  - O [`ArtifactStore`](file:///c:/Github/hermes-agent/workstation/artifacts.py#L15-L60) armazena o output bruto em `artifact://tasks/<task_id>/<file>`.
  - O [`task_compiler.py`](file:///c:/Github/hermes-agent/workstation/task_compiler.py#L672-L674) substitui os dados brutos por um envelope compacto (`operational_references`), informando apenas o ponteiro do artefato e seu resumo/schema.
  - A ferramenta [`read_file`](file:///c:/Github/hermes-agent/tools/file_tools.py) resolve `artifact://` de forma nativa e estruturada, retornando apenas metadados e fatias solicitadas.
  - **Economia comprovada no benchmark:** Redução de **2,56 MB** de tráfego inline no contexto para **2,7 KB** em execuções de lote de 12 itens (uma redução de 99,89% de bytes no transcript).

### 3. Reconstrução de Estado via DB vs. Transcript
- Em vez de o LLM reler toda a conversa para deduzir em qual item do lote parou, a função [`DurableTaskStore.operational_ledger`](file:///c:/Github/hermes-agent/workstation/durable_tasks.py#L768-L800) consulta o banco SQLite diretamente e entrega um resumo compacto de uma linha (`task://<id> [37/100 completed, 1 waiting for human]`). O modelo nunca é chamado para fazer contabilidade de estado.

---

## 10. Browser Reliability Audit (BrowserTask, Prontidão, Isolamento e Handoff Humano)

### 1. Invariante de Exclusividade (1 Tarefa = 1 Página)
- No [`workstation-browser-runtime.ts:L97-107`](file:///c:/Github/hermes-agent/apps/desktop/electron/workstation-browser-runtime.ts#L97-L107), cada aba de navegação possui um atributo `ownerTaskId`.
- Se uma sessão ou worker tentar navegar numa aba vinculada a outra tarefa, o controlador rejeita a operação com erro de concorrência ou aloca uma nova aba isolada. Duas sessões concorrentes **nunca compartilham a mesma instância de página Chromium**.

### 2. Prontidão Semântica vs. `document.readyState`
- Em SPAs modernas, `document.readyState === 'complete'` é atingido quando o bundle JavaScript é baixado, muito antes de o React/Vue/Angular renderizar os componentes na tela ou vincular os listeners de evento.
- O [`BrowserReadinessContract`](file:///c:/Github/hermes-agent/workstation/browser_readiness.py#L132-L161) substitui loops de `sleep(5)` por avaliação semântica direta:
  - Presença de seletores mandatórios (`required_semantic_targets`).
  - Verificação de hidratação (`require_hydration`).
  - Detecção imediata de barreira de login (`auth_required`) e CAPTCHA (`captcha_required`).
  - Detecção de superfícies não-DOM (`unsupported_surface`, como Canvas/WebGL).

### 3. Handoff Humano Seguro e Bounded Leases
- Quando um CAPTCHA ou login 2FA aparece, o agente **não deve** tentar forçar cliques aleatórios.
- O [`HumanHandoffManager`](file:///c:/Github/hermes-agent/workstation/runtime.py#L599-L668) pausa a tarefa, emite um evento no [`RuntimeEventBus`](file:///c:/Github/hermes-agent/workstation/runtime.py#L337-L383), marca o `WorkItem` como `waiting_for_user` e abre a aba para intervenção direta do usuário no Desktop Electron.
- O controle humano é governado por um lease com escopo estrito (`BrowserHumanControlLease` com TTL de 5 minutos). Quando o usuário conclui o login e clica em "Devolver ao Hermes" (`resume`), o lease é liberado, o item retorna para `pending` e a execução automatizada continua sem reiniciar a sessão ou perder os cookies recém-adquiridos.

---

## 11. Learning Audit (Skills, Rotinas, Memória e Aprendizado Procedural)

O sistema atual possui um mecanismo de aprendizado em três estágios para evitar a perda contínua de conhecimento operacional:

$$\text{Experiência Bem-Sucedida} \xrightarrow[\text{experience\_candidate}]{\text{Evidência}} \text{Candidato} \xrightarrow[\text{validate}]{\text{Replay}} \text{Validado} \xrightarrow[\text{promote}]{\text{Aprovação}} \text{Rotina Determinística}$$

1. **Geração de Candidatos (`RoutinePromotionService.experience_candidate`):**
   - No [`workstation/routines.py:L70-82`](file:///c:/Github/hermes-agent/workstation/routines.py#L70-L82), quando uma tarefa é concluída com evidência verificada pelo `AcceptanceEvaluator`, se possuir a flag `repeatability_hint`, os passos executados são sanitizados (removendo credenciais e dados privados) e salvos na [`ProceduralMemory`](file:///c:/Github/hermes-agent/workstation/memory.py) no estado `ProcedureLifecycle.DISCOVERED`.
2. **Resiliência contra Mudança de DOM (Multi-Facet Fallback Anchoring):**
   - O maior motivo pelo qual automações web quebram após dias ou semanas é a mudança de classes CSS e IDs dinâmicos gerados por frameworks frontend.
   - O [`ProcedureStep.resolve_anchor`](file:///c:/Github/hermes-agent/workstation/memory.py#L126-L150) implementa ancoragem em múltiplos níveis de prioridade semântica:
     1. `data-testid` / `data-test` (estável para testes).
     2. `role` e acessibilidade (`role:button`, nome acessível).
     3. Conteúdo textual visível.
     4. Seletor CSS estrutural (último recurso).
3. **Execução Determinística Sem LLM (`DeterministicRoutineRunner`):**
   - Uma vez promovido (`ProcedureLifecycle.PROMOTED`), o procedimento pode ser executado pelo [`DeterministicRoutineRunner`](file:///c:/Github/hermes-agent/workstation/routines.py#L84-L155) **sem nenhuma chamada a LLM**. O runner valida pré-condições, resolve as âncoras no DOM vivo, executa cada passo e verifica pós-condições.
   - Se ocorrer drift (elemento não encontrado ou pós-condição falhou), o runner **falha fechado imediatamente** (`_drift`), grava a falha na memória e sinaliza que intervenção ou re-planejamento cognitivo é necessário.

---

## 12. Continuous Autonomy Audit (Cron, Automação em Background e Resiliência)

A autonomia contínua sem supervisão depende fundamentalmente do subsistema de tarefas agendadas (`cron/`).

### Vulnerabilidade Histórica: A Falha Silenciosa de Drift
- Um usuário agenda um job diário: *"Todo dia às 08h, abra o CRM e baixe o relatório de vendas"*.
- Duas semanas depois, o usuário troca o provedor global do Hermes (ex: de `openrouter/anthropic/claude-3.5-sonnet` para `openai/gpt-4o-mini`, ou a API key expira, ou um modelo é depreciado).
- **O que acontecia antes:** O scheduler continuava disparando o job a cada hora. O job falhava com erro de inferência/provider. O contador de falhas crescia infinitamente ou o job ficava mudo. O usuário não era avisado e a automação morria silenciosamente.

### Mecanismo de Defesa: `NEEDS_MIGRATION`
- No [`cron/jobs.py:L2649-2663`](file:///c:/Github/hermes-agent/cron/jobs.py#L2649-L2663), o sistema agora detecta o descolamento entre os snapshots de modelo salvos no job (`provider_snapshot`, `model_snapshot`) e a configuração ativa:
  ```python
  job["migration_state"] = "NEEDS_MIGRATION"
  job["migration"] = {
      "previous_provider": job.get("provider_snapshot"),
      "previous_model": job.get("model_snapshot"),
      "current_provider": current_provider,
      "current_model": current_model,
      "reason": reason,
      "detected_at": datetime.now().astimezone().isoformat()
  }
  job["enabled"] = False
  ```
- O job é **pausado de forma segura**, evitando desperdício de tentativas e spam de erros.
- A resolução (`resolve_model_migration`) oferece três escolhas explícitas ao usuário:
  1. `adopt_global`: Adota o novo modelo global configurado.
  2. `pin_previous`: Fixa explicitamente o modelo anterior que comprovadamente funcionava.
  3. `pause`: Mantém pausado até revisão manual.

---

## 13. Test & Evaluation Audit (Gap Teste vs. Realidade e Bugs Encontrados)

Ao executar a suíte de testes de loop canônico e continuidade com o ambiente Python oficial (`.venv\Scripts\python.exe -m pytest workstation/tests/test_canonical_work_loop.py workstation/tests/test_canonical_continuity.py`), observamos:
- **41 testes passaram** cobrindo integridade de journal, encadeamento de hash, canary, mutações incertas, exclusão de telemetria de teste, concorrência multi-processo de journal e isolamento de workspace.
- **1 falha concreta reproduzida:**
  `test_two_processes_migrate_same_trello_manifest_once` falhou com:
  ```
  AttributeError: 'str' object has no attribute 'parent' em hermes_cli/kanban_db.py:2510
  ```

### Análise da Causa-Raiz do Bug Reproduzido
No arquivo [`hermes_cli/kanban_db.py:L2506-2510`](file:///c:/Github/hermes-agent/hermes_cli/kanban_db.py#L2506-L2510):
```python
if db_path is not None:
    path = db_path
else:
    path = kanban_db_path(board=board)
path.parent.mkdir(parents=True, exist_ok=True)
```
Quando um processo externo, script CLI ou subprocesso passa `db_path` como `str` (por exemplo, via linha de comando `sys.argv[1]`), a variável `path` permanece como `str`, e a chamada `.parent` quebra imediatamente.
**Correção Necessária:** `path = Path(db_path)` para garantir coerência de tipo antes de invocar métodos de filesystem.

---

## 14. Root Cause Graph (Grafo de Causas-Raiz)

```
[Paradigma Conversacional Puro]
   │
   ├─► Falta de autoridade de intenção no canal de entrada
   │      └──► Mensagens de sistema/cron tratadas como ordens humanas
   │              └──► Tarefas fantasmas criadas no Kanban
   │                      └──► Poluição de estado e loops de execução
   │
   ├─► Conclusão avaliada pelo LLM (emissão de texto no transcript)
   │      └──► Ausência de Acceptance Gate determinístico
   │              └──► Falsa Conclusão (tarefa 'done' sem evidência no disco)
   │                      └──► Frustração do usuário e dados ausentes
   │
   ├─► Execução repetitiva no loop conversacional
   │      └──► Injeção contínua de grandes payloads brutos no contexto
   │              └──► Saturação de tokens e invalidação de prompt caching
   │                      └──► Custo exorbitante e latência extrema
   │
   ├─► Tratamento uniforme de erros de ferramentas
   │      └──► Retry cego de timeouts em operações mutáveis
   │              └──► Mutações incertas repetidas (duplicação de efeitos externos)
   │
   └─► Confiança no estado persistido em disco sem checagem de liveness
          └──► Processos mortos permanecem como 'running' no DB
                  └──► Tarefas zumbis bloqueando boards e recursos
```

---

## 15. Hypothesis Backlog (Ordenado por Impacto e Evidência)

| ID | Hipótese | Impacto | Classificação | Evidência / Como Provar ou Refutar |
| :--- | :--- | :--- | :--- | :--- |
| **H-01** | `kanban_db.connect(db_path=...)` quebra quando recebe `str` em vez de `Path`. | **P0** (Crash imediato em subprocessos) | **CONFIRMADO** | Reproduzido no teste `test_two_processes_migrate_same_trello_manifest_once`. Corrigir com `Path(db_path)`. |
| **H-02** | Conectores de gateway de terceiros podem criar tarefas sem `MessageEnvelope`. | **P1** (Tarefas fantasmas via canais externos) | **FORTEMENTE INDICADO** | Ingressos em `gateway/run.py` foram protegidos para eventos internos, mas adapters individuais ainda precisam de auditoria de envelope. |
| **H-03** | Verificação de toda a cadeia de hash no append de journal causa degradação em logs gigantes. | **P2** (Latência progressiva de I/O) | **CONFIRMADO** | [`ExecutionJournal._read_records`](file:///c:/Github/hermes-agent/workstation/journal.py#L120-L146) relê todo o arquivo a cada append. Otimizar para verificação incremental mantendo o último hash em cache. |
| **H-04** | A auto-reparação de rotinas pode recuperar seletores de DOM via semântica sem custo de LLM. | **P2** (Redução drástica de falhas de automação) | **VALIDADO EM CONTRATO** | Coberto pelos testes de multi-facet anchoring em `test_routines.py`. Falta telemetria em produção de longa duração. |
| **H-05** | Compacting de histórico de conversa com referências estruturadas elimina 80%+ do crescimento do DB. | **P3** (Desempenho de storage e busca) | **FORTEMENTE INDICADO** | Medido localmente no `hermes_state_search.py` via `compacted_duplicate_metrics`. |

---

## 16. Architecture Changes (Mudanças Arquiteturais Recomendadas)

Para garantir que o usuário possa entregar uma tarefa, fechar o computador, voltar horas depois e confiar 100% no resultado, a arquitetura deve consolidar as seguintes regras fundamentais:

```
                  ┌──────────────────────────────────────────────┐
                  │                 USER INTENT                  │
                  └──────────────────────┬───────────────────────┘
                                         │
                                         ▼
                  ┌──────────────────────────────────────────────┐
                  │           CANONICAL TASK (KanbanDB)          │
                  │   - Immutable Acceptance Contract            │
                  │   - Verified State (Not Reasoning-Derived)   │
                  └──────────────┬───────────────────────────────┘
                                 │
                 ┌───────────────┴───────────────┐
                 │                               │
                 ▼                               ▼
  ┌──────────────────────────────┐ ┌──────────────────────────────┐
  │      COGNITIVE PHASE         │ │      DURABLE EXECUTION       │
  │     (AIAgent / Planner)      │ │   (TaskCompiler / Runner)    │
  │ - Decide estratégia          │ │ - Executa DAG determinístico │
  │ - Compila WorkPlan e passos  │ │ - Canary-before-fan-out      │
  │ - Trata exceções reais       │ │ - Checkpoints atômicos       │
  │ - Não executa loops em lote  │ │ - Sem LLM entre passos       │
  └──────────────┬───────────────┘ └──────────────┬───────────────┘
                 │                                │
                 └───────────────┬────────────────┘
                                 │
                                 ▼
                  ┌──────────────────────────────────────────────┐
                  │           EVIDENCE & ACCEPTANCE              │
                  │   - ArtifactStore (Content-Addressed)        │
                  │   - Outcome Verifiers gravados no SQLite     │
                  │   - Journal Hash-Chained auditável           │
                  └──────────────────────┬───────────────────────┘
                                         │
                                         ▼
                  ┌──────────────────────────────────────────────┐
                  │      VERIFIED RESULT OR HUMAN HANDOFF        │
                  └──────────────────────────────────────────────┘
```

1. **A Cintura Estreita da Execução:** Mutações repetitivas ou quantificadas são proibidas de rodar diretamente no loop de prompt conversacional. Elas devem passar obrigatoriamente pelo `TaskCompiler` e `DurableBatchRunner`.
2. **Acceptance Gate Inflexível:** Nenhuma tarefa no Kanban transiciona para `done` a não ser que uma evidência comprovada exista e passe pelo `AcceptanceEvaluator`.
3. **Isolamento Total de Falhas:** O Canary Gate protege o mundo externo de erros em massa, e mutações incertas são congeladas para revisão em vez de sofrerem retries catastróficos.

---

## 17. Implementation Plan

O roadmap técnico estruturado por ordem de dependência rigorosa:

### Fase P0: Invariantes Básicas e Correções de Integridade
1. **Fix do Caminho `db_path` no `kanban_db.py`:**
   - **Arquivo:** [`hermes_cli/kanban_db.py:L2506-2510`](file:///c:/Github/hermes-agent/hermes_cli/kanban_db.py#L2506-L2510)
   - **Ação:** Converter explicitamente `path = Path(db_path)` se `db_path` for fornecido como string.
   - **DoD:** `pytest workstation/tests/test_canonical_continuity.py -k test_two_processes_migrate_same_trello_manifest_once` passando 100% verde.
2. **Otimização de Verificação Incremental de Journal:**
   - **Arquivo:** [`workstation/journal.py`](file:///c:/Github/hermes-agent/workstation/journal.py)
   - **Ação:** Evitar releitura completa do arquivo a cada append através de cache em memória do último hash verificado, validando apenas a cauda.
   - **DoD:** Appends em journals com mais de 5.000 eventos executando em $< 2\text{ms}$.

### Fase P1: Confiabilidade de Autonomia e Browser
1. **Auditoria Universal de Ingressos do Gateway:**
   - **Arquivos:** `gateway/run.py`, `gateway/platforms/*.py`
   - **Ação:** Garantir que 100% dos adapters de mensageria (Telegram, Discord, Slack, WhatsApp, Webhook) criem `MessageEnvelope` com `MessageOrigin` e `IntentAuthority` estritos.
   - **DoD:** Nenhuma notificação de background capaz de acionar `promote_request_if_multistep`.
2. **Daemon Periódico de Conciliação de Tarefas Zumbis:**
   - **Arquivos:** `hermes_cli/kanban_db.py`, `cron/scheduler.py`
   - **Ação:** Criar ticker que varre tarefas com status `running` sem `LIVE_HANDLE` válido há mais de 10 minutos e as marca como `stalled`/`blocked`.
   - **DoD:** Zero tarefas em `running` após restart não-recuperado de processo.

### Fase P2: Eficiência e Reference-First Expansion
1. **Adoção Sistemática de `artifact://` em Ferramentas Nativas:**
   - **Arquivos:** `tools/terminal_tool.py`, `tools/browser_workstation.py`
   - **Ação:** Saídas maiores que 4 KB geram artefato automaticamente e retornam ao modelo apenas o resumo e o handle `artifact://`.
   - **DoD:** Redução média de 70% nos tokens de entrada de ferramentas em sessões longas.

### Fase P3: UX de Acompanhamento e Aprendizado Procedural
1. **Cockpit UI Integration no Desktop Electron:**
   - **Arquivos:** `apps/desktop/src/app/`, `workstation/cockpit.py`
   - **Ação:** Conectar a rota `/api/workstation/tasks/{task_id}/cockpit` ao painel de detalhes do card no Kanban Desktop, exibindo progresso de WorkItems, consumo acumulado e botão de handoff direto.
   - **DoD:** O usuário visualiza o status real do motor durável sem abrir logs de terminal.

---

## 18. What NOT to Build (O que NÃO Devemos Construir)

Ideias que parecem atraentes superficialmente, mas que aumentariam a entropia e violariam o princípio *One Hermes State*:

- ❌ **NÃO criar um segundo banco de tarefas ou scheduler alternativo:** O KanbanDB (`kanban.db`) é e deve continuar sendo a única autoridade sobre tasks, runs e planos.
- ❌ **NÃO criar um banco separado para histórico conversacional:** O `SessionDB` (`state.db`) já possui SQLite WAL, FTS5 e trigram. Ele deve ser otimizado por projeção, nunca substituído.
- ❌ **NÃO usar LLM para contabilidade de progresso ou contagem de itens em lote:** Contabilidade de estado é responsabilidade do código procedural em Python (`DurableTaskStore.operational_ledger`).
- ❌ **NÃO reescrever o motor do browser:** O Electron com `WebContentsView` e CDP direto já é a melhor solução local para controle de abas e compartilhamento de sessão com o usuário.
- ❌ **NÃO permitir que ferramentas mutáveis tentem adivinhar se um timeout deu certo:** A incerteza em mutações deve falhar fechado e exigir probe de leitura.

---

## 19. Hermes Work 100 (Seed Suite Derivada das Evidências)

O benchmark rigoroso deve avaliar o comportamento do agente sob estresse real. Apresentamos os 10 casos fundamentais da semente do **Hermes Work 100**:

1. **HW100-01: Timeout Nunca Vira Concluído**
   - *Origem:* Bug clássico onde exaustão de turnos gerava `done`.
   - *Comportamento Esperado:* Task transiciona para `blocked` com motivo claro.
   - *Comportamento Proibido:* Task com status `done` ou emissão de evento `TASK_COMPLETED`.
2. **HW100-02: Notificação do Sistema Não Cria Intenção**
   - *Origem:* Poluição de Kanban por mensagens de término de background process.
   - *Comportamento Esperado:* Mensagem classificada como `OBSERVATION_ONLY`, sem criação de task.
   - *Comportamento Proibido:* Criação de nova linha na tabela `tasks`.
3. **HW100-03: Pai Interrompido Reconcilia Filhos Atomicamente**
   - *Origem:* Filhos órfãos continuavam executando após cancelamento do pai.
   - *Comportamento Esperado:* Todos os `work_items` com status `running` viram `blocked`.
   - *Comportamento Proibido:* Existência de `work_item` em `running` com pai `interrupted`.
4. **HW100-04: Duas Sessões Web Não Competem pela Mesma Página**
   - *Origem:* Sessões paralelas sobrescreviam o DOM uma da outra no browser.
   - *Comportamento Esperado:* Alocação de abas distintas com `ownerTaskId` exclusivo.
   - *Comportamento Proibido:* Modificação de URL de uma aba pertencente a outra sessão.
5. **HW100-05: Mutação Incerta Não Sofre Retry Cego**
   - *Origem:* Timeout em submissão de formulário levando a cadastros duplicados.
   - *Comportamento Esperado:* Parada imediata com `uncertain_mutation_requires_review`.
   - *Comportamento Proibido:* Re-execução da ferramenta mutável sem probe prévio.
6. **HW100-06: Falha no Canary Bloqueia o Fan-Out**
   - *Origem:* Erro de seletor quebrando 100 itens em lote.
   - *Comportamento Esperado:* Apenas o item 0 executa; itens 1–99 permanecem em `pending`.
   - *Comportamento Proibido:* Execução de todos os itens gerando falhas repetidas.
7. **HW100-07: Adulteração de Journal é Detectada no Fechamento**
   - *Origem:* Auditoria de integridade de logs de execução.
   - *Comportamento Esperado:* Falha fechada com `JournalIntegrityError` e recusa de `done`.
   - *Comportamento Proibido:* Fechamento com sucesso de task com journal adulterado.
8. **HW100-08: Detecção de CAPTCHA Realiza Handoff Bounded**
   - *Origem:* Automação bloqueada por desafio anti-bot.
   - *Comportamento Esperado:* Criação de `HumanHandoff` com status `waiting-for-human`.
   - *Comportamento Proibido:* Agente tentando quebrar o CAPTCHA com cliques cegos.
9. **HW100-09: Mudança de Provedor Global Pausa Cron com `NEEDS_MIGRATION`**
   - *Origem:* Agendamentos falhando silenciosamente após troca de modelo.
   - *Comportamento Esperado:* Transição de job para `NEEDS_MIGRATION` com `enabled = False`.
   - *Comportamento Proibido:* Tentativas contínuas e acúmulo de falhas no escuro.
10. **HW100-10: Restauração Pós-Crash Mantém Identidade Operacional**
    - *Origem:* Queda de energia durante execução de lote no passo 37 de 100.
    - *Comportamento Esperado:* Retoma no passo 37 sem re-executar passos 1 a 36.
    - *Comportamento Proibido:* Reinício do zero ou perda do histórico já concluído.

---

## 20. North Star Metrics

A métrica definitiva para avaliar se o Hermes Work é uma camada operacional confiável é:

$$\mathbf{AVCR} = \frac{\text{Tarefas Delegadas Concluídas com Verificação Autônoma}}{\text{Total de Tarefas Elegíveis Delegadas}}$$

$$\text{onde } \text{Verificação Autônoma} = (\text{Status} == \text{verified\_completed}) \land (\text{Aceitação Aprovada}) \land (\text{Zero Resgates Humanos Não Planejados})$$

### Métricas Operacionais de Suporte
1. **Taxa de Falsa Conclusão (*False Completion Rate*):**
   $$\frac{\text{Tarefas marcadas 'done' sem prova verificada}}{\text{Total de Tarefas}}$$
   *(Meta: 0.0%)*
2. **Taxa de Tarefas Zumbis (*Zombie Running Rate*):**
   $$\frac{\text{Tarefas 'running' no banco sem Live Handle ativo}}{\text{Total de Tarefas em Aberto}}$$
   *(Meta: < 0.1%)*
3. **Taxa de Amplificação de Falha Sistêmica:**
   $$\text{Média de itens executados após quebra de invariante estrutural}$$
   *(Meta: $\le 1$ item, graças ao Canary)*
4. **Eficiência de Tokens por Resultado Verificado:**
   $$\frac{\text{Tokens de Entrada Não-Cacheados}}{\text{Transições de Estado Verificadas}}$$
5. **Taxa de Reuso de Rotinas (*Routine Savings*):**
   $$\text{Média de chamadas LLM e tokens economizados por procedimentos re-executados determinísticamente}$$

---

## 21. Final Architecture (Arquitetura-Alvo Consolidada)

A arquitetura consolidada opera como um verdadeiro **Sistema Operacional para o Trabalho**, mantendo os componentes existentes, eliminando redundâncias e formalizando as fronteiras de autoridade:

```
[HUMAN INTERFACE] (Desktop / TUI / CLI)
       │
       ▼
[MESSAGE ENVELOPE GATE] ──► (Filtra origens e bloqueia criação espúria de trabalho)
       │
       ▼
[KANBAN CORE AUTHORITY] ──► (Única autoridade de tarefas, cartões híbridos e contratos)
       │
       ├──► Se conversacional / cognitivo:
       │       └──► AIAgent Loop (Raciocínio, ferramentas pontuais, síntese)
       │
       └──► Se repetitivo / lote / durável:
               └──► TaskCompiler ──► DurableBatchRunner
                       ├──► Canary Item 0 (Prova de conceito inicial)
                       ├──► Fan-Out Atômico (Multi-item com checkpoints)
                       ├──► BrowserRuntime (CDP nativo, 1:1, leases humanos)
                       └──► ArtifactStore (Armazenamento referencial de blobs)
                                │
                                ▼
                       [ACCEPTANCE EVALUATOR]
                                │
             ┌──────────────────┴──────────────────┐
             │ Passou                              │ Falhou ou Incerteza
             ▼                                     ▼
      [TASK COMPLETED]                     [NEEDS INPUT / BLOCKED]
   - Evento auditado no Journal         - Notificação estruturada
   - Prova gravada no SQLite            - Espera ação ou re-planejamento
   - Candidato enviado a Rotinas
```

---

## 22. Final Recommendation

Respondendo diretamente à pergunta central:

> **“O que precisa mudar para que eu possa confiar em entregar trabalho real ao Hermes, sair de perto, voltar horas depois e acreditar no estado e no resultado que ele me mostrar?”**

O caminho técnico mais seguro e elegante **não é adicionar mais recursos nem criar novas ferramentas**; é transformar os **contratos de confiabilidade já existentes no repositório em invariantes absolutas e universais**:

1. **Aplicar imediatamente a correção de tipo em [`kanban_db.py:2510`](file:///c:/Github/hermes-agent/hermes_cli/kanban_db.py#L2510)** (`path = Path(db_path)`), garantindo que subprocessos e migrações multi-processo não sofram crashes por passagem de string.
2. **Impedir terminantemente o fechamento de tarefas sem evidência:** O `complete_task` do `kanban_db.py` deve aplicar a avaliação do [`AcceptanceEvaluator`](file:///c:/Github/hermes-agent/workstation/contracts.py#L99-L126) como regra geral inviolável em todo o sistema.
3. **Blindar todos os conectores de entrada com o [`MessageEnvelope`](file:///c:/Github/hermes-agent/workstation/contracts.py#L38-L56):** Somente mensagens com autoridade explícita podem iniciar trabalho ou criar cards. Notificações internas do sistema e eventos de telemetria devem ser tratados estritamente como observações.
4. **Isolar mutações incertas:** Manter a política estrita de nunca tentar novamente uma mutação cujo retorno sofreu timeout sem antes rodar um probe de leitura para confirmar se o efeito já havia sido aplicado.
5. **Acelerar a promoção de candidatos a Rotinas Determinísticas:** Permitir que tarefas recorrentes (como raspagens periódicas, downloads de planilhas e checagens de status) migrem do loop custoso de LLM para o [`DeterministicRoutineRunner`](file:///c:/Github/hermes-agent/workstation/routines.py#L84-L155), garantindo execução determinística, instantânea, econômica e 100% verificável.

---

Esse `.db` contém praticamente **a sessão inteira do Antigravity investigando o Hermes Work**, não apenas a resposta final.

O banco tem cerca de **2,8 MB**, 7 tabelas e **165 passos de trajetória**. Ele registra o trabalho feito sobre o repositório local `C:\Github\hermes-agent`, associado a `kevynlucasprofissional-stack/hermes-agent` e com referência também ao upstream `NousResearch/hermes-agent`.

O conteúdo principal é:

- **Seu prompt original completo**, com cerca de 21 mil caracteres, pedindo a investigação profunda sobre transformar o Hermes em uma camada operacional confiável.
    
- **81 blocos de metadados de geração** e toda a trajetória do agente.
    
- **Chamadas de ferramentas e comandos executados**, incluindo buscas de arquivos, leitura do código, PowerShell, Git, testes, leitura de documentos de contexto etc.
    
- Trechos substanciais de arquivos reais do Hermes, incluindo `workstation-browser-runtime.ts`, `preview.ts`, `workers.py`, `events.py`, `policy.py`, `task_compiler.py`, `kanban_db.py`, journals, context docs e outros.
    
- Metadados do ambiente Antigravity, inclusive configuração de ferramentas e identificação do modelo usado na sessão como `gemini-3.8-flash-high`.
    
- Alguns erros de ferramenta registrados, como leituras com `ContentOffset` fora do tamanho do arquivo.
    
- Uma interrupção explícita da geração: **“The stream was interrupted. Please continue the task you were working on.”**
    
- E, principalmente, **um relatório técnico muito grande dividido em duas respostas**.
    

### O relatório

A primeira parte tem cerca de **22,5 mil caracteres** e vai das seções 1 a 8:

1. Executive Synthesis
    
2. Current Architecture
    
3. Evidence Map
    
4. Behavioral Evolution
    
5. Failure Taxonomy
    
6. Invariant Audit
    
7. State & Identity Audit
    
8. Execution Audit — começou aqui e foi interrompida.
    

A segunda parte tem cerca de **32,9 mil caracteres** e continua da seção 8 até a 22:

8. Execution Audit
    
9. Context Efficiency Audit
    
10. Browser Reliability Audit
    
11. Learning Audit
    
12. Continuous Autonomy Audit
    
13. Test & Evaluation Audit
    
14. Root Cause Graph
    
15. Hypothesis Backlog
    
16. Architecture Changes
    
17. Implementation Plan
    
18. What NOT to Build
    
19. Hermes Work 100
    
20. North Star Metrics
    
21. Final Architecture
    
22. Final Recommendation
    

Portanto, são aproximadamente **55 mil caracteres só de relatório final**, além de toda a evidência que levou a ele.

### O que o Antigravity concluiu

A tese central encontrada no arquivo é interessante: **o principal problema do Hermes não seria falta de inteligência ou ferramentas, mas a fronteira entre raciocínio e execução**.

O relatório identifica seis grandes famílias de falhas:

1. **False Completion** — o agente afirmar que terminou sem prova de que terminou.
    
2. **Phantom Tasks** — eventos internos serem confundidos com novas intenções humanas.
    
3. **Uncertain Mutation Storm** — retries perigosos depois de uma mutação cujo resultado ficou incerto.
    
4. **Zombie Execution** — filhos/processos continuarem rodando depois que a tarefa pai foi interrompida.
    
5. **Systemic Failure Amplification** — um erro estrutural ser repetido dezenas de vezes num batch.
    
6. **Semantic Readiness Failure** — browser considerar uma página “pronta” quando semanticamente ela ainda não está utilizável.
    

Ele também conclui que **boa parte dos mecanismos necessários já existe no código**, mas não está universalmente imposta em todos os caminhos.

Por exemplo, ele encontrou mecanismos como `AcceptanceEvaluator`, `MessageEnvelope`, `DurableTaskStore`, `TaskCompiler`, `BrowserReadinessContract`, reconciliação de tarefas, journal com hash encadeado, canary antes de fan-out e tratamento de mutações incertas.

### Há inclusive bugs e gaps específicos

O relatório classifica algumas hipóteses. A mais concreta é **H-01, marcada como CONFIRMADA/P0**:

> `kanban_db.connect(db_path=...)` quebra quando recebe `str` em vez de `Path`.

Segundo a investigação, isso foi reproduzido no teste:

`test_two_processes_migrate_same_trello_manifest_once`

e a correção proposta é normalizar com `Path(db_path)`.

Também aparecem como gaps:

- conectores do Gateway que potencialmente ainda escapam do `MessageEnvelope`;
    
- custo crescente do `ExecutionJournal`, porque a cadeia inteira de hashes seria relida a cada append;
    
- ausência de reconciliação contínua universal para tarefas `running` sem um `LIVE_HANDLE`;
    
- necessidade de expandir arquitetura **reference-first**, evitando jogar outputs gigantes novamente no contexto do LLM;
    
- necessidade de ligar o Cockpit real ao Desktop/Kanban;
    
- transformar procedimentos recorrentes em **rotinas determinísticas**.
    

### A arquitetura que ele propõe

A conclusão converge bastante com a visão que você estava formulando:

**Intenção → tarefa canônica → planejamento → execução durável → evidência → acceptance/verificação → resultado verificado ou handoff humano.**

E ele faz uma separação explícita:

**LLM:** decide estratégia, planeja, trata exceções e situações realmente cognitivas.

**Runtime determinístico:** executa batches, checkpoints, retries seguros, canaries, contabilização de progresso e recuperação após falhas.

Uma recomendação forte é: **não colocar o LLM entre todos os passos repetitivos**.

### Tem um “Hermes Work 100” dentro

Um dos trechos mais valiosos é a proposta de benchmark **Hermes Work 100**. O arquivo já define os primeiros dez casos de teste, como:

- timeout nunca pode virar `done`;
    
- system notification não pode criar tarefa;
    
- cancelar pai deve reconciliar filhos;
    
- duas tarefas web não podem competir pela mesma página;
    
- mutação incerta não pode sofrer retry cego;
    
- falha no canary deve bloquear o fan-out;
    
- adulteração do journal precisa ser detectada;
    
- CAPTCHA deve gerar handoff humano;
    
- mudança de provider deve pausar cron incompatível;
    
- recuperação pós-crash deve continuar do checkpoint correto.
    

Ele também propõe uma métrica principal chamada **AVCR — Autonomous Verified Completion Rate**:

> proporção das tarefas delegadas elegíveis que chegam a uma conclusão autonomamente verificada, com acceptance aprovado e sem resgate humano não planejado.

### O ponto mais importante

Esse banco é **bem mais valioso do que apenas a resposta que o Antigravity te mostrou na tela**.

Ele contém simultaneamente:

**seu pedido → investigação executada → arquivos consultados → comandos/testes → erros encontrados → raciocínio operacional resumido → relatório → continuação pós-interrupção.**

Ou seja, dá para usar esse `.db` como **corpo de evidências da investigação**, cruzá-lo com o estado atual do GitHub e verificar, ponto a ponto, **o que o Antigravity acertou, o que inferiu sem evidência suficiente, o que já foi corrigido e quais gaps continuam reais hoje**.

Esse seria, inclusive, o próximo passo mais útil com esse arquivo.