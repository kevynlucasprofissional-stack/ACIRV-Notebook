---
id: metrica-telemetria-do-trabalho-humano
titulo: Telemetria-do-Trabalho-Humano
aliases: [Metricas do Trabalho Humano, Telemetria Operacional Humana]
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
- hipotese_de_trabalho
- interpretacao_operacional
tags:
- metricas
- trabalho
- atendimento
- conexao
- telemetria
notas_relacionadas:
- '[[Pesquisa-Pos-Relatorio-Diario]]'
- '[[Matriz-de-Metricas-por-Objetivo]]'
- '[[Diagnostico-e-Governanca-de-Adocao-de-IA]]'
- '[[Sistema-Operacional-de-Marketing]]'
confidencialidade: interno
subtipo: modelo_experimental
---

# Telemetria-do-Trabalho-Humano

> [!summary] Síntese
> A ACIRV pode estudar métricas sobre atendimento, conexão, execução e fluxo de trabalho, mas a finalidade deve ser **compreender e melhorar o sistema de trabalho**, não automatizar culpa, vigilância ou julgamento de pessoas. O desenho deve começar por processos e equipes, usar contexto e qualidade junto de volume, e tratar qualquer avaliação individual como caso excepcional que exige propósito explícito, transparência e governança.

## Princípio

> **Dados para encontrar oportunidades de melhoria, não culpados.**

Mensurar pode revelar gargalos que hoje ficam invisíveis. O risco aparece quando o indicador deixa de ser instrumento de gestão e passa a ser interpretado como retrato completo da pessoa.

## Ordem de medição

Começar nesta ordem:

1. **processo/sistema** — demanda, espera, bloqueios, retrabalho, handoffs, capacidade;
2. **equipe** — distribuição de carga, qualidade coletiva, fluxo e resultado;
3. **indivíduo** — somente quando a finalidade exigir e houver contexto suficiente.

Uma métrica individual nunca deve ser presumida como medida direta de esforço, competência ou valor.

## Famílias de métricas candidatas

### Atendimento
- volume de atendimentos;
- tempo até primeira resposta;
- tempo até resolução;
- taxa de retorno/reabertura;
- necessidade de encaminhamento;
- retrabalho;
- satisfação pós-atendimento;
- temas e dúvidas recorrentes.

### Conexão
- conexões iniciadas;
- encaminhamentos realizados;
- reciprocidade/interesse;
- continuidade após o primeiro contato;
- resultado posterior quando verificável;
- participação em eventos/rede;
- qualidade percebida da conexão.

### Fluxo de trabalho
- planejado × realizado;
- proporção de trabalho imprevisto;
- itens reagendados e motivo;
- tempo bloqueado/aguardando terceiros;
- interrupções;
- WIP;
- retrabalho;
- ciclos de aprovação.

### Trabalho de marketing e execução
- entregas por objetivo, não só por quantidade;
- tempo de ciclo;
- número e natureza das revisões;
- erros factuais evitáveis;
- impacto/resultado quando mensurável;
- aprendizado gerado;
- reutilização de ativos;
- demandas extras e origem.

## Métricas que não devem operar sozinhas

Quantidade de mensagens, tarefas fechadas, horas conectadas, velocidade de resposta, volume de posts ou número de conexões podem ser úteis como contexto, mas são perigosas como score isolado. Elas podem premiar comportamento superficial e punir trabalho complexo, preventivo ou invisível.

## Anti-Goodhart

Quando um indicador vira meta de desempenho, as pessoas tendem a adaptar comportamento ao indicador. Por isso:

- combinar volume + qualidade + resultado + contexto;
- revisar efeitos adversos;
- evitar ranking simplista;
- manter campo para explicação/exceção;
- comparar períodos e processos antes de pessoas;
- auditar se a métrica está mudando o comportamento de forma indesejada.

## Papel da IA

IA pode:
- estruturar registros;
- detectar padrões;
- agrupar causas de atraso;
- gerar perguntas;
- resumir tendências;
- sugerir hipóteses de melhoria.

IA **não deve** emitir automaticamente vereditos de desempenho pessoal, culpa, competência ou mérito a partir de telemetria operacional.

## Piloto recomendado

Usar primeiro a [[Pesquisa-Pos-Relatorio-Diario]] como fonte de baixa intrusão para observar:
- imprevistos;
- bloqueios;
- retrabalho;
- dependências;
- capacidade;
- aprendizagem.

Depois de algumas semanas, avaliar quais padrões são suficientemente estáveis para merecer indicadores formais.

## Governança mínima

Antes de qualquer métrica:
- definir pergunta de gestão;
- definir unidade de análise;
- declarar fonte e fórmula;
- registrar limitações;
- decidir periodicidade;
- informar quem vê o dado;
- estabelecer prazo de retenção quando houver dado pessoal;
- impedir que dado agregado seja convertido em julgamento individual por inferência.

## Estado

Há um cartão aberto no Trello `ACIRV + VCOM: SCRUM`, lista `Repositório GERAL`, para desenhar essa frente. O desenho ainda é exploratório e não constitui política de avaliação de funcionários.

## Proveniência

Direção registrada pelo usuário em 23/09/2026, inspirada por uma discussão sobre telemetria aplicada ao trabalho e explicitamente condicionada a um uso administrativo, de melhoria contínua e não punitivo.
