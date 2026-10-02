Consegui avançar a investigação de forma material, mas não vou fingir que concluí a auditoria exaustiva inteira: o corpus é grande — especialmente o `conversations.zip` descompactado, com mais de 300 MB — e nesta execução consegui fechar a parte mais importante de **estado persistido + invariantes centrais**, além de confrontá-la com a arquitetura que já vínhamos construindo. O resultado já muda significativamente a prioridade técnica do Hermes Work.

## 1. Executive synthesis

O principal limitador do Hermes hoje **não parece ser falta de capacidade agêntica, browser tooling ou features**. O problema fundamental é que ainda não existe uma garantia suficientemente forte de que:

> **o estado que Hermes apresenta ao usuário corresponde causalmente ao que realmente aconteceu no mundo externo.**

O sistema já possui grande parte das peças necessárias: Task/Run, WorkPlan/WorkItem, Kanban, browser runtime, evidence store, journal, workers, artifacts, cron, Skills e mecanismos de recuperação. O gargalo está nas **relações e invariantes entre essas peças**.

A evidência mais importante que encontrei é concreta:

> **existem WorkPlans em estado terminal enquanto ainda possuem WorkItems vivos.**

No snapshot analisado, encontrei, entre outros casos:

- um WorkPlan `interrupted` de 12 itens com:
    - 2 `completed`;
    - 2 `blocked`;
    - **1 `running`**;
    - **7 `pending`;
- outro WorkPlan `interrupted` de 100 itens com:
    - 1 `completed`;
    - **99 `pending`**.

Isso é exatamente a classe:

```
parent = interrupted
child = running/pending
```

que você pediu que procurássemos.

Portanto, a menor mudança que elimina uma enorme família de bugs é esta:

> **Estados terminais precisam ser invariantes de árvore, não atributos locais.**

Um WorkPlan não pode simplesmente escrever `interrupted`. A transição precisa iniciar ou concluir uma reconciliação causal dos descendentes.

Esse ponto é mais importante que adicionar novas features.

---

# 2. Current Architecture

A evidência também obriga a corrigir uma interpretação anterior de **One Hermes State**.

O snapshot possui, pelo menos:

```
state.db
profiles/eco-v3/state.db

kanban.db

verification_evidence.db

projects.db

cron/
  executions.db
  jobs.json
  usage_audit.jsonl
  Windows Task Scheduler XMLs

boards/
  múltiplos bancos Kanban
```

O `state.db` global e o `profiles/eco-v3/state.db` possuem aproximadamente o mesmo tamanho, mas são arquivos diferentes.

O `state.db` observado contém principalmente:

```
key_value
session_messages
session_tool_events
messages_fts
processed_files
schema_version
```

Enquanto o Kanban mantém separadamente:

```
tasks
task_runs
task_events
work_plans
work_items

hybrid_boards
hybrid_cards
hybrid_card_delegations

hybrid_trello_links
hybrid_trello_sync_state
hybrid_trello_sync_ledger
hybrid_trello_webhook_events
hybrid_trello_webhook_state
hybrid_trello_badges
```

Isso significa que **One Hermes State não deve significar “um SQLite”**.

A formulação correta é:

> **One Hermes State = uma autoridade canônica por domínio + identidade compartilhada + lineage explícito + projeções reconciliáveis.**

Uma tentativa de fundir tudo em um banco provavelmente pioraria o sistema.

A arquitetura conceitual correta já está muito próxima do que existe:

```
                    WORK IDENTITY
                         │
           ┌─────────────┼──────────────┐
           │             │              │
         Intent      Execution       Evidence
           │             │              │
        Task/         WorkPlan       Verification
      AgentTask       WorkItem        Artifacts
           │             │              │
           └─────────────┼──────────────┘
                         │
                     Outcome
                         │
                   Acceptance
                         │
                Verified Completion
```

E stores especializados podem continuar existindo.

---

# 3. Evidence Map

