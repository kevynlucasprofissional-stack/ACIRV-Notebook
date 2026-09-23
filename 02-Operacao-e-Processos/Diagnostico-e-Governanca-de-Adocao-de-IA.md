---
id: processo-diagnostico-e-governanca-de-adocao-de-ia
titulo: Diagnostico-e-Governanca-de-Adocao-de-IA
aliases: [Governanca de Adocao de IA, Diagnostico de IA]
tipo: processo
status: auditado
profundidade: avancada
versao_schema: '1.0'
versao_conteudo: '1.0'
idioma: pt-BR
data_criacao: '2026-09-22'
ultima_revisao: '2026-09-22'
grau_confianca: medio_alto
camadas_evidencia:
- recurso_pedagogico
- interpretacao_operacional
- hipotese_de_trabalho
tags:
- ia
- governanca
- diagnostico
- automacao
fontes_documentais:
- '000-Arquivos-originais/Dados para mega-relatório pós Sudoexpo/Material Balestrin/Perguntas pesquisa do Balestrin.md'
- '[[Contexto-Mega-Relatorio-Pos-SudoExpo]]'
notas_relacionadas:
- '[[Estrategia-ACIRV-2026]]'
- '[[Politica-Editorial-de-Evidencia]]'
- '[[Riscos-Operacionais]]'
- '[[Pesquisa-e-Aprendizado-de-Marketing]]'
confidencialidade: interno
subtipo: governanca_tecnologia
---

# Diagnostico-e-Governanca-de-Adocao-de-IA

> [!summary] Síntese
> A adoção de IA na ACIRV deve começar por problema, valor, risco e capacidade — não por ferramenta ou compra de infraestrutura. O material de 100 perguntas de maturidade funciona como referência para diagnosticar a organização, escolher pilotos e criar governança. Ele não comprova a maturidade atual da ACIRV e não deve ser usado como score institucional sem aplicação formal.

## O que o material de referência oferece

O diagnóstico compilado no material Balestrin/iGPRO contém **100 perguntas em 12 dimensões**:

1. estratégica;
2. governança;
3. integridade;
4. segurança;
5. cultura;
6. dados;
7. investimento;
8. tecnologia;
9. pessoas;
10. projetos;
11. relacionamento;
12. operação.

A utilidade dessa estrutura é impedir que “adotar IA” seja reduzido a escolher um modelo ou assinar uma ferramenta. A capacidade depende também de decisão, dados, pessoas, controles, custo, segurança e aprendizado.

## Regra de interpretação

As perguntas são um **instrumento de diagnóstico externo**. Elas não autorizam concluir que a ACIRV:

- possui governança formal de IA;
- está em determinado nível de maturidade;
- cumpre controles específicos;
- possui infraestrutura suficiente;
- já demonstra ROI;
- deveria investir imediatamente em hardware ou plataforma.

Essas conclusões exigem aplicação, evidência e decisão interna.

## Quatro gates para qualquer iniciativa de IA

### Gate 1 — Problema e valor

Antes de escolher tecnologia:

- qual tarefa ou decisão está ruim hoje?
- quem sente o problema?
- quanto tempo, retrabalho, erro ou espera existe?
- o benefício proposto é percebido pela área usuária?
- existe alternativa mais simples que IA?

Sem problema relevante, a iniciativa não avança apenas porque é tecnicamente interessante.

### Gate 2 — Dados, autoridade e risco

Antes de permitir ação:

- quais dados entram?
- quem pode acessá-los?
- há dados pessoais, confidenciais ou estratégicos?
- a ação pode ser revertida?
- qual erro é tolerável?
- qual ação exige aprovação humana?
- o sistema registra evidência suficiente para auditoria?

Casos de maior impacto precisam de mais supervisão e verificabilidade.

### Gate 3 — Piloto mensurável

O piloto deve ter:

- escopo pequeno;
- usuário real;
- tarefa definida;
- baseline anterior;
- critério de sucesso;
- registro de erro e exceção;
- revisão humana;
- prazo para decidir continuar, ajustar ou encerrar.

