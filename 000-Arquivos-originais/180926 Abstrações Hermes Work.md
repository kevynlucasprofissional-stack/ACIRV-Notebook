Sim — **a arquitetura tem boas chances de funcionar**, mas existe uma peça que agora fica tão importante quanto o próprio Experience Compiler: **o mecanismo de seleção**.

Aprender uma capability não basta. O Hermes precisa saber, diante de uma intenção ou mudança de estado, se deve:

```text
usar uma Capability conhecida
compor várias Capabilities
continuar deterministicamente
esperar por algum evento
pedir intervenção humana
ou acordar o LLM porque apareceu novidade
```

Eu colocaria isso explicitamente na arquitetura como um **Capability Router / Operational Router**.

A arquitetura completa começa a ficar assim:

```text
                         ┌─────────────────────┐
                         │  evento / usuário   │
                         └──────────┬──────────┘
                                    ↓
                         ┌─────────────────────┐
                         │ Operation Intent    │
                         │ + Current State     │
                         └──────────┬──────────┘
                                    ↓
                         ┌─────────────────────┐
                         │ Capability Router   │
                         └──────────┬──────────┘
                                    │
            ┌───────────────────────┼───────────────────────┐
            ↓                       ↓                       ↓
       EXACT MATCH            COMPOSITION              NO MATCH
            ↓                       ↓                       ↓
     deterministic          capability DAG             LLM reasons
       execution                  ↓                       ↓
            │                work_execute              learns
            │                       │                       ↓
            └───────────────→ verify ←──────── Experience Compiler
                                    │
                              drift/novelty?
                               │         │
                              no        yes
                               │         ↓
                              done   wake LLM only
                                     for that fragment
```

Esse Router é a resposta para grande parte das suas perguntas.

## Skills devem citar capabilities?

**Não como mecanismo principal.**

Eu evitaria algo como:

```text
Skill GitHub:
use cap_93aa1827 version 4.1.0
```

porque isso cria acoplamento, envelhece rápido e volta a transformar o modelo em roteador.

Uma Skill pode conhecer **capacidades conceituais**:

```text
Para concluir um merge:
- localizar PR
- verificar mergeabilidade
- executar merge
- confirmar estado merged
```

ou até declarar:

```text
requires:
  - github.pull_request.inspect
  - github.pull_request.merge
```

Mas isso seria uma **interface semântica**, não necessariamente um ID físico.

O Runtime resolve:

```text
github.pull_request.merge
        ↓
qual versão?
qual backend?
qual scope?
qual capability é compatível com este estado?
```

A dependência exata fica internamente no Capability Graph.

Então:

```text
Skill
  = sabe O QUE / POR QUÊ / estratégia

Capability Router
  = decide QUAL implementação operacional usar

Capability
  = sabe COMO executar deterministicamente
```

Isso é muito mais limpo.

---

# E gatilhos? Dá para “avisar a IA”?

Sim. E acho que isso deveria virar outra peça explícita da arquitetura:

# **Event / Trigger Plane**

Na realidade, o melhor desenho nem é manter a IA “esperando”.

O ideal é **parar a IA completamente**.

Suponha:

```text
Hermes envia um processamento
↓
resultado ainda não está pronto
```

Hoje um agente pode cair na tentação de:

```text
checar
esperar
checar
esperar
checar
esperar
```

Isso é péssimo.

Em vez disso:

```text
Hermes registra:

AwaitCondition:
  condition = job.status == "completed"
  deadline = 30 min
  wake_policy = ON_CHANGE
```

e encerra a execução ativa.

O runtime continua observando sem LLM.

Quando acontece:

```text
job.status:
running -> completed
```

o Event Plane produz algo como:

```text
RuntimeEvent
  type = STATE_CHANGED
  object = job_123
  before = running
  after = completed
  evidence_ref = artifact://...
```

Então existem duas possibilidades.

Se já existe uma reação determinística:

```text
trigger:
job.completed

→ execute capability:
job.collect_result
```

Nem acorda o modelo.

Mas se for necessária interpretação:

```text
trigger:
pull_request.merge_conflict_detected
```

o runtime produz:

```text
ReasoningWakeup
```

com algo parecido com:

```text
reason:
  capability drift

capability:
  github.merge_pull_request@3.2

completed_until:
  verify_mergeability

expected:
  mergeable=true

observed:
  mergeable=false
  conflict=true

state_ref:
  artifact://...

question:
  determine how to resolve this exception
```

E **só aí o LLM volta**.

Isso é literalmente “avisar a IA”.

E é melhor do que inserir uma mensagem artificial de usuário. Deve ser um **evento confiável do runtime**, preservando a autoridade e a procedência do dado.

---

# Também podemos colocar a IA para aguardar

Eu criaria estados formais:

```text
RUNNING

WAITING_FOR_EVENT
WAITING_FOR_TIMER
WAITING_FOR_EXTERNAL_STATE
WAITING_FOR_HUMAN
WAITING_FOR_APPROVAL

NEEDS_REASONING

COMPLETED
FAILED
CANCELLED
```

A IA não fica ocupando contexto nem tokens em `WAITING_*`.

Ela simplesmente:

```text
persist state
register subscription
yield
```

Quando o Trigger Plane dispara:

```text
resume deterministic runtime
```

ou:

```text
wake reasoning
```

dependendo da situação.

Isso casa perfeitamente com a arquitetura que estamos criando.

---

# 1. O que exatamente deve virar Capability?

Nem necessariamente uma ação atômica, nem necessariamente um workflow inteiro.

A regra é:

> **Capability deve ser o menor segmento semanticamente fechado que possua utilidade real de reutilização.**

Eu separaria três níveis:

```text
PRIMITIVE
browser.click
filesystem.write
process.start

↓ composição

ATOMIC OPERATIONAL CAPABILITY
browser.fill_field(field, value)
github.merge_pull_request(repo, pr)
filesystem.rename_using_pattern(...)

↓ composição

COMPOSITE CAPABILITY / ROUTINE
github.prepare_and_merge_pull_request(...)
publish_campaign(...)
sync_repository_and_verify(...)
```

Uma Capability “atômica” pode conter 7 tool calls.

Por exemplo:

```text
snapshot
locate
click
wait
confirm
reload
verify
```

pode ser uma única Capability:

```text
github.merge_pull_request(pr)
```

porque o efeito significativo só existe quando:

```text
PR.state == merged
```

Por outro lado:

```text
scroll
```

geralmente não deveria virar Capability.

É mecanismo incidental.

Portanto o teste é:

> Existe um precondition observável, uma transformação operacional fechada e uma postcondition verificável?

Se sim, temos uma candidata.

O workflow inteiro pode virar uma **Composite Capability**, mas deve reutilizar as atômicas:

```text
release.deploy
    ├── git.sync_main
    ├── tests.run_release_gate
    ├── package.build
    └── release.verify
```

Não copie esses procedimentos dentro da mega-capability.

---

# 2. Como provar que duas execuções pertencem à mesma operação semântica?

Não pela igualdade das tool calls.

E não apenas porque ambas tiveram sucesso.

A identidade deveria resultar de algo próximo a:

```text
Semantic Operation Identity =
    operation_family
  + route/runtime
  + target_family
  + effect_class
  + scope_family
  + state_transition_shape
  + parameter_relations
  + verifier/postcondition family
```

Exemplo:

```text
browser_click(@e12)
browser_click(@e99)
```

fisicamente diferentes.

Mas:

```text
operation_family = github.merge
target_family = pull_request
before = pr_state:open
after = pr_state:merged
```

podem ser instâncias da mesma operação.

Por outro lado:

```text
browser_click(@e12) → open settings
browser_click(@e99) → delete account
```

não pertencem à mesma operação mesmo tendo exatamente a mesma assinatura estrutural.

A evidência aumenta progressivamente:

```text
C0  apareceu uma vez
C1  apareceu repetidamente
C2  sucessos/falhas discriminam corretamente
C3  replay reproduziu o efeito
C4  ablation mostrou quais passos são necessários
C5  continuou válido em contextos/inputs diferentes
```

Não existe uma “prova matemática absoluta” de equivalência semântica para ambientes arbitrários.

Existe **confiança operacional crescente baseada em invariantes testáveis**.

---

# 3. Quando parar de raciocinar?

Essa é talvez a regra mais importante:

> **O Hermes para de raciocinar quando não existe mais nenhuma decisão semanticamente aberta no próximo segmento.**

Eu criaria uma espécie de:

# Determinism Readiness Gate

Antes de executar sem LLM:

```text
Capability promoted/admitted?          ✓
Exact compatibility?                  ✓
Inputs resolvidos?                     ✓
Preconditions verificáveis?            ✓
Preconditions satisfeitas?             ✓
Route conhecida?                       ✓
Effect conhecido?                      ✓
Authority/approval resolvidos?          ✓
Branches dependem de predicados?        ✓
Postcondition existe?                  ✓
Verifier existe?                       ✓
Nenhuma ambiguidade semântica aberta?  ✓
```

Se tudo for verdade:

```text
ResolverResult.EXACT_EXECUTABLE
```

→ zero raciocínio.

Se faltar alguma coisa:

```text
NEEDS_REASONING
```

Não é:

> “confiança chegou a 87%, então não raciocine.”

É muito mais estrutural:

> **Todos os graus de liberdade da execução estão resolvidos?**

Se sim, execute.

---

# 4. Como validar uma Capability?

Eu usaria quatro camadas.

Primeiro, **validação estrutural**:

```text
schemas válidos
effects declarados
inputs tipados
sem refs transitórios
sem secrets
pre/postcondition existentes
verifier conhecido
authority conhecida
```

Depois, **validação observacional**:

```text
múltiplas execuções
parâmetros diferentes
contextos diferentes
success/failure examples
drift examples
```

Depois, quando seguro, **validação por replay**:

```text
mesmo modelo
novo estado compatível
novos parâmetros
→ mesma postcondition
```

Isso leva a C3.

Depois, quando seguro:

```text
ablation / delta debugging
```

Remove passos:

```text
A B C D E
```

e verifica se:

```text
A C D E
```

ainda produz o mesmo resultado.

Assim distinguimos:

```text
coincidência
```

de:

```text
passo necessário / modelo causal mais forte
```

Para uma operação local reversível:

```text
C3 talvez seja suficiente
```

Para uma mutação externa importante:

```text
C4+
+
E2/E3
+
approval policy
```

faz mais sentido.

---

# 5. Como compor capabilities sem LLM?

Typed DAGs.

Exemplo:

```text
Capability:
release.prepare
```

declara:

```text
dependencies:
  git.sync_main
  tests.run_suite
  package.build
```

e mapeamentos:

```text
git.sync_main.output.commit
         ↓
tests.run_suite.inputs.commit
```

O `CapabilityResolver` resolve o DAG:

```text
git.sync_main
       ↓
tests.run_suite
       ↓
package.build
       ↓
release.prepare
```

O `OperationalKernel` executa.

Branches devem ser baseadas em predicados observáveis:

```text
IF repo_dirty:
    git.stash_or_commit

IF tests_pass:
    build
ELSE:
    NEEDS_REASONING
```

Não:

```text
"decida inteligentemente se devemos buildar"
```

Isso exigiria LLM.

Uma Capability determinística pode usar:

```text
DAG
FSM
condition
loop bounded
wait condition
dependency
```

sem raciocínio generativo.

---

# 6. Como detectar drift e mandar só o trecho quebrado?

Cada Capability precisa funcionar como um pequeno programa verificável.

Depois de cada boundary relevante:

```text
expected state
vs
observed state
```

Se coincidem:

```text
continue
```

Se não:

```text
DRIFT
```

O runtime localiza a **primeira hipótese invalidada**.

Por exemplo:

```text
step 1 ✓
step 2 ✓
step 3 ✓
step 4 ✗
step 5 not executed
step 6 not executed
```

Não devolva o workflow inteiro.

Devolva:

```text
NEEDS_REASONING

capability:
github.merge_pull_request@3.1

completed_until:
step_3

failed_assumption:
merge_control_available == true

observed:
merge_control_available == false
merge_conflict == true

confirmed_effects:
[...]

unresolved_subgraph:
steps 4-6

state_ref:
artifact://...

safe_to_resume:
true
```

O LLM resolve:

```text
o que fazer com merge conflict?
```

Não precisa raciocinar novamente sobre:

