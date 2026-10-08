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
versao_conteudo: '1.1'
idioma: pt-BR
data_criacao: '2026-10-07'
ultima_revisao: '2026-10-08'
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

O formulário pode ter dezenas de seções internas. Isso não significa que o respondente verá dezenas de seções. A contagem de itens cadastrados não equivale à quantidade de perguntas respondidas.

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

Cada resposta **pode** levar a uma pergunta diferente quando o conteúdo da etapa seguinte realmente muda:

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

Como padrão operacional da ACIRV, perguntas de escolha devem buscar **no máximo quatro alternativas no total**, inclusive “Outra” ou “Não se aplica” quando necessárias. Não é obrigatório preencher as quatro vagas.

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

## 28. Aprendizado de outubro de 2026 — pesquisa adaptativa sobre IA

Esta seção registra a experiência concreta de planejar, construir, revisar e testar estruturalmente a pesquisa **“Como você usa Inteligência Artificial hoje?”**. Complementa as regras gerais deste manual sem substituir as lições anteriores sobre imagem espontânea, relacionamento institucional, priming e perfil do respondente.

### Instrumentos comparados

Foram consultados os formulários “Como você usa Inteligência Artificial — e o que ainda gostaria de conseguir fazer com ela?”, “IA na prática: queremos entender como você usa e o que precisa”, “Queremos entender melhor sua relação com a ACIRV” e a referência “Avaliação rápida — Aula de IA, ChatGPT, GitHub e Trello”.

A pesquisa geral de IA tinha 31 perguntas e listas que, em alguns itens, ultrapassavam 20 alternativas. A amplitude temática era valiosa, mas “atividades que realiza”, “problemas que quer resolver”, “temas de interesse”, “o que deseja aprender” e “iniciativas desejadas” frequentemente aproximavam-se do mesmo construto. A nova arquitetura reorganizou essas dimensões no encadeamento:

**estágio de uso → finalidade principal → ferramenta/contexto → atividade concreta → barreira (ou ausência dela) → próximo passo desejado → encerramento.**

### O que os dados realmente sustentam

Na consulta à pesquisa geral de IA, estavam disponíveis **16 respostas**. Nas perguntas multirresposta, observaram-se 13 marcações para pesquisar informações, 12 para escrever/revisar textos, 11 para criar imagens, 10 para analisar dados e 9 para criar conteúdo para redes sociais. Entre interesses, vendas/prospecção, gestão empresarial e automação de tarefas receberam 10 marcações cada; agentes de IA, 9.

Esses valores são **marcações de uma amostra pequena e possivelmente selecionada**, e não prevalências populacionais. As mesmas pessoas podem marcar vários itens; não se devem somar as categorias como se fossem indivíduos distintos. Os dados foram úteis **como revisão do instrumento**, especialmente para revelar a subcobertura de vendas, atendimento, gestão e operação na primeira taxonomia. Não permitem inferir as preferências de todos os empresários de Rio Verde.

Respostas abertas reforçaram a necessidade de contemplar atendimento automatizado, mensagens, relatórios, planilhas, prospecção, organização de processos, agentes e criação de sistemas. Trata-se de evidência qualitativa de **possibilidades a cobrir**, não de prova de sua distribuição no público.

---

## 29. Taxonomia: primeiro a finalidade, depois o formato e a ferramenta

### Problema da primeira versão

A categorização inicial separava: (1) texto/pesquisa/documentos; (2) imagens/design/vídeo; (3) dados/análise/decisão; (4) automação/sites/programação.

Essa divisão misturava **formato de saída**, **atividade**, **finalidade de negócio** e **meio técnico**. Criar vídeo para captar clientes poderia caber em imagem/vídeo ou marketing; automatizar atendimento caberia em atendimento ou automação. O resultado é uma escolha ambígua.

### Taxonomia adotada por finalidade predominante

| Trilha | Pergunta que responde | Desdobramentos concretos |
| --- | --- | --- |
| **Criação e comunicação** | O que a IA me ajuda a produzir para comunicar? | textos/documentos/apresentações; imagens/design; vídeos; redes sociais/marketing |
| **Pesquisa e análise** | O que a IA me ajuda a compreender ou decidir? | pesquisa/comparação; planilhas/números; aprendizado/conhecimento; cenários/decisão |
| **Vendas e operação** | Em que atividade comercial ou rotina a IA me ajuda? | atendimento; vendas/prospecção/leads; gestão/metas; organização operacional |
| **Automação e construção** | Que processo ou solução eu automatizo ou construo? | tarefas repetitivas; agentes/integrações; sites/sistemas; programação |

