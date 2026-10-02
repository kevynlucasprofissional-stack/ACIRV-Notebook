---
Modificado:
  - sábado 101 11/04/2026
Criado: sábado 101 11/04/2026
---
# Briefing inicial

## Briefing — Dashboard de Métricas ACIRV no Lovable

### 1. Nome do projeto

Dashboard de Métricas da ACIRV no Lovable.

### 2. Objetivo do dashboard

Criar uma página de dashboard no Lovable para centralizar os principais dados de métricas da ACIRV, com visualização em gráficos, atualização prática a partir de uma tabela-base e uso direto na apresentação do relatório de métricas. A intenção é transformar os dados recorrentes da operação em uma interface visual mais fácil de acompanhar e apresentar.

### 3. Contexto de uso

O dashboard será usado como apoio na reunião de apresentação de métricas de março e também como estrutura contínua para acompanhar os números da ACIRV ao longo do tempo. Você quer que ele sirva tanto para análise quanto para apresentação executiva.

### 4. Fonte de dados

A base dos dados deve ficar em uma **tabela Excel** que funcione como fonte central. O Lovable precisa estar integrado a essa tabela para que, sempre que ela for atualizada, os gráficos do dashboard também possam ser atualizados. No seu áudio, você fala em “tabela Excel”, então este é o requisito explicitamente mencionado no documento.

### 5. Requisito central de integração

O dashboard deve ser conectado à tabela-base de forma que os dados possam ser relidos e refletidos nos gráficos sem necessidade de reconstruir a página manualmente. A lógica desejada é: atualizou a tabela, o dashboard consegue puxar os novos números e refletir isso visualmente.

### 6. Funcionalidade obrigatória de atualização

A página precisa ter um botão de ação do tipo **“Sincronizar agora”**, para forçar a releitura da tabela e atualizar os gráficos e indicadores com os dados mais recentes. Isso foi pedido de forma explícita.

### 7. Funcionalidade obrigatória de exportação

Todos os gráficos gerados no dashboard devem poder ser salvos em **PNG**. Você citou isso como uma necessidade direta, especialmente para gráficos como quantidade de interações e quantidade de seguidores, mas a lógica vale para todos os gráficos da página.

### 8. Métricas que o dashboard deve exibir

O dashboard deve contemplar os dados que você considera “o de sempre” na reunião de métricas, incluindo: quantidade de postagens, visualizações, evolução de seguidores, quantidade de stories publicados, quantidade de vídeos produzidos, quantidade de reels publicados, número de interações, total de seguidores, quantos seguidores foram ganhos e quantos deixaram de seguir.

### 9. Visualizações esperadas

Você deixou claro que quer **gráficos** para esses dados, especialmente para acompanhar evolução e volume. Isso inclui gráficos de stories, evolução de seguidores e outros indicadores operacionais do Instagram e da produção de conteúdo. O dashboard, portanto, deve ser visualmente orientado a leitura rápida e comparação temporal.

### 10. Papel do dashboard na apresentação

Além de funcionar como ferramenta de gestão, o dashboard precisa ser “apresentável”, porque você quer mostrá-lo na reunião de relatório de métricas. Isso significa que a página não deve ser apenas funcional; ela também precisa ter aparência limpa, clara e adequada para exposição em reunião.

### 11. Escopo de conteúdo que provavelmente entra no dashboard

Pelo que você descreve, o núcleo da página deve girar em torno de métricas de comunicação e marketing da ACIRV: redes sociais, produção de conteúdo, assessoria de imprensa e, possivelmente, tráfego pago. A parte de tráfego pago aparece como um ponto relevante porque você diz que quer apresentar melhor esses dados e que Rafael está preocupado com isso.

### 12. Indicadores relacionados a tráfego pago

Embora você não tenha detalhado no trecho um conjunto fechado de KPIs de mídia paga, você deixa claro que quer melhorar a apresentação dos dados de tráfego pago e também mostrar resultado de investimento, inclusive no contexto do aporte de R$ 500 do Diney para crescimento e seguidores. Isso sugere que o dashboard pode ter uma área dedicada a performance de mídia paga.

### 13. Possível organização da página

Com base no que você falou, a página pode ser organizada em blocos como: visão geral de métricas, desempenho de conteúdo, evolução de seguidores, stories e vídeos, interações, e uma área de tráfego pago. Essa organização é uma consolidação lógica do que você pediu, não uma estrutura que você tenha nomeado exatamente dessa forma.

## Contexto estratégico que influencia o dashboard, mas não aparece como requisito técnico direto

### 14. O dashboard também nasce de uma necessidade de organizar a operação

No material, o dashboard não aparece apenas como painel bonito de métricas. Ele surge dentro de um contexto de excesso de demandas, múltiplos stakeholders e necessidade de tornar a operação mais visível, mensurável e menos caótica.

### 15. Quatro frentes de demanda impactam a leitura de resultados

Você cita quatro frentes principais enviando demandas ao mesmo tempo: José Carlos, Janaine, Viviane e Rafael. Cada uma puxa o trabalho para uma direção diferente, o que reforça a importância de um dashboard que ajude a mostrar o que está sendo produzido e o que está gerando resultado.

### 16. Há espaço para um módulo futuro de gestão operacional

Na segunda parte do material, aparecem ideias que podem virar uma segunda camada do dashboard: acompanhamento de tarefas, priorização por critérios de prioridade/dificuldade/tempo, pontuação por tarefa, quase 300 tarefas acumuladas e dado de que apenas 45% do tempo estaria sendo efetivamente produtivo por causa de interrupções e trocas de foco. Isso parece mais um **módulo futuro de gestão de operação** do que o escopo principal do dashboard de métricas.

### 17. Também existe um desejo de mostrar evolução qualitativa

Você menciona interesse em mostrar que houve evolução de cadência e qualidade no Instagram da ACIRV, comparando o cenário de um ano atrás com o atual: antes, postagem a cada dois a quatro dias; agora, quase diariamente. Esse tipo de comparação pode virar um bloco de “evolução histórica” dentro do dashboard ou da apresentação conectada a ele.

---

## Resumo executivo do briefing

Você quer um dashboard no Lovable conectado a uma tabela Excel, capaz de atualizar gráficos automaticamente, com botão de sincronização manual, exportação de todos os gráficos em PNG e foco principal nas métricas de marketing e comunicação da ACIRV. O painel deve servir tanto para acompanhamento contínuo quanto para apresentação formal na reunião de métricas. Como contexto ampliado, ele também nasce da necessidade de dar mais clareza à operação, reduzir ruído e tornar visível tanto o desempenho das ações quanto, futuramente, a sobrecarga de demandas e a lógica de priorização.

Posso transformar esse briefing no próximo passo em um **prompt pronto para o Lovable**, já estruturado para gerar a página.