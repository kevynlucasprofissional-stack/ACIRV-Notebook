---
id: metrica-registro-de-decisoes
titulo: Registro-de-Decisoes
aliases: []
tipo: metrica
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
- decisao
fontes_documentais:
- '[[Fonte - Reunioes de Junho 2026]]'
- '[[Fonte - Briefing do projeto]]'
notas_relacionadas:
- '[[Governanca-de-Aprovacoes]]'
- '[[Ritual-Mensal-de-Metricas]]'
- '[[Ritual-Semanal-de-Priorizacao]]'
- '[[Campanha-Eu-Faco-Parte]]'
- '[[Conecta-ACIRV]]'
confidencialidade: interno
subtipo: registro
---

# Registro-de-Decisoes

> [!summary] Síntese
> Índice para decisões que alteram estratégia, prioridade, calendário, processo, dado, orçamento ou versão.

## Formato

Data; decisão; contexto; opções; responsável; aprovador; efeito; prazo de revisão; evidência; status.

## Quando criar nota própria

Quando a decisão afeta mais de um projeto, muda regra, envolve risco ou precisa ser lembrada após a reunião.

## Decisões iniciais deste vault

V5 como referência de tom; ZIP original em área restrita; dados não corrigidos silenciosamente; Dataview/Kanban opcionais; Bases e MOCs como navegação principal.

## Validações de 2026-09-17

### Campanha de Pertencimento

- **Decisão**: registrar abril de 2026 como início originalmente planejado e maio de 2026 como início efetivo da execução.
- **Efeito**: elimina a falsa escolha entre abril e maio e preserva a diferença entre planejamento e execução.
- **Destino canônico**: [[Campanha-Eu-Faco-Parte]].
- **Status**: resolvida.

### Conecta ACIRV — Cota Diamante

- **Decisão**: considerar **R$ 18.000** como valor oficial da Cota Diamante para fins canônicos.
- **Efeito**: substituir a divergência R$ 20.000 × R$ 18.000 pela referência oficial validada.
- **Destino canônico**: [[Conecta-ACIRV]].
- **Status**: resolvida.

### Conecta ACIRV — R$ 4 milhões

- **Decisão**: interpretar **R$ 4 milhões** como volume histórico acumulado de negócios movimentados ao longo de várias edições do Conecta.
- **Efeito**: remover a classificação incorreta de “meta anual de 2026”.
- **Destino canônico**: [[Conecta-ACIRV]].
- **Status**: resolvida.

### Arquivos locais com credenciais

- **Decisão**: `000-Arquivos-originais/Contas e Senhas.md` e `000-Arquivos-originais/Minha Chave API Antropic.md` devem permanecer somente no computador local e não voltar a ser sincronizados com o GitHub.
- **Implementação segura**: adicionar os caminhos ao `.gitignore`, depois retirar os arquivos do índice Git **no clone local** com `git rm --cached`, verificar que os arquivos continuam fisicamente presentes e somente então remover a versão rastreada do repositório remoto.
- **Observação de segurança**: como credenciais reais já foram versionadas, remover os arquivos da branch atual não elimina segredos do histórico; rotação/revogação continua necessária.
- **Status**: proteção preparada; remoção remota pendente de confirmação local.

## Revisão

Decisões expiradas não são apagadas: recebem status substituída, data e link para a sucessora.

## Relações justificadas

- [[Governanca-de-Aprovacoes]] — origina decisões.
- [[Ritual-Mensal-de-Metricas]] — produz decisões.
- [[Ritual-Semanal-de-Priorizacao]] — produz decisões.
- [[Campanha-Eu-Faco-Parte]] — recebe a cronologia validada.
- [[Conecta-ACIRV]] — recebe valores e interpretação histórica validados.

## Fontes e rastreabilidade

- [[Fonte - Reunioes de Junho 2026]]
- [[Fonte - Briefing do projeto]]
- validação humana de 2026-09-17.

## Limitações e revisão

Esta nota deve ser revisada quando a fonte, o responsável, a data, a metodologia ou o estado operacional mudar.

## Dados disponíveis nas fontes

Esta nota possui informações complementares nos seguintes arquivos-fonte:

- `Dados ACIRV/Notas\\Como fazer o relatório de março ser de alto nível.md`
- `Dados ACIRV/Notas\\Como é realizado a reunião de apresentação de Métricas de todo dia 30 - Modelo da Vivi.md`
- `Dados ACIRV/Notas\\Contraproposta para o relatório de abril.md`
- `Dados ACIRV/Notas\\Dados sobre o Conecta Saúde 2º ed..md`
- `Dados ACIRV/Notas\\Todos os dados para relatório de métricas.md`

> **Status da integração**: Dados identificados. Aguardando extração e incorporação dirigida.
