---
id: processo-manual-de-pesquisas-e-questionarios-adaptativos
titulo: Manual-de-Pesquisas-e-Questionarios-Adaptativos
aliases:
- Manual de Pesquisas
- Questionarios Adaptativos
- Logica de Direcionamento em Formularios
tipo: processo
subtipo: manual
status: ativo
profundidade: avancada
versao_schema: '1.0'
versao_conteudo: '1.0'
idioma: pt-BR
data_criacao: '2026-10-07'
ultima_revisao: '2026-10-07'
grau_confianca: alto
camadas_evidencia:
- fato_documentado
- interpretacao_operacional
tags:
- pesquisa
- questionario
- formularios
- google-forms
- experiencia-do-respondente
- dados
- decisao
notas_relacionadas:
- '[[Diagnostico-e-Governanca-de-Adocao-de-IA]]'
- '[[Qualidade-dos-Dados-de-Marketing]]'
- '[[Matriz-de-Metricas-por-Objetivo]]'
confidencialidade: interno
---

# Manual-de-Pesquisas-e-Questionarios-Adaptativos

> [!summary] Síntese
> Uma boa pesquisa da ACIRV não deve tentar perguntar tudo a todos. Ela deve descobrir **quem está respondendo, qual decisão precisa ser informada e qual é a próxima pergunta realmente necessária**. O método adotado é: **núcleo comum curto + trilhas adaptativas por perfil e resposta + aprofundamento apenas quando há motivo + segmentação mínima + controle explícito de viés e carga cognitiva**. A complexidade deve ficar na arquitetura do formulário, não na experiência do respondente.

## Por que este manual existe

Este manual consolida o aprendizado adquirido na revisão e reconstrução da pesquisa geral da ACIRV sobre relacionamento, valor, futuro e Inteligência Artificial.

A pesquisa anterior tinha uma boa arquitetura intelectual: media imagem espontânea, entendimento da ACIRV, experiência real, barreiras, comunicação, valor percebido e uma pergunta contrafactual forte. O problema estava na execução:

- muitas alternativas por pergunta;
- opções semanticamente sobrepostas;
- perguntas abertas em excesso;
- perguntas obrigatórias que exigiam texto mesmo quando o respondente não tinha o que acrescentar;
- repetição de classificação do mesmo perfil;
- pouca ramificação;
- mistura de públicos com papéis diferentes;
- baterias que favoreciam resposta mecânica;
- um bloco de IA posicionado no meio da pesquisa, capaz de influenciar perguntas posteriores.

A reconstrução mostrou que **reduzir perguntas não é o único caminho para deixar uma pesquisa mais leve**. É possível manter profundidade criando um formulário internamente amplo, mas fazendo cada pessoa percorrer apenas uma pequena parte dele.

Essa é a ideia central deste manual.

---

## 1. Regra-mãe: toda pergunta precisa justificar uma decisão

Antes de escrever uma pergunta, responder:

1. **Qual decisão esta resposta poderá alterar?**
2. **Quem precisa dessa informação?**
3. **O que faremos de diferente se a resposta A for maior que B?**
4. **A informação já existe em outra fonte?**
5. **Esta pergunta precisa ser feita a todos ou apenas a um perfil?**

Se não existe consequência decisória clara, a pergunta é candidata a remoção.

Uma pesquisa não deve ser um inventário de curiosidades. Deve ser um **instrumento de redução de incerteza para decisões reais**.

### Exemplo

Pergunta fraca:

> “Você gosta dos eventos da ACIRV?”

Ela gera opinião, mas pouca ação.

Pergunta melhor:

> “Qual é hoje a principal barreira para você participar mais do que a ACIRV oferece?”

As respostas podem orientar comunicação, horário, formato ou priorização temática.

---

## 2. Complexidade no formulário; simplicidade para o respondente

A arquitetura recomendada é:

```text
Abertura
  ↓
Imagem espontânea
  ↓
Classificação de perfil
  ↓
Trilha específica do perfil
  ↓
Núcleo comum
  ↓
Segmentação mínima
  ↓
Módulos temáticos opcionais ou finais
  ↓
Fim
```

O formulário pode ter dezenas de seções internas. Isso não significa que o respondente verá dezenas de seções.

O objetivo é que:

- o **sistema saiba muito** sobre o fluxo;
- o **respondente precise saber pouco** sobre o fluxo;
- cada resposta elimine perguntas irrelevantes;
- cada trilha seja coerente com o contexto real da pessoa.