As conclusões mais fortes vieram do cruzamento dos três pacotes fornecidos com o estado atual do repositório `kevynlucasprofissional-stack/hermes-agent`.

No `kanban.db` principal observado:

- **67 tasks**;
- **358 task runs**;
- **2.360 task events**;
- **6 WorkPlans**;
- aproximadamente **162 WorkItems** no conjunto principal analisado.

Além disso, os dumps Kanban contêm bancos de boards como:

```
default
hermes-tests-...
secondstore-...
test1
```

Somando apenas os bancos únicos do conjunto — sem contar as cópias duplicadas existentes nos dois pacotes — encontramos aproximadamente:

- **139 WorkPlans**;
- **8.124 WorkItems**.

Isso oferece um corpus interessante de comportamento real, mas também revela uma provável deficiência de isolamento entre ambientes de teste e estado utilizável pelo produto.

---

# 4. Behavioral Evolution

A trajetória do Hermes parece ser aproximadamente:

### Fase histórica

```
execution falha
      ↓
LLM interpreta superficialmente
      ↓
task pode terminar como done
```

Os corpus anteriores continham indícios de:

- reconstrução repetitiva de estado;
- browser refs expiradas;
- competição por página;
- polling;
- tentativas repetidas;
- provider failures;
- conclusão narrativa não necessariamente equivalente a conclusão operacional.

### Hardening intermediário

Foram introduzidos mecanismos como:

- TaskCompiler;
- WorkPlans;
- WorkItems;
- validation;
- bindings;
- evidence;
- BrowserTask;
- runtime estruturado;
- journals;
- recovery.

A classe de falha mudou.

Um padrão observado agora é:

```
antes
falha → interpretação incorreta → done

agora
falha → detectada corretamente
      ↓
mesma falha é executada por vários irmãos
      ↓
falha sistêmica × N
```

Nos WorkItems bloqueados observados, a grande maioria das razões de bloqueio examinadas estava concentrada em **`unexpected_state`**.

Portanto uma hipótese anterior foi fortalecida:

> **o Hermes está ficando melhor em reconhecer falhas individuais, mas ainda não está suficientemente bom em reconhecer que várias falhas individuais representam uma única falha sistêmica.**

É uma evolução positiva, mas cria a necessidade de um circuit breaker semântico.

---

# 5. Failure Taxonomy

As falhas observadas se agrupam melhor em famílias causais do que em bugs isolados.

### Família A — incoerência hierárquica

```
transição local de parent
        ↓
ausência de cascade/reconciliation forte
        ↓
parent terminal
        ↓
children permanecem pending/running
        ↓
estado apresentado deixa de representar execução
        ↓
restart/recovery encontram estado ambíguo
```

**CONFIRMADO.**

---

### Família B — terminalidade temporal fraca

Foi identificado um caso concreto:

```
task:
Upgrade cloudflared e validar página da promoção
```

com evento:

```
{
  "source": "runtime",
  "timeout_seconds": 2,
  "title": "Upgrade cloudflared e validar página da promoção"
}
```

e posteriormente estado `done`.

Isso não prova que houve false completion.

Pode ter ocorrido:

```
dispatch
↓
deadline local expira
↓
operação continua
↓
resultado verdadeiro chega
↓
runtime reconcilia
```

Mas prova uma coisa importante:

> **timeout não é atualmente equivalente, por si só, a um estado físico irreversivelmente terminal.**

Portanto, para operações mutáveis, o modelo:

```
SUCCESS
FAILED
TIMEOUT
```

é insuficiente.

É necessário algo conceitualmente equivalente a:

```
UNCERTAIN
```

---

### Família C — amplificação de falha

```
shared capability/problem
        ↓
item 1 falha
        ↓
failure class não é elevada ao batch
        ↓
item 2 executa
        ↓
...
        ↓
item N executa
```

Resultado:

```
1 causa
→ N tool calls
→ N failures
→ N journal entries
→ N tokens
→ potencialmente N side-effects
```

**FORTEMENTE INDICADO / parcialmente confirmado pelos estados observados.**

---

