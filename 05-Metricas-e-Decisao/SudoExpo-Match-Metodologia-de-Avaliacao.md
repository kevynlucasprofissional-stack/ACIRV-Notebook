---
id: metrica-sudoexpo-match-metodologia-de-avaliacao
titulo: SudoExpo-Match-Metodologia-de-Avaliacao
aliases: [Metodologia de Avaliacao do SudoExpo Match]
tipo: metrica
status: auditado
profundidade: avancada
versao_schema: '1.0'
versao_conteudo: '1.0'
idioma: pt-BR
data_criacao: '2026-09-22'
ultima_revisao: '2026-09-22'
grau_confianca: alto
camadas_evidencia:
- fato_documentado
- interpretacao_operacional
- hipotese_de_trabalho
tags:
- sudoexpo
- match
- metricas
- privacidade
fontes_documentais:
- '000-Arquivos-originais/Dados para mega-relatório pós Sudoexpo/CONTEXTO_UNIFICADO_SUDOEXPO_MATCH.md'
- '000-Arquivos-originais/Dados para mega-relatório pós Sudoexpo/210926 - sudoexpo-match-base-completa.json'
- '[[Contexto-Mega-Relatorio-Pos-SudoExpo]]'
notas_relacionadas:
- '[[SudoExpo-2026]]'
- '[[Cafe-Entre-Amigos]]'
- '[[Politica-Editorial-de-Evidencia]]'
- '[[Qualidade-dos-Dados-de-Marketing]]'
confidencialidade: interno
subtipo: metodologia_analitica
---

# SudoExpo-Match-Metodologia-de-Avaliacao

> [!summary] Síntese
> O SudoExpo Match deve ser avaliado como um funil de comportamento e conexão, não como uma contagem única de “matches”. A base permite medir aquisição, oportunidades apresentadas, decisões humanas e progressão de conexões; negócio fechado, receita e ROI exigem acompanhamento posterior. Esta nota fixa as regras semânticas para que análises futuras sejam comparáveis e não transformem hipóteses do briefing em resultados.

## O que o sistema pode demonstrar

Depois de recalculados diretamente da base bruta, são elegíveis para uso como **dados calculados**:

1. perfis cadastrados;
2. matches gerados;
3. usuários que avaliaram matches;
4. decisões de interesse e “agora não”;
5. interesses mútuos;
6. conexões registradas e seus estados;
7. tempo entre cadastro, decisão e conexão, quando os timestamps permitirem.

Esses eventos descrevem comportamento **dentro do sistema**. Uma conexão registrada não equivale, por si só, a venda, contrato, parceria realizada ou valor econômico movimentado.

## Reconstrução temporal

A modelagem histórica possui uma limitação conhecida: o Café Entre Amigos não foi corretamente separado por `event_id` em todos os registros. Por isso, a origem não deve ser reconstruída apenas pelo identificador de evento.

Regra analítica atual:

- perfil criado em **27/08/2026** → `origem_estimada = Café Entre Amigos`;
- perfil criado entre **09/09/2026 e 12/09/2026** → `origem_estimada = SudoExpo`;
- demais datas → outro período ou classificação específica, se houver evidência adicional.

A palavra **estimada** é parte da informação. Ela impede que uma regra de reconstrução vire um fato histórico inexistente no banco.

## Score e decisão humana

O score do Matchmaker é **direcional**. O score de A para B pode ser diferente do score de B para A. Toda análise de aceitação deve associar a decisão ao score visto da perspectiva de quem tomou aquela decisão.

Há duas convenções que não devem ser confundidas:

- classificação histórica de interface documentada: **75+ = alta compatibilidade; 40–74 = boa oportunidade; abaixo de 40 = conexão possível**;
- threshold analítico adotado no estudo pós-evento: **score >= 80** para testar “alta compatibilidade”.

O threshold de 80 é uma decisão metodológica de análise, não uma reescrita da classificação histórica do produto.

## Hipóteses que ainda precisam ser testadas

O briefing pós-evento sugeriu a existência de usuários mais **permissivos** e mais **seletivos**, além de alegações como forte concentração de conexões em poucos usuários e elevada aceitação de scores altos entre usuários seletivos.

Esses pontos permanecem **hipóteses de trabalho**. A análise correta deve primeiro observar a distribuição de comportamento por usuário — taxa de interesse, volume de decisões, quartis ou clusters — e só depois definir grupos. Não se deve criar a categoria e, em seguida, usar a própria categoria para “provar” a hipótese.

Pergunta analítica central:

> **quanto maior o score atribuído à oportunidade, maior a probabilidade de interesse humano do participante correspondente?**

Essa pergunta é mais informativa do que afirmar que “a IA acertou”, porque permite medir associação entre previsão e comportamento sem transformar correlação em prova causal.

## Funil canônico

A leitura padrão do produto é:

**Cadastro → Match apresentado → Decisão → Interesse mútuo → Conexão registrada → Evolução da conexão → Follow-up comercial**

Cada etapa responde a uma pergunta diferente:

- **Cadastro:** conseguimos colocar pessoas no sistema?
- **Match:** o sistema conseguiu gerar oportunidades?
- **Decisão:** as pessoas consideraram as oportunidades relevantes?
- **Interesse mútuo:** houve reciprocidade?
- **Conexão:** a oportunidade avançou para contato/relacionamento?
- **Follow-up:** houve resultado comercial ou institucional depois?

A última etapa não pode ser inferida apenas dos eventos internos atuais.

## Meta de 300 cadastros

A referência de **300 cadastros** é meta contextual do projeto. O resultado deve ser lido junto com:

- janela de ativação;
- mecanismo de aquisição;
- capacidade de abordagem presencial;
- fricções de cadastro e uso;
- disponibilidade da equipe;
- exposição do Match dentro do estande e da feira.

Diferença entre meta e realizado não deve ser convertida automaticamente em avaliação individual ou causa única.

## Pesquisa de satisfação é outra camada

As pesquisas do Café Entre Amigos e da SudoExpo são fontes de **percepção declarada**. Elas complementam o comportamento observado no sistema, mas não devem ser misturadas silenciosamente com telemetria.

Quando uma pessoa avalia negativamente uma funcionalidade que declara não ter conhecido ou usado, a resposta não deve ser simplesmente descartada. Ela pode indicar problema de descoberta, comunicação ou exposição. O tratamento precisa ser explicitado antes do cálculo.

## Privacidade

A base contém dados pessoais. Em apresentações, relatórios e notas derivadas:

- trabalhar com agregados;
- anonimizar participantes;
- não expor telefone, e-mail ou outro identificador desnecessário;
- evitar rankings nominais de usuários;
- guardar tabelas intermediárias auditáveis sem ampliar acesso ao dado bruto.

## Linguagem de evidência

Preferir:

- “o sistema registrou”;
- “a base indica”;
- “a análise encontrou”;
- “houve associação entre”;
- “o usuário demonstrou interesse”;
- “origem estimada pela data de cadastro”.

Evitar:

- “o algoritmo provou”;
- “a IA acertou”;
- “o aplicativo gerou vendas”;
- “a conexão virou negócio”;
- atribuições causais de cadastro sem fonte específica.

## Próxima promoção de resultados

Antes de transformar números do Match em resultado canônico:

1. recalcular a base JSON diretamente;
2. documentar filtros e regras;
3. gerar tabelas intermediárias auditáveis;
4. comparar Café × SudoExpo sem apagar a incerteza de origem;
5. testar score × decisão;
6. analisar concentração e seletividade sem pressupor os grupos;
7. separar conexão de resultado comercial;
8. realizar follow-up quando a pergunta for ROI ou negócio realizado.

## Fontes e rastreabilidade

- `000-Arquivos-originais/Dados para mega-relatório pós Sudoexpo/CONTEXTO_UNIFICADO_SUDOEXPO_MATCH.md` — blob `0c1646de1a7281768f635ef31f66a2f5f0d37937`.
- `000-Arquivos-originais/Dados para mega-relatório pós Sudoexpo/210926 - sudoexpo-match-base-completa.json` — blob `13ef630ee0bde374d73cf4715fd8148ac9ed3df7`.
- `[[Contexto-Mega-Relatorio-Pos-SudoExpo]]` — consolidação de trabalho de 21/09/2026.

## Limitações e revisão

Esta nota governa a **metodologia**. Ela não certifica os totais preliminares registrados em briefings ou contextos. Os resultados quantitativos só devem ser promovidos depois de recomputados na fonte bruta.