```text
como abrir o PR
como localizar o botão
como verificar estado
```

Depois podemos gerar:

```text
Capability v3.2 Candidate
```

com a nova branch:

```text
IF merge_conflict:
    ...
```

Esse é o mecanismo que realmente amortiza raciocínio.

---

# 7. Como encontrar capabilities sem mandar centenas delas para o modelo?

Este ponto é crítico:

> **Capabilities não devem ser tools do prompt.**

Ter:

```text
800 capabilities
```

não significa:

```text
800 tool schemas enviados ao LLM.
```

O catálogo fica atrás do **Capability Router**.

O modelo idealmente vê algo próximo de:

```text
work_execute
```

ou nem isso diretamente em certos caminhos.

Quando chega uma intenção:

```text
"junte esse PR"
```

temos um pequeno objeto intermediário:

```text
OperationIntent

action_family:
merge_pull_request

target:
repository / pull_request

desired_effect:
pr_state = merged

scope:
repo=X
pr=42

constraints:
...
```

Então:

```text
Capability Router
```

procura internamente.

Índice possível:

```text
operation_family
effect
route
target_family
scope
preconditions
compatibility fingerprint
version
```

Resultado:

```text
EXACT_MATCH
```

→ executar.

Se houver:

```text
NO_MATCH
```

→ LLM.

Se houver:

```text
POSSIBLE_MATCHES
```

podemos mostrar ao LLM só:

```text
3 candidatos compactos
```

e nunca 800 schemas.

Algo como:

```text
Known operations potentially relevant:

1. github.merge_pull_request
2. github.rebase_and_merge
3. github.resolve_simple_conflict
```

Mesmo aí, o **runtime ainda verifica a compatibilidade** antes de executar.

Similarity ajuda retrieval.

Não concede authority.

---

# 8. Como provar que estamos amortizando raciocínio?

Não devemos medir apenas:

```text
“o LLM foi chamado menos”
```

porque poderíamos ter criado um monstro de compiler que custa mais do que economiza.

A métrica certa é **custo total por resultado verificado ao longo de múltiplas execuções**.

Suponha uma operação repetida N vezes.

Sem aprendizado:

```text
Cost_baseline(N) =
N × reasoning_cost
```

Com Experience Compiler:

```text
Cost_learned(N) =
discovery_cost
+ validation_cost
+ compiler_cost
+ maintenance_cost
+ N × replay_cost
+ drift_recovery_cost
```

Queremos:

```text
Cost_learned(N) < Cost_baseline(N)
```

a partir de algum N.

Isso nos dá inclusive o:

# Break-even reuse count

Exemplo hipotético:

```text
descobrir + validar = 8 unidades
replay = 0.3

LLM convencional = 2 unidades por execução
```

Então:

```text
sem compiler:
2N

com compiler:
8 + 0.3N
```

break-even:

```text
8 + 0.3N < 2N
8 < 1.7N
N > 4.7
```

Após aproximadamente a quinta reutilização, começou a compensar.

Isso é muito mais útil do que dizer apenas:

> “reduzimos tokens”.

Eu acompanharia especialmente:

```text
LLM calls / verified outcome

tokens / verified outcome

discovery cost / capability

validation cost / capability

deterministic replay rate

capability hit rate

cross-task reuse rate

cross-session reuse rate

Operational Novelty Rate

drift rate

human rescue rate

failed replay rate

compiler CPU/time

registry lookup latency

maintenance/refinement cost

average Operational Slice reduction

break-even reuse count

% capabilities never reused
```

Essa última é importantíssima.

Se tivermos:

```text
10.000 capabilities
```

e:

```text
8.000 nunca mais usadas
```

o compiler provavelmente está superproduzindo lixo.

---

## O pedaço que eu acrescentaria agora à arquitetura

Depois dessas perguntas, eu considero que há **dois conceitos que ainda precisam ganhar nome e owner explícitos**:

```text
CAPABILITY ROUTER

intent/state
→ exact capability resolution
→ composition
→ fallback to reasoning
```

e:

```text
EVENT / TRIGGER PLANE

event/state change
→ deterministic reaction
OR
→ wake LLM with minimal Attention Packet
```

Isso cria uma separação muito elegante:

```text
Experience Compiler
= aprende COMO fazer

Capability Router
= reconhece QUANDO usar o que já sabemos

Trigger Plane
= reconhece QUANDO alguma coisa mudou

LLM
= entra apenas quando ainda existe uma decisão aberta
```

E as Skills ficam acima disso:

```text
Skill
= conhecimento estratégico

Router
= seleção operacional

Capability
= conhecimento operacional compilado

Kernel
= execução física

Trigger Plane
= temporalidade/eventos
```

Esse desenho também responde à sua pergunta sobre “avisar a IA”: **o LLM deixa de ser um processo que fica continuamente acordado**. Ele passa a ser quase um recurso de escalonamento cognitivo.

O sistema tenta primeiro:

```text
resolver
executar
esperar
verificar
reagir
```

deterministicamente.

Só quando chega a uma fronteira que realmente contém novidade:

```text
→ wake_reasoner()
```

Essa, para mim, é a consequência mais interessante de tudo que estamos construindo: **o Hermes deixa progressivamente de ser um LLM que usa ferramentas e começa a virar um runtime operacional que possui um LLM para resolver apenas as partes que ainda não conseguiu compilar.**

Essas quatro perguntas definem, na prática, o **Control Plane** do Hermes. O Experience Compiler responde “o que aprendemos”; agora precisamos definir formalmente **como o sistema decide agir com o que aprendeu**.

Minha síntese é:

```text
MessageEnvelope / Trigger / Capability
            ↓
      OperationIntent
            +
      Current State
            ↓
     Capability Router
            ↓
 ┌──────────┼───────────┬───────────┬───────────┐
EXECUTE   COMPOSE      WAIT      ASK_HUMAN    WAKE_LLM
```

E há uma consequência importante: **Skills não deveriam normalmente citar IDs físicos de Capabilities**. Skills deveriam produzir objetivos/intents semânticos. O Router escolhe a Capability concreta.

---

# 1. Qual é a representação canônica da intenção operacional?

Eu criaria duas abstrações relacionadas:

```text
OperationIntent
    contains
GoalContract
```

O princípio é:

> **Intent deve dizer o que precisa se tornar verdadeiro, não como produzir isso.**