### Família D — evidência não equivale a audit trail

O banco `verification_evidence.db` analisado apresenta:

```
verification_state = 9 rows
verification_events = 0 rows
```

Portanto:

```
verification state exists
```

não implica:

```
audit trail of verification exists
```

Não afirmaria ainda que a verificação está quebrada. Pode haver migrations, projeções ou caminhos legítimos que escrevem somente state.

Mas é suficiente para rejeitar:

> “há registro em verification state, logo a execução foi verificavelmente concluída”.

**CONFIRMADO como gap de auditabilidade no snapshot.**

---

# 6. Invariant Audit

O Hermes precisa tornar explícitas algumas propriedades que hoje parecem estar distribuídas implicitamente pelo código.

A mais importante:

```
INV-01

parent.status ∈ TERMINAL
⇒
∀ descendant:
    descendant.status ∉ LIVE
```

onde:

```
LIVE = pending | ready | claimed | running | retrying
```

Hoje há violação observada.

Outra:

```
INV-02

task.status = verified_completed
⇒
AcceptanceContract satisfied
AND
required Evidence exists
AND
Evidence is attributable to same execution lineage
```

Ainda não há evidência suficiente para afirmar que esse gate é universal.

Outra:

```
INV-03

a mutable operation that may have crossed
the external side-effect boundary
cannot automatically be retried after loss of acknowledgement.
```

Ela deve entrar em:

```
UNCERTAIN
```

até reconciliação.

Outra:

```
INV-04

one live browser page
has at most one mutating execution lease.
```

Handles podem ser compartilhados para leitura; autoridade de mutação não.

Outra:

```
INV-05

one external effect
has one idempotency identity.
```

Não:

```
retry 1 = nova operação
retry 2 = nova operação
```

Outro:

```
INV-06

projection state cannot become authoritative
merely because the canonical source is unavailable.
```

---

# 7. State & Identity Audit

A questão mais profunda continua sendo identidade.

Hoje existem conceitos como:

```
Conversation
Session
Task
TaskRun
Agent Task
Human Card
Delegation
WorkPlan
WorkItem
BrowserTask
Worker
Process
Artifact
Evidence
```

Eles não devem virar uma mega-entidade.

Isso destruiria a separação de lifecycle que já é uma das boas decisões do Hermes Work.

O que falta é **lineage obrigatório**.

Algo equivalente a:

```
WorkIntent ID
   │
   ├─ HumanCard ID
   │     └─ Delegation ID
   │
   └─ AgentTask ID
          │
          ├─ Run ID
          │
          └─ WorkPlan ID
                 └─ WorkItem ID
                        ├─ WorkerExecution ID
                        ├─ BrowserTask ID
                        ├─ Artifact ID
                        └─ Evidence ID
```

A vantagem é enorme: em vez de tentar perguntar:

> “Qual desses bancos diz a verdade?”

perguntamos:

> “Qual entidade é autoridade para este estado e qual é a cadeia causal que produziu essa projeção?”

---

# 8. Execution Audit

A mudança mais importante para Durable Execution seria formalizar uma **state machine de efeitos**, não somente de tasks.

Para operação sem side effect:

```
PENDING
→ DISPATCHED
→ RUNNING
→ SUCCEEDED / FAILED
```

Para operações mutáveis:

```
PREPARED
→ DISPATCHED
→ ACKNOWLEDGED
→ VERIFIED
```

e:

```
DISPATCHED
→ timeout/network loss
→ UNCERTAIN
→ RECONCILING
→ VERIFIED_APPLIED
   | VERIFIED_NOT_APPLIED
   | NEEDS_HUMAN
```

Esse estado intermediário elimina uma classe inteira de erros.

Exemplo:

```
Hermes clica "Enviar"
↓
site envia
↓
resposta HTTP/browser event se perde
↓
tool timeout
```

Retry ingênuo:

```
Enviar novamente
```

pode duplicar o efeito.

Runtime correto:

```
UNCERTAIN
↓
consultar sent state / DOM / API / durable evidence
↓
só então decidir retry
```

