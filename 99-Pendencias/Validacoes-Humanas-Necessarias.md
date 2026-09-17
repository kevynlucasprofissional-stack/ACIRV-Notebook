---
id: pendencia-validacoes-humanas-necessarias
titulo: Validacoes-Humanas-Necessarias
aliases: []
tipo: pendencia
status: auditado
profundidade: avancada
versao_schema: '1.0'
versao_conteudo: '1.2'
idioma: pt-BR
data_criacao: '2026-06-17'
ultima_revisao: '2026-09-17'
grau_confianca: alto
camadas_evidencia:
- fato_documentado
- interpretacao_operacional
tags:
- pendencia
fontes_documentais:
- '[[Fonte - Briefing do projeto]]'
notas_relacionadas:
- '[[Pendencias-Assumidas]]'
- '[[Riscos-Operacionais]]'
- '[[Registro-de-Decisoes]]'
- '[[Triagem-Inicial-000-Arquivos-Originais-2026-09-17]]'
confidencialidade: interno
subtipo: pendencia
---

# Validacoes-Humanas-Necessarias

> [!summary] Síntese
> Lista de confirmações que dependem de responsáveis da ACIRV ou de decisão humana consciente antes de serem tratadas como estado canônico.

## Estratégia

- Confirmar metas, linhas de base, proprietários e campanhas vigentes quando ainda não houver evidência operacional suficiente.

A divergência da Campanha de Pertencimento foi resolvida em 2026-09-17: **planejada para começar em abril e iniciada efetivamente em maio de 2026**. A resolução foi promovida para `[[Campanha-Eu-Faco-Parte]]` e `[[Registro-de-Decisoes]]`.

## Governança

Confirmar cargos, alçadas, SLA, RACI e canal oficial de aprovação.

## Calendário

Confirmar datas, escopo e status de eventos e campanhas quando houver divergência entre planejamento e execução real.

## Conecta ACIRV

As divergências identificadas na triagem inicial foram resolvidas em 2026-09-17:

- **Cota Diamante oficial**: R$ 18.000;
- **R$ 4 milhões**: volume histórico acumulado de negócios movimentados ao longo de várias edições do Conecta, e não meta anual de 2026.

As resoluções foram promovidas para `[[Conecta-ACIRV]]` e `[[Registro-de-Decisoes]]`.

## Dados

Aprovar dicionário, tabela canônica e tratamento das divergências. Valores públicos de impacto devem registrar período, fonte e método sempre que essas informações estiverem disponíveis.

## Marca

Resoluções validadas em 2026-09-17:
- **Manuais de Tom de Voz vigentes**: As versões **V4.5** e **V5** são utilizadas simultaneamente no cotidiano operacional da equipe.
- **Versão V6**: Constitui uma visão/planejamento de evolução futura da marca.

Promovido para `[[Manual-Operacional-de-Tom-de-Voz]]`.

## Serviços e Consultorias

Resolução validada em 2026-09-17:
- **Gratuidade**: Todas as consultorias oferecidas pela ACIRV (Jurídica, Contábil, Engenharia Ambiental, Tecnologia & Inovação, Atração de Investimentos, Infraestrutura Rodoviária e Comunicação) são **100% gratuitas para associados**.

Promovido para `[[Servicos-e-Beneficios-da-ACIRV]]`.

## SudoExpo — Situação Financeira

Resolução validada em 2026-09-17:
- O termo "complicada" anotado em 03/08/2026 refere-se à **impressão operacional qualitativa pós-reunião de diretoria** sobre os números do evento, e não a déficit contábil formal.

Promovido para `[[SudoExpo-2026]]`.

## Segurança

- Foi confirmado em 2026-09-17 que `000-Arquivos-originais/Contas e Senhas.md` e `000-Arquivos-originais/Minha Chave API Antropic.md` contêm credenciais reais.
- Os dois caminhos devem permanecer **somente locais** e estão destinados ao `.gitignore`.
- Antes de removê-los do GitHub, é obrigatório executar no clone local um `git rm --cached` dos dois caminhos e verificar que os arquivos físicos continuam existindo no disco; a remoção remota não deve ocorrer antes dessa confirmação.
- Rotacionar/revogar qualquer credencial real que tenha sido versionada, pois removê-la da branch atual não elimina versões históricas do Git.
- Revisar `.env` e artefatos de protótipos sem expor valores em notas, issues ou PRs.
- Migrar credenciais ativas para gerenciador de segredos.
- Avaliar reescrita de histórico Git após rotação quando houver necessidade de eliminar segredos de commits antigos.
- Manter a regra de que agentes **não abrem** arquivos suspeitos de conter credenciais e **não alteram** `000-Arquivos-originais/`.

## Tecnologia

Decidir arquivar, revisar ou pilotar protótipos de SaaS e separar claramente experimento técnico de conhecimento institucional.

## Relações justificadas

- [[Pendencias-Assumidas]] — explica origem.
- [[Riscos-Operacionais]] — prioriza risco.
- [[Registro-de-Decisoes]] — recebe confirmações resolvidas.
- [[Triagem-Inicial-000-Arquivos-Originais-2026-09-17]] — registra evidências da ingestão inicial.
- [[Campanha-Eu-Faco-Parte]] — contém a cronologia validada da campanha.
- [[Conecta-ACIRV]] — contém os valores e interpretação histórica validados.

## Fontes e rastreabilidade

- [[Fonte - Briefing do projeto]]
- [[Triagem-Inicial-000-Arquivos-Originais-2026-09-17]]
- validação humana de 2026-09-17.

## Limitações e revisão

Esta nota deve ser revisada quando uma validação for resolvida, quando novas divergências forem encontradas ou quando o estado operacional mudar.
