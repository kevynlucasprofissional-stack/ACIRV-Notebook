# CONTEXTO UNIFICADO — SUDOEXPO MATCH
## Guia de leitura, interpretação e análise da base completa

**Arquivo-fonte principal:** `sudoexpo-match-base-completa.json`  
**Objetivo deste documento:** permitir que qualquer IA, analista ou agente leia e interprete corretamente os dados do SudoExpo Match sem precisar reconstruir todo o contexto histórico e sem tirar conclusões que a base não sustenta.

---

# 1. FINALIDADE DA ANÁLISE

O objetivo é analisar quantitativamente o desempenho do **SudoExpo Match**, especialmente nos seguintes contextos:

1. **Café Entre Amigos — 27/08/2026**
2. **SudoExpo 2026 — 09/09/2026 a 12/09/2026**
3. Período posterior, quando necessário para observar continuidade de uso, decisões ou conexões.

A análise deverá permitir responder, entre outras, às perguntas:

- Quantas pessoas se cadastraram?
- Quantos matches foram gerados?
- Quantas pessoas visualizaram ou avaliaram matches?
- Quantos interesses foram registrados?
- Quantos interesses mútuos ocorreram?
- Quantas conexões foram criadas?
- Quantas conexões chegaram a estágios mais avançados?
- Qual a relação entre o score do Matchmaker e a aceitação humana?
- Existem padrões comportamentais diferentes entre usuários?
- Usuários mais seletivos tendem a aceitar matches de maior compatibilidade?
- Qual foi o funil real de conversão do produto?
- Onde o produto funcionou bem?
- Onde houve perda de usuários ou baixa conversão?

---

# 2. O QUE EXISTE NA BASE

A exportação é ampla e contém, entre outras informações:

- perfis de participantes;
- empresas e segmentos;
- necessidades e ofertas;
- matches gerados;
- score de compatibilidade para cada lado do match;
- razões e pesos utilizados pelo Matchmaker;
- decisões dos usuários;
- interesses;
- rejeições / `agora_nao`;
- conexões;
- mudanças de status de conexões;
- eventos relacionados às conexões;
- conexões registradas offline;
- telemetria;
- eventos de onboarding e uso;
- dados temporais;
- versões do algoritmo;
- informações auxiliares utilizadas pelo sistema.

Na auditoria preliminar, a base apresentou aproximadamente:

- **33 tabelas**
- **32.779 registros**
- **133 perfis**
- **2.630 matches**
- **563 decisões**
- **389 conexões**
- **919 eventos de conexão**
- **469 mudanças de status**
- **11 conexões offline**
- **7.493 eventos de telemetria**
- **16.703 registros relacionados às explicações/razões dos scores**

Esses números devem ser recalculados diretamente do JSON antes de qualquer apresentação final, pois este documento serve como contexto e não substitui a análise programática da fonte.

---

# 3. ALERTA DE PRIVACIDADE / LGPD

O arquivo contém dados pessoais reais e conteúdo bruto coletado de fontes associadas aos participantes.

**Regra obrigatória:**
- não expor telefone;
- não expor dados pessoais desnecessários;
- não projetar nomes individuais em apresentação pública;
- não publicar conteúdo bruto individual sem necessidade;
- preferir métricas agregadas ou dados anonimizados.

Em apresentações para diretoria/comitê, usar participantes individuais apenas quando houver finalidade legítima e contexto adequado. Para análises gerais, trabalhar com IDs anonimizados.

---

# 4. REGRA FUNDAMENTAL SOBRE EVENTOS

## 4.1. Problema de modelagem histórica

O arquivo se declara como contendo dados de:

- `sudoexpo-2026`
- `cafe-entre-amigos-ago-2026`

Porém, na prática, o **Café Entre Amigos não foi corretamente cadastrado como evento separado no sistema**.

Os registros de perfis, matches e conexões acabaram sendo associados ao evento principal do SudoExpo Match.

Portanto:

> **NÃO usar apenas `event_id` para separar Café Entre Amigos e SudoExpo.**

---

# 5. COMO IDENTIFICAR O CAFÉ ENTRE AMIGOS

O Café Entre Amigos ocorreu em:

**27 de agosto de 2026**