### Princípio operacional

> **Não perguntar “o que mais podemos perguntar?”; perguntar “qual é a próxima pergunta necessária para esta pessoa?”.**

---

## 3. Lógica de direcionamento: branching por significado

“Lógica de direcionamento”, “ramificação”, “branching” ou “skip logic” designam o mesmo princípio: a resposta determina qual seção vem em seguida.

### Exemplo genérico

Pergunta:

> “Como está seu uso de IA hoje?”

Opções:

1. uso com frequência;
2. uso ocasionalmente;
3. já usei, mas parei;
4. nunca usei.

Cada resposta deve levar a uma pergunta diferente:

- **uso frequente** → “Em qual tipo de atividade você mais usa?”
- **uso ocasional** → “O que mais impede você de usar mais?”
- **já usei e parei** → “Qual foi o principal motivo?”
- **nunca usei** → “O que faria você experimentar?”

A pesquisa deixa de ser uma sequência fixa e passa a se comportar como uma **árvore de diagnóstico**.

### Quando criar uma ramificação

Criar uma trilha separada quando a resposta muda:

- o significado da próxima pergunta;
- o contexto de interpretação;
- as opções plausíveis;
- a ação que a ACIRV poderá tomar;
- a linguagem adequada ao respondente.

### Quando NÃO criar uma ramificação

Não ramificar apenas porque é tecnicamente possível.

Exemplos que normalmente não exigem trilha própria:

- setor;
- porte;
- função;
- faixa de tempo de empresa.

Essas variáveis geralmente servem para **segmentar a análise**, não para mudar imediatamente a experiência do questionário.

---

## 4. Regra de até quatro opções

Como padrão operacional da ACIRV, perguntas de escolha devem buscar **no máximo quatro alternativas principais**.

A regra não é estética. Ela reduz:

- carga de leitura;
- redundância;
- ambiguidade;
- fadiga;
- escolhas por desistência;
- dificuldade de comparação entre categorias.

### Como chegar a quatro opções

Antes de adicionar uma quinta alternativa, verificar se:

1. duas opções representam o mesmo fenômeno;
2. uma opção é subconjunto de outra;
3. duas opções podem ser agrupadas em uma categoria mais estável;
4. a alternativa deveria virar um aprofundamento posterior;
5. a pergunta está tentando medir mais de um construto ao mesmo tempo.

### Exemplo de sobreposição

Ruim:

- falta tempo;
- datas dificultam;
- horários dificultam;
- agenda não combina;
- não consigo participar;
- fico sabendo tarde.

Melhor:

Pergunta principal:

- comunicação/clareza;
- tempo/disponibilidade;
- relevância;
- sem barreira relevante.

Se a pessoa escolher **tempo/disponibilidade**, abre-se:

- divulgação com antecedência;
- horários alternativos;
- conteúdo sob demanda;
- formato online/híbrido.

A profundidade foi preservada sem obrigar todos a ler oito alternativas.

---

## 5. Alternativas devem ser mutuamente distintas

As opções de uma pergunta devem competir entre si de forma compreensível.

Evitar:

- uma opção que contém outra;
- duas formas de dizer quase a mesma coisa;
- misturar causa com consequência;
- misturar intensidade com categoria;
- uma alternativa genérica que absorve todas as demais.

### Exemplo observado na pesquisa anterior

Havia alternativas como:

- “Procuro Sebrae, sindicato, associação ou outra entidade”
- “Procuro a ACIRV”

Como a ACIRV é uma associação, uma categoria continha conceitualmente a outra.

Também havia “Depende muito do tipo de necessidade”, uma alternativa tão abrangente que podia funcionar como saída fácil para quase qualquer pessoa.

### Regra

> Se duas opções puderem ser verdadeiras pela mesma razão, revisar a taxonomia.

---

## 6. Pergunta fechada para medir; aberta para descobrir

Perguntas fechadas e abertas têm papéis diferentes.

### Pergunta fechada

Use quando é preciso:

- comparar pessoas;
- calcular proporções;
- cruzar segmentos;
- monitorar tendência;
- priorizar uma categoria;
- alimentar dashboard.

### Pergunta aberta

Use quando é preciso:

- descobrir linguagem espontânea;
- encontrar temas ainda não previstos;
- entender uma experiência específica;
- captar nuance;
- registrar um caso concreto.

### Erro comum

Transformar todo tema importante em campo aberto obrigatório.

Isso cria respostas como:

- “não”;
- “nada”;
- “.”;
- respostas genéricas;
- texto de baixa informação produzido apenas para liberar a próxima página.

### Padrão recomendado

```text
Houve problema?
  ├─ Não → segue
  └─ Sim → campo aberto opcional para explicar
```

Assim, a pergunta quantitativa mede a incidência e o campo qualitativo explica o caso.

---

## 7. Campos abertos obrigatórios devem ser raros

Perguntas abertas obrigatórias devem existir apenas quando a ausência de resposta tornaria o instrumento inútil.

Na pesquisa reconstruída, preservou-se como obrigatória a pergunta contrafactual:

> “Imagine que a ACIRV deixasse de existir amanhã. O que faria falta — se alguma coisa fizesse falta?”

Ela é central porque busca revelar valor percebido sem perguntar diretamente “qual é o valor da ACIRV?”.

Mesmo nesse caso, a instrução deve aceitar explicitamente uma resposta negativa:

> “Se nada fizesse falta, pode escrever ‘nada’.”

Isso reduz pressão por elogio artificial.

---

## 8. Perguntar comportamento antes de opinião abstrata

Sempre que possível, priorizar perguntas sobre:

- último contato;
- ação realizada;
- resultado obtido;
- canal usado;
- dificuldade concreta;
- comportamento após receber uma comunicação.

Comportamento recente tende a ser mais acionável que avaliação abstrata.

### Comparação

Menos útil:

> “Você considera a comunicação da ACIRV boa?”

Mais útil:

> “Nos últimos 30 dias, por qual canal você mais se lembra de ter recebido comunicação da ACIRV?”

Depois:

> “Quando algo parece relevante nesse canal, o que você costuma fazer?”

O primeiro mede lembrança. O segundo mede comportamento.

---

## 9. Imagem espontânea deve vir antes da imagem induzida

Se a pesquisa quer entender marca, reputação ou posicionamento, começar com perguntas abertas e neutras.

Exemplos:

- “Quando você pensa na ACIRV, qual é a primeira coisa que vem à cabeça?”
- “Se alguém perguntasse o que a ACIRV faz, o que você responderia?”

Somente depois devem aparecer categorias como:

- conecta empresas;
- representa interesses;
- oferece soluções;
- desenvolve empresas.

### Por quê

Se primeiro mostramos os atributos desejados, contaminamos a resposta espontânea.

A pessoa passa a responder usando o vocabulário que a própria pesquisa forneceu.

---

## 10. Controle de priming: a ordem altera respostas

Um questionário não é apenas uma lista de perguntas. A pergunta anterior muda o estado mental do respondente.

Na pesquisa anterior, havia um bloco de Inteligência Artificial antes de uma pergunta sobre como a pessoa age diante de necessidades empresariais. Uma das opções posteriores era “uso ferramentas de IA”.

Isso cria risco de **priming**: o tema foi ativado mentalmente imediatamente antes de ser oferecido como alternativa.

### Regra

Módulos temáticos capazes de influenciar a percepção do objeto principal devem ser:

- colocados no final; ou
- isolados após todas as medidas centrais.

Na pesquisa adaptativa, o módulo de IA foi deslocado para o final.

---

## 11. Separar papéis que parecem iguais, mas não são

Um dos principais erros da pesquisa anterior era tratar:

- responsável pela decisão de associação;
- funcionário de empresa associada;

como se fossem o mesmo respondente.

Não são.

O primeiro pode avaliar:

- permanência;
- custo-benefício;
- valor da associação;
- intenção de continuar.

O segundo pode avaliar:

- experiência;
- utilidade percebida;
- atendimento;
- eventos;
- conhecimento;
- conexões.

Mas pode não ter autoridade nem informação para responder sobre permanência da empresa.

### Regra

> Segmentar pelo **papel real na decisão**, não apenas pela relação nominal com a organização.

---

## 12. Evitar perguntas de confirmação redundantes

Não pedir duas vezes a mesma classificação apenas para viabilizar um desvio técnico de seção.

Na pesquisa anterior, a relação com a ACIRV era perguntada no início e confirmada novamente antes do branching. Já houve resposta inconsistente entre as duas classificações.

Na nova arquitetura, a primeira classificação já serve como roteador principal.

### Regra

Uma variável estrutural deve ter:

- uma definição;
- uma pergunta;
- uma posição;
- um valor canônico.

---

## 13. Escalas precisam medir um único eixo

Escalas numéricas devem ser semanticamente monotônicas.

Ruim:

1. não consigo entender;
2. tenho muita dificuldade;
3. tenho pouca dificuldade;
4. entendo parcialmente;
5. é muito claro.

Aqui o eixo alterna entre “dificuldade”, “entendimento” e “clareza”.

Melhor:

1. nada claro;
2. pouco claro;
3. razoavelmente claro;
4. claro;
5. muito claro.

Todos os pontos representam o mesmo construto: **clareza**.

### Regra

> O número deve aumentar porque a mesma variável aumentou — não porque a frase mudou de significado.

---

## 14. Cuidado com matrizes e straight-lining

Matrizes longas parecem eficientes, mas incentivam resposta mecânica.

Na pesquisa anterior, os poucos respondentes disponíveis para teste repetiram a mesma nota em praticamente todos os atributos da matriz. Esse padrão é conhecido como **straight-lining**.

A amostra observada era pequena demais para representar os associados, mas suficiente para sinalizar um problema de instrumento.

### Alternativa

Em vez de:

> “Dê nota de 1 a 5 para oito atributos da ACIRV.”

Usar:

> “Qual destas ideias mais combina com a ACIRV para você?”

E, em seguida:

> “O que fortaleceria essa imagem?”

Isso força discriminação e produz uma resposta mais acionável.

---

## 15. Respostas existentes servem primeiro como teste do instrumento

Uma base pequena de respostas não deve ser tratada como pesquisa de opinião representativa.

Ela ainda pode ser extremamente útil para detectar:

- campos abandonados;
- respostas artificiais;
- perguntas mal interpretadas;
- alternativas redundantes;
- inconsistência entre classificações;
- straight-lining;
- campos abertos que geram pouco conteúdo.

### Caso aprendido

Na revisão da pesquisa anterior, havia apenas três respostas disponíveis. Elas **não foram usadas para concluir o que “os associados pensam”**.

Foram usadas como evidência de UX e qualidade do instrumento:

- resposta “.” em campo aberto obrigatório;
- resposta muito genérica no fim do questionário;
- repetição de notas em matriz;
- divergência entre duas perguntas que deveriam representar a mesma relação com a ACIRV.

### Regra

> Amostra pequena pode diagnosticar o formulário; não necessariamente diagnostica a população.

---

## 16. A pesquisa precisa de uma variável central de resultado

Um questionário pode medir dezenas de drivers e ainda assim não permitir responder “isso melhora o quê?”.

Sempre que houver objetivo longitudinal, definir uma variável central, por exemplo:

- valor percebido;
- clareza;
- probabilidade de permanência;
- intenção de participação;
- resolução da necessidade;
- satisfação com determinada experiência.

Depois, cruzar os demais fatores com essa variável.

### Estrutura analítica

```text
Variável de resultado
       ↑
       │
drivers: clareza, contato, barreiras, canal, experiência, perfil
```

Isso transforma uma coleção de respostas em um modelo de decisão.

---

## 17. Segmentação: pouco, mas suficiente

Segmentação excessiva aumenta atrito e pode criar sensação de cadastro.

Segmentação insuficiente impede análise útil.

Para pesquisas gerais da ACIRV, três dimensões costumam ser um bom ponto de partida:

- **função/papel profissional**;
- **setor**;
- **porte da empresa**.

Dependendo do objetivo, podem entrar:

- tempo de associação;
- tempo de empresa;
- cidade/região;
- poder de decisão;
- estágio da empresa.

### Regra

Só adicionar uma variável de perfil se houver intenção real de cruzá-la na análise.

---

## 18. O contexto de aplicação precisa combinar com a pergunta

Perguntas como:

> “O que trouxe você à ACIRV hoje?”

funcionam em:

- recepção;
- evento;
- atendimento presencial;
- QR localizado na sede.

Podem ficar estranhas quando o link chega por:

- WhatsApp;
- e-mail;
- Instagram;
- grupo empresarial.

A redação deve ser compatível com o canal real de coleta.

### Antes de publicar

Definir:

- onde o link será distribuído;
- em que momento;
- para qual público;
- em qual dispositivo a maioria responderá;
- se o respondente estará na ACIRV ou fora dela.

---

## 19. Experiência adaptativa: padrão recomendado

Uma pesquisa adaptativa da ACIRV deve seguir, quando aplicável, este desenho:

### Camada 1 — abertura neutra

Objetivo: captar percepção não induzida.

- imagem espontânea;
- descrição livre curta.

### Camada 2 — roteamento de perfil