---

# 9. Context Efficiency Audit

A direção arquitetural anterior continua válida: uma parcela excessiva da “inteligência” do agente está sendo usada para **reconstruir estado que poderia ser estruturado**.

A divisão desejada é:

```
LLM:
semantic ambiguity
planning under uncertainty
interpretation
decision
exception handling

Runtime:
IDs
polling
deadlines
leases
retry bookkeeping
state transitions
artifact lookup
dependency resolution
idempotency
reconciliation
progress accounting
```

Uma regra de projeto útil:

> Se a mesma pergunta objetiva precisa ser respondida pelo modelo duas vezes, provavelmente falta estado estruturado ou uma operação determinística.

Exemplos:

```
"esse comando já terminou?"
"qual era o ID?"
"qual aba eu estava usando?"
"esse arquivo existe?"
"essa task já foi executada?"
"qual item falhou?"
"eu já rodei git status?"
```

não deveriam consumir raciocínio reiteradamente.

---

# 10. Browser Reliability Audit

A ideia anterior de **Live Handle × Durable Proof** continua forte, mas merece uma formulação melhor.

Uma página ou elemento é:

```
capability lease
```

e não identidade durável.

Portanto:

```
tab_id / ref / DOM node
```

não deve sobreviver semanticamente a:

```
navigation
SPA hydration
reload
takeover
browser restart
profile recreation
DOM replacement
```

A verdade durável deve se parecer com:

```
BrowserTask:
  intent
  session identity
  profile identity
  expected origin
  expected semantic state
  mutation history
  verification recipe
  evidence
```

Ao recomeçar:

```
resolve state
→ reacquire page
→ semantic readiness
→ reacquire selectors/ref
→ reconcile previous effect
→ continue
```

e não:

```
reuse stale ref
```

---

# 11. Learning Audit

O pipeline correto não é simplesmente:

```
conversation
→ Markdown Skill
```

É:

```
Experience
   ↓
Candidate Procedure
   ↓
Replay/Validation
   ↓
measured benefit
   ↓
Promoted Skill
   ↓
repeated success
   ↓
Routine
   ↓
drift detection
```

E a distinção importante é:

```
Skill
= conhecimento/procedimento ainda adaptativo

Routine
= caminho suficientemente estável para execução determinística
```

Quando uma rotina pode virar:

```
def execute(...):
    ...
```

ela não deveria continuar custando dezenas de milhares de tokens só porque originalmente foi descoberta por um LLM.

---

# 12. Continuous Autonomy Audit

O estado do cron merece atenção especial porque encontrei uma arquitetura aparentemente dividida.

Existem:

```
cron/executions.db
cron/notepad.db
cron/jobs.json
usage_audit.jsonl
Windows Task Scheduler XMLs
```

No SQLite examinado:

```
executions = 0
job_failure_state = 0
schedule_events = 0
```

ao mesmo tempo em que existem definições de jobs e bastante material do Task Scheduler.

Isso é um excelente candidato à investigação:

```
job definition authority?
execution authority?
Windows scheduler projection?
migration legacy?
```

A solução que você propôs anteriormente, `NEEDS_MIGRATION`, continua conceitualmente superior a transformar incompatibilidade permanente em:

```
FAILED
FAILED
FAILED
FAILED
...
```

Estados de automação deveriam distinguir:

```
HEALTHY
DEGRADED
FAILED
NEEDS_MIGRATION
PAUSED_BY_POLICY
BLOCKED_AUTH
BLOCKED_PROVIDER
```

---

# 13. Test & Evaluation Audit

O snapshot oferece um sinal preocupante.

Há boards chamados:

```
hermes-tests-...
secondstore-...
test1
```

persistindo junto ao universo de boards analisado.

Ainda não há evidência suficiente para afirmar que eles aparecem para o usuário ou interferem no board produtivo.

Então classifico:

**FORTEMENTE INDICADO — isolamento incompleto do estado de testes.**

