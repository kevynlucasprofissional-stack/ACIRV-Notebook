---
id: projeto-check-in-inteligente-eventos
titulo: Check-In-Inteligente-de-Eventos
aliases: [Check-in inteligente]
tipo: projeto
status: em_construcao
profundidade: avancada
versao_schema: '1.0'
versao_conteudo: '1.1'
idioma: pt-BR
data_criacao: '2026-09-22'
ultima_revisao: '2026-09-23'
grau_confianca: medio
camadas_evidencia:
- fato_documentado
- interpretacao_operacional
- hipotese_de_trabalho
tags:
- eventos
- dados
- check-in
- produto
fontes_documentais:
- '000-Arquivos-originais/210926 Reunião com equipe de Marketing.md'
notas_relacionadas:
- '[[Cafe-Entre-Amigos]]'
- '[[Qualidade-dos-Dados-de-Marketing]]'
- '[[Pendencias-de-Dados]]'
- '[[Sistema-Operacional-de-Marketing]]'
confidencialidade: interno
subtipo: produto_operacional
---

# Check-In-Inteligente-de-Eventos

> [!summary] Síntese
> Iniciativa registrada na reunião de marketing de 21/09/2026 para transformar o check-in de eventos em uma base estruturada de presença e relacionamento. Em 23/09, o usuário propôs **Sympla** como direção preferida para inscrição e check-in, mantendo uma camada própria de inteligência a partir dos dados exportados. O piloto ainda precisa ser validado em operação.

## Problema

Listas de presença isoladas respondem apenas “quem esteve aqui?”. Uma base de check-in bem desenhada pode permitir perguntas mais úteis:

- quantas pessoas retornam a eventos diferentes?
- qual proporção é associada?
- que eventos atraem novos públicos?
- quais participantes precisam de follow-up?
- onde existe recorrência, abandono ou conversão posterior?

O valor está em **persistir contexto entre eventos**, não em coletar mais campos.

## Estado atual

**Documentado em 21/09:** desenvolver check-in inteligente e priorizar a aplicação no próximo Café Entre Amigos.\n\n**Direção proposta em 23/09:** utilizar **Sympla** para inscrição e check-in, aproveitando a exportação de dados para construir a base analítica própria da ACIRV. A motivação é evitar desenvolver uma plataforma específica quando uma ferramenta pronta já cobre a operação básica.

**Ainda não documentado como concluído:**

- validação operacional do Sympla como ferramenta do piloto;
- schema final;
- integração com CRM;
- automação de mensagens;
- identidade única de participante;
- consentimento;
- dashboard;
- operação em produção.

## Arquitetura proposta com Sympla

Fluxo:

**inscrição → check-in → exportação → base de dados → pesquisa → análise → melhoria do próximo evento**

O Sympla deve resolver a camada transacional de inscrição/check-in. A inteligência longitudinal permanece fora da plataforma:
- deduplicação;
- recorrência;
- associação com eventos anteriores;
- segmentação;
- follow-up;
- cruzamento com condição de associado;
- pesquisa pós-evento.

A decisão evita confundir “usar uma plataforma pronta” com “ter inteligência própria”. O ativo estratégico é a base e o ciclo de aprendizagem, não o software de check-in.

## MVP recomendado — interpretação operacional

Um MVP deve coletar apenas o necessário para responder perguntas reais.

### Camada do evento

- ID do evento;
- nome;
- data;
- tipo de evento;
- campanha/projeto relacionado.

### Camada de presença

- timestamp do check-in;
- participante;
- empresa quando necessário;
- condição de associado quando houver fonte confiável;
- origem do convite/inscrição, se conhecida;
- consentimentos necessários.

### Camada derivada

Depois do evento, a base pode calcular:

- presença total;
- associados × não associados;
- novos × recorrentes;
- frequência por pessoa/empresa;
- taxa de retorno;
- participação por categoria de evento.

Campos derivados não devem ser digitados manualmente quando puderem ser calculados.

## Identidade e deduplicação

O maior risco de uma base longitudinal é tratar a mesma pessoa como várias.

Antes de escalar, definir uma chave ou rotina de reconciliação que:

- não dependa apenas de nome escrito livremente;
- minimize exposição de dado pessoal;
- permita corrigir duplicatas;
- preserve origem e histórico.

## Privacidade

O check-in deve seguir minimização de dados:

- coletar só o que será usado;
- não transformar formulário de presença em cadastro excessivo;
- definir finalidade;
- limitar acesso;
- separar dado pessoal de métricas agregadas;
- evitar replicar dados sensíveis em apresentações e notas narrativas.

## Relação com associados

A reunião também registra a necessidade de responder **quantos associados foram conquistados em 2026**.

O check-in pode futuramente ajudar a observar participação antes/depois da associação, mas não deve virar sistema mestre de associados sem definição explícita. A condição de associado precisa vir de uma fonte institucional confiável.

## Piloto no Café Entre Amigos

O próximo Café é o primeiro caso sugerido.

Perguntas mínimas do piloto:

1. quanto tempo leva para fazer check-in?
2. quantos registros duplicados aparecem?
3. a base consegue distinguir recorrência?
4. a equipe consegue operar sem criar fila?
5. quais campos realmente foram usados depois?
6. o dado melhora follow-up ou apenas aumenta coleta?

## Critério de sucesso

O piloto deve ser considerado útil se produzir uma base mais confiável e reutilizável **sem aumentar desnecessariamente fricção e coleta de dados**.

## Fontes e rastreabilidade

- Direção operacional do usuário em 23/09/2026 — preferência pelo Sympla e pelo ciclo inscrição → check-in → base → pesquisa → análise → melhoria; fonte conversacional ainda não persistida em `000-Arquivos-originais/`.

- `000-Arquivos-originais/210926 Reunião com equipe de Marketing.md` — blob `308a5c51194de989dc931e7fd15d2196685fa21d`.

## Limitações e revisão

Esta nota traduz uma intenção operacional em projeto estruturado. Arquitetura, ferramenta e campos são propostas para validação, não decisões já aprovadas.
