---
id: projeto-check-in-inteligente-eventos
titulo: Check-In-Inteligente-de-Eventos
aliases: [Check-in inteligente]
tipo: projeto
status: em_construcao
profundidade: avancada
versao_schema: '1.0'
versao_conteudo: '1.0'
idioma: pt-BR
data_criacao: '2026-09-22'
ultima_revisao: '2026-09-22'
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
> Iniciativa registrada na reunião de marketing de 21/09/2026 para transformar o check-in de eventos em uma base estruturada de presença e relacionamento. O MVP ainda não está implementado: a decisão atual é desenvolver um formulário personalizado e começar pelo próximo Café Entre Amigos.

## Problema

Listas de presença isoladas respondem apenas “quem esteve aqui?”. Uma base de check-in bem desenhada pode permitir perguntas mais úteis:

- quantas pessoas retornam a eventos diferentes?
- qual proporção é associada?
- que eventos atraem novos públicos?
- quais participantes precisam de follow-up?
- onde existe recorrência, abandono ou conversão posterior?

O valor está em **persistir contexto entre eventos**, não em coletar mais campos.

## Estado atual

**Documentado:** desenvolver check-in inteligente por formulário personalizado e priorizar a aplicação no próximo Café Entre Amigos.

**Ainda não documentado como concluído:**

- ferramenta escolhida;
- schema final;
- integração com CRM;
- automação de mensagens;
- identidade única de participante;
- consentimento;
- dashboard;
- operação em produção.

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

- `000-Arquivos-originais/210926 Reunião com equipe de Marketing.md` — blob `308a5c51194de989dc931e7fd15d2196685fa21d`.

## Limitações e revisão

Esta nota traduz uma intenção operacional em projeto estruturado. Arquitetura, ferramenta e campos são propostas para validação, não decisões já aprovadas.