Regra operacional definida pelo responsável pelo projeto:

> **Perfis criados em 27/08/2026 devem ser considerados cadastros originados no Café Entre Amigos.**

Essa regra é uma reconstrução histórica baseada na data.

## 5.1. Cuidados

Ao executar a análise:

- usar o timestamp real de criação do perfil;
- normalizar timezone antes de classificar datas;
- considerar o fuso local de Rio Verde/GO (Brasil);
- verificar se timestamps estão em UTC antes de converter;
- deixar documentada a regra de classificação.

Sugestão de campo derivado:

```text
origem_estimada =
    "Cafe Entre Amigos"  se data_local_criacao == 2026-08-27
    "SudoExpo"           se data_local_criacao entre 2026-09-09 e 2026-09-12
    "Outro periodo"      nos demais casos
```

A palavra **"estimada"** é importante porque o Café não possui event_id confiável.

---

# 6. DATAS CORRETAS DA SUDOEXPO 2026

A tabela de eventos possui datas antigas, erradas ou obsoletas.

**Não utilizar as datas registradas em `public.events` para definir a janela real da feira.**

As datas reais devem ser consideradas:

**09/09/2026 a 12/09/2026**

Portanto, para análises temporais do evento:

```text
SudoExpo 2026:
2026-09-09 00:00:00
até
2026-09-12 23:59:59
```

Sempre converter timestamps para o horário local antes da classificação.

---

# 7. META ORIGINAL DE CADASTROS

A meta estabelecida para o SudoExpo Match foi:

## **300 cadastros**

Segundo o briefing do responsável pelo projeto, essa meta implicava aproximadamente:

## **1 cadastro a cada 5 minutos**

Essa meta é externa ao banco de dados.

Portanto:

- o **resultado real** deve ser calculado pela base;
- a **meta de 300** deve ser tratada como contexto fornecido;
- não procurar essa meta obrigatoriamente dentro das tabelas;
- não concluir que o sistema possuía capacidade operacional para atingir a meta apenas porque ela foi definida.

Uma comparação útil para apresentação é:

```text
META FORMAL
300 cadastros

vs.

RESULTADO REAL
[calcular da base]

vs.

CAPACIDADE / SISTEMA DISPONÍVEL
avaliar qualitativamente
```

Evitar transformar essa comparação automaticamente em avaliação de desempenho individual.

---

# 8. AQUISIÇÃO PRESENCIAL DE USUÁRIOS

Durante a SudoExpo, houve trabalho ativo de aquisição presencial:

- visita a estandes;
- abordagem direta;
- convite para cadastro no SudoExpo Match.

Estimativa pessoal do responsável:

## **aproximadamente 30 pessoas aceitaram se cadastrar após abordagem direta.**

Porém:

> **A base não permite provar causalmente que determinado cadastro aconteceu por causa dessa abordagem.**

Portanto:

### Pode ser dito:
- houve abordagem presencial;
- aproximadamente 30 pessoas aceitaram se cadastrar nesse contexto, segundo relato do responsável;
- existe crescimento de cadastros durante a feira que pode ser medido pela base.

### Não pode ser dito como fato derivado do banco:
- "30 usuários do banco vieram comprovadamente da abordagem";
- "X% dos cadastros ocorreram porque o responsável visitou os estandes".

Se necessário, apresentar isso como **estimativa operacional / relato**, não como telemetria.

---

# 9. SCORE DO MATCHMAKER

## 9.1. Não usar escala 0–10

O Matchmaker real utiliza scores que podem ultrapassar 100 pontos.

Portanto, qualquer referência anterior a "score 8 ou mais" era apenas uma simplificação verbal para representar **alta compatibilidade**.

Ela não representa a escala real atual.

## 9.2. Regra definida para esta análise

Para fins analíticos e de apresentação:

## **Alta compatibilidade = score >= 80 pontos**

Usar essa definição como corte operacional inicial.

Exemplo:

```text
Baixa / média compatibilidade: score < 80
Alta compatibilidade: score >= 80
```

Não transformar essa classificação em verdade ontológica do algoritmo. É um **threshold analítico escolhido para facilitar a leitura**.

Sempre que possível, também analisar a distribuição contínua do score em vez de depender somente do corte de 80.

