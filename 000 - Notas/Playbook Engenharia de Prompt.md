# 📘 O Playbook Definitivo de Engenharia de Prompt

## FASE 1: Configurando o Motor (Parâmetros)
Antes de escrever, entenda os "botões" que você pode girar no seu LLM (Large Language Model). 
*   **Temperature (0.0 a 2.0):** Controla a criatividade.
    *   *Tarefas exatas (Código, Extração de Dados, Matemática):* Use **0.0** (respostas determinísticas).
    *   *Tarefas criativas (Ideação, Escrita de e-mails, Brainstorming):* Use entre **0.7 e 0.9**.
*   **Top-K e Top-P:** Controlam a aleatoriedade limitando o vocabulário de onde o modelo pode escolher a próxima palavra. Se for mexer na Temperature, geralmente deixe esses no padrão (ou vice-versa).
*   **Max Tokens:** Limite o tamanho da resposta para evitar que o modelo entre em *loops* de repetição sem fim.

---

## FASE 2: A Anatomia do Prompt Ideal
Um prompt de nível de produção não é apenas uma frase. Ele deve ser estruturado como um documento. Lembre-se do **Princípio da Chapeuzinho Vermelho**: *os modelos imitam os dados em que foram treinados*. Se o seu prompt parece um documento de alta qualidade e bem estruturado, a resposta também será.

Divida seu prompt nestes 4 blocos (usando Markdown para separar):

1.  **Introdução / Preamble (System Prompt):** Define o papel (Persona), o tom e o comportamento do modelo.
2.  **Contexto (Context):** A injeção de dados (documentos, histórico de chat, regras de negócio).
3.  **Refoco (Refocus):** Modelos sofrem do *"Valley of Meh"* (eles lembram do começo e do fim do prompt, mas ignoram o meio). Coloque sua pergunta principal ou instrução mais importante no **final** do prompt para "refocar" a atenção da IA.
4.  **Transição / Inception:** Deixe a porta aberta para o modelo começar a falar exatamente no formato que você quer. (Ex: `Resposta em JSON: {`)

---

## FASE 3: Os 5 Princípios de Ouro do Prompting

### 1. Dê Direção (Give Direction)
Diga exatamente o que o modelo deve fazer.
*   **Aja como um especialista:** Use *Role Prompting* (Ex: "Aja como um consultor sênior de marketing...").
*   **Instruções > Restrições:** LLMs funcionam melhor quando você diz o que eles *devem* fazer, em vez do que *não devem*.
    *   ❌ *Não faça:* "Não escreva uma introdução longa."
    *   ✅ *Faça:* "Vá direto ao ponto e comece no primeiro tópico."

### 2. Especifique o Formato (Specify Format)
Nunca deixe a formatação por conta do modelo. Use formatos estruturados para evitar "enrolação" (fluff).
*   Peça a saída em **JSON, YAML, XML ou Markdown**. 
*   Forneça o *schema* (esqueleto) exato que você espera receber. Isso facilita a extração de dados por sistemas automatizados.

### 3. Forneça Exemplos (Provide Examples / Few-Shot)
O modelo aprende melhor vendo do que ouvindo. 
*   **Zero-shot:** Sem exemplos (útil para tarefas muito simples).
*   **Few-shot:** Dê de 3 a 5 exemplos de pares "Entrada -> Saída desejada". 
*   *Atenção:* Misture as classes nos exemplos para não viciar o modelo (ex: não coloque 3 exemplos positivos seguidos se quiser que ele também identifique sentimentos negativos).

### 4. Divida o Trabalho (Divide Labor)
LLMs falham em tarefas gigantescas. Se a tarefa é complexa, divida-a em partes.
*   **Cadeias de Prompts (Prompt Chaining):** Use a saída do Prompt 1 como entrada do Prompt 2. (Ex: Prompt 1 extrai dados de um site -> Prompt 2 cria ideias de produtos -> Prompt 3 escreve o e-mail de vendas).

### 5. Avalie a Qualidade (Evaluate Quality)
Não dependa da sorte. Avalie seus prompts metodicamente.
*   Use o método **SOMA** para fazer o próprio LLM avaliar saídas: Faça perguntas **S**pecíficas, use notas **O**rdinais (1 a 5), com cobertura **M**ulti-**A**specto (avalie tom, precisão e formatação separadamente).

