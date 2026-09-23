---
id: projeto-sudoexpo-match
titulo: SudoExpo-Match
aliases: [ACIRV Connect]
tipo: projeto
status: em_revisao
profundidade: avancada
versao_schema: '1.0'
versao_conteudo: '1.1'
idioma: pt-BR
data_criacao: '2026-09-22'
ultima_revisao: '2026-09-22'
grau_confianca: medio_alto
camadas_evidencia:
- fato_documentado
- interpretacao_operacional
- hipotese_de_trabalho
tags:
- sudoexpo
- networking
- produto
- match
fontes_documentais:
- '000-Arquivos-originais/Dados para mega-relatório pós Sudoexpo/Contexto conversas do zap.md'
- '000-Arquivos-originais/Dados para mega-relatório pós Sudoexpo/CONTEXTO_UNIFICADO_SUDOEXPO_MATCH.md'
- '[[SudoExpo-2026]]'
- '000-Arquivos-originais/210926 Reunião com equipe de Marketing.md'
notas_relacionadas:
- '[[SudoExpo-2026]]'
- '[[Cafe-Entre-Amigos]]'
- '[[Conecta-ACIRV]]'
- '[[SudoExpo-Match-Metodologia-de-Avaliacao]]'
- '[[Check-In-Inteligente-de-Eventos]]'
confidencialidade: interno
subtipo: produto_experimento
---

# SudoExpo-Match

> [!summary] Síntese
> O SudoExpo Match foi um experimento de networking digital associado à SudoExpo 2026: participantes declaravam quem eram e o que buscavam, o sistema gerava oportunidades de conexão e a decisão permanecia humana. O projeto começou com o nome **ACIRV Connect**, foi renomeado para evitar confusão com o Conecta ACIRV e teve uma fase inicial observável no Café Entre Amigos de 27/08 antes da feira de 09–12/09. O produto deve ser avaliado por adoção, relevância percebida e progressão de conexões — não por promessa de venda automática.

## Problema que o produto tenta resolver

Eventos empresariais geram grande volume de pessoas, mas o networking depende de:

- descobrir quem está presente;
- entender quem pode ser relevante;
- iniciar contato;
- converter encontro casual em conversa útil.

O Match tenta reduzir essa fricção tornando a descoberta de oportunidades mais estruturada.

A lógica registrada no contexto de WhatsApp pode ser resumida como:

> **“eu digo quem sou e digo o que quero”.**

Essas informações alimentam o processo de matching.

## Evolução do nome

O projeto foi inicialmente chamado **ACIRV Connect**.

Em **21/08/2026**, o nome foi alterado para **SudoExpo Match** para reduzir confusão com o projeto já existente [[Conecta-ACIRV]].

Essa mudança é importante porque diferencia:

- **Conecta ACIRV:** iniciativa/evento institucional de networking;
- **SudoExpo Match:** produto/experimento digital de recomendação e conexão.

Eles podem se complementar, mas não são o mesmo projeto.

## Jornada de produto

A jornada conceitual é:

**Cadastro → Declaração de perfil/necessidade → Match → Decisão humana → Interesse mútuo → Conexão → Continuidade**

O sistema organiza oportunidades; ele não elimina a decisão da pessoa.

## Matchmaker

O contexto técnico registra um mecanismo de score para estimar compatibilidade.

Duas regras devem permanecer explícitas:

1. o score é **direcional**;
2. score alto é hipótese de relevância, não prova de resultado comercial.

A avaliação quantitativa está em [[SudoExpo-Match-Metodologia-de-Avaliacao]].

## Integração físico-digital

No Café Entre Amigos de 27/08, o contexto de WhatsApp registra que o indicador de **“conexões concluídas”** dependia de confirmação no mapa físico — os pinos das pessoas conectadas deveriam ser colocados no mapa.

Isso significa que, naquele estágio do produto, “concluída” não era necessariamente sinônimo de um simples clique ou aceite digital.

Consequência analítica:

> antes de comparar status de conexão entre Café, SudoExpo e períodos posteriores, verificar se a regra de conclusão permaneceu igual.

Uma mudança de regra pode alterar o número sem que o comportamento humano tenha mudado na mesma proporção.

## Café Entre Amigos — 27/08/2026

O Café funciona como primeira janela histórica relevante de uso/medição.

Há registro textual de que existiam “Resultados do Café Entre Amigos de hoje”, porém os números estavam em mídia oculta no export de WhatsApp. O pacote posterior adiciona base e pesquisa que permitem reconstrução mais segura.

Para atribuição histórica, a regra operacional atual classifica perfis criados em 27/08 como:

`origem_estimada = Café Entre Amigos`.

Ver [[Cafe-Entre-Amigos]].

## SudoExpo — 09 a 12/09/2026

A feira é a principal janela de escala do experimento.

A meta contextual registrada é **300 cadastros**. A avaliação não deve parar em “bateu/não bateu a meta”; precisa observar:

- aquisição;
- fricção de cadastro;
- pessoas que realmente avaliaram oportunidades;
- interesse;
- reciprocidade;
- conexão;
- continuidade depois do evento.

## Aquisição presencial

Os briefings registram abordagem ativa de visitantes e expositores para incentivar cadastro. Também há estimativa contextual de cerca de 30 cadastros após abordagem presencial.

Esse dado deve permanecer como **relato de operação**, não como causalidade comprovada, salvo identificação verificável da origem.

## Hipóteses de comportamento

Os briefings levantaram ideias sobre usuários:

- mais permissivos;
- mais seletivos;
- concentração de conexões em poucos participantes;
- maior interesse em matches de score alto.

Essas hipóteses são úteis porque geram perguntas testáveis, mas não devem ser incorporadas como perfil real dos usuários antes da recomputação.

## O que significa sucesso

O produto pode gerar valor em estágios diferentes:

### Adoção

Pessoas entram e completam o cadastro.

### Descoberta

O sistema apresenta oportunidades que não seriam óbvias.

### Relevância

A pessoa demonstra interesse nas oportunidades.

### Reciprocidade

Duas partes sinalizam interesse.

### Conexão

O relacionamento avança para contato/ação.

### Resultado posterior

A conexão produz parceria, venda, indicação, aprendizado ou outro valor.

O sistema atual mede melhor os estágios iniciais e intermediários. Resultado econômico exige follow-up.

## O que não afirmar sem evidência

- “a IA acertou”;
- “o algoritmo gerou vendas”;
- “match = negócio”;
- ROI;
- valor econômico movimentado;
- taxa final de sucesso baseada apenas em status interno;
- causalidade de aquisição sem fonte.

## Próximo ciclo — Café Entre Amigos

A reunião de marketing de **21/09/2026** reposiciona o Match como frente ativa para o próximo [[Cafe-Entre-Amigos]], e não apenas como memória da SudoExpo.

Foram registrados dois direcionamentos:

- melhorar o SudoExpo Match;
- no próximo Café, operar o Match **apenas para associados**.

A restrição “apenas para associados” é tratada aqui como **escopo da próxima edição**, porque a fonte não estabelece que o produto inteiro tenha mudado permanentemente de público.

O mesmo ciclo prevê testar [[Check-In-Inteligente-de-Eventos]], criando a possibilidade de relacionar presença, recorrência e uso do Match sem misturar automaticamente as duas bases.

Perguntas para a próxima edição:

1. a restrição a associados melhora qualidade dos matches ou reduz descoberta?
2. qual proporção dos presentes realmente usa o produto?
3. o check-in permite medir uso sem criar fricção adicional?
4. quais melhorias do pós-SudoExpo foram efetivamente incorporadas?

> Fonte: `000-Arquivos-originais/210926 Reunião com equipe de Marketing.md` — blob `308a5c51194de989dc931e7fd15d2196685fa21d`.

## Próxima evolução orientada por pesquisa

O produto deve ser melhorado combinando:

- telemetria;
- decisões dos usuários;
- pesquisa de satisfação;
- entrevistas;
- benchmarking de outras formas de networking;
- follow-up das conexões.

Perguntas prioritárias:

1. o cadastro é simples o suficiente?
2. os matches são compreendidos?
3. o usuário sabe por que aquela pessoa apareceu?
4. score alto se associa a maior interesse?
5. o que faz uma pessoa ignorar uma oportunidade?
6. quantas conexões continuam depois do evento?
7. que parte do processo ainda exige mediação humana?

## Relações justificadas

- [[SudoExpo-2026]] — contexto de escala.
- [[Cafe-Entre-Amigos]] — janela inicial de adoção.
- [[Conecta-ACIRV]] — iniciativa institucional distinta de networking.
- [[SudoExpo-Match-Metodologia-de-Avaliacao]] — regras quantitativas.

## Fontes e rastreabilidade

- `000-Arquivos-originais/Dados para mega-relatório pós Sudoexpo/Contexto conversas do zap.md` — blob `55dc5567f601d73606f472bca4fb8f80a2a4a9d9`.
- `000-Arquivos-originais/Dados para mega-relatório pós Sudoexpo/CONTEXTO_UNIFICADO_SUDOEXPO_MATCH.md` — blob `0c1646de1a7281768f635ef31f66a2f5f0d37937`.
- `000-Arquivos-originais/Dados para mega-relatório pós Sudoexpo/210926 - sudoexpo-match-base-completa.json` — blob `13ef630ee0bde374d73cf4715fd8148ac9ed3df7`.

## Limitações e revisão

O projeto está em `em_revisao` porque o pós-evento ainda exige recomputação do banco, análise das pesquisas e follow-up de conexões. A próxima promoção deve acrescentar resultados calculados e mudanças de produto realmente confirmadas.