Isso converge com arquiteturas BDI, nas quais goals descrevem estados desejáveis enquanto plans são os meios aplicáveis em determinado contexto; planos podem então ser escolhidos em função de eventos e crenças atuais. ([Springer Nature Link](https://link.springer.com/article/10.1007/s10458-020-09453-y?utm_source=chatgpt.com "Agent programming in the cognitive era | Autonomous Agents and Multi-Agent Systems | Springer Nature Link"))

Portanto isto seria errado:

```text
OperationIntent:
  open github
  click PR
  click merge
  confirm
```

Porque isso já é um plano.

O correto seria algo próximo de:

```yaml
intent_id: intent_9182

mode: ACHIEVE

target:
  resource_type: github.pull_request
  selector:
    repository: kevyn/hermes
    pr_number: 42

goal:
  predicates:
    state: merged

invariants:
  - repository.default_branch unchanged
  - no unrelated pull_request modified

constraints:
  forbidden_effects:
    - delete_repository
  deadline: null

acceptance:
  required_predicates:
    state: merged
  minimum_evidence: E2

authority:
  source_ref: message_envelope_...
  permitted_effect: external_mutation

lineage:
  task_id: ...
  run_id: ...
  parent_intent_id: null

context_refs:
  - artifact://...
```

Observe o que **não aparece**:

```text
capability_id
tool name
DOM ref
recipe
browser instructions
implementation
```

A intenção sobrevive mesmo se o Hermes trocar de implementação.

Hoje:

```text
github.merge_pull_request_ui
```

pode realizá-la.

Amanhã talvez:

```text
github.merge_pull_request_api
```

Faça o mesmo trabalho.

O `OperationIntent` continua igual.

## Há quatro tipos especialmente úteis de goal

Eu usaria algo próximo de:

```text
ACHIEVE
estado X deve passar a ser verdadeiro

MAINTAIN
X deve continuar verdadeiro

OBSERVE
descobrir/verificar qual é X

AVOID
X não deve ocorrer
```

Por exemplo:

```text
ACHIEVE:
pr.state == merged
```

ou:

```text
MAINTAIN:
server.health == healthy
```

Isso também abre naturalmente o caminho para triggers.

---

## E de onde vem o OperationIntent?

Ele pode ser produzido por vários atores:

```text
usuário
LLM
Skill
Capability composta
Trigger
Workflow/Routine
```

Mas existe uma distinção essencial:

> **quem descreve o objetivo não necessariamente possui autoridade para criá-lo.**

Isso combina muito bem com o `MessageEnvelope` que o Hermes já possui.

A linguagem/LLM pode produzir:

```text
goal = pr.state == merged
```

Mas:

```text
authority = external_mutation
```

não pode ser inventada pelo LLM.

Vem do envelope/policy confiável.

Portanto:

```text
Natural Language
      ↓
Intent interpretation
      ↓
OperationIntent

Trusted MessageEnvelope
      ↓
Authority
```

As duas coisas se juntam depois.

---

# 2. Qual é o algoritmo mínimo para `EXECUTE / COMPOSE / WAIT / ASK_HUMAN / WAKE_LLM`?

Eu acredito que podemos fazer isso surpreendentemente pequeno.

O Router não precisa ser outro “agente inteligente”.

Ele pode ser essencialmente um **motor de prova de executabilidade**.

A entrada é:

```text
R(Intent I, State S, CapabilityLibrary L, Policy P)
```

e a saída:

```text
RoutingDecision
```

Eu adicionaria também um sexto resultado:

```text
SATISFIED
```

porque às vezes o objetivo já está cumprido.

A semântica seria:

|Decisão|Significado|
|---|---|
|`SATISFIED`|objetivo já é verdadeiro|
|`EXECUTE`|uma Capability resolve diretamente|
|`COMPOSE`|DAG determinístico de Capabilities resolve|
|`WAIT`|falta apenas uma mudança futura observável|
|`ASK_HUMAN`|falta decisão/autoridade exclusivamente humana|
|`WAKE_LLM`|existe uma decisão semântica/estratégica ainda aberta|

O algoritmo pode funcionar assim.

Primeiro:

```text
goal(I) já é verdadeiro em S?
```

Se sim:

```text
SATISFIED
```

Isso evita até executar coisas desnecessárias.

Depois verifica se existe algum estado incerto:

```text
mutation dispatched
ACK lost
persisted effect unknown
```

Nesse caso ele não procura uma nova Capability.

Primeiro entra em:

```text
RECONCILE
```

que pode resultar em WAIT, ASK_HUMAN ou continuar.

---

## Direct Capability resolution

O Router consulta um índice interno aproximadamente assim:

```text
goal predicates
target family
operation family
effect class
scope
route
```

Encontra capabilities cujo:

```text
postcondition
```

satisfaz o `GoalContract`.

Então aplica admission:

```text
version promoted?
drift healthy?
target compatible?
scope compatible?
preconditions satisfied?
effect authorized?
approval satisfied?
input mapping complete?
evidence/verifier available?
```

Se houver uma:

```text
EXECUTE
```

---

# Composição

Se nenhuma Capability isolada resolve o goal:

```text
desired state
   ↓
quais Capability effects produzem isso?
   ↓
quais preconditions elas exigem?
   ↓
já são verdadeiras?
   │
   └─ não
      ↓
quais outras Capabilities produzem essas preconditions?
```

Isso é **backward chaining**.

É bastante próximo da ideia de HTN de decompor tarefas abstratas em subtarefas até chegar a operações executáveis, embora aqui estejamos raciocinando principalmente sobre efeitos declarativos e capabilities já aprendidas. ([DCC - UMD](https://www.cs.umd.edu/projects/shop/description.html?utm_source=chatgpt.com "SHOP (Simple Hierarchical Ordered Planner)"))

Exemplo:

```text
GOAL:
local_main == remote_main
```

Não existe uma Capability única.

Mas:

```text
git.fetch
     ↓
git.checkout_main
     ↓
git.fast_forward
     ↓
git.verify_sync
```

satisfaz.

Resultado:

```text
COMPOSE
```

---

## Mas a busca precisa ser limitada

Senão criamos outro planner caro.

Eu imporia:

```text
max composition depth
max candidates examined
max branching factor
deadline
risk budget
```

Algo como:

```text
depth <= 5
```

não precisa ser uma regra eterna, mas precisamos de um limite.

Se a busca explode:

```text
WAKE_LLM
```

O LLM descobre uma estratégia nova.

Depois ela pode virar conhecimento compilado.

---

# A regra para WAIT / HUMAN / LLM

Depois das tentativas de direct match/composition, olhamos **o tipo da lacuna**.

### Temporal gap

Sabemos exatamente o que fazer, mas uma condição ainda não ocorreu:

```text
job.status != complete
```

→

```text
WAIT
```

### Authority/preference gap

O sistema sabe as opções, mas a decisão pertence à pessoa:

```text
publicar ou não?
aceitar custo?
aprovar pagamento?
captcha/handoff?
```

→

```text
ASK_HUMAN
```

### Knowledge/strategy gap

Temos autoridade, mas não sabemos deterministicamente como chegar ao objetivo:

```text
merge conflict desconhecido
layout novo
erro nunca visto
objetivo ambíguo
```

→

```text
WAKE_LLM
```

Essa distinção é extremamente poderosa:

```text
falta TEMPO      → WAIT
falta AUTORIDADE → HUMAN
falta CONHECIMENTO → LLM
```

---

# O Router deve explicar toda decisão

Nunca apenas:

```text
EXECUTE
```

Ele deve produzir um `RoutingDecision` auditável:

```yaml
decision: EXECUTE

intent_id: intent_9182

capability:
  id: github.merge_pull_request
  version: 3.2.0

proof:
  goal_coverage:
    pr.state: merged

  satisfied_preconditions:
    - pr.state == open
    - mergeable == true

  authority:
    external_mutation: allowed

  compatibility:
    exact: true

state_ref: artifact://...

policy_version: router-v1
```

Isso permite descobrir depois se uma falha foi:

```text
Capability failure
```

ou:

```text
Router failure
```

Uma distinção fundamental.

---

# 3. Qual é a menor unidade que pode suspender e retomar uma TaskRun?

Não é um Event.

É uma:

# `AwaitCondition`

Esse é um ponto importante.

Um evento é efêmero:

```text
download_completed
```

Se o Hermes estiver desligado no instante em que ele ocorrer, talvez perca o evento.

O que queremos persistir é:

> **a condição que precisa tornar-se verdadeira para que a continuação possa prosseguir.**

Eu modelaria assim:

```text
AwaitCondition =
<
  Predicate,
  Observer,
  Correlation,
  Continuation,
  Deadline,
  Fence
>
```

Concretamente:

```yaml
wait_id: wait_8821

predicate:
  resource: download_123
  field: status
  operator: eq
  value: completed

observer:
  kind: runtime_event
  event_type: download_completed

correlation:
  download_id: 123

continuation:
  workplan_id: work_882
  next_node: process_download
  capability_snapshot:
    id: reports.process_download
    version: 2.1.0

fence:
  task_id: task_10
  run_id: 17
  operation_id: op_51

deadline:
  at: ...

on_timeout:
  action: WAKE_LLM
```

A TaskRun então faz:

```text
persist AwaitCondition
↓
yield
↓
zero LLM
zero reasoning
```

---

# Evento não é verdade; evento é um wakeup hint

Esse é um princípio que eu tornaria canônico.

Suponha que recebemos:

```text
DOWNLOAD_COMPLETED
```

O Hermes não deve imediatamente assumir:

```text
download == complete
```

Ele deve:

```text
event
  ↓
locate matching AwaitCondition
  ↓
check TaskRun fence
  ↓
read authoritative current state
  ↓
predicate true?
```

Só então resume.

Isso resolve:

```text
duplicate event
stale event
event received before commit
lost event
restart
event replay
```

Se o evento for perdido, polling ou restart reconciliation ainda pode observar:

```text
status == completed
```

e continuar.

Portanto:

> **Eventos acordam condições; condições autorizam continuações.**

---

# Essa unidade também unifica todos os WAITING_*

Não precisamos criar cinco subsistemas completamente diferentes.

Podemos ter:

```text
AwaitCondition
```

com observadores diferentes.

Por exemplo:

```text
WAITING_FOR_TIMER
observer = clock

WAITING_FOR_EVENT
observer = event bus

WAITING_FOR_EXTERNAL_STATE
observer = connector/API/readback

WAITING_FOR_HUMAN
observer = human handoff state

WAITING_FOR_APPROVAL
observer = approval store
```

A semântica de suspensão permanece uma só.

---

# E a continuação é crucial

O AwaitCondition não deve apenas dizer:

```text
acorde o Hermes
```

Ele precisa dizer:

```text
continue daqui
```

Por exemplo:

```text
WorkPlan:
1 ✓
2 ✓
3 WAITING
4 pending
5 pending
```

Quando a condição ocorre:

```text
resume node 4
```

Não:

```text
mande tudo para o LLM de novo
```

---

# Fencing também é obrigatório

Imagine:

```text
TaskRun 17 suspenso
```

Depois:

```text
TaskRun 18
```

substitui o run.

Então chega atrasado o evento da Run 17.

Sem fence:

```text
evento velho
→ execução nova
```

péssimo.

Portanto:

```text
AwaitCondition.run_id == current_run_id
```

é obrigatório antes do resume.

Isso encaixa perfeitamente no TaskRun fencing que o Hermes já possui.

---

## O repositório atual já tem boas sementes

No código atual há uma escolha correta importante: eventos de sistema **não correlacionados são tratados como observações, não como autorização para criar novo trabalho**.

Isso deve continuar.

O Trigger Plane não deve criar intenção do nada.

Ele pode:

```text
satisfazer uma AwaitCondition existente
```

ou:

```text
gerar observação para triagem
```

Só uma autoridade legítima cria novo trabalho.

Isso também harmoniza com a separação existente entre `MessageEnvelope.content` e `IntentAuthority`.

---

# 4. Como provar que o Router realmente amortiza raciocínio?

Aqui precisamos ser muito rigorosos porque esse projeto pode facilmente se enganar.

Diminuir:

```text
LLM calls
```

não prova que melhoramos o sistema.

Poderíamos diminuir 100 chamadas de LLM e adicionar:

```text
5 segundos de lookup
1 GB de índices
200 ms de polling constante
50 capabilities inúteis
muita manutenção
10% de roteamento errado
```

Precisamos medir **custo total por resultado verificado**.

Eu definiria:

```text
TotalOperationalCost =
    ReasoningCost
  + RoutingCost
  + RetrievalCost
  + CompilationCost
  + ValidationCost
  + MonitoringCost
  + ReplayCost
  + DriftRecoveryCost
  + MaintenanceCost
  + HumanInterventionCost
```

Não precisa imediatamente transformar tudo em dólares.

Podemos manter um vetor:

```text
tokens
LLM calls
CPU time
wall time
tool calls
I/O
polls
human interventions
failed effects
```

---

# A comparação correta é acumulativa

Sem aprendizado:

```text
Baseline(N) =
N × (
  reasoning
  + execution
  + verification
)
```

Com Hermes:

```text
Hermes(N) =
discovery
+ compiler
+ validation
+ N × (
    router
    + deterministic replay
    + verification
  )
+ drift/recovery
+ maintenance
```

No começo:

```text
Hermes(N) > Baseline(N)
```

é perfeitamente possível.

Porque tivemos que aprender.

O que importa é existir um N onde:

```text
Hermes(N) < Baseline(N)
```

Esse é o:

# Break-even reuse count

---

## Exemplo

Hipoteticamente:

```text
resolver normalmente com LLM = 100 unidades

descobrir + compilar + validar = 300

router + replay = 10
```

Sem aprendizado:

```text
100N
```

Com aprendizado:

```text
300 + 10N
```

Break-even:

```text
300 + 10N < 100N

300 < 90N

N > 3.33
```

Na quarta reutilização começou a compensar.

Esse número deveria virar uma métrica real para cada família de capability.

---

# Reasoning Amortization Ratio

Eu refinaria a métrica que propusemos anteriormente.

Algo como:

```text
RAR =
reasoning cost actually avoided
/
new system overhead introduced to avoid it
```

Então:

```text
RAR > 1
```

significa:

> economizamos mais raciocínio do que gastamos com Router/Compiler/monitoramento.

Por exemplo:

```text
LLM cost avoided = 800
router + compiler + monitor = 200

RAR = 4
```

Excelente.

Se:

```text
RAR = 0.7
```

criamos complexidade líquida.

---

# Mas custo não basta

Também precisamos medir qualidade de roteamento.

Eu acompanharia especialmente:

```text
Exact Reuse Precision
```

Das vezes em que Router disse EXECUTE:

```text
quantas realmente eram executáveis?
```

Idealmente extremamente próximo de 100%.

E:

```text
Missed Reuse Rate
```

Quantas vezes:

```text
WAKE_LLM
```

aconteceu apesar de já existir Capability válida.

E:

```text
False Reuse Rate
```

Quantas vezes EXECUTE/COMPOSE ocorreu para uma Capability incompatível.

Essa é provavelmente a métrica de segurança mais importante do Router.

---

# Outra métrica crítica: Operational Novelty Rate

```text
ONR =
segments requiring new reasoning
/
all operational segments
```

Imagine:

```text
mês 1: 72%
mês 2: 48%
mês 3: 31%
mês 6: 15%
```

Mantendo a qualidade constante.

Isso seria uma evidência extraordinária de que Hermes está acumulando competência.

---

# E uma métrica pouco óbvia: Dead Capability Rate

```text
capabilities nunca reutilizadas
/
capabilities promovidas
```

Se for:

```text
80%
```

o Experience Compiler está produzindo lixo.

Isso é tão importante quanto token savings.

---

# Como testar cientificamente?

Eu faria quatro regimes.

Primeiro:

```text
ADAPTIVE BASELINE
```

Hermes resolve normalmente.

Depois:

```text
SHADOW ROUTER
```

Router escolhe Capability, mas não controla a execução.

Registramos:

```text
qual Capability teria escolhido?
```

e comparamos com o que realmente ocorreu.

Depois:

```text
LOW-RISK ROUTER
```

Router assume:

```text
reads
filesystem temp
sandbox
safe capabilities
```

Depois:

```text
MUTATING ROUTER
```

capabilities C3/C4+ entram gradualmente.

Isso nos permite medir precisão antes de dar autoridade.

---

# Também precisamos de holdout

Não basta testar:

```text
PR 123
```

e depois:

```text
PR 123 novamente
```

Isso prova replay.

Não generalização.

Precisamos:

```text
train/experience:
PR 123
PR 891
PR 42

holdout:
PR 1772
```

e idealmente outra sessão.

Assim provamos:

```text
cross-instance reuse
cross-task reuse
cross-session reuse
```

---

# A arquitetura completa que emerge

Depois dessas quatro respostas eu formalizaria o Hermes assim:

```text
                    HUMAN / SYSTEM / AGENT
                              │
                        MessageEnvelope
                              │
                              ▼
                       OperationIntent
                              │
                   ┌──────────┴──────────┐
                   │                     │
             Current State        Capability Index
                   │                     │
                   └──────────┬──────────┘
                              ▼
                     CAPABILITY ROUTER
                              │
          ┌──────────┬────────┼────────┬───────────┐
          ▼          ▼        ▼        ▼           ▼
      EXECUTE    COMPOSE     WAIT   ASK_HUMAN   WAKE_LLM
          │          │        │
          └────┬─────┘        ▼
               │       AwaitCondition
               │             │
               │        Event/Observer
               │             │
               │          predicate
               │           becomes
               │            true
               │             │
               └───────┬─────┘
                       ▼
                  Work Runtime
                       │
                 Operational
                    Kernel
                       │
                    verify
                       │
              ┌────────┴────────┐
              │                 │
           success            drift
              │                 │
              ▼                 ▼
        Experience        Attention Packet
         Compiler                │
              │                  ▼
              │                LLM
              ▼
        Capability
          Library
```

E aí cada componente possui uma pergunta muito simples:

**OperationIntent:** o que precisa tornar-se verdadeiro?

**Capability Router:** já sabemos deterministicamente como tornar isso verdadeiro?

**AwaitCondition:** sabemos exatamente o que fazer, mas precisamos esperar alguma coisa?

**Human:** falta uma decisão cuja autoridade é humana?

**LLM:** existe uma decisão cognitiva genuinamente nova?

**Capability:** como produzir determinada transformação?

**Experience Compiler:** podemos transformar o raciocínio usado agora em conhecimento operacional reutilizável?

**Operational Kernel:** execute a transformação.

---

A consequência arquitetural mais importante é esta:

> **O LLM não deveria mais ser o scheduler do Hermes.**

Nem o Router.

Nem o monitor.

Nem o waiter.

Nem o executor mecânico.

Ele se torna:

> **o resolvedor de graus de liberdade ainda não compilados.**

E eu diria que a próxima pergunta fundamental agora é uma só:

> **Como definir formalmente o `OperationIntent` e o `RoutingDecision` de forma que possamos provar, com propriedades e testes, que o Capability Router nunca executa uma transformação que não esteja logicamente coberta pelo objetivo, pela autoridade e pelo estado atual?**

Essa é a pergunta que transforma o Router de uma boa heurística em uma peça confiável do Hermes.

Sim. Essas 33 perguntas já formam quase a especificação do **Control Plane do Hermes**. A conclusão principal é que não precisamos de mais um “agente inteligente” entre o LLM e as Capabilities. Precisamos de uma camada pequena, declarativa e verificável que decida **agir, compor, esperar, pedir autoridade humana ou escalar para raciocínio**.

A arquitetura que eu adotaria é esta:

```text
Trusted ingress / User / Trigger / Skill
                 │
                 ▼
          OperationIntent
                 │
          + Current State
                 │
          + Policy/Authority
                 │
                 ▼
        ┌──────────────────┐
        │ Capability Router │
        └────────┬─────────┘
                 │
 ┌────────┬──────┼──────┬──────────┐
 ▼        ▼      ▼      ▼          ▼
DONE   EXECUTE COMPOSE WAIT    ASK_HUMAN
                                │
                         ou WAKE_LLM
```

E o princípio máximo seria:

> **O LLM resolve graus de liberdade ainda não compilados. Ele não deve ser scheduler, monitor, waiter, router nem executor mecânico.**

---

# I. Intenção e decisão operacional

## 0. Como transformar intenção + estado + eventos em decisão operacional?

Eu faria uma função conceitual única:

```text
Decision =
Route(
    OperationIntent,
    SemanticState,
    CapabilityLibrary,
    AuthorityPolicy,
    RuntimeState
)
```

A ordem importa. O Router deveria decidir assim:

```text
1. Validar TaskRun + authority.
2. Verificar se existe mutação anterior UNCERTAIN.
      sim → RECONCILE antes de qualquer coisa.

3. Observar somente o estado necessário.

4. Goal já está satisfeito?
      sim → SATISFIED.

5. Existe Capability exata e admissível?
      sim → EXECUTE.

6. Existe composição determinística bounded?
      sim → COMPOSE.

7. Falta apenas uma condição futura observável?
      sim → WAIT.

8. Falta decisão/autoridade humana?
      sim → ASK_HUMAN.

9. Existe decisão semântica/estratégica aberta?
      sim → WAKE_LLM.
```

Essa ordem impede dois erros fundamentais:

```text
usar LLM quando poderíamos esperar

e

planejar novamente algo que já sabemos executar
```

---

## 1. Representação mínima de `OperationIntent`

A intenção não deve conter plano.

Deve declarar **estado desejado**.

Eu usaria:

```yaml
intent_id: int_123

mode: ACHIEVE

target:
  family: github.pull_request
  identity:
    repo: kevyn/hermes
    number: 42

goal:
  predicates:
    state: merged

constraints:
  preserve:
    - repository.default_branch
  forbidden_effects:
    - repository.delete

acceptance:
  predicates:
    state: merged
  minimum_evidence: E2

authority_ref:
  envelope: msg_123

lineage:
  task_id: task_1
  run_id: run_7
```

O mínimo conceitual é:

```text
Target
+
Desired State
+
Constraints
+
Authority
+
Acceptance
+
Lineage
```

Não deve conter:

```text
browser_click
capability_id
work_execute
@e57
GitHub UI
steps
```

Assim:

> “sincronize meu repositório”

pode virar:

```text
target:
  repository X

goal:
  local.main.commit == remote.main.commit

constraints:
  preserve_worktree_changes == true
```

Independentemente de isso ser realizado por Git, GitHub API ou outra implementação futura.

---

## 2. Como o Router prova que uma Capability serve?

Toda Capability precisa possuir um **Capability Contract** suficiente para gerar uma pequena prova.

Algo como:

```text
CapabilityContract

inputs
preconditions
postconditions
effect
target_family
operation_family
route/runtime
scope
authority_required
risk
verifier
compatibility_fingerprint
version
drift_state
```

Então temos quatro estados importantes.

### `EXACT_EXECUTABLE`

Só ocorre se:

```text
goal coberto pela postcondition          ✓
target compatível                         ✓
todos inputs deterministicamente ligados ✓
preconditions conhecidas                  ✓
preconditions verdadeiras                 ✓
capability promoted                       ✓
drift_state healthy                       ✓
route/runtime disponível                  ✓
authority suficiente                      ✓
approval resolvido                        ✓
effect permitido                          ✓
verifier disponível                       ✓
versão pinned                             ✓
nenhuma condição aberta                   ✓
```

### `POSSIBLE_MATCH`

Existe forte compatibilidade semântica, mas falta alguma informação.

Por exemplo:

```text
talvez sirva,
mas mergeable ainda é desconhecido
```

Ela pode justificar uma observação adicional.

Não autoriza mutação.

### `INCOMPATIBLE`

Existe contradição demonstrável:

```text
wrong target family
wrong effect
scope incompatível
precondition falsa
authority insuficiente
version incompatible
```

### `NEEDS_REASONING`

O runtime possui informação, mas não consegue eliminar uma escolha semântica:

```text
duas estratégias materialmente diferentes
objetivo ambíguo
novo estado
search budget excedido
sem modelo operacional conhecido
```

O Router deveria produzir um **RoutingCertificate** explicando por que classificou o candidato assim.

---

## 3. Como separar entendimento da intenção de planejamento?

Por uma fronteira persistida.

```text
linguagem natural
       ↓
LLM interpreta
       ↓
OperationIntent
       ↓
────────── FREEZE ──────────
       ↓
Capability Router
```

Depois de o `OperationIntent` estar formado e autorizado, ele se torna um artefato operacional.

O modelo não continua interpretando:

> “sincroniza meu repo”

durante cada passo.

Ele já interpretou isso como:

```text
goal:
local.main == remote.main

constraint:
preserve local work
```

A partir daí o runtime trabalha com essa representação.

Se o LLM for acordado depois por drift, recebe apenas um **subproblema**.

Ele não ganha automaticamente permissão para reinterpretar o objetivo original.

Uma mudança real de intenção deveria gerar:

```text
IntentRevision
```

com lineage própria.

---

## 4. Qual linguagem intermediária usar?

Eu usaria uma pequena **Operational Intent IR**, não uma nova linguagem de programação.

Os conceitos fundamentais seriam:

```text
OperationIntent
GoalContract
StatePredicate
AuthorityContract
AcceptanceContract
TemporalCondition
```

A linguagem de predicados precisa ser limitada.

Exemplo:

```text
eq(resource.field, value)
neq(...)
exists(resource)
absent(resource)
contains(collection, item)
subset(...)
greater_than(...)
matches_schema(...)
```

E relações de estado:

```text
before → after
```

Por exemplo:

```text
pr.state:
open → merged
```

Evitaria código arbitrário:

```python
lambda state: ...
```

como representação persistente.

A IR precisa ser:

```text
serializável
versionável
comparável
fingerprintável
auditável
avaliável sem LLM
```

---

# II. Skills, descoberta e composição

## 5. Skills devem referenciar Capabilities?

Na maioria dos casos, **não IDs físicos**.

Uma Skill deveria declarar:

```yaml
requires:
  - operation_family: scm.pull_request.merge
```

e não:

```yaml
requires:
  - cap_92f83a@4.1.7
```

O Router resolve:

```text
scm.pull_request.merge
            ↓
github implementation?
gitlab implementation?
API?
browser?
qual versão?
```

Referência direta a Capability faria sentido somente quando a implementação específica for semanticamente necessária, por exemplo:

```text
compliance
reprodutibilidade
benchmark
workflow pinned
```

Então teríamos dois conceitos:

```text
requires_family
pins_capability
```

Skills descrevem estratégia.

Capabilities descrevem execução.

---

## 6. Como achar uma Capability entre milhares?

Com um índice interno, não com tool schemas enviados ao modelo.

Eu faria filtros sucessivos:

```text
1. target_family
2. desired effect / postcondition keys
3. operation_family
4. route/runtime
5. scope
6. capability lifecycle
7. semantic/compatibility fingerprint
8. preconditions
```

Exemplo de índice:

```text
github.pull_request
    └── state=merged
          ├── github.merge_pr_api
          ├── github.merge_pr_browser
          └── github.squash_merge
```

Isso pode ser resolvido por índices normais em memória/SQLite/artifacts.

Não começaria com embeddings.

### Retrieval aproximado

Serve para:

```text
encontrar possíveis candidatos
```

Não serve para:

```text
autorizar execução
```

Regra:

> **Approximate retrieval proposes. Symbolic admission authorizes.**

Se o Router achar 800 possibilidades, pode usar similaridade para reduzir a cinco.

Esses cinco ainda passam pelo admission gate determinístico.

---

## 7. Quando compor Capabilities automaticamente?

Quando nenhuma Capability isolada satisfizer a postcondition, mas existir uma cadeia verificável de efeitos.

O algoritmo mínimo pode ser **backward chaining bounded**.

Goal:

```text
local.main == remote.main
```

Procure quem produz isso:

```text
git.fast_forward
```

Precondition:

```text
remote refs fetched
```

Quem produz isso?

```text
git.fetch
```

Resultado:

```text
git.fetch
   ↓
git.fast_forward
   ↓
git.verify_sync
```

HTN planning usa justamente conhecimento hierárquico e decomposição para limitar espaços de planejamento muito grandes, em vez de considerar indiscriminadamente todas as ações possíveis. ([ScienceDirect](https://www.sciencedirect.com/topics/computer-science/hierarchical-task-network?utm_source=chatgpt.com "Hierarchical Task Network - an overview | ScienceDirect Topics"))

Mas não devemos transformar o Router num planner geral.

Coloque budgets:

```text
max_depth
max_nodes_expanded
max_candidates_per_goal
max_wall_time
max_risk
```

Se a composição não fecha dentro do orçamento:

```text
WAKE_LLM
```

O LLM descobre a nova estrutura.

Depois ela pode virar Composite Capability.

---

## 8. Quando o Hermes pode parar de pensar?

Quando passa pela **Determinism Readiness Gate**.

Não é um confidence score.

É ausência de variáveis semânticas abertas.

Formalmente:

```text
READY ⇔

intent resolved
∧ target resolved
∧ exact capabilities selected
∧ inputs bound
∧ preconditions observed
∧ all preconditions true
∧ branches have measurable predicates
∧ authority satisfied
∧ approvals satisfied
∧ effects known
∧ verifier known
∧ recovery/wait semantics known
∧ versions pinned
∧ no unresolved uncertain mutation
```

Se tudo isso for verdadeiro:

> não existe decisão semântica restante até a próxima boundary.

Execute.

Se algo faltar:

```text
condição futura → WAIT
autoridade       → HUMAN
estado observável desconhecido → deterministic probe
decisão semântica → LLM
```

---

# III. Drift, espera e eventos

## 9. Menor unidade de incerteza que acorda o LLM

Eu chamaria de:

```text
OpenCondition
```

Não é necessariamente um step inteiro.

Pode ser:

```text
mergeable == ?
```

ou:

```text
target button has disappeared
```

Quando a Capability quebra, produzimos:

```yaml
AttentionPacket:

reason: PRECONDITION_INVALIDATED

intent_ref: int_123

capability:
  id: github.merge_pull_request
  version: 3.2

completed:
  - resolve_pr
  - verify_open

confirmed_effects: []

open_condition:
  expected:
    mergeable: true
  observed:
    mergeable: false
    conflicts: true

remaining_subgraph:
  - merge
  - verify

authority:
  repository_write: allowed

state_refs:
  - artifact://...

safe_to_resume: true
```

O modelo recebe:

> “Como resolver este merge conflict?”

Não:

> “Faça o trabalho todo novamente.”

---

## 10. Como representar espera?

Eu evitaria cinco sistemas diferentes.

Criaria uma abstração:

# `AwaitCondition`

Com um `kind`.

```yaml
wait_id: wait_123

kind: EXTERNAL_STATE

predicate:
  job.status: completed

observer:
  type: runtime_event
  event_type: job.status.changed

continuation:
  workplan_id: ...
  node_id: collect_result

fence:
  task_id: ...
  run_id: ...
  operation_id: ...

created_from_state_version: 71

deadline: ...

timeout_action: WAKE_LLM

capability_snapshot:
  ...
```

Os estados visíveis podem continuar sendo:

```text
WAITING_FOR_EVENT
WAITING_FOR_TIMER
WAITING_FOR_EXTERNAL_STATE
WAITING_FOR_HUMAN
WAITING_FOR_APPROVAL
```

mas todos usam o mesmo mecanismo.

O LLM sai completamente de execução.

```text
persist await
yield worker
```

Durable workflow systems usam exatamente esse padrão: timers e sinais persistem no histórico e permitem suspender execução sem manter o worker/raciocínio ativo. ([GitHub](https://github.com/temporalio/documentation/blob/main/docs/evaluate/understanding-temporal.mdx?utm_source=chatgpt.com "documentation/docs/evaluate/understanding-temporal.mdx at main · temporalio/documentation · GitHub"))

---

## 11. O que é um Trigger confiável?

Um Trigger confiável não é texto.

É:

```text
EventPattern
+
Trusted Observer
+
Correlation
+
State Predicate
```

Um evento deveria conter:

```text
event_id
event_type
source
resource_id
resource_version / sequence
observed_at
correlation_id
evidence_ref
trust_class
causal_parent
```

São boas fontes:

```text
timer interno
filesystem watcher
process supervisor
API response
webhook autenticado
Browser runtime estruturado
Kanban transition
approval state
human control lease
```

Isto:

```text
DOM text:
"Your download finished"
```

não é autoridade.

Mas o Browser runtime pode observar estruturalmente:

```text
download.status = completed
```

e produzir uma observação.

Outra regra fundamental:

> **Evento acorda; estado confirma.**

Quando chega:

```text
DOWNLOAD_COMPLETED
```

o Hermes deve reler o estado autoritativo antes da continuação mutável.

---

## 12. Quando Trigger executa Capability ou acorda LLM?

A mesma Determinism Gate.

```text
trigger
  ↓
correlated AwaitCondition?
  ↓
re-evaluate predicate
  ↓
predicate true?
```

Então:

```text
exact deterministic continuation
→ EXECUTE

deterministic composition
→ COMPOSE

authority missing
→ ASK_HUMAN

new semantic choice
→ WAKE_LLM
```

Assim:

```text
download.completed
→ reports.archive_download
```

pode ser automático.

Mas:

```text
merge_conflict.detected
```

não tem uma única consequência universal.

Então:

```text
WAKE_LLM
```

até que o Hermes aprenda capabilities mais específicas para algumas classes de conflito.

---

## 13. Como evitar event storms e loops?

Precisamos de uma `CausalEventEnvelope`.

Cada reação carrega lineage:

```text
root_event_id
parent_event_id
trigger_id
task_id
run_id
operation_id
causal_depth
resource_version
```

E mecanismos:

```text
dedupe key
sequence/version checks
TTL
debounce
coalescing
rate limit
causal depth bound
cycle detection
circuit breaker
```

Exemplo de chave de loop:

```text
(trigger_id, capability_id, resource_id, state_fingerprint)
```

Se reaparece sem progresso:

```text
A → X → B → Y → A → X ...
```

o runtime detecta fixpoint/ciclo.

Então:

```text
CIRCUIT_BREAK
→ NEEDS_REASONING
```

Eventos obsoletos também são rejeitados por:

```text
event.resource_version <= current_version
```

---

## 14. Como garantir effectively-once?

Para sistemas externos arbitrários, **exactly-once real geralmente não pode ser prometido unilateralmente**.

O objetivo deveria ser:

# effectively-once effects

Estado:

```text
PREPARED
DISPATCHED
ACKNOWLEDGED
VERIFIED
COMMITTED
```

E uma bifurcação:

```text
DISPATCHED
    ↓
connection lost
    ↓
UNCERTAIN
```

Toda mutação recebe um:

```text
operation_id
```

que também funciona como:

```text
idempotency_key
```

se o sistema externo aceitar.

AWS, por exemplo, recomenda idempotency keys para operações repetíveis e diferencia operações seguras para at-least-once das que requerem comportamento at-most-once; nem a infraestrutura durável promete magicamente exactly-once para todo efeito externo. ([Documentação AWS](https://docs.aws.amazon.com/durable-execution/patterns/best-practices/idempotency/?utm_source=chatgpt.com "Idempotency and retries - AWS Durable Execution SDK Developer Guide"))

No Hermes:

```text
before dispatch:
persist operation intent

dispatch with operation_id

if ACK lost:
DO NOT RETRY BLINDLY

read authoritative state

already applied?
    yes → VERIFIED
    no → safe retry if permitted
    unknown → HUMAN / reconciliation
```

Isso combina perfeitamente com o uncertain-mutation contract que já estamos usando.

---

## 15. Quem possui um Trigger?

Três responsabilidades diferentes:

```text
Capability
→ declara event semantics que produz/entende

TaskRun / WorkPlan
→ possui uma AwaitCondition concreta

Persistent Automation/Scheduler
→ possui uma regra recorrente independente de um TaskRun
```

Não deixe Capability criar um segundo scheduler.

Exemplo:

```text
Capability contract:
emits process.finished
```

Mas:

```text
wait until process.finished for task 123
```

pertence ao WorkPlan/TaskRun.

E:

```text
todo dia às 8:00 faça X
```

pertence ao scheduler/automation owner existente.

O Event Plane somente transporta/normaliza eventos.

---

## 16. Como Capability declara eventos?

Eu adicionaria:

```yaml
event_contract:

  emits:
    - type: process.finished
      schema_version: 1
      correlation:
        - process_id

  observes:
    - type: process.stdout.changed

  resumes_on:
    - type: approval.granted
      predicate:
        approval.operation_id: $operation_id
```

Mas novamente:

> evento não substitui postcondition.

Capability:

```text
process.run
```

deve declarar:

```text
postcondition:
process.exit_state == exited
```

e opcionalmente:

```text
emits:
process.finished
```

O effect contract continua sendo a verdade operacional.

---

## 17. Como modelar tempo?

Eu usaria uma pequena `TemporalCondition`.

Exemplos:

```text
AT(timestamp)

NOT_BEFORE(timestamp)

DEADLINE(timestamp)

AFTER(event, duration)

UNTIL(predicate)

WITHIN(predicate, duration)

STABLE_FOR(predicate, duration)

STABLE_FOR_N_OBSERVATIONS(predicate, n)
```

Por exemplo:

> “quando X ficar verdadeiro por 30 segundos”

vira:

```text
STABLE_FOR(X, 30s)
```

Não:

```text
sleep 30
```

Timeout deve ter comportamento explícito:

```text
FAIL
ASK_HUMAN
WAKE_LLM
FALLBACK
CANCEL
```

E evento stale deve ser definido por:

```text
resource version
subscription baseline
event timestamp
correlation
```

O evento precisa representar uma mudança posterior ao baseline relevante.

Durable timers/signals são um padrão consolidado para waits que sobrevivem a crashes/restarts. ([GitHub](https://github.com/temporalio/documentation/blob/main/docs/evaluate/understanding-temporal.mdx?utm_source=chatgpt.com "documentation/docs/evaluate/understanding-temporal.mdx at main · temporalio/documentation · GitHub"))

---

## 18. Event-driven ou polling?

Regra:

> **Use eventos quando houver fonte confiável; use polling para compensar ausência ou para verificar.**

Preferência:

```text
durable webhook/signal
        >
trusted runtime event
        >
filesystem/process observer
        >
bounded polling
```

Eu usaria bastante:

```text
event + verification read
```

e, para confiabilidade:

```text
event + low-frequency reconciliation polling
```

Polling policy fica no `AwaitCondition`:

```text
initial_interval
backoff
max_interval
deadline
max_attempts
cost_budget
```

Pode usar exponential backoff.

Nada disso requer LLM.

---

# IV. Efeitos, política e autoridade

## 19. Como Capability comunica efeito ao Router?

Como delta declarativo.

Exemplo:

```yaml
preconditions:
  pr.state: open
  pr.mergeable: true

effects:
  set:
    pr.state: merged

  preserves:
    repository.default_branch: true

effect_scope:
  external: github.pull_request

verification:
  predicate:
    pr.state: merged
```

O Router pode fazer backward chaining sobre esse vocabulário limitado.

Não construa um theorem prover geral.

Limites:

```text
predicados tipados
effects explícitos
depth bounded
finite candidate set
sem arbitrary code
```

Composites aprendidas reduzem ainda mais a necessidade de busca.

---

## 20. “Posso executar” versus “devo executar”

Devem ser duas fases diferentes.

### Capability Admission

Pergunta:

> **Posso?**

Verifica:

```text
compatibility
preconditions
runtime
schema
authority minimum
```

### Execution Decision Policy

Pergunta:

> **Devo?**

Verifica:

```text
user intent
constraints
preferences
risk
approval
cost
deadline
policy
```

Portanto:

```text
technically executable
```

não implica:

```text
authorized/desirable
```

O Router deve retornar algo como:

```text
EXACT_COMPATIBLE_BUT_POLICY_BLOCKED
```

e depois:

```text
ASK_HUMAN
```

ou não executar.

---

## 21. Como propagar authority em composites?

Authority é monotônica.

Uma composição nunca pode reduzir artificialmente o nível de efeito de seus filhos.

Defina um lattice.

Por exemplo:

```text
READ
<
LOCAL_MUTATION
<
EXTERNAL_REVERSIBLE
<
EXTERNAL_IRREVERSIBLE
```

Então:

```text
required_authority(composite)
=
JOIN(required_authority(children))
```

Se:

```text
A = READ
B = EXTERNAL_MUTATION
```

então:

```text
A → B
```

é uma composição `EXTERNAL_MUTATION`.

O parent intent precisa permitir esse nível.

Approval também propaga.

Blast radius pode ser:

```text
union(resources_touched)
```

mais um fator de interação quando múltiplos sistemas são modificados.

Nenhuma composição pode realizar privilege escalation.

---

## 22. O que versionar para reproduzir uma execução?

Eu pinaria pelo menos:

```text
OperationIntent schema version
OperationIntent artifact/hash

Capability IDs + exact versions
Capability Registry snapshot/digest

Router policy version

State abstraction version

Effect taxonomy version

Trigger/Event schema version

AwaitCondition semantics version

Policy/authority snapshot

Composition graph
input bindings
```

Não é necessário congelar fisicamente toda a biblioteca.

Basta registrar tudo que influenciou aquela decisão.

O TaskRun executa o plano pinned.

Um novo TaskRun pode usar a biblioteca atualizada.

---

# V. Aprendizado e evolução do Router

## 23. Como aprender com erros do Router?

Precisamos classificar culpa.

Não existe simplesmente:

```text
execution_failed
```

Categorias:

```text
INTENT_ERROR
usuário/LLM produziu GoalContract errado

OBSERVATION_ERROR
estado semanticamente abstraído errado/stale

ROUTING_ERROR
Capability escolhida não satisfazia o intent

CAPABILITY_DRIFT
escolha estava correta; implementação/ambiente mudou

COMPOSITION_ERROR
capabilities individuais válidas, combinação inválida

POLICY_ERROR
execução tecnicamente correta mas não deveria ter sido autorizada

RUNTIME_FAILURE
infraestrutura falhou
```

Isso exige preservar o `RoutingCertificate`.

Assim uma falha de Router não reduz injustamente a reputação da Capability.

E drift real não “treina” o Router para parar de selecionar uma Capability correta.

---

## 24. Como detectar Capabilities redundantes?

Não por nome.

Calcule uma assinatura normalizada:

```text
target family
operation family
abstract preconditions
abstract effects
input schema
parameter relationships
authority/effect class
verifier family
```

Então:

```text
github.merge_pr
github.merge_pull_request
pull_request.merge
```

podem entrar no mesmo:

```text
CapabilityFamily
```

Não delete versões históricas.

Use:

```text
alias_of
superseded_by
family_id
preferred_implementation
```

Runs antigos continuam apontando para o ID original.

Para escolher a implementation preferida considere:

```text
validation
drift rate
coverage
latency
cost
risk
evidence quality
```

---

## 25. Quando generalizar versus criar nova?

Três níveis resolvem bem isso.

### Mesma Capability, nova versão

Mesmo:

```text
semantics
inputs
effects
authority
```

mas implementação melhorou.

### Mesma CapabilityFamily, implementation diferente

Exemplo:

```text
scm.pull_request.merge

├── github.pull_request.merge
└── gitlab.merge_request.merge
```

O contrato abstrato é:

```text
review_request.state → merged
```

Mas cada backend possui preconditions e implementação próprios.

### Capability totalmente nova

Quando mudam materialmente:

```text
desired effect
target semantics
authority
verification semantics
```

Não generalize GitHub/GitLab simplesmente porque os nomes parecem parecidos.

A implementação especializada precisa satisfazer o contrato abstrato sob suas preconditions.

---

## 26. O que o Operational Kernel deve esconder?

Regra:

> **Se trocar o mecanismo não altera a semântica da Capability, provavelmente pertence ao Kernel.**

Normalmente ficam abaixo:

```text
scroll até ficar visível
focus
retry transient
DOM reacquisition
stale ref recovery
wait for DOM readiness
transport/session plumbing
filesystem atomic replace
process pipe mechanics
```

Normalmente ficam como Capability:

```text
merge_pull_request
rename_file
select_account
upload_document
change_customer_email
```

Teste útil:

> Esse comportamento seria um goal independente razoável?

`scroll 400px` normalmente não.

`select_option(field, value)` talvez sim.

Outra pergunta:

> Essa operação possui pre/postcondition semanticamente interessante fora do mecanismo?

Se não, deixe no Kernel.

---

# VI. Segurança da composição

## 27. Como provar que `C1 → C2 → C3` é seguro?

Precisamos de uma **Composition Certificate** antes da execução.

Verifique:

```text
input/output type compatibility

todas preconditions possuem produtor
ou já estão verdadeiras no estado inicial

causal links válidos

ordering constraints

nenhum effect invalida precondition futura

nenhum effect conflitante

resource scopes compatíveis

authority closure permitida

approval closure satisfeita

idempotency/retry semantics compatíveis

uncertain-effect boundaries tratados

verifier coverage suficiente

risk/blast radius aceitável
```

Partial-order planning usa justamente conceitos de causal links e “threats”: uma ação pode ameaçar uma condição estabelecida para outra ação, exigindo ordering constraints. ([CMU School of Computer Science](https://www.cs.cmu.edu/afs/cs/project/jair/pub/volume20/younes03a-html/node2.html?utm_source=chatgpt.com "Basic POCL Planning Algorithm"))

Exemplo:

```text
C1:
creates temp file

C2:
deletes temp directory

C3:
reads temp file
```

Individualmente todas podem ser válidas.

Mas:

```text
C1 → C2 → C3
```

não é.

O static composition check deve detectar.

Quando não puder provar ausência de conflito:

```text
não autoexecutar
```

---

## 28. Quando uma Capability ficou generalizada demais?

Use evidência estrutural.

Sinais:

```text
branch count crescendo
preconditions enormes
branch entropy alta
drift concentrado em subcontexts
muitos conditional exceptions
baixa replay success rate
grupos de falha claramente separáveis
diferentes backends escondidos na mesma Capability
```

Nesse caso o Experience Compiler testa:

```text
1 capability complexa
vs
2 capabilities especializadas
```

Critério útil:

> Qual representação reduz melhor custo total + erros em holdout?

É uma aplicação da nossa lógica de MDL/utilidade.

Se a separação melhora:

```text
predictability
reuse
drift
simplicity
```

divida.

---

# VII. Métricas

## 29. Como medir Router quality?

Além de hit rate:

### Exact Reuse Precision

```text
verified successful exact executions
/
EXACT_EXECUTABLE decisions
```

Essa deveria ser a métrica principal para autoridade automática.

### False Exact Match Rate

```text
matches admitidos que retrospectivamente
já eram incompatíveis no momento da decisão
/
exact matches
```

Muito importante diferenciar isso de drift posterior.

### Missed Reuse Rate

```text
WAKE_LLM decisions
nas quais uma exact deterministic solution
já existia
/
all WAKE_LLM
```

### Unnecessary LLM Rate

Inclui soluções determinísticas compostas que o Router não encontrou.

### Wrong Capability Rate

```text
routing failures
/
capability selections
```

### Routing-Induced Drift

Drift causado por selection mismatch, não mudança real no ambiente.

Também:

```text
mean candidates examined
p95 candidates examined
lookup latency p50/p95
composition nodes expanded
composition depth
Router CPU
recovery cost after wrong route
coverage by target/effect family
```

Eu adicionaria:

# Router Regret

```text
actual routed cost
-
best known valid deterministic route cost
```

útil em avaliação offline.

---

## 30. Como medir Trigger Plane?

Eu usaria:

### Wakeup Precision

```text
useful wakeups
/
all wakeups
```

### Wakeup Recall

```text
conditions that required wakeup and got one
/
conditions requiring wakeup
```

### Duplicate Wakeup Rate

### Missed Wakeup Rate

### Stale Event Acceptance Rate

Ideal:

```text
≈ 0
```

### Event-to-Resume Latency

```text
predicate becomes true
→ continuation resumes
```

### Polling Cost

```text
polls
API calls
CPU
network
per completed wait
```

### Event Loss Recovery Rate

Quantos waits foram corretamente retomados via reconciliation apesar de o evento ter sido perdido.

### LLM Waiting Waste

Idealmente:

```text
0
```

porque o modelo não deveria estar ativo durante wait.

### Trigger Loop / Circuit Break Rate

Se alto, a modelagem de eventos está errada.

---

# VIII. Objetivo global

## 31. Qual deve ser a função objetivo?

Sua formulação está certa, com uma correção importante:

> **Safety, authority e correctness não devem ser simples penalidades econômicas. Devem ser constraints rígidas.**

Então:

```text
minimize

Expected Lifetime Cost
----------------------
Verified Outcomes
```

onde:

```text
Lifetime Cost =
reasoning
+ routing
+ retrieval
+ compiler
+ validation
+ monitoring
+ execution
+ storage
+ drift recovery
+ maintenance
+ human intervention
```

sujeito a:

```text
Safety invariants        = satisfied
Authority invariants     = satisfied
Correctness threshold    = satisfied
Evidence requirements    = satisfied
Latency SLO              = satisfied
```

Depois podemos otimizar:

```text
tokens
latency
CPU
tool calls
human effort
```

Nunca o contrário.

Eu chamaria a métrica principal:

# `Verified Outcome Lifetime Cost — VOLC`

E manteria:

```text
Operational Novelty Rate
Reasoning Amortization Ratio
Break-even reuse count
```

como métricas auxiliares.

---

## 32. Como saber se criamos algo pior que um agente LLM tradicional?

Precisamos manter um **Adaptive Baseline** permanentemente.

Benchmark:

```text
A. LLM-first adaptive Hermes

B. Compiler + Router + Trigger Hermes
```

sobre:

```text
novel tasks
repeated tasks
cross-session tasks
drift tasks
long waits
failures/restarts
```

Nossa arquitetura está falhando se, após a janela prevista de amortização:

```text
VOLC(Hermes) >= VOLC(Baseline)
```

sem melhoria compensatória de:

```text
correctness
reliability
auditability
latency
```

Outros sintomas de falha:

```text
Dead Capability Rate crescendo

capability count cresce muito mais
que cross-task reuse

Operational Novelty Rate não cai

Router lookup/planning fica caro

Missed Reuse Rate alto

False Exact Match não é desprezível
em mutações

Trigger Wakeup Precision baixa

polling cost excessivo

drift aumenta com reuse

manutenção de capabilities consome
mais que raciocínio economizado

LLM continua sendo acordado
para operações conhecidas
```

O mais importante é possuir **kill switches** por camada:

```text
disable auto-learning
disable automatic composition
disable mutating Router
disable Trigger auto-execution
fallback to adaptive LLM
```

Sem apagar a infraestrutura.

---

# A arquitetura consolidada

Depois de responder às 33 perguntas, eu definiria formalmente o Control Plane assim:

```text
                   TRUSTED INTENT SOURCE
                           │
                           ▼
                    OperationIntent
                           │
                ┌──────────┴──────────┐
                │                     │
         Semantic State        Authority/Policy
                │                     │
                └──────────┬──────────┘
                           ▼
                   Capability Router
                           │
           ┌───────────────┼─────────────────┐
           │               │                 │
       SATISFIED       deterministic       open gap
                           │                 │
                   ┌───────┴───────┐      classify
                   │               │          │
               EXECUTE          COMPOSE       ├─ temporal → WAIT
                   │               │          ├─ authority → HUMAN
                   └───────┬───────┘          └─ semantic → LLM
                           │
                           ▼
                   Operational Kernel
                           │
                         verify
                           │
              ┌────────────┴─────────────┐
              │                          │
           success                     drift
              │                          │
              ▼                          ▼
      Experience Compiler         Attention Packet
              │                          │
              ▼                          ▼
       Capability Library               LLM
              │
              └──────────→ Router ←─────┘


WAIT
 │
 ▼
AwaitCondition
 │
 Event / Timer / Poll / Human / Approval
 │
 ▼
predicate verified
 │
 ▼
resume exact continuation
```

Há cinco abstrações que eu trataria como **canônicas daqui para frente**:

|Abstração|Pergunta que responde|
|---|---|
|`OperationIntent`|**O que deve se tornar verdadeiro?**|
|`Capability`|**Como sabemos produzir essa transformação?**|
|`CapabilityRouter`|**O que já sabemos usar nesta situação?**|
|`AwaitCondition`|**O que precisa acontecer antes de continuarmos?**|
|`AttentionPacket`|**Qual é exatamente a parte que ainda precisa de inteligência?**|

E isso produz uma definição muito precisa para o papel final do LLM:

> **O LLM é invocado somente quando o conjunto atual de OperationIntent + State + Capability Library deixa pelo menos uma variável de decisão semântica aberta que não pode ser resolvida por observação, política, espera, composição determinística ou intervenção humana.**

Esse é, a meu ver, o critério que transforma toda a arquitetura que estamos criando em um sistema coerente, em vez de uma coleção de automações sofisticadas.

Sim. Eu definiria isso como um **sistema de prova de executabilidade**. O Router não “escolhe uma Capability porque parece adequada”; ele só pode emitir `EXECUTE` ou `COMPOSE` quando consegue construir um certificado verificável de que:

```text
1. a transformação produz o objetivo;
2. não produz efeitos fora do objetivo/constraints;
3. o estado atual satisfaz as preconditions;
4. a autoridade disponível cobre todos os efeitos;
5. as invariantes são preservadas;
6. a execução pode ser verificada depois.
```

Isso se aproxima diretamente da lógica de Hoare: `{P} C {Q}` significa que, partindo de um estado que satisfaz `P`, se `C` terminar, seu estado final satisfaz `Q`. ([Cambridge University](https://www.cl.cam.ac.uk/archive/mjcg/HL/Lectures/Lectures.a4.trimmed.numbered.pdf?utm_source=chatgpt.com "Hoare Logic")) Para Hermes, precisamos estender isso com **authority + effect footprint + evidence + uncertainty**.

## 1. O objeto fundamental: `OperationIntent`

Eu o definiria formalmente como:

```text
I = ⟨ id, mode, target, G, Inv, B, AuthRef, Acc, Lin, v ⟩
```

Onde:

```text
target
    recurso ou família de recursos sobre os quais o objetivo vale

G = Goal
    fórmula que deve ser verdadeira no estado final

Inv = Invariants
    propriedades que devem permanecer verdadeiras durante/depois da transformação

B = Effect Budget
    conjunto máximo de efeitos semanticamente autorizados por essa intenção

AuthRef
    referência a autoridade confiável, nunca autoridade inventada pelo LLM

Acc = Acceptance Contract
    como provar que G foi atingido

Lin = Lineage
    task_id / run_id / parent intent / operation lineage

v
    schema version
```

Exemplo:

```yaml
intent_id: int_42
schema_version: "1"

mode: ACHIEVE

target:
  family: github.pull_request
  identity:
    repo: kevyn/hermes
    number: 123

goal:
  eq:
    path: target.state
    value: merged

invariants:
  - eq:
      path: repository.default_branch
      value_from_initial_state: true

effect_budget:
  allow:
    - github.pull_request.merge:
        resource: target

  forbid:
    - github.repository.delete
    - github.branch.delete

authority_ref:
  envelope_id: env_779

acceptance:
  minimum_evidence: E2
  predicate:
    eq:
      path: target.state
      value: merged

lineage:
  task_id: task_9
  run_id: 17
```

O detalhe mais importante é o `EffectBudget`.

Só dizer:

```text
goal = PR merged
```

não basta.

Porque uma Capability que:

```text
merge PR
+
delete repository
```

também satisfaria logicamente:

```text
PR.state == merged
```

Precisamos provar simultaneamente:

```text
Goal covered
AND
Effects contained
```

---

# 2. Intent e Authority são duas chaves independentes

Essa distinção deveria ser uma das invariantes centrais.

Imagine que o usuário tenha tecnicamente permissão para:

```text
merge PR
delete branch
delete repo
```

mas pediu somente:

```text
merge PR
```

Então:

```text
Authority(delete_repo) = true
```

não significa:

```text
IntentCovers(delete_repo) = true
```

Execução exige:

```text
INTENT ALLOWS
       ∧
AUTHORITY ALLOWS
```

Nunca `OR`.

Isso é compatível com modelos de autorização baseados em atributos: a decisão de autorização pode depender de atributos do sujeito, objeto, operação e ambiente avaliados contra uma policy. ([NIST Segurança da Informação](https://csrc.nist.gov/pubs/sp/800/205/final?utm_source=chatgpt.com "SP 800-205, Attribute Considerations for Access Control Systems | CSRC"))

No Hermes:

```text
CanExecute(effect e) =
    e ∈ Intent.effect_budget
    ∧
    PolicyAllows(
        authority_ref,
        target,
        e,
        current_environment
    )
```

Essa regra bloqueia tanto:

```text
ação desejada mas não autorizada
```

quanto:

```text
ação autorizada mas não desejada
```

---

# 3. A Capability também precisa ser um contrato formal

Definiria:

```text
C = ⟨ id, version, T, Inputs, P, R, F, Areq, Q, V ⟩
```

Onde:

```text
T
target family

Inputs
inputs tipados

P
preconditions

R
transition relation / deterministic implementation

F
effect footprint

Areq
authority requirement

Q
postconditions

V
verifier/evidence contract
```

Exemplo:

```yaml
capability: github.pull_request.merge
version: 3.2.0

target_family:
  github.pull_request

preconditions:
  - target.state == open
  - target.mergeable == true

effects:
  - set:
      target.state: merged

effect_footprint:
  - github.pull_request.merge:
      resource: $target

authority_required:
  github.pull_request.write: $target.repo

postconditions:
  - target.state == merged

verification:
  minimum_evidence: E2
  verifier: github.pull_request.readback
```

Repare que a Capability não diz:

> “essa operação é permitida”.

Ela apenas declara:

> “essa operação faz isso e exige esta autoridade”.

O Router é quem prova se isso é admissível **nesta intenção específica**.

---

# 4. A fórmula fundamental do Router

Para uma Capability `C`, Intent `I` e estado atual `S`, eu definiria:

```text
Executable(I, C, S) :=
    TargetMatch(I, C)
 ∧  InputsBound(I, C, S)
 ∧  PreconditionsHold(C, S)
 ∧  GoalCovered(I, C)
 ∧  EffectsCovered(I, C)
 ∧  InvariantsPreserved(I, C)
 ∧  AuthoritySatisfied(I, C, S)
 ∧  PolicySatisfied(I, C, S)
 ∧  VerificationAvailable(I, C)
 ∧  StateFresh(S)
 ∧ ¬OutstandingUncertainMutation(I)
 ∧  CapabilityHealthy(C)
```

Só existe:

```text
RoutingDecision.EXECUTE
```

se **todos** forem verdadeiros.

Isso já nos dá algo testável.

---

# 5. Como provar `GoalCovered`?

Formalmente, queremos:

```text
∀ s,s'.

P_C(s)
∧
Transition_C(s,s')

⇒

G_I(s')
```

Ou, em linguagem de Hoare:

```text
{ P_C } C { G_I }
```

Mas geralmente a Capability possui sua própria postcondition `Q_C`.

Então podemos fazer a prova modular:

```text
{P_C} C {Q_C}
```

e depois verificar:

```text
Q_C ⇒ G_I
```

Exemplo:

Capability:

```text
Q_C:
target.state == merged
AND
target.merged_at exists
```

Intent:

```text
G_I:
target.state == merged
```

Temos:

```text
Q_C ⇒ G_I
```

Logo ela cobre o objetivo.

---

# 6. Mas isso ainda não é suficiente: `EffectsCovered`

Precisamos exigir:

```text
EffectFootprint(C)
⊆
EffectBudget(I)
```

Com alguma normalização de resource scope.

Exemplo correto:

```text
Capability effects:
merge(PR123)

Intent allowed:
merge(PR123)

✓
```

Errado:

```text
Capability:
merge(PR123)
delete(branch main)

Intent:
merge(PR123)

✗
```

Mesmo que o objetivo final esteja correto.

Isso é talvez a proteção formal mais importante contra uma Capability excessivamente poderosa.

---

# 7. Invariantes também são diferentes de goal

Suponha:

```text
Goal:
main local == main remoto

Invariant:
working tree changes must be preserved
```

Uma Capability:

```text
git reset --hard origin/main
```

atinge o goal.

Mas viola a invariant.

Portanto precisamos provar:

```text
∀ s,s'.

P_C(s)
∧ Transition_C(s,s')

⇒ Inv_I(s,s')
```

Assim:

```text
goal coverage ✓
effect budget talvez ✓
invariant preservation ✗

→ INCOMPATIBLE
```

---

# 8. Authority deve formar um lattice

Eu usaria uma ordem parcial de poder.

Por exemplo:

```text
READ
  <
LOCAL_MUTATION
  <
EXTERNAL_REVERSIBLE
  <
EXTERNAL_IRREVERSIBLE
```

Mas idealmente também por resource/family.

Então:

```text
RequiredAuthority(C)
⊑
GrantedAuthority(I, S, Policy)
```

Para composites:

```text
RequiredAuthority(C1 ○ C2 ○ C3)
=
JOIN(
    RequiredAuthority(C1),
    RequiredAuthority(C2),
    RequiredAuthority(C3)
)
```

Uma composition nunca pode “lavar” autoridade.

Se um filho faz write:

```text
composite(read + write)
```

é write.

Isso é consistente com o princípio de least privilege: conceder apenas o acesso necessário ao trabalho autorizado. ([Publicações Técnicas NIST](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/800-171r3/NIST.SP.800-171r3.html?utm_source=chatgpt.com "Protecting Controlled Unclassified Information in Nonfederal Systems and Organizations"))

---

# 9. `OperationIntent` precisa ser imutável durante a execução

Depois que a linguagem natural vira:

```text
OperationIntent
```

eu faria:

```text
intent_hash = SHA256(canonical_serialization(intent))
```

Esse hash entra no TaskRun.

O Router trabalha sobre:

```text
intent_hash
```

e não mais sobre o texto original.

Se o objetivo mudar, não mutamos silenciosamente o Intent.

Geramos:

```text
IntentRevision
```

com:

```text
parent_intent_id
reason
authority_ref
new_hash
```

Isso é crucial para auditabilidade.

---

# 10. `RoutingDecision` também precisa ser um objeto formal

Algo como:

```text
D = ⟨ kind, intent_ref, state_ref, plan, cert, open, policy_v ⟩
```

Onde:

```text
kind =
    SATISFIED
    EXECUTE
    COMPOSE
    WAIT
    ASK_HUMAN
    WAKE_LLM
```

Para `EXECUTE`:

```yaml
decision_id: rd_492
kind: EXECUTE

intent:
  id: int_42
  hash: ...

state:
  ref: artifact://state/...
  version: 891

selection:
  capability_id: github.pull_request.merge
  capability_version: 3.2.0

bindings:
  target: github://repo/pr/123

certificate:
  target_match: PROVEN
  inputs_bound: PROVEN
  preconditions: PROVEN
  goal_coverage: PROVEN
  effect_containment: PROVEN
  invariant_preservation: PROVEN
  authority: PROVEN
  policy: PROVEN
  verifier_available: PROVEN
  no_uncertain_mutation: PROVEN

router_policy_version: router-1.0
```

O `RoutingDecision` é essencialmente:

> **uma decisão + a prova que autoriza essa decisão.**

---

# 11. Crie um `RoutingCertificate`

Eu faria dele uma estrutura first-class.

Formalmente:

```text
Cert(I,C,S)
```

contém evidências para cada proof obligation.

Por exemplo:

```text
GoalCoverageProof
EffectContainmentProof
InvariantProof
AuthorityProof
PreconditionProof
BindingProof
CompatibilityProof
FreshnessProof
VerificationProof
```

Nem todos precisam ser provas SMT sofisticadas.

Muitos podem ser avaliações determinísticas sobre ASTs tipadas.

Exemplo:

```text
Capability postcondition:
eq(target.state, merged)

Intent goal:
eq(target.state, merged)
```

Prova trivial por normalização AST.

Outro:

```text
Capability postcondition:
and(
  eq(target.state, merged),
  exists(target.merged_at)
)

Intent goal:
eq(target.state, merged)
```

Pode haver regra de entailment simples:

```text
A ∧ B ⇒ A
```

Não precisamos começar com theorem prover geral.

---

# 12. A linguagem lógica deve ser deliberadamente pequena

Isso é crucial.

Se permitirmos:

```python
goal=lambda state: arbitrary_python(state)
```

acabou a verificabilidade.

Eu começaria com uma pequena álgebra:

```text
TRUE
FALSE

EQ(path,value)
NEQ(path,value)

EXISTS(resource)
ABSENT(resource)

AND(...)
OR(...)
NOT(...)

IN(item,set)
SUBSET(a,b)

LT / LTE / GT / GTE

UNCHANGED(path)

TRANSITION(path, before, after)
```

E effects:

```text
SET(path,value)
CREATE(resource)
DELETE(resource)
MOVE(a,b)
CALL(operation,target)
SEND(channel,target)
```

Isso já cobre uma quantidade enorme de computer-use.

Refinement types usam exatamente a ideia de tipos enriquecidos com fórmulas lógicas para expressar pre/postconditions e gerar verification conditions. ([Microsoft](https://www.microsoft.com/en-us/research/publication/refinement-types-for-secure-implementations/?utm_source=chatgpt.com "Refinement Types for Secure Implementations - Microsoft Research"))

---

# 13. O Router deveria ser quase um typechecker

Essa analogia é muito boa.

Em vez de perguntar:

> “qual ferramenta parece adequada?”

ele pergunta:

> “este plano typechecks contra este Intent?”

Uma Capability possui um “tipo”:

```text
Capability<
    InputState,
    OutputState,
    Effects,
    Authority
>
```

Por exemplo:

```text
MergePR :
{
  state=open,
  mergeable=true,
  authority=PR_WRITE
}
→
{
  state=merged
}
effects {merge(PR)}
```

O `OperationIntent` exige:

```text
Goal:
state=merged

Allowed:
merge(PR)
```

Typecheck passa.

Uma Capability que adiciona:

```text
delete(repo)
```

falha no effect type.

Isso torna o Router muito menos parecido com IA e muito mais parecido com compilador.

---

# 14. `POSSIBLE_MATCH` nunca pode executar

Devemos separar retrieval de proof.

Pipeline:

```text
Intent
  ↓
candidate retrieval
  ↓
POSSIBLE_MATCH[]
  ↓
formal admission
  ↓
EXACT_EXECUTABLE | INCOMPATIBLE | NEEDS_REASONING
```

Embedding, similaridade textual, heuristic ranking etc. podem existir somente na primeira metade.

Nunca:

```text
cosine similarity = 0.97
→ execute
```

Similarity não participa da autorização.

---

# 15. Como provar uma composição?

Para:

```text
C1 → C2 → C3
```

precisamos de uma generalized Hoare composition.

Se:

```text
{P1} C1 {Q1}
{P2} C2 {Q2}
{P3} C3 {Q3}
```

precisamos provar:

```text
InitialState ⇒ P1

Q1 ⇒ P2

Q2 ⇒ P3

Q3 ⇒ GoalIntent
```

Além disso:

```text
Effects(C1) ∪ Effects(C2) ∪ Effects(C3)
⊆
EffectBudget(Intent)
```

e:

```text
JOIN(Auth(C1),Auth(C2),Auth(C3))
⊑
GrantedAuthority
```

e todas as invariants precisam sobreviver.

Isso produz um:

```text
CompositionCertificate
```

---

# 16. Compositions também precisam detectar threats

Por exemplo:

```text
C1:
creates file A

C2:
deletes directory containing A

C3:
reads file A
```

Temos:

```text
Q1 ⇒ P3
```

mas C2 destrói o predicado no meio.

Então devemos verificar:

```text
CausalLink:
C1 -- exists(A) --> C3
```

e detectar que:

```text
Effect(C2):
¬exists(A)
```

ameaça esse causal link.

Isso é o equivalente operacional de threat detection em planejamento.

O Router deve rejeitar ou reorder.

---

# 17. `WAIT`, `ASK_HUMAN` e `WAKE_LLM` são provas de não-executabilidade

Isso é uma consequência elegante.

`WAIT` não significa:

> “Router não soube.”

Significa:

```text
todos os passos estão resolvidos
EXCETO
predicate P ainda é false/unknown
e P possui Observer determinístico
```

Então temos:

```text
WAIT(P)
```

`ASK_HUMAN` significa:

```text
plano existe
mas Authority/Preference obligation
não pode ser satisfeita automaticamente
```

`WAKE_LLM` significa:

```text
existe OpenCondition sem
deterministic observer,
policy resolution
ou known capability plan
```

Ou seja, até as não-execuções são justificadas formalmente.

---

# 18. `OpenCondition` deve ser first-class

Por exemplo:

```yaml
open_condition:
  type: SEMANTIC_GAP

  proposition:
    strategy_for_merge_conflict: unknown

  known:
    target: PR123
    conflicts: [fileA,fileB]

  authority:
    modify_files: allowed

  unresolved_effect:
    choose_resolution_strategy: true
```

Só isso vai para o LLM.

Quando resolvido:

```text
OpenCondition
      ↓
Intent refinement / plan fragment
      ↓
Router
```

Não pula o Router.

Mesmo uma resposta do LLM precisa voltar pelo typechecker.

Essa regra é importantíssima:

> **LLM reasoning proposes; Router admission authorizes.**

---

# 19. O runtime precisa revalidar antes do side effect

Mesmo tendo RoutingCertificate:

```text
state S
→ Router proves EXECUTE
```

o mundo pode mudar:

```text
S → S'
```

antes da mutação.

Portanto:

```text
ROUTE
↓
PIN
↓
PREFLIGHT REVALIDATE
↓
DISPATCH
```

Preconditions críticas são lidas novamente imediatamente antes da ação.

Exemplo:

```text
Router:
mergeable=true

100 ms depois:
outro commit altera PR

Preflight:
mergeable=false

→ DO NOT EXECUTE
→ RoutingCertificate stale
→ reroute / NEEDS_REASONING
```

Esse é o limite entre **proof over observed model** e realidade concorrente.

---

# 20. Cada decisão precisa ter state version/freshness

O `SemanticState` deve carregar:

```text
state_ref
state_hash
observed_at
source
resource_versions
evidence_refs
```

O RoutingCertificate referencia exatamente esse estado.

Se um recurso relevante mudou:

```text
certificate invalidated
```

Não faça:

```text
decision on S1
execute on unknown S2
```

sem revalidação.

---

# 21. Um teorema útil para o Hermes

Eu escreveria a propriedade principal aproximadamente assim:

## Router Soundness

Para qualquer:

```text
Intent I
State S
Decision D
```

se:

```text
Router(I,S) = EXECUTE(C, bindings, cert)
```

então deve ser verificável deterministicamente que:

```text
Applicable(C,S)
∧
GoalCovered(I,C)
∧
Effects(C) ⊆ AllowedEffects(I)
∧
PreservesInvariants(I,C)
∧
RequiredAuthority(C) ⊑ GrantedAuthority(I,S)
∧
PolicyAllows(I,C,S)
∧
InputsFullyBound(C)
∧
Verifiable(C)
∧
NoOutstandingUncertainty(I)
```

E:

```text
¬CertificateValid
⇒
¬Dispatch
```

Essa última linha é essencial.

Não deve existir fallback do tipo:

```text
certificate failed
but it probably works
→ dispatch
```

---

# 22. Segunda propriedade: Goal Non-Expansion

Uma Capability não pode ampliar o objetivo.

Formalmente:

```text
SemanticEffects(Plan)
⊆
Closure(Intent.effect_budget)
```

Qualquer novo efeito não declarado:

```text
blocks execution
```

ou exige:

```text
IntentRevision + authority
```

Isso evita _goal drift_.

---

# 23. Terceira: Authority Non-Escalation

Para qualquer composite:

```text
AuthorityRequired(plan)
=
JOIN(authority_required(each node))
```

e:

```text
AuthorityRequired(plan)
⊑
GrantedAuthority(intent)
```

Nunca:

```text
child requires write
parent advertises read
```

---

# 24. Quarta: Deterministic Closure

`EXECUTE` só pode existir quando:

```text
OpenConditions(plan) = ∅
```

Ou todos os branches restantes são funções determinísticas de predicados observáveis.

Isso formaliza nossa `Determinism Readiness Gate`.

---

# 25. Quinta: Verification Closure

Toda mutação semanticamente relevante precisa estar coberta por um verifier apropriado.

Por exemplo:

```text
External mutation
→ E0 ACK alone insufficient
```

Se Intent exige E2:

```text
capability only supports E1
→ not executable
```

Mesmo que todo o resto esteja correto.

---

# 26. Sexta: Uncertainty Dominance

Se existe:

```text
outstanding_uncertain_mutation
```

sobre o mesmo resource/effect domain:

```text
EXECUTE prohibited
```

até reconciliation.

Isso evita “provar” novo plano sobre estado que talvez já tenha sido alterado.

---

# 27. Como testar isso de verdade?

Eu usaria **três camadas complementares**.

Primeiro, unit tests sobre as regras lógicas.

Exemplo:

```text
postcondition implies goal
→ accept

postcondition does not imply goal
→ reject

goal satisfied but extra forbidden effect
→ reject

authority missing
→ reject
```

Depois, property-based testing.

Gere automaticamente milhares de combinações de:

```text
Intent
CapabilityContract
State
Authority
Effects
```

e verifique invariantes.

A propriedade mais importante:

```python
if decision.kind in {EXECUTE, COMPOSE}:
    assert verify_certificate(decision.certificate)
```

e:

```python
if not verify_certificate(cert):
    assert dispatch_is_impossible
```

---

# 28. Mutation testing é particularmente útil

Quebre deliberadamente o Router.

Por exemplo remova:

```text
effect containment
```

O teste:

```text
merge + delete repo
```

precisa ficar vermelho.

Remova:

```text
authority check
```

teste vermelho.

Remova:

```text
invariant preservation
```

vermelho.

Isso prova que os testes realmente protegem cada obrigação.

---

# 29. Use metamorphic properties

Exemplo:

Se adicionarmos autoridade que não é necessária:

```text
decision não deve mudar
```

Se retirarmos autoridade necessária:

```text
EXECUTE → ASK_HUMAN/POLICY_BLOCKED
```

Se fortalecermos o Intent com nova invariant incompatível:

```text
EXECUTE → INCOMPATIBLE
```

Se a capability adiciona um efeito proibido:

```text
EXECUTE → INCOMPATIBLE
```

Se o state muda tornando uma precondition falsa:

```text
EXECUTE → INCOMPATIBLE/NEEDS_REASONING
```

Esses testes são extremamente fortes.

---

# 30. Differential / shadow testing

Antes de dar autoridade real:

```text
Router = SHADOW
```

Ele produz:

```text
would_execute
would_compose
would_wait
```

mas o LLM/adaptive runtime ainda executa.

Depois comparamos:

```text
RoutingCertificate
vs
resultado real
```

Medimos:

```text
false exact match
missed reuse
wrong capability
```

Só depois promovemos mutating Router.

---

# 31. E podemos usar um SMT solver?

Talvez, mas eu **não começaria por ele**.

Uma IR limitada permite que grande parte das proofs seja implementada com:

```text
normalização
set inclusion
AST implication rules
type checking
resource matching
lattice comparison
```

Exemplo:

```text
AND(A,B) ⇒ A
EQ(x,3) ⇒ EXISTS(x)
SET(x,3) satisfies EQ(x,3)
```

Se a linguagem crescer até um ponto onde entailment fique complexo, aí um SMT solver como Z3 pode gerar/validar verification conditions — exatamente o tipo de abordagem usada por sistemas com refinement types. ([Microsoft](https://www.microsoft.com/en-us/research/publication/refinement-types-for-secure-implementations/?utm_source=chatgpt.com "Refinement Types for Secure Implementations - Microsoft Research"))

Mas não transformaria Hermes num projeto de theorem proving antes de precisar.

---

# 32. O mais importante: nunca confiar no `RoutingDecision` sem certificado

Eu faria a API impossível de usar errado.

Não:

```python
decision = RoutingDecision(
    kind=EXECUTE,
    capability=cap
)
```

Mas algo como:

```python
decision = router.prove_execute(
    intent,
    state,
    capability
)
```

O único construtor público de `ExecutableDecision` exige um certificado válido.

Talvez até tipos diferentes:

```text
RoutingDecision
├── SatisfiedDecision
├── ExecutableDecision
├── ComposedDecision
├── WaitDecision
├── HumanDecision
└── ReasoningDecision
```

E somente:

```text
ExecutableDecision
ComposedDecision
```

implementam:

```text
dispatchable = true
```

Isso transforma uma regra arquitetural numa regra do tipo.

---

# 33. O dispatcher também deve recusar objetos não certificados

Mesmo que algum código tente:

```text
dispatcher.execute(capability)
```

não deveria existir essa API.

A API é:

```text
dispatcher.execute(
    ExecutableDecision
)
```

O dispatcher valida:

```text
certificate hash
intent hash
state freshness
TaskRun fence
capability version
router policy version
approval token
```

antes do side effect.

Defense in depth.

---

# 34. O modelo formal final

Eu resumiria toda a arquitetura com esta relação:

```text
S ⊨ Preconditions(C)

Post(C) ⇒ Goal(I)

Effects(C) ⊆ EffectBudget(I)

Transition(C) ⊨ Invariants(I)

Authority(C) ⊑ AuthorityGranted(I)

Policy(I,S,C) = PERMIT

Verification(C) ≥ Acceptance(I)

OpenConditions(C,I,S) = ∅

Uncertainty(I,S) = ∅
```

Somente então:

```text
⊢ EXECUTE(I,C,S)
```

Para composition `P`:

```text
⊢ COMPOSE(I,P,S)
```

somente se as mesmas propriedades forem verdadeiras para o **plano inteiro**, não apenas para cada Capability isoladamente.

Esse símbolo `⊢` é exatamente a mentalidade que eu adotaria:

> **o Router não escolhe. O Router deriva uma decisão.**

---

## A consequência arquitetural

Isso nos dá uma separação muito forte:

```text
LLM
→ propõe significado / resolve novidade

Experience Compiler
→ aprende transformações

Capability Library
→ conhece transformações

Router
→ prova aplicabilidade

Policy
→ prova autoridade

Operational Kernel
→ executa

Verifier
→ prova resultado
```

E nenhuma dessas camadas sozinha pode autorizar uma transformação.

A regra máxima pode ser escrita assim:

> **Nenhuma Capability é executável porque “parece correta”. Ela é executável somente quando existe um certificado reproduzível demonstrando que seus efeitos são necessários ou permitidos pelo `OperationIntent`, estão dentro da autoridade concedida, são aplicáveis ao estado observado, preservam as invariantes e possuem uma condição verificável de sucesso.**

Isso é, a meu ver, o ponto em que o Capability Router deixa de ser uma heurística de IA e começa a parecer um **compilador/typechecker operacional**. E essa é exatamente a direção certa para o Hermes.