---

## FASE 4: Técnicas Avançadas de Raciocínio

Quando o modelo erra lógica ou matemática, aplique estes "hacks" cognitivos:

*   **Chain of Thought (CoT):** Adicione a frase mágica *"Let's think step-by-step"* (Vamos pensar passo a passo) no final do seu prompt. Isso força o modelo a criar uma "voz interna" e fazer os cálculos antes de dar a resposta final, aumentando drasticamente a precisão.
*   **Self-Consistency:** Gere 5 ou mais respostas diferentes (usando Temperature alta) e programe seu sistema para escolher a resposta que mais se repetiu (votação por maioria).
*   **Step-Back Prompting:** Antes de pedir a solução de um problema específico, peça ao modelo para listar os princípios gerais ou as leis fundamentais que regem aquele problema.
*   **ReAct (Reason + Act):** A arquitetura para Agentes. O modelo opera em um loop: *Pensar -> Escolher uma Ferramenta (ex: Busca no Google) -> Observar o resultado -> Pensar novamente -> Dar a resposta final*.

---

## FASE 5: Tratando Contexto e Dados (RAG)

Quando precisar que o modelo responda com base em documentos da sua empresa (Retrieval-Augmented Generation):

1.  **Snippetizing (Fatiamento):** Não jogue um PDF de 500 páginas no prompt. Fatie o texto em "pedaços" (chunks) com sobreposição (overlap) para não cortar o sentido das frases no meio.
2.  **Cuidado com a Falácia da Arma de Chekhov:** Se você colocar uma informação inútil no contexto, a IA tentará usá-la a todo custo. Filtre rigorosamente o contexto usando busca semântica (bancos de dados vetoriais como FAISS ou Pinecone) antes de enviar ao modelo.
3.  **Prevenindo Alucinações:** Adicione a regra: *"Responda APENAS usando os documentos fornecidos. Se a resposta não estiver nos documentos, diga 'Não sei'."*

---

## FASE 6: Prompts para Imagens (Midjourney, DALL-E, Stable Diffusion)

Modelos de imagem de difusão não "entendem" a gramática da mesma forma que os de texto. A ordem e o vocabulário mandam:

*   **Palavras-Chave de Qualidade (Boosters):** Adicione termos como *4k, highly detailed, photorealistic, trending on artstation, masterpiece*. 
*   **Modificadores de Formato e Estilo:** Defina a mídia física. (Ex: *oil painting, 35mm photography, polaroid, 1960s comic book, studio lighting*).
*   **Negative Prompts:** Diga o que você *não quer*. Para remover distorções, use: *ugly, deformed, bad anatomy, low resolution*.
*   **Pesos (Weights):** Em Midjourney (::) e Stable Diffusion (()), você pode dar pesos às palavras. Ex: `A cat::2 and a dog::1` fará o gato ser duas vezes mais proeminente que o cachorro.
*   **Engenharia Reversa:** Não sabe descrever uma imagem? Use comandos como `/describe` no Midjourney (ou o CLIP Interrogator) fazendo upload da imagem para que a própria IA gere o prompt perfeito para você copiar.

---

## ✅ O Checklist de Mesa (Cheat Sheet)

Sempre que for criar um novo prompt profissional, passe por este checklist:

- [ ] Defini um papel/persona claro no início do prompt? (System Prompt)
- [ ] Forneci instruções dizendo o que *fazer* em vez de apenas o que *não fazer*?
- [ ] Inseri contexto relevante e excluí o lixo informacional?
- [ ] Coloquei a instrução principal e a pergunta no final do prompt para fugir do *Valley of Meh*?
- [ ] Pedi uma saída em um formato rigoroso (JSON/Markdown) para facilitar a automação?
- [ ] Mostrei pelo menos 2 exemplos (Few-shot) do que eu considero uma resposta perfeita?
- [ ] Pedi para a IA "pensar passo a passo" e mostrar a lógica antes de me dar a resposta final?
- [ ] "Forcei a largada" (Inception) escrevendo a primeira palavra da resposta esperada (Ex: `