Essa taxonomia é **distinta por objetivo principal**, não mutuamente exclusiva na vida real. Uma tarefa pode envolver várias finalidades. O enunciado precisa pedir **o uso principal ou mais frequente**, e não sugerir que o respondente usa IA apenas em uma área. Para medir todos os usos, não basta a resposta única utilizada como roteador; planejar levantamento complementar multirresposta quando a decisão exigir essa informação.

### Testes de fronteira obrigatórios

Antes de aprovar a taxonomia, simular exemplos difíceis: vídeo de marketing, atendimento automatizado, textos comerciais, relatório de vendas baseado em planilhas, estudo com chatbot, agente que cria sites. Verificar se é possível escolher o **objetivo predominante** sem perder o sentido da atividade. Se essa distinção for central à decisão, coletar também o uso secundário ou dados qualitativos.

### Por que não classificar primeiro pela ferramenta?

ChatGPT, Gemini, Claude ou Copilot podem servir para inúmeras finalidades. O nome da ferramenta não revela, sozinho, o que a pessoa faz, seu resultado ou sua necessidade. A sequência é **finalidade → ferramenta/contexto → atividade**. Não perguntar ferramentas como se fossem aplicações.

---

## 30. Quatro alternativas: limite útil, mas não dogma cego

### Nova interpretação operacional

“Até quatro” significa **quatro alternativas totais exibidas**, não quatro alternativas substantivas mais “Outra”. Nem toda pergunta precisa ter quatro opções. Uma questão com três respostas corretas e distintas é melhor do que inventar uma quarta apenas para preencher espaço.

O limite não garante boa taxonomia. Perguntas com quatro opções podem permanecer inválidas quando misturam níveis de abstração, ocultam casos legítimos, obrigam falsa escolha ou usam rótulos extensos demais.

### Duas falhas descobertas

1. **Mistura entre marcas e famílias:** alternativas como “ChatGPT”, “Gemini”, “Claude” e “Canva ou outra ferramenta visual” são úteis para triagem, mas não constituem uma medição homogênea de participação de mercado. Da mesma forma, “Copilot ou IA integrada a planilhas/BI” combina produto com classe. Não interpretar tais grupos como ranking de fornecedores.
2. **Ausência de saída honesta:** ao selecionar exatamente quatro ferramentas, a pesquisa pode deixar sem resposta quem usa Perplexity, Grok, um modelo local ou outras soluções. Obrigar o usuário a marcar uma ferramenta que não utiliza introduz viés. Para mensurar ferramentas especificamente, preferir **três categorias prioritárias + “Outra (qual?)”**, ou uma pergunta em duas etapas (classe → ferramenta) com campo opcional de especificação. Quando necessário, “Não sei” ou “Não se aplica” também consomem uma das quatro vagas.

A escolha das marcas precisa ser periodicamente revisada. O que funciona em uma amostra de outubro de 2026 não deve ser perpetuado como lista definitiva de ferramentas mais utilizadas.

### Teste editorial de cada conjunto de opções

- Todas medem o **mesmo eixo** (finalidade, frequência, motivo, ferramenta ou formato)?
- Há sinônimos, subcategorias sobrepostas ou uma alternativa vaga que absorve as demais?
- Qual caso importante ficou de fora? Um respondente real consegue escolher sem mentir?
- São comparáveis as unidades que se pretende contar depois?
- A quarta alternativa melhora a precisão ou está ali apenas para atingir quatro?
- Se alguém escolher qualquer uma delas, a próxima pergunta precisa realmente mudar?

---

## 31. Personalização por valor informacional, não por multiplicação de páginas

O novo desenho separa dois grandes perfis:

**Trilha A — não usa ou usa muito pouco:** pergunta a barreira inicial; em seguida, o aprofundamento é diferente para quem não sabe começar, não vê aplicação, não dispõe de tempo ou não tem interesse. Uma recusa de continuidade deve oferecer saída direta, sem impor contato.

**Trilha B — já usa:** pergunta qual das quatro finalidades domina seu uso; a pessoa vê apenas a seção relacionada, indicando ferramenta/contexto e atividade concreta. Depois escolhe o maior obstáculo e recebe um aprofundamento adequado: transformar experimentos em processo, escolher/conectar ferramentas, avançar com pouco tempo ou desenvolver usos mais sofisticados.

**Convergência:** todas as trilhas pertinentes reencontram um bloco final com **uma pergunta aberta opcional** sobre tarefa/problema concreto, interesse em iniciativas da ACIRV e, apenas para “Sim” ou “Talvez”, um **campo de contato opcional**.

### Regra derivada da implementação

As quatro alternativas de uma pergunta **não precisam** levar a quatro seções diferentes. Se “ChatGPT” e “Gemini” exigem a mesma próxima pergunta sobre o tipo de atividade, **convergir para a mesma seção** é correto. Repetir páginas idênticas é uma falsa personalização, aumenta risco de inconsistência e dificulta manutenção.

Criar trilhas distintas apenas quando a resposta altera significado, opções plausíveis, linguagem, elegibilidade ou decisão posterior.

### Não forçar o respondente a declarar uma dificuldade

A versão inicial da pergunta sobre obstáculos não oferecia uma resposta válida para alguém sem barreira relevante. A revisão criou **“Não tenho uma dificuldade relevante; quero avançar para usos mais sofisticados”**, com aprofundamento em agentes, integrações, sistemas e uso de IA para dados/gestão/decisão.

É um princípio geral: questionários não devem **pressupor a existência do problema que procuram medir**. Dar saída neutra evita respostas inventadas para continuar.

### Quantidade de itens versus carga real

O Google Forms revisado continha **45 itens internos**, incluindo títulos de seção; isso não significa 45 perguntas respondidas. Os percursos previstos variavam, conforme o perfil e a decisão de contato, de cerca de **3 a 9 respostas**. Essa faixa é **contagem do caminho desenhado**, não tempo real medido de preenchimento. Somente piloto com pessoas permite afirmar duração, facilidade e taxa de conclusão.

---

## 32. Engenharia do branching no Google Forms

### Ordem recomendada de implementação

1. Definir, fora do Forms, o grafo com **seção inicial, decisão, destinos, convergência, contato e envio**.
2. Criar as seções de destino e registrar seus **IDs reais**.
3. Inserir cada pergunta na seção correspondente e configurar navegação por resposta nos tipos compatíveis, sobretudo múltipla escolha e lista suspensa. Não presumir branching individual por opção de checkbox.
4. Apontar os saltos para os IDs das seções, **não seus títulos**.
5. Preservar os IDs de perguntas/itens quando editar conteúdo existente e verificar índices se houver inserções ou movimentos.
6. Conferir os caminhos de **saída imediata**, **convergência comum** e **contato facultativo**.
7. Reler o formulário depois de cada operação importante. Uma chamada composta pode falhar **após criar o formulário vazio**; existência do arquivo não comprova que ele contenha as perguntas.
8. Fazer teste funcional no link de resposta, inclusive em dispositivo móvel. Validar a lógica pelo percurso que o respondente vê, não apenas pela estrutura da API.

### Duas camadas de Quality Gate

**Validação estática:** número de opções (máximo quatro), todos os destinos existentes, perguntas obrigatórias apropriadas, fim alcançável, seções sem IDs quebrados e contato não obrigatório.

**Validação comportamental:** testar cada alternativa de cada pergunta roteadora, verificar saltos na navegação, ausência de passagem acidental para a seção vizinha, inexistência de laços e envio bem-sucedido. **Ter todos os IDs de destino válidos não prova que os caminhos funcionem**: saltos semanticamente errados e avanços automáticos ainda podem ocorrer.

### Matriz mínima de perfis simulados

| Perfil | O que precisa acontecer |
| --- | --- |
| Não usa IA e não sabe começar | Pergunta de ajuda inicial; não deve ver ferramentas de quem já usa |
| Não usa IA e não quer receber conteúdo | Encerrar sem obrigar contato ou problema aberto |
| Criação/comunicação | Ferramenta e atividade de criação; não cair em vendas ou dados |
| Pesquisa/análise | Ferramenta e atividade de análise/aprendizado |
| Vendas/operação | Atendimento, prospecção, gestão ou rotina |
| Automação/construção | Agentes, integração, aplicativos, processos ou código |
| Usuário experiente sem barreira | Resposta “sem dificuldade” → interesse avançado |
| Responde “Sim/Talvez” para receber notícias | Exibir contato opcional |
| Responde “Não” para receber notícias | Ir diretamente ao envio |

Cobrir cada alternativa de ramificação, não somente um exemplo por categoria. Se houver mudança de ramo ao voltar para uma questão anterior, verificar também esse comportamento.

---

## 33. Como analisar e melhorar uma pesquisa adaptativa

### Dados ausentes por desenho

Quem nunca usa IA não responde à pergunta de ferramentas; quem seleciona vendas/operação não vê perguntas de criação. A ausência de dado nesses casos significa **não elegível / não exibido**, nunca automaticamente “Não” ou “Não sei”.

Denominadores precisam ser explícitos:

- estágio de uso: todos os respondentes elegíveis;
- finalidade: pessoas que alcançaram a trilha de usuários;
- ferramenta e atividade: somente pessoas da finalidade correspondente;
- obstáculo: pessoas da trilha de usuários que chegaram à pergunta;
- interesse de contato: somente pessoas que visualizaram o bloco;
- respostas abertas: contabilizar preenchimento e conteúdo útil separadamente.

Quando um formulário é alterado durante a coleta, registrar **versão do questionário, data da mudança, alterações de texto/opções e compatibilidade analítica**. Não combinar silenciosamente respostas de taxonomias diferentes.

### Leitura de dados antigos e piloto

As 16 respostas da pesquisa geral ajudaram a identificar **lacunas de cobertura**. Não validaram representatividade, preferência do público como um todo, duração do formulário novo nem desempenho de todas as rotas. Na nova pesquisa, pilotar com pessoas de níveis e profissões diferentes e observar:

- pessoas que não encontram nenhuma alternativa adequada;
- motivos de “Outra” quando houver essa opção;
- esforço para diferenciar categorias;
- abandono, duração real e respostas mínimas;
- erros de navegação ou seção;
- coerência do denominador em cada indicador;
- recorrência de casos concretos relevantes.

### Privacidade e propósito

O campo de contato deve permanecer facultativo e coerente com a finalidade comunicada. Interesse genérico em acompanhar iniciativas não autoriza qualquer uso futuro dos dados pessoais. Antes de utilizar contatos, observar o aviso de privacidade, base legal e regras aplicáveis de comunicação/descadastro. No **ACIRV Notebook público**, promover **métodos e agregados**, não respostas individuais ou contatos identificáveis.

### Roteiro reutilizável

**Decisão a informar → fontes e pesquisas anteriores → construtos únicos → taxonomia de até quatro opções honestas → grafo de ramificações e convergência → implementação → verificação estática + funcional → piloto e análise por base elegível → ajuste/versionamento → decisão.**

O critério final não é “a pesquisa tem muitas ramificações”, mas: **cada pessoa recebe poucas perguntas pertinentes e a ACIRV consegue transformar as respostas em uma decisão defensável**.

---

## Relações justificadas

- [[Diagnostico-e-Governanca-de-Adocao-de-IA]] — exemplo de instrumento diagnóstico que exige cuidado para não confundir perguntas com evidência de maturidade real.
- [[Qualidade-dos-Dados-de-Marketing]] — reforça a separação entre evidência observada, interpretação e inferência.
- [[Matriz-de-Metricas-por-Objetivo]] — conecta medição a objetivos e decisões, princípio também aplicado à construção de pesquisas.

## Histórico

### 2026-10-08 — v1.1

Acrescentado estudo de caso da pesquisa adaptativa de IA: taxonomia por finalidade, diferença entre ferramenta e atividade, limite total de quatro opções, risco de alternativas sem saída adequada, branching com convergência, percurso para usuários sem barreiras, validação técnica e funcional, denominadores condicionais, proteção de dados e versionamento. As 16 respostas da pesquisa anterior foram usadas apenas como insumo exploratório para revisão do instrumento.

### 2026-10-07 — v1.0

Manual criado a partir da revisão da pesquisa geral da ACIRV e da construção de uma nova versão adaptativa. A experiência consolidada incluiu: limite de quatro alternativas principais, branching por perfil e resposta, redução de perguntas abertas obrigatórias, controle de priming, separação entre decisor e funcionário de empresa associada, uso de respostas-piloto para QA do instrumento e substituição de matrizes propensas a straight-lining por escolhas mais discriminativas.
