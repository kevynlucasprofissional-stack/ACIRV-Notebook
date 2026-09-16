A aba **Vault** ficou interessante como MVP e já ajuda a visualizar o potencial da ideia, mas ainda precisa evoluir bastante.

No futuro, quero integrar ao Hermes Work projetos open source semelhantes ao **NotebookLM**, especialmente alternativas que possam funcionar em conjunto com o Obsidian. Inclusive, talvez faça sentido renomear a seção “Vault” para algo que represente melhor sua finalidade, como **PKM**, **Notas/Notes**, **Aprender/Learn** ou algum conceito semelhante.

A ideia é transformar essa área em um ambiente integrado de conhecimento e aprendizado, combinando elementos de:

- **Obsidian**, para organização e conexão de notas;
    
- **Anki**, com repetição espaçada;
    
- **NotebookLM**, para estudo, consulta e interação com fontes;
	
- **Atom**, para criação dos melhores flashcards de repetição espaçada;
	
- recursos de IA do próprio Hermes.
    

Ou seja, não quero que seja apenas um cofre de arquivos, mas uma espécie de sistema pessoal de conhecimento e aprendizado.

Também estou começando a considerar a integração do **K-Tools** diretamente ao Hermes Work. Em vez de permanecer como um conjunto separado de ferramentas, algumas funcionalidades poderiam se tornar recursos nativos do próprio Hermes Work.

Entre os problemas e melhorias que já identifiquei estão:

- A aba **Vault** ainda está muito inicial e precisa ser bastante aprimorada.
    
- A **visualização em grafo** atualmente não está funcionando corretamente.
    
- O ícone do Hermes Work na barra de tarefas não está sendo exibido. Atualmente aparece um ícone genérico de documento sem extensão, quando deveria utilizar o ícone personalizado que criei, com a personagem.
    

Outra possibilidade interessante seria criar um sistema semelhante aos **plugins ou conectores do ChatGPT**. O ChatGPT, por exemplo, consegue trabalhar de forma bastante integrada com ferramentas como GitHub e Lovable.

O Hermes provavelmente já conseguirá fazer boa parte disso por meio do Browser Runtime, navegando e interagindo com GitHub, Lovable, ChatGPT e outras aplicações. Ainda assim, pode valer a pena desenvolver uma camada de integrações mais estruturada, para que determinados serviços possam ser acessados de forma nativa, sem depender exclusivamente da automação pelo navegador.

Também precisamos melhorar a forma como o Hermes referencia elementos internos do sistema.

Os cartões do Kanban, por exemplo, deveriam possuir algum identificador simples e utilizável nos comandos e conversas com o agente. Poderíamos adotar algo como:

`#KB123`

ou

`KBID:123`

ou

`/nome_ou_id_do_cartao_kanban`

Assim, seria possível dizer ao Hermes algo como “execute esta tarefa usando o cartão #KB123”, “atualize o #KB123” ou “entregue o resultado no #KB123”.

Isso permitiria que cartões, projetos e outros objetos do Hermes Work fossem facilmente referenciados durante as conversas com os agentes.

### Tipos de quadros Kanban

Ao criar um novo quadro, também deveria existir uma opção para definir seu tipo.

Penso inicialmente em dois modos:

**1. Quadro de agentes**

Um quadro destinado exclusivamente à execução e ao gerenciamento de tarefas por agentes. Nesse tipo de quadro, o usuário não precisaria manipular diretamente o fluxo de trabalho. O próprio sistema e os agentes seriam responsáveis pelo ciclo de vida das tarefas.

**2. Quadro híbrido**

Um quadro compartilhado entre humanos e agentes.

Esse modo deve funcionar de maneira muito mais próxima ao Trello, permitindo ao usuário:

- criar, renomear e excluir colunas;
    
- criar e excluir cartões;
    
- mover cartões livremente entre colunas;
    
- editar títulos;
    
- adicionar descrições;
    
- organizar manualmente o quadro;
    
- permitir que agentes também criem, movimentem e atualizem cartões.
    

A diferença fundamental é que o **quadro de agentes representa o fluxo operacional dos agentes**, enquanto o **quadro híbrido funciona como um espaço colaborativo entre usuário e IA**.

Por fim, percebi também um problema no processo atual de desenvolvimento com IA: frequentemente ela implementa apenas parte do que foi solicitado inicialmente. Alguns requisitos acabam ficando de fora e precisam ser cobrados novamente em prompts posteriores.

Precisamos pensar em uma forma de reduzir esse comportamento. Idealmente, o Hermes Work deveria possuir algum mecanismo para acompanhar requisitos, subtarefas ou critérios de conclusão, permitindo verificar automaticamente se tudo o que foi solicitado realmente foi implementado antes de considerar uma tarefa concluída.

---

Nubia de Jesus
Murilo Garcia
Isabely da MP Infinity

Eu quero criar o próximo passo na evolução do motor de match, mas para isso precisamos analisar os dados que já temos. Primeiro, analise todos os interesses registrados disponíveis no repositório do Sudoexpo Match no @GitHub e perceba que vários interesses registrados são de duplas com score baixo. Faça várias perguntas inteligentes e tente responder para ir em busca da seguinte informação: Por qual motivo existe tantos interesses registrados em duplas com score tão baixo? E como podemos evoluir o motor de match para que, com base na análise dos dados que temos, possamos prever com maior precisão quais duplas realmente são compatíveis afim de criar matchs que fazem sentido, O que sinto é que se uma pessoa demonstrou interesse me outra mesmo o score sendo baixo, só pode ser uma dessas opções: A) A pessoa que clicou que tem interesse clicou sem querer ou simplesmente foi clicando "tenho interesse" sem nem ler quem era, sem considerar nada, foi clicando "tenho interesse" de forma aleatória. B) O mecanismo de score não conseguiu prever com precisão a compatibilidade dessa dupla, não conseguiu ver que ali existia um possível match.