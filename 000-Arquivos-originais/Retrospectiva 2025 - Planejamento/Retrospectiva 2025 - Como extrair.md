---
Modificado:
  - sexta-feira 332 28/11/2025
Criado: sexta-feira 332 28/11/2025
---
Esta é uma excelente abordagem. Para um presidente que foca em ROI e dados, histórias vagas não funcionam; ele precisa ver o "lucro" institucional que a gestão trouxe.

Como os dados são massivos e virão de fontes "sujas" (conversas de WhatsApp misturadas com legendas de Instagram), precisamos de um **Prompt de Mineração (Extração)** rigoroso e um **Prompt de Consolidação (Síntese)** analítico.

Aqui está a estratégia dividida em dois passos.

### Passo 1: O Minerador de Dados (Prompt de Extração)

Este prompt deve ser usado em cada "pedaço" de texto que você inserir no chat. Ele ignora "bom dia/boa tarde", fofocas ou ruídos e foca puramente em fatos e métricas.

**Copie e cole este prompt antes de cada bloco de dados:**

Atue como um Analista de Dados Sênior da ACIRV.

Estou fornecendo um fragmento de dados brutos (conversas de WhatsApp, legendas de Instagram, relatórios internos). Sua missão é ignorar conversas informais e extrair exclusivamente dados concretos, datas e indicadores de performance (KPIs).

O objetivo final é montar um relatório para uma presidência focada em ROI e números exatos.

Extraia e estruture as informações APENAS se elas aparecerem neste texto, seguindo rigorosamente o formato abaixo:

1. Registro de Eventos e Ações (Tabela Cronológica)
Liste cada evento encontrado. Se a data exata não estiver clara, estime pelo contexto (ex: "postado em maio") ou marque como "Data a confirmar".
*   Data: DD/MM/AAAA
*   Nome do Evento/Ação: (Ex: Café entre Amigos, Conecta, Festival Barzim, Reunião de Diretoria).
*   Categoria: (Networking, Institucional, Festivo, Vendas, Educação).
*   Métricas Chave (DADOS): Extraia qualquer número associado (Público presente, valor arrecadado, número de expositores, leads gerados, visualizações/engajamento na mídia). Se não houver números, escreva "N/D".
*   Status/Resultado: (Ex: "Sucesso de público", "Esgotado", "Lançamento realizado").

2. Contagem de Itens Específicos (Acumulador)
Identifique se este texto menciona a ocorrência ou números dos seguintes itens específicos:
*   Novos Associados (Qtd):
*   Edições do "Café entre Amigos":
*   Edições do "Conecta":
*   Edições do "Festival Barzim e Violão":
*   Outros eventos proprietários:

3. Destaques de ROI e Mídia
*   Citações de crescimento financeiro ou economia.
*   Menções de alcance orgânico alto (viralização, cobertura de imprensa).
*   Feedback qualitativo de alto impacto (elogios de autoridades, grandes empresários).

Regra de Ouro: Seja frio e calculista. Não invente dados. Se o texto diz "tivemos muita gente", extraia "Grande público (sem número exato)". Se diz "150 pessoas", extraia "150".

---

### Passo 2: O Estrategista (Prompt de Síntese)

Depois de rodar o primeiro prompt várias vezes e guardar as respostas (em um documento Word ou Bloco de Notas), você terá uma lista longa de dados extraídos. Agora, você vai colar todos esses resumos de uma vez (ou em grandes blocos) e usar este prompt para criar o relatório final.

**Prompt:**

Atue como um Consultor Estratégico preparando uma apresentação para o Presidente da ACIRV.

Abaixo, vou colar os dados extraídos e fragmentados de todo o período. Sua tarefa é consolidar, somar e organizar essas informações em uma Linha do Tempo Mestra e um Dashboard de Resultados, focando em provar o valor (ROI) da gestão.

O Presidente é cético e orientado a dados. Use linguagem executiva.

Realize as seguintes tarefas:

1. O "Big Data" da Gestão (Somatória Total)
Analise todos os fragmentos e me dê os números totais estimados. Se houver conflito de dados, use o mais conservador ou note a divergência.
*   Total de Eventos Realizados: (Soma geral).
*   Total de Novos Associados: (Soma identificada).
*   Raio-X dos Programas:
*   Café entre Amigos: Qtd total edições | Estimativa total de público.
*   Conecta: Qtd total edições.
*   Festival Barzim e Violão: Qtd total edições | Resultados de destaque.
*   Performance de Mídia: Resumo do alcance e presença digital baseada nos dados.

2. A Linha do Tempo Mestra (Cronologia)
Organize os principais marcos em ordem cronológica (do mais antigo ao mais recente). Não liste cada pequena reunião, foque nos Milestones (Marcos de Sucesso).
*   Formato: Mês/Ano - Evento: O dado numérico mais impressionante deste evento.
*   Exemplo: "Março/2023 - 5º Conecta: Recorde de 300 empresários presentes."

3. Análise de ROI (Argumentos de Narrativa)
Com base nos números acima, crie 3 "Bullets Points" poderosos que o presidente possa falar em um discurso.
*   Exemplo de estrutura: "Aumentamos a base de associados em X%, o que gerou Y de receita recorrente." ou "Realizamos X eventos com custo reduzido e alto engajamento."

4. Lacunas de Dados (Auditoria)
Aponte se houver algum período de tempo (meses/anos) que parece estar vazio ou sem dados relevantes na lista fornecida, para que eu possa buscar mais informações manualmente.

### Dicas para a execução:

1.  **Limpeza Prévia:** Se você tem arquivos de log do WhatsApp muito grandes, tente remover as mídias (imagens/vídeos) e manter apenas o texto antes de jogar no GPT.
2.  **O "Homem dos Números":** Ao gerar a narrativa final depois (que não é o foco destes prompts, mas será o próximo passo), lembre-se de usar verbos de ação: *Otimizamos, Lucramos, Crescemos, Atingimos, Reduzimos custos*.
3.  **Instagram é Ouro para Datas:** Se o WhatsApp for confuso com datas, use as legendas do Instagram extraídas para ancorar a data correta dos eventos mencionados no WhatsApp. O Prompt 1 já pede para cruzar isso.