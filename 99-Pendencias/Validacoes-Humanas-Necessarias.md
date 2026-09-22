---
id: pendencia-validacoes-humanas-necessarias
titulo: Validacoes-Humanas-Necessarias
aliases: []
tipo: pendencia
status: auditado
profundidade: avancada
versao_schema: '1.0'
versao_conteudo: '1.3'
idioma: pt-BR
data_criacao: '2026-06-17'
ultima_revisao: '2026-09-22'
grau_confianca: alto
camadas_evidencia:
- fato_documentado
- interpretacao_operacional
tags:
- pendencia
fontes_documentais:
- '[[Fonte - Briefing do projeto]]'
- '[[Contexto-Mega-Relatorio-Pos-SudoExpo]]'
notas_relacionadas:
- '[[Pendencias-Assumidas]]'
- '[[Riscos-Operacionais]]'
- '[[Registro-de-Decisoes]]'
- '[[SudoExpo-2026]]'
- '[[SudoExpo-Match-Metodologia-de-Avaliacao]]'
- '[[Diagnostico-e-Governanca-de-Adocao-de-IA]]'
confidencialidade: interno
subtipo: pendencia
---

# Validacoes-Humanas-Necessarias

> [!summary] Síntese
> Confirmações que dependem de responsáveis da ACIRV, decisão humana consciente ou análise ainda não concluída antes de virarem estado canônico definitivo. Esta lista existe para impedir que ambiguidade seja “resolvida” por suposição.

## Estratégia

- Confirmar metas, linhas de base, proprietários e campanhas vigentes quando ainda não houver evidência operacional suficiente.

A divergência da Campanha de Pertencimento foi resolvida em 17/09/2026: **planejada para começar em abril e iniciada efetivamente em maio de 2026**.

## Governança

Confirmar cargos, alçadas, SLA, RACI e canal oficial de aprovação quando a informação for necessária para decisão ou publicação.

## Calendário

Confirmar datas, escopo e status de eventos e campanhas quando houver divergência entre planejamento e execução real.

## Conecta ACIRV

Resoluções de 17/09/2026:

- **Cota Diamante oficial:** R$ 18.000;
- **R$ 4 milhões:** volume histórico acumulado de negócios movimentados em várias edições, não meta anual de 2026.

Promovido para [[Conecta-ACIRV]] e [[Registro-de-Decisoes]].

## SudoExpo — execução pós-evento

Validar antes de transformar em resultado fechado:

- a alegação de que **100% do planejamento definido antes da feira foi entregue**;
- quais itens pertenciam ao baseline pré-09/09;
- quais foram extras;
- quais foram pedidos tardios;
- quais itens não foram concluídos;
- em quais casos a responsabilidade de fornecedor está sustentada por evidência independente.

A validação deve usar uma matriz **Planejado × Entregue × Extra × Pedido tardio × Dependência externa**, preferencialmente cruzando briefing, mensagens e fotos.

## SudoExpo Match

Não promover como resultado sem recomputação:

- totais finais de cadastros, matches, decisões e conexões;
- hipótese de que poucos usuários geram a maior parte das conexões;
- hipótese de “permissivos” × “seletivos”;
- aceitação de scores altos;
- qualquer conclusão de negócio/ROI.

A metodologia está em [[SudoExpo-Match-Metodologia-de-Avaliacao]].

## Pesquisas pós-SudoExpo

Analisar e documentar:

- número de respostas;
- satisfação;
- conhecimento/uso do Match;
- tratamento de quem avaliou sem conhecer a funcionalidade;
- comentários e oportunidades;
- critérios de exclusão, se houver.

Não descartar respostas silenciosamente.

## Instagram julho–setembro

Reconciliar:

- agosto original;
- agosto MASTER;
- setembro;
- relatório mensal;
- definição de “Seguidores”;
- orgânico × promovido;
- coautoria;
- recorte pré-feira × feira × pós-feira.

Não atribuir causalidade à SudoExpo apenas pela coincidência temporal.

## Evento Raphael — 08/10/2026

Confirmar:

- local definitivo: Hotel Bons Tempos ou sede da ACIRV;
- papel formal da ACIRV;
- existência e natureza da parceria;
- capacidade;
- número de inscritos;
- preço;
- ferramentas usadas;
- possibilidade de pesquisa;
- consentimento e tratamento de dados;
- qualquer espaço para demonstração de outros projetos.

Até confirmação, essas informações permanecem pendentes e não devem ser apresentadas como compromisso institucional.

## IA / Hermes Work

Antes de defender adoção ampla ou investimento:

- aplicar diagnóstico de dores e casos de uso;
- definir pilotos;
- medir baseline;
- validar benefício percebido;
- registrar riscos e ações que exigem aprovação;
- produzir benchmark executivo antes de afirmar ROI, economia de tempo/tokens ou aumento de produtividade.

A ideia de centro de processamento permanece hipótese; infraestrutura própria só deve ser dimensionada depois de demonstrada demanda real.

Ver [[Diagnostico-e-Governanca-de-Adocao-de-IA]].

## Dados

Aprovar dicionário, tabela canônica e tratamento das divergências. Valores públicos de impacto devem registrar período, fonte e método.

## Marca

Resoluções validadas em 17/09/2026:

- V4.5 e V5 do tom de voz são utilizadas simultaneamente;
- V6 é visão/planejamento de evolução futura.

Promovido para [[Manual-Operacional-de-Tom-de-Voz]].

## Serviços e Consultorias

Resolução validada em 17/09/2026:

- consultorias Jurídica, Contábil, Engenharia Ambiental, Tecnologia & Inovação, Atração de Investimentos, Infraestrutura Rodoviária e Comunicação são **100% gratuitas para associados**.

Promovido para [[Servicos-e-Beneficios-da-ACIRV]].

## SudoExpo — Situação Financeira

Resolução validada em 17/09/2026:

- “complicada” era **impressão operacional qualitativa pós-reunião**, não déficit contábil formal.

Promovido para [[SudoExpo-2026]].

## Segurança

- Foi confirmado em 17/09/2026 que `000-Arquivos-originais/Contas e Senhas.md` e `000-Arquivos-originais/Minha Chave API Antropic.md` contêm credenciais reais.
- Os caminhos devem permanecer sob tratamento restrito e nunca ser abertos por agentes.
- Antes de qualquer remoção remota, preservar a cópia local conforme decisão humana.
- Credencial versionada deve ser rotacionada/revogada; remover da branch atual não elimina histórico.
- Revisar `.env` e protótipos sem expor valores.
- Migrar credenciais ativas para gerenciador de segredos.
- Avaliar reescrita de histórico apenas depois de rotação e decisão humana.
- Agentes não alteram `000-Arquivos-originais/`.

## Tecnologia

Decidir arquivar, revisar ou pilotar protótipos e separar experimento técnico de conhecimento institucional.

Prompts, logs de agente, handoffs, estados de teste e abstrações do Hermes Work **não devem ser promovidos automaticamente** para o estado institucional da ACIRV. Só decisões estáveis, princípios validados ou resultados de piloto devem atravessar essa fronteira.

## Relações justificadas

- [[Pendencias-Assumidas]] — explica origem.
- [[Riscos-Operacionais]] — prioriza risco.
- [[Registro-de-Decisoes]] — recebe confirmações resolvidas.
- [[SudoExpo-2026]] — concentra pós-evento.
- [[SudoExpo-Match-Metodologia-de-Avaliacao]] — define o que exige cálculo.
- [[Diagnostico-e-Governanca-de-Adocao-de-IA]] — governa hipóteses de IA.

## Fontes e rastreabilidade

- [[Fonte - Briefing do projeto]]
- [[Triagem-Inicial-000-Arquivos-Originais-2026-09-17]]
- [[Contexto-Mega-Relatorio-Pos-SudoExpo]]
- validações humanas de 17/09/2026.

## Limitações e revisão

Atualizar quando uma validação for resolvida ou quando nova evidência mudar o grau de certeza. Não apagar o histórico da dúvida; registrar sua resolução.