---

# 10. SCORE É DIRECIONAL

Um match pode possuir score diferente para cada participante.

Exemplo conceitual:

```text
Pessoa A -> Pessoa B = score_for_a
Pessoa B -> Pessoa A = score_for_b
```

Logo:

> **Nunca presumir que um match possui um único score simétrico.**

Ao analisar se uma pessoa demonstrou interesse em determinada conexão, utilizar o score correspondente **à perspectiva daquela pessoa**.

Se o participante que tomou a decisão foi A:

```text
usar score_for_a
```

Se foi B:

```text
usar score_for_b
```

Isso é especialmente importante para testar a relação:

```text
compatibilidade prevista pelo Matchmaker
        ↓
decisão humana real
```

---

# 11. HIPÓTESE "PERMISSIVOS × SELETIVOS"

Existe uma hipótese observacional levantada durante o uso do sistema:

### Usuário permissivo
Tende a marcar interesse em grande parte ou quase todos os matches apresentados.

### Usuário seletivo
Analisa cada oportunidade e demonstra interesse apenas em uma parcela dos matches.

Essa classificação **não deve ser assumida previamente como verdadeira**.

A IA deve testar a hipótese quantitativamente.

---

# 12. COMO DEFINIR PERMISSIVIDADE

Construir, para cada usuário:

```text
matches_avaliados
interesses
agora_nao
taxa_interesse = interesses / matches_avaliados
```

Explorar a distribuição real da `taxa_interesse`.

Não definir arbitrariamente o corte antes de observar os dados.

Sugestões possíveis após análise exploratória:

- clusterização;
- quartis;
- distribuição bimodal;
- thresholds baseados em comportamento observado.

Exemplo apenas ilustrativo:

```text
permissivo: taxa_interesse >= 80%
seletivo: taxa_interesse < 80%
```

Esse corte NÃO é obrigatório.

A classificação final deve ser guiada pela distribuição observada.

---

# 13. HIPÓTESE PRINCIPAL A TESTAR

Hipótese:

> Mesmo usuários seletivos tendem a aceitar matches de alta compatibilidade calculados pelo Matchmaker.

Definição operacional inicial:

```text
alta compatibilidade = score >= 80
```

Teste recomendado:

Para cada decisão de usuário:

1. identificar o match;
2. identificar quem tomou a decisão;
3. selecionar o score correspondente ao lado daquela pessoa;
4. classificar o usuário segundo comportamento;
5. verificar se marcou `interesse` ou `agora_nao`;
6. calcular taxa de aceitação por faixa de score.

Exemplo:

```text
Score 0–39
Score 40–59
Score 60–79
Score 80–99
Score 100+
```

Depois comparar:

```text
Todos os usuários
vs.
Usuários permissivos
vs.
Usuários seletivos
```

Essa análise é mais robusta do que afirmar previamente que "100% aceitaram score alto".

---

# 14. NÃO CONFUNDIR MATCH, INTERESSE E CONEXÃO

Esses conceitos precisam permanecer separados.

## Match
O sistema identificou uma oportunidade potencial entre dois participantes.

## Decisão
Um participante avaliou a oportunidade.

Possíveis estados incluem, por exemplo:

- `interesse`
- `agora_nao`

## Interesse unilateral
Uma das partes demonstrou interesse.

## Interesse mútuo
As duas partes demonstraram interesse, quando aplicável à lógica do sistema.

## Conexão
O sistema criou/registrou uma conexão entre participantes.

## Conexão concluída
A conexão atingiu determinado estado operacional considerado concluído pelo sistema.

---

# 15. CONEXÃO CONCLUÍDA NÃO SIGNIFICA NEGÓCIO FECHADO

Regra crítica:

> **Nunca interpretar automaticamente uma conexão concluída como venda, contrato, parceria ou negócio efetivamente fechado.**

O banco consegue medir principalmente:

- criação da oportunidade;
- interesse;
- conexão;
- apresentação;
- liberação/troca de contato;
- progressão de status;
- conclusão operacional.

Para medir impacto econômico real seria necessário um **follow-up posterior** com os participantes.

Exemplos de perguntas para follow-up:

- Vocês chegaram a conversar depois da conexão?
- Houve reunião?
- Houve proposta?
- Houve contratação?
- Houve venda?
- Houve parceria?
- Qual valor aproximado foi movimentado?
- A conexão teria acontecido sem o SudoExpo Match?

Somente com esse acompanhamento seria possível estimar ROI comercial ou negócios gerados.

---

# 16. FUNIL RECOMENDADO

Construir um funil sempre que os dados permitirem:

```text
PERFIS CADASTRADOS
        ↓
MATCHES GERADOS
        ↓
MATCHES VISUALIZADOS
        ↓
MATCHES AVALIADOS
        ↓
INTERESSES
        ↓
INTERESSES MÚTUOS
        ↓
CONEXÕES
        ↓
CONTATOS LIBERADOS / TROCADOS
        ↓
CONEXÕES CONCLUÍDAS
```

Não forçar uma etapa caso o banco não sustente tecnicamente aquela transição.

Calcular:

- volume absoluto;
- taxa de conversão entre etapas;
- taxa acumulada desde cadastro;
- perdas entre etapas.

---

# 17. ANÁLISES TEMPORAIS RECOMENDADAS

Criar séries por:

- dia;
- hora;
- evento estimado;
- antes / durante / depois da SudoExpo.

Janelas principais:

### Café Entre Amigos
**27/08/2026**

### SudoExpo
**09/09/2026–12/09/2026**

Análises úteis:

- cadastros por hora;
- decisões por hora;
- interesses por hora;
- conexões por hora;
- momento de maior atividade;
- distância temporal entre cadastro e primeira ação;
- distância entre match e decisão;
- distância entre interesse e conexão.

---

# 18. ANÁLISES POR USUÁRIO

Para cada participante, quando tecnicamente possível, calcular:

```text
data de cadastro
matches recebidos
matches visualizados
matches avaliados
interesses
agora_nao
taxa de interesse
score médio dos matches recebidos
score médio aceito
score médio rejeitado
conexões
conexões concluídas
tempo até primeira interação
tempo até primeira conexão
```

Não expor nomes no relatório executivo.

---

# 19. ANÁLISE DO MATCHMAKER

Objetivo central:

> verificar se scores maiores estão associados a maior probabilidade de interesse humano.

Análises recomendadas:

### 19.1. Taxa de interesse por faixa de score

### 19.2. Score médio:
- aceitos;
- rejeitados.

### 19.3. Distribuição dos scores:
- todos;
- aceitos;
- rejeitados.

### 19.4. Usuários seletivos
Repetir as análises apenas para usuários classificados como seletivos.

### 19.5. Correlação / modelo
Se houver volume suficiente:
- regressão logística;
- curva de probabilidade de interesse por score;
- AUC/ROC, se fizer sentido;
- calibration curve, se o score puder ser interpretado probabilisticamente.

Não chamar o score de "probabilidade" sem confirmar que o algoritmo foi desenhado para isso.

---

# 20. VERSÕES DO ALGORITMO

A base possui informação de versão do Matchmaker.

Sempre verificar se houve mais de uma versão ativa no período analisado.

Se houver mudança de algoritmo:

- separar análises por versão;
- verificar se scores são comparáveis;
- evitar misturar distribuições diferentes sem normalização.

---

# 21. CAFÉ ENTRE AMIGOS × SUDOEXPO

A comparação é desejável, mas deve respeitar as limitações da origem estimada.

Comparar, quando possível:

```text
Cadastros
Matches
Decisões
Taxa de interesse
Conexões
Conversão
Score médio
Tempo até interação
```

Identificar os participantes do Café principalmente pela data de cadastro de **27/08/2026**.

Se um participante criado no Café continuou usando o sistema durante a SudoExpo:

- manter `origem_estimada = Café Entre Amigos`;
- analisar suas ações posteriores normalmente;
- não reclassificar o cadastro como SudoExpo.

Assim é possível distinguir:

```text
origem do usuário
vs.
momento da ação
```

---

# 22. PESQUISA DE SATISFAÇÃO É UMA FONTE SEPARADA

A pesquisa de satisfação **não está contemplada como substituto pelo JSON**.