Objetivo: descobrir quem pode responder o quê.

Máximo recomendado: quatro perfis estruturalmente distintos.

### Camada 3 — diagnóstico específico

Objetivo: aprofundar apenas a questão relevante para aquele perfil.

Exemplos:

- associado decisor → valor e permanência;
- funcionário → experiência e utilidade percebida;
- ex-associado → motivo de saída;
- não associado → barreira de entrada.

### Camada 4 — núcleo comum

Objetivo: criar variáveis comparáveis entre todos.

Exemplos:

- contato;
- resultado;
- barreira;
- comunicação;
- imagem;
- valor contrafactual.

### Camada 5 — segmentação

Objetivo: permitir cruzamentos sem interromper o fluxo principal.

### Camada 6 — módulo temático

Objetivo: investigar assunto adicional sem contaminar o objeto central.

Exemplo: IA no final.

---

## 20. Checklist de redação de cada pergunta

Antes de aprovar uma pergunta, verificar:

- [ ] mede apenas uma coisa?
- [ ] a redação é compreensível sem contexto interno da ACIRV?
- [ ] evita sugerir uma resposta desejável?
- [ ] é necessária para uma decisão?
- [ ] precisa mesmo ser obrigatória?
- [ ] precisa mesmo ser aberta?
- [ ] deve aparecer para todos?
- [ ] as opções são distintas?
- [ ] existe sobreposição entre alternativas?
- [ ] uma opção é subconjunto de outra?
- [ ] há no máximo quatro opções principais?
- [ ] existe uma alternativa fácil demais que esvazia as demais?
- [ ] a janela temporal está clara quando necessário?
- [ ] a pessoa realmente tem informação para responder?
- [ ] a pergunta anterior pode influenciar esta resposta?

---

## 21. Checklist de arquitetura antes da publicação

- [ ] objetivo da pesquisa escrito em uma frase;
- [ ] decisões que serão informadas mapeadas;
- [ ] variável central de resultado definida;
- [ ] imagem espontânea vem antes de atributos induzidos;
- [ ] perfis com papéis diferentes possuem trilhas diferentes;
- [ ] nenhuma classificação estrutural é perguntada duas vezes;
- [ ] perguntas fechadas têm no máximo quatro alternativas principais;
- [ ] perguntas abertas obrigatórias são exceção;
- [ ] aprofundamentos qualitativos aparecem apenas quando fazem sentido;
- [ ] módulos com risco de priming foram movidos para o final;
- [ ] escalas usam o mesmo eixo semântico do início ao fim;
- [ ] matrizes extensas foram evitadas;
- [ ] perguntas contraditórias não podem ser selecionadas simultaneamente;
- [ ] segmentação é suficiente para análise, mas não parece cadastro;
- [ ] fluxo foi testado em cada rota possível;
- [ ] cada rota chega ao fim sem cair em seção errada;
- [ ] formulário foi testado em celular;
- [ ] tempo declarado reflete o caminho real do respondente;
- [ ] cópias vazias ou versões antigas não estão publicadas por engano;
- [ ] coleta de e-mail e identificação estão coerentes com a finalidade;
- [ ] existe plano para analisar as respostas antes da divulgação.

---

## 22. Quality Gate pós-piloto

Antes de considerar o formulário definitivo, aplicar um piloto pequeno.

O objetivo inicial não é estimar percentuais da população. É descobrir defeitos.

Verificar:

### Sinais de fadiga

- respostas vazias ou mínimas no fim;
- aumento de “não sei”;
- campos com “.”, “-” ou texto sem informação;
- abandono em determinada seção.

### Sinais de taxonomia ruim

- pessoas pedindo “outro” com frequência;
- duas opções escolhidas mentalmente ao mesmo tempo;
- comentários dizendo “depende”;
- categoria residual grande demais.

### Sinais de pergunta mal construída

- respostas contraditórias;
- grande concentração em uma alternativa genérica;
- divergência entre perguntas equivalentes;
- interpretação diferente da pretendida.

### Sinais de matriz ruim

- mesma nota em todas as linhas;
- padrões repetitivos;
- baixa variância sem explicação substantiva.

### Sinais de branching ruim

- pessoa recebendo pergunta para a qual não tem autoridade;
- trilha que pressupõe algo não declarado;
- caminho que pula uma informação necessária;
- seções que não convergem corretamente.

---

## 23. Como usar IA na construção de pesquisas

IA pode ajudar muito em:

- mapear redundâncias;
- encontrar sobreposição semântica;
- propor taxonomias com quatro categorias;
- simular perfis de respondentes;
- testar caminhos de branching;
- revisar neutralidade;
- detectar priming;
- transformar perguntas abertas em arquitetura fechada + aprofundamento;
- analisar respostas-piloto;
- gerar documentação do fluxo.

Mas a IA não deve decidir sozinha:

- qual decisão institucional importa;
- qual público tem autoridade para responder;
- se uma amostra é representativa;
- se uma resposta prova uma hipótese;
- se um dado sensível deve ser coletado.

### Regra

> IA pode otimizar o instrumento; a validade depende do objetivo, do público e da interpretação correta dos dados.

---

## 24. O que preservar da pesquisa que originou este método

A reconstrução não descartou tudo. Alguns elementos da pesquisa anterior foram preservados justamente porque eram fortes:

- abertura neutra;
- imagem espontânea;
- pergunta “o que a ACIRV faz?”;
- distinção entre percepção e experiência;
- comportamento real em vez de apenas opinião;
- investigação de barreiras;
- lembrança de comunicação;
- ação após comunicação relevante;
- percepção de valor;
- gap entre expectativa e experiência;
- pergunta contrafactual sobre o desaparecimento da ACIRV.

A evolução foi principalmente estrutural: **menos carga por pessoa, melhor segmentação e mais uso de branching**.

---

## 25. Anti-padrões

Evitar:

### “Perguntar tudo para todos”

Resultado: questionário longo e respostas pouco cuidadosas.

### “Lista de dez alternativas”

Resultado: leitura cansativa e categorias sobrepostas.

### “Toda pergunta importante é aberta”

Resultado: baixa comparabilidade e fadiga.

### “Toda pergunta fechada precisa de ‘Outro’”

Resultado: taxonomia mal resolvida escondida atrás de uma saída genérica.

### “Se temos quatro opções, todas precisam gerar quatro páginas”

Resultado: complexidade artificial. Ramificar só quando a próxima pergunta muda de verdade.

### “Mais dados sempre é melhor”

Resultado: coleta sem decisão e análise cara.

### “Três respostas já mostram o que o público pensa”

Resultado: inferência indevida. Pequenas amostras são ótimas para QA, não necessariamente para representar a população.

### “O bloco temático pode entrar em qualquer lugar”

Resultado: priming e contaminação das respostas.

---

## 26. Padrão mínimo recomendado para uma nova pesquisa

Antes de criar qualquer novo formulário da ACIRV, produzir primeiro este mini-briefing:

```yaml
objetivo:
decisoes_que_a_pesquisa_deve_informar:
publico:
canal_de_distribuicao:
variavel_central:
segmentos_necessarios:
nucleo_comum:
trilhas_condicionais:
perguntas_abertas_realmente_necessarias:
riscos_de_priming:
tempo_maximo_desejado:
plano_de_analise:
```

Só depois escrever as perguntas.

---

## 27. Critério de sucesso

Uma pesquisa bem construída não é a que contém mais perguntas nem a que parece mais sofisticada.

Ela é a que consegue simultaneamente:

1. **reduzir a incerteza necessária para uma decisão;**
2. **ser fácil de responder;**
3. **não induzir artificialmente o resultado;**
4. **permitir comparação e segmentação;**
5. **preservar espaço para descoberta qualitativa;**
6. **gerar dados que alguém realmente usará.**

O padrão desejado para a ACIRV é:

> **questionário profundo na arquitetura, curto na experiência e acionável na análise.**

---

## Relações justificadas

- [[Diagnostico-e-Governanca-de-Adocao-de-IA]] — exemplo de instrumento diagnóstico que exige cuidado para não confundir perguntas com evidência de maturidade real.
- [[Qualidade-dos-Dados-de-Marketing]] — reforça a separação entre evidência observada, interpretação e inferência.
- [[Matriz-de-Metricas-por-Objetivo]] — conecta medição a objetivos e decisões, princípio também aplicado à construção de pesquisas.

## Histórico

### 2026-10-07 — v1.0

Manual criado a partir da revisão da pesquisa geral da ACIRV e da construção de uma nova versão adaptativa. A experiência consolidada incluiu: limite de quatro alternativas principais, branching por perfil e resposta, redução de perguntas abertas obrigatórias, controle de priming, separação entre decisor e funcionário de empresa associada, uso de respostas-piloto para QA do instrumento e substituição de matrizes propensas a straight-lining por escolhas mais discriminativas.