O teste decisivo deve ser:

```
fresh real user profile
→ run E2E suite
→ restart Hermes
→ enumerate user-visible boards/tasks/runs
→ assert zero test entities
```

Outro erro metodológico a evitar:

```
unit test:
interrupt_plan() sets status='interrupted'
```

pode passar perfeitamente enquanto o produto permanece:

```
plan = interrupted
work_item = running
```

Portanto o teste correto é de **invariante transversal**, não de função.

---

# 14. Root Cause Graph

A árvore causal mais importante que emerge é:

```
                     ┌─────────────────────────┐
                     │ Weak cross-domain       │
                     │ execution invariants    │
                     └────────────┬────────────┘
                                  │
          ┌───────────────────────┼──────────────────────┐
          ↓                       ↓                      ↓
 weak terminality          weak effect identity   weak lineage
          │                       │                      │
          ↓                       ↓                      ↓
parent terminal            timeout ambiguity       state lookup
child alive                retry uncertainty        reconstruction
          │                       │                      │
          ↓                       ↓                      ↓
zombies                    duplicate effects        LLM bookkeeping
restart ambiguity           unsafe recovery          context cost
wrong progress              human rescue            audit gaps


             shared failures not promoted
                        │
                        ↓
                  N child retries
                        │
                        ↓
           systemic failure amplification


            completion ≠ acceptance
                        │
                        ↓
            result exists / run ended
                        │
                        ↓
               possible false done
                        │
                        ↓
                 low user trust
```

Isso sugere algo importante:

> **“Intent Authority”, “Verified Completion”, “One Hermes State”, “Systemic Failure Circuit Breaker” e “Live Handle × Durable Proof” não são cinco iniciativas independentes.**

Todas atacam o mesmo problema mais profundo:

### **autoridade causal insuficientemente formalizada.**

---

# 15. Hypothesis Backlog

As hipóteses que mais valem testes agora são:

|Hipótese|Evidência|Impacto|Testabilidade|
|---|---|---|---|
|parent terminal não reconcilia descendants atomicamente|Muito alta|Crítico|Muito fácil|
|falha sistêmica é amplificada por fan-out|Alta|Crítico|Fácil|
|completion ainda possui caminhos sem acceptance gate|Média/alta|Crítico|Fácil|
|timeout mutável pode produzir side-effect desconhecido|Alta conceitual|Crítico|Fácil|
|test stores podem contaminar descoberta de boards|Média|Alta|Fácil|
|verification state não possui provenance suficiente|Alta|Alta|Fácil|
|cron possui autoridades paralelas/legacy|Média|Alta|Média|
|context usa texto para reconstruir estado disponível estruturalmente|histórica forte|Alta|Média|
|browser leases não são completamente isolados por execução|histórica|Crítico|Média|
|Skill promotion não mede benefício/regressão|forte|Média|Fácil|

---

# 16. Architecture Changes

Eu reduziria as mudanças fundamentais a **sete**, reaproveitando os subsistemas atuais.

### A. Canonical Work Lineage

Não criar outro store.

Adicionar/normalizar IDs e relações entre o que já existe.

---

### B. Lifecycle Invariant Engine

Não deixar cada componente decidir isoladamente se uma transição é válida.

Algo equivalente a:

```
transition(parent, INTERRUPTED)
→ calculate reconciliation set
→ cancel/interrupt descendants
→ persist causal events
→ assert invariant
→ expose terminal parent
```

Dependendo do custo transacional, a exposição pública do parent terminal pode esperar o reconciliation barrier.

---

### C. Acceptance Gate

Separar definitivamente:

```
execution finished
```

de:

```
accepted outcome
```

e:

```
verified outcome
```

---

### D. Mutation Uncertainty Protocol

Introduzir semântica `UNCERTAIN` para side effects.

---

### E. Failure Cohort / Circuit Breaker

Falhas precisam ganhar fingerprint.

Exemplo:

```
provider=browser
operation=selector
origin=example.com
error_class=auth_wall
capability=authenticated_navigation
```