O resultado do piloto deve medir valor real, não apenas quantidade de chamadas, tokens, tarefas internas ou métricas produzidas pelo próprio agente.

### Gate 4 — Escala e infraestrutura

Somente depois de valor e uso comprovados entram decisões como:

- padronização;
- integração corporativa;
- orçamento recorrente;
- capacidade local ou nuvem;
- hardware dedicado;
- continuidade de fornecedor;
- treinamento amplo;
- governança mais formal.

Infraestrutura é consequência de demanda demonstrada, não ponto de partida.

## Diagnóstico curto recomendado para a ACIRV

Em vez de aplicar imediatamente as 100 perguntas, a primeira rodada pode responder cinco blocos.

### 1. Dores

- quais tarefas mais consomem tempo?
- onde há retrabalho?
- onde a informação fica presa em pessoas?
- onde a equipe troca entre muitos sistemas?
- quais tarefas têm erro recorrente?

### 2. Valor percebido

- o que seria melhor: velocidade, qualidade, redução de erro, padronização, atendimento, capacidade ou receita?
- qual ganho seria suficiente para justificar mudança de processo?
- em quais tarefas IA não é desejada?

### 3. Adoção

- quais ferramentas já são usadas?
- para quê?
- onde funcionam?
- onde falham?
- que treinamento ou interface reduziria barreira?

### 4. Confiança e risco

- quais dados não podem sair da organização?
- quais ações precisam de aprovação?
- quais erros são críticos?
- que evidência faria a equipe confiar numa automação?

### 5. Priorização

- top 3 problemas;
- top 3 casos de uso;
- top 3 benefícios esperados;
- top 3 riscos;
- áreas dispostas a pilotar;
- resultado mínimo que provaria valor.

## Hermes Work: enquadramento correto

Os materiais atuais registram desenvolvimento e uso operacional do Hermes Work, inclusive ideias de browser, automação e compilação de experiência. Isso sustenta sua existência como **proposta técnica em desenvolvimento**, não um business case institucional concluído.

Até haver benchmark e piloto controlado, não tratar como fato comprovado:

- economia percentual de tempo;
- economia de tokens;
- ganho de produtividade;
- confiabilidade superior;
- ROI;
- redução financeira;
- substituição segura de fluxos atuais.

O enquadramento canônico é:

> **candidato a piloto e hipótese de capacidade que precisa provar valor em tarefas reais da ACIRV.**

## Centro de processamento

A ideia de infraestrutura própria de IA permanece hipótese estratégica. Antes de defender investimento, devem existir evidências sobre:

- demanda;
- casos de uso;
- frequência;
- sensibilidade dos dados;
- custo de API/nuvem atual;
- custo total de hardware;
- energia, refrigeração, rede e manutenção;
- governança de acesso;
- capacidade efetivamente necessária.

A pergunta correta é **“a demanda comprovada justifica infraestrutura própria?”**, não “qual máquina comprar?”.

## Eventos como ambiente de aprendizado

Eventos de capacitação em IA podem ser usados como ambiente de observação e pesquisa **se houver acordo com o organizador, base legal e consentimento adequados**. Participação do público em um evento não implica autorização automática para pesquisa, demonstração de outros sistemas ou coleta adicional de dados.

## Ciclo de governança

**Problema → Pesquisa → Priorização → Piloto → Evidência → Decisão → Escala ou encerramento**

Esse ciclo deve permitir tanto confirmar quanto invalidar uma proposta.

## Fontes e rastreabilidade

- `000-Arquivos-originais/Dados para mega-relatório pós Sudoexpo/Material Balestrin/Perguntas pesquisa do Balestrin.md` — blob `3b3e4d727b6b07ce054bbafa6550fdb6236e5d17`.
- `[[Contexto-Mega-Relatorio-Pos-SudoExpo]]` — enquadramento do Hermes Work e da hipótese de infraestrutura.
- Briefings do mega-relatório pós-SudoExpo — visão e propostas em estágio de hipótese.

## Limitações e revisão

Esta nota não substitui política jurídica, de LGPD ou segurança da informação. O diagnóstico precisa ser aplicado antes de qualquer classificação de maturidade da ACIRV.
