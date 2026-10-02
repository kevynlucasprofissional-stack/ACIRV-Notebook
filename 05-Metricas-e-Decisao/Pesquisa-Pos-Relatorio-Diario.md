---
id: metrica-pesquisa-pos-relatorio-diario
titulo: Pesquisa-Pos-Relatorio-Diario
aliases: [Pesquisa do Relatorio Diario, Feedback Operacional Diario]
tipo: metrica
status: em_construcao
profundidade: avancada
versao_schema: '1.0'
versao_conteudo: '1.0'
idioma: pt-BR
data_criacao: '2026-09-23'
ultima_revisao: '2026-09-23'
grau_confianca: medio
camadas_evidencia:
- direcao_do_usuario
- fato_operacional
- interpretacao_operacional
tags:
- pesquisa
- relatorio-diario
- operacao
- feedback
notas_relacionadas:
- '[[Telemetria-do-Trabalho-Humano]]'
- '[[Sistema-Operacional-de-Marketing]]'
- '[[Ritual-Semanal-de-Priorizacao]]'
- '[[Pesquisa-e-Aprendizado-de-Marketing]]'
confidencialidade: interno
subtipo: pesquisa_recorrente
---

# Pesquisa-Pos-Relatorio-Diario

> [!summary] Síntese
> O relatório diário pode virar uma fonte longitudinal de pesquisa operacional. Depois do fechamento do dia, um registro curto captura o que mudou entre plano e realidade, por que mudou e o que deve ser ajustado. O objetivo é descobrir padrões de capacidade, bloqueio, imprevisto, retrabalho e aprendizagem — não criar score diário de produtividade.

## Evidência de continuidade

O próprio Trello já possui versões históricas de `Relatório diário` com perguntas como:
- o que cumpri?;
- o que precisou ser reagendado?;
- por qual motivo?;
- o que entrou que não estava planejado?;
- quais tarefas imprevistas apareceram e quem solicitou?

A proposta atual é transformar essa prática em coleta mais estruturada e analisável.

## Momento

Aplicar **sempre depois do relatório diário**, preferencialmente em poucos minutos, enquanto o contexto ainda está fresco.

## Instrumento mínimo

1. O que estava planejado para hoje?
2. O que foi concluído?
3. O que foi reagendado e por qual motivo?
4. Que demanda entrou sem estar planejada? De onde veio?
5. Houve bloqueio ou espera por terceiro? Qual tipo?
6. Houve retrabalho? O que o causou?
7. Que interrupção teve impacto material no fluxo?
8. Qual aprendizado ou ajuste deve ser levado para o próximo dia/semana?
9. Existe algo que precisa de escalonamento, decisão ou cobrança?
10. Qual informação faltou para executar melhor?

As respostas podem ser estruturadas em categorias, mas deve existir espaço curto para contexto.

## Variáveis derivadas

Depois de acumular dados suficientes, calcular em nível agregado:
- taxa de conclusão do planejado;
- proporção de demanda imprevista;
- motivos de reagendamento;
- frequência de bloqueios;
- tipos de dependência;
- recorrência de retrabalho;
- fontes de interrupção;
- volume de escalonamentos;
- aprendizados recorrentes.

Esses indicadores não equivalem a produtividade individual.

## Uso na gestão

A análise semanal deve responder:
- o planejamento está realista?;
- que dependências mais bloqueiam?;
- quais demandas entram fora do fluxo?;
- onde há retrabalho evitável?;
- quais atividades absorvem capacidade sem aparecer no planejamento?;
- qual regra/processo deveria mudar?

A análise mensal pode alimentar [[Ritual-Mensal-de-Metricas]] e o desenho de [[Telemetria-do-Trabalho-Humano]].

## Hermes Work

O Hermes Work pode:
- abrir/atualizar o arquivo local do dia;
- normalizar categorias;
- preservar texto bruto localmente quando houver dado identificável;
- consolidar tendências;
- gerar resumo semanal;
- sugerir hipóteses de melhoria;
- cruzar com Trello, eventos e outras fontes quando a semântica for compatível.

O GitHub deve receber apenas metodologia, agregados, decisões e aprendizados que mereçam promoção canônica.

## Guardrails

- não transformar o registro diário em vigilância contínua;
- não atribuir causa sem contexto;
- não comparar pessoas com tarefas diferentes usando volume bruto;
- não publicar dados individuais;
- não confundir “trabalho não planejado” com trabalho desnecessário;
- manter a possibilidade de registrar contexto excepcional.

## Estado operacional

Foi criado em 23/09/2026 um cartão no Trello `ACIRV + VCOM: SCRUM`, lista `Repositório GERAL`, para desenhar e implementar este ciclo.