Se irmãos acumulam o mesmo fingerprint:

```
STOP FANOUT
```

---

### F. Reconciliation Plane

No startup e periodicamente:

```
parent/child
run/task
worker/run
browser/session
artifact/evidence
cron/job
```

devem ser reconciliados.

Importante: reconciliation **não significa “consertar silenciosamente”**.

Ela pode produzir:

```
INCONSISTENT
NEEDS_RECONCILIATION
UNCERTAIN
```

---

### G. Evidence Provenance

Evidence deve responder:

```
what claim?
from what execution?
using what verifier?
against what acceptance criterion?
when?
with what environment?
```

---

# 17. Implementation Plan

## P0 — Invariants

### P0.1 — Terminal-tree reconciliation

Componentes:

```
WorkPlan
WorkItem
task runtime
cancellation/recovery
journal
```

Migration, caso necessária:

```
terminal_reason
terminal_requested_at
reconciled_at
reconciliation_state
```

Não é obrigatório colocar todos os campos se os eventos existentes permitirem derivação.

**DoD:**

```
SELECT terminal_parent JOIN live_descendant = 0
```

após reconciliation deadline.

Teste obrigatório: reproduzir os WorkPlans encontrados no corpus.

---

### P0.2 — Completion Gate

Mudança:

```
DONE
```

não deve ser sinônimo universal de:

```
Verified Completion
```

DoD:

```
required acceptance criterion unsatisfied
→ verified completion impossible
```

---

### P0.3 — Mutation uncertainty

Testar:

```
mutation finishes after timeout
network ack lost
runtime killed between dispatch/checkpoint
```

DoD:

zero retry automático enquanto effect state = `UNCERTAIN`.

---

### P0.4 — Intent Authority

O runtime deve carregar origem tipada:

```
USER
SYSTEM
TOOL
SCHEDULER
RECOVERY
WORKER
INTERNAL
```

e criação de trabalho deve exigir autoridade apropriada.

DoD:

system notification nunca cria Agent Task como se fosse pedido do usuário.

---

## P1 — Reliability

### P1.1 — Systemic Failure Circuit Breaker

Primeiro item ou pequena canary cohort antes de 100 operações equivalentes.

DoD:

falha estrutural em item 1 não produz automaticamente mais 99 execuções idênticas.

---

### P1.2 — Startup reconciliation

Ao reiniciar:

```
RUNNING + no live worker
```

não permanece eternamente `RUNNING`.

Mas também não vira automaticamente failed.

Deve ser classificado pela evidência disponível.

---

### P1.3 — Browser lease ownership

DoD:

duas mutating sessions não controlam simultaneamente a mesma page lease.

Human takeover revoga/suspende lease de agente explicitamente.

---

### P1.4 — Cron health/migration semantics

DoD:

provider/model incompatível deixa estado diagnosticável e acionável, sem failure loop infinito.

---

## P2 — Efficiency

### P2.1 — Runtime State Resolver

Centralizar consultas determinísticas como:

```
current task
current run
current browser
last effect
artifacts
dependencies
verification
```

O modelo recebe resposta estruturada.

---

### P2.2 — No-progress detector

Fingerprints:

```
same tool
same effective arguments
same observed state
same failure
```

por N ciclos.

Interromper loop e elevar situação.

---

### P2.3 — Skill economics

Registrar por execução:

```
skill_used
tokens
tool_calls
wall_time
verified_result
fallback_used
```

---

## P3 — UX/Learning

### P3.1 — Task Cockpit

Só depois que os invariantes forem verdadeiros.

Mostrar:

```
INTENT
PLAN
NOW
EVIDENCE
BLOCKERS
HUMAN ACTION
OUTCOME
```

O Cockpit deve ser projeção — nunca autoridade.

---

### P3.2 — Learn → Validate → Routine

Promoção baseada em dados e regression suite.

---

# 18. What NOT to build

Neste momento eu **não** construiria:

- outro Kanban;
- outro SessionDB;
- um “super banco Hermes”;
- outra camada de orchestration baseada em LLM;
- outro framework de memória;
- um segundo browser abstraction;
- mais estados visuais sem semântica formal;
- autonomous self-improvement irrestrito;
- sofisticado dashboard de métricas antes de confiarmos nos eventos;
- dezenas de novas Skills;
- mais parallelism.

Especialmente parallelism.

O sistema ainda precisa provar:

```
N=1 trustworthy
```

antes de otimizar:

```
N=100 concurrent
```

---

# 19. Hermes Work 100 — seed suite

Eu começaria com estes **20 casos derivados de problemas reais**, e não com 100 testes artificiais.

|Caso|Expected|Forbidden|
|---|---|---|
|Parent Interrupted|descendants reconciliados|running child|
|Parent Cancelled During Child|child recebe cancellation lineage|zombie|
|Late Completion After Timeout|reconciliation/uncertain|blind retry|
|Applied Mutation + Lost ACK|detectar efeito|duplicar efeito|
|System Message|permanecer system|virar user task|
|False Completion|acceptance impede close|`done` narrativo|
|12× Same Failure|circuit breaker|12 retries cegos|
|100-item Failure|canary interrompe batch|99 failures adicionais|
|Worker Dies|startup reconciliation|eternal running|
|Runtime Restart|resume/checkpoint|state reconstruction por guess|
|Browser Restart|reacquire semantic state|stale ref reuse|
|Two Sessions / One Page|exclusive mutation lease|competing clicks|
|Human Takeover|explicit suspended/handoff|corrida agente-humano|
|DOM Drift|reacquire/semantic resolution|blind old selector|
|SPA Hydration|readiness wait|premature mutation|
|CAPTCHA|blocked-human state|retry loop|
|Provider 429|bounded backoff|token-burning loop|
|Stale Skill|validate/block|99 bad executions|
|Cron Model Removed|NEEDS_MIGRATION|FAILED forever|
|E2E Test Isolation|zero residual state|`hermes-tests-*` visible|

Cada caso deve emitir pelo menos:

```
pass/fail
final canonical state
events
tool calls
tokens
elapsed time
human interventions
evidence coverage
```

---

# 20. North Star Metrics

**AVCR continua sendo uma boa North Star, mas é insuficiente sozinha.**

Eu definiria:

```
AVCR =
autonomous runs satisfying verified acceptance criteria
-------------------------------------------------------
eligible autonomous runs
```

O detalhe decisivo é “eligible”.

Não penalizar:

```
planned human handoff
CAPTCHA legitimately requiring human
approval deliberately required by policy
```

como falha autônoma comum.

Eu acompanharia junto:

### False Completion Rate

```
reported completed
but acceptance later shown unsatisfied
──────────────────────────────────────
reported completed
```

Esse talvez seja o **guardrail mais importante de todos**.

### Zombie Running Rate

```
live state without live execution
─────────────────────────────────
all running states
```

### Evidence Coverage

```
verified requirements with attributable evidence
────────────────────────────────────────────────
requirements requiring evidence
```

### Human Rescue Rate

Intervenções não planejadas necessárias para salvar a execução.

Separar de:

### Planned Handoff Rate

Intervenções explicitamente previstas.

### Systemic Failure Amplification

```
redundant child failures after systemic failure detectable
─────────────────────────────────────────────────────────
systemic failure incidents
```

Ideal → próximo de zero.

### Context Reconstruction Overhead

```
tokens/tool calls used to rediscover known structured state
──────────────────────────────────────────────────────────
total execution cost
```

Essa métrica pode acabar sendo extremamente reveladora.

E, finalmente:

```
Tool Calls / Verified Outcome
Tokens / Verified Outcome
Cost / Verified Outcome
Time / Verified Outcome
```

O denominador importa.

Não medir custo por “resposta”.

Medir custo por **resultado verificado**.

---

# 21. Final Architecture

A arquitetura-alvo que eu recomendaria não é uma revolução.