Ela deverá ser analisada separadamente e depois cruzada com os resultados operacionais quando possível.

Não tentar inferir satisfação subjetiva apenas a partir da telemetria.

A pesquisa poderá responder questões que o banco não responde, como:

- percepção de utilidade;
- facilidade de uso;
- conhecimento ou desconhecimento do aplicativo;
- satisfação;
- confiança;
- intenção de reutilizar;
- percepção da qualidade das conexões.

---

# 23. OBSERVAÇÃO SOBRE NOTAS BAIXAS NA PESQUISA

Existe uma hipótese contextual importante:

Algumas avaliações de 1 estrela podem ter sido dadas por pessoas que **não conheceram ou não utilizaram o SudoExpo Match na feira**.

Essa hipótese deverá ser testada diretamente nas respostas da pesquisa antes de ser apresentada como fato.

Ideal:

```text
usuários que conheciam/utilizaram
vs.
usuários que não conheciam/não utilizaram
```

Comparar avaliações entre os grupos.

---

# 24. O QUE PODE SER AFIRMADO COM A BASE

A base pode sustentar, quando calculado corretamente:

- quantidade de cadastros;
- momento dos cadastros;
- quantidade de matches;
- distribuição de scores;
- decisões;
- interesses;
- rejeições;
- conexões;
- status das conexões;
- interações;
- telemetria;
- comportamento agregado;
- diferenças comportamentais;
- relação entre score e decisão;
- funil de uso;
- evolução temporal.

---

# 25. O QUE NÃO DEVE SER INFERIDO SEM EVIDÊNCIA EXTERNA

Não afirmar apenas a partir da base:

- quantidade de vendas geradas;
- receita gerada;
- contratos fechados;
- parcerias efetivamente consolidadas;
- ROI financeiro;
- que uma conexão foi "um negócio";
- que determinada pessoa se cadastrou por causa de uma abordagem específica;
- que usuários gostaram do sistema apenas porque interagiram;
- que nota baixa da pesquisa significa rejeição ao produto sem verificar se a pessoa o conhecia;
- que meta de 300 representa capacidade real do sistema.

---

# 26. HIERARQUIA DE EVIDÊNCIAS

Ao produzir relatório, utilizar esta ordem:

## Nível A — Fato do banco
Informação diretamente observável no JSON.

Exemplo:
> 133 perfis constam na exportação.

## Nível B — Métrica derivada
Resultado calculado sobre registros do banco.

Exemplo:
> X% dos usuários avaliadores demonstraram interesse em pelo menos metade dos matches.

## Nível C — Regra contextual fornecida
Informação fornecida pelo responsável pelo projeto.

Exemplo:
> A meta formal era de 300 cadastros.

## Nível D — Hipótese
Interpretação que precisa ser testada.

Exemplo:
> Usuários seletivos aceitam proporcionalmente mais matches com score >=80.

## Nível E — Inferência não suportada
Não apresentar como fato.

Exemplo:
> Cada conexão concluída gerou um negócio.

---

# 27. TERMINOLOGIA RECOMENDADA NA APRESENTAÇÃO

Preferir:

- "o sistema registrou";
- "a base indica";
- "a análise encontrou";
- "houve associação entre";
- "o Matchmaker atribuiu";
- "o usuário demonstrou interesse";
- "a conexão foi registrada";
- "a conexão atingiu o status X";
- "origem estimada pelo dia de cadastro".

Evitar:

- "o algoritmo provou";
- "o aplicativo gerou vendas";
- "o usuário comprou";
- "o match virou negócio";
- "100% garantido";
- "a IA acertou";
- "essa pessoa veio por causa da abordagem" sem evidência.

---

# 28. MÉTRICAS PRIORITÁRIAS PARA A APRESENTAÇÃO

Prioridade 1:

1. Total de perfis cadastrados.
2. Meta: 300 cadastros.
3. Cadastros durante a SudoExpo.
4. Cadastros estimados do Café Entre Amigos.
5. Matches gerados.
6. Usuários que realmente avaliaram matches.
7. Interesses registrados.
8. Interesses mútuos.
9. Conexões registradas.
10. Conexões concluídas / estágio equivalente.
11. Taxa de interesse por faixa de score.
12. Taxa de aceitação de score >=80.
13. Resultado específico entre usuários seletivos.
14. Funil completo.

Prioridade 2:

15. Distribuição de scores.
16. Score médio aceito × rejeitado.
17. Usuários mais ativos.
18. Conversão por evento/período.
19. Tempo até primeira decisão.
20. Tempo até conexão.
21. Segmentos com mais atividade.
22. Necessidades/ofertas mais frequentes.

---

# 29. STORYTELLING RECOMENDADO

A análise do SudoExpo Match deve responder a quatro perguntas:

## 1. Conseguimos colocar pessoas dentro do sistema?
Mostrar cadastros e aquisição.

## 2. O sistema conseguiu gerar oportunidades?
Mostrar volume e distribuição dos matches.

## 3. As pessoas consideraram essas oportunidades relevantes?
Mostrar decisões, interesse e relação com score.

## 4. As oportunidades viraram conexões?
Mostrar funil de conexão.

Depois:

## 5. O que ainda não sabemos?
Negócios efetivamente fechados e impacto econômico.

Conclusão correta:

> O SudoExpo Match pode ser avaliado com alta precisão até a etapa de conexão. O efeito comercial posterior exige follow-up.

---

# 30. REGRAS FINAIS PARA A PRÓXIMA IA

Ao receber este documento junto do JSON:

1. **Leia o JSON diretamente.**
2. **Recalcule todos os números.**
3. Não confie cegamente nos números escritos neste contexto se houver divergência com a fonte.
4. Ignore as datas obsoletas da tabela de eventos para definir a SudoExpo.
5. Use **09–12/09/2026** como janela real da feira.
6. Classifique perfis criados em **27/08/2026** como origem estimada `Café Entre Amigos`.
7. Use **score >=80** como definição operacional inicial de alta compatibilidade.
8. Lembre que score é **direcional**, podendo existir `score_for_a` e `score_for_b`.
9. Relacione a decisão do usuário ao score do lado correto.
10. Não assuma a hipótese permissivo/seletivo: **teste-a**.
11. Não interprete conexão concluída como negócio fechado.
12. A meta formal é **300 cadastros**.
13. A estimativa de aproximadamente **30 pessoas cadastradas após abordagem presencial** é relato contextual, não causalidade comprovada pelo banco.
14. Trate a pesquisa de satisfação como fonte separada.
15. Preserve LGPD e anonimização.
16. Diferencie claramente fato, métrica derivada, contexto e hipótese.
17. Sempre que possível, gere tabelas intermediárias auditáveis antes dos gráficos.
18. Documente filtros, thresholds e regras de classificação.
19. Não omita resultados que contradigam as hipóteses iniciais.
20. O objetivo é descobrir o que os dados mostram, não confirmar o briefing.

---

# 31. RESUMO EXECUTIVO DO CONTEXTO

```text
FONTE:
sudoexpo-match-base-completa.json

CAFÉ ENTRE AMIGOS:
27/08/2026
Perfis criados nesse dia = origem estimada Café Entre Amigos.

SUDOEXPO:
09/09/2026 a 12/09/2026.
Ignorar datas obsoletas cadastradas na tabela de eventos.

META:
300 cadastros.
Aproximadamente 1 cadastro a cada 5 minutos segundo o briefing.

ALTA COMPATIBILIDADE:
score >= 80.

SCORE:
direcional; usar score correspondente ao participante que tomou a decisão.

HIPÓTESE:
usuários permissivos e seletivos têm comportamento diferente.
Testar quantitativamente.

HIPÓTESE PRINCIPAL:
usuários seletivos tendem a aceitar matches de score alto.
Testar; não assumir.

AQUISIÇÃO PRESENCIAL:
aprox. 30 pessoas teriam aceitado cadastro após abordagem direta.
Tratar como relato, não como causalidade comprovada pela base.

CONEXÃO:
não equivale a negócio fechado.

NEGÓCIO / ROI:
exige follow-up posterior.

PESQUISA:
fonte separada; deve ser cruzada posteriormente.

PRIVACIDADE:
arquivo sensível; anonimizar dados pessoais.
```

---

**Este documento deve acompanhar a base JSON em futuras análises do SudoExpo Match.**