É a arquitetura existente **com invariantes fortes atravessando-a**:

```
                         MESSAGE ENVELOPE
                               │
                        INTENT AUTHORITY
                               │
                         ┌─────▼─────┐
                         │ WorkIntent│
                         └─────┬─────┘
                               │
                   CANONICAL WORK LINEAGE
                               │
        ┌──────────────────────┼──────────────────────┐
        │                      │                      │
     Human Card             Agent Task              Cron
        │                      │                      │
        │                  Task Run                   │
        │                      │                      │
        │                  WorkPlan                   │
        │                      │                      │
        │                  WorkItems                  │
        │                      │                      │
        └──────────────────────┼──────────────────────┘
                               │
                      EXECUTION SUPERVISOR
                               │
             ┌─────────────────┼─────────────────┐
             │                 │                 │
          Browser           Worker           Host/System
             │                 │                 │
             └─────────────────┼─────────────────┘
                               │
                       EFFECT JOURNAL
                               │
                 ┌─────────────┼────────────┐
                 │             │            │
              Evidence      Artifacts    Checkpoints
                 │             │            │
                 └─────────────┼────────────┘
                               │
                     ACCEPTANCE ENGINE
                               │
                     VERIFIED OUTCOME
                               │
                 ┌─────────────┴─────────────┐
                 │                           │
              Result                    Experience
                                             │
                                        Candidate
                                             │
                                        Validation
                                             │
                                      Skill / Routine
```

Transversalmente:

```
Invariant Engine
Reconciliation Plane
Capability Registry
Policy Engine
Event Bus
Execution Environment Identity
```

Isso é muito menos uma “nova arquitetura” do que parece.

É **formalizar as relações que o Hermes já tenta manter informalmente**.

---

# 22. Final Recommendation

A investigação reforça uma mudança de direção importante.

O próximo grande marco do Hermes Work não deveria ser:

> “o Hermes consegue fazer mais coisas”.

Deveria ser:

> **“o Hermes consegue provar que sabe em que estado o trabalho está.”**

Eu concentraria a próxima fase quase exclusivamente em quatro propriedades:

```
1. Identity
2. Terminality
3. Effect certainty
4. Acceptance
```

Ou, em português:

> **quem pediu, qual trabalho é esse, o que efetivamente aconteceu e o que prova que terminou.**

Depois disso, browser reliability, recovery, cron, learning e Task Cockpit passam a se encaixar naturalmente.

A hipótese anterior de uma “identidade operacional canônica” sobreviveu à tentativa de refutação, mas em uma forma mais precisa: **não devemos criar um megaestado centralizado**. Devemos criar uma **cadeia causal canônica entre autoridades especializadas**.

A evidência também reforçou a necessidade de Verified Completion e do Systemic Failure Circuit Breaker. Já a interpretação mais simples de One Hermes State — “consolidar os bancos” — deve ser descartada.

A mudança arquitetural com maior relação impacto/custo é, portanto:

> **transformar lifecycle transitions em invariantes causais reconciliáveis, em vez de permitir que cada entidade registre seu próprio estado terminal isoladamente.**

Se isso for feito corretamente, vários sintomas desaparecem juntos: zombie WorkItems, progresso falso, restart ambíguo, cancellation parcial, recovery inseguro, estados contraditórios e boa parte da dificuldade de auditoria.

Essa é a fundação sobre a qual eu construiria o **Hermes Work 100**. Só depois de essa suite começar a medir continuamente `False Completion ≈ 0`, `Zombie Running ≈ 0` e AVCR crescente eu trataria novas capacidades como prioridade.

A pergunta que você colocou — _“posso entregar trabalho real, sair e acreditar no que ele me mostrar horas depois?”_ — tem uma resposta bastante clara após os dados examinados:

**o Hermes já tem muitas das peças de um sistema desse tipo, mas ainda não conquistou essa confiança no nível dos invariantes. O próximo salto não é mais inteligência; é tornar causalidade, terminalidade, side effects e evidência impossíveis de contradizer silenciosamente.**