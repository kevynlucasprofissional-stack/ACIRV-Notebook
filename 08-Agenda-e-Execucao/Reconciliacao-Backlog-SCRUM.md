---
id: reconciliacao-backlog-scrum
titulo: Reconciliação Backlog × SCRUM
tipo: operacao
status: em_construcao
versao_conteudo: '0.1'
idioma: pt-BR
data_criacao: '2026-09-23'
ultima_revisao: '2026-09-23'
grau_confianca: alto
camadas_evidencia:
  - fato_documentado
  - interpretacao_operacional
tags:
  - backlog
  - scrum
  - reconciliacao
  - proveniencia
confidencialidade: interno
---

# Reconciliação Backlog × SCRUM

> [!summary] Função
> Ponte canônica entre a memória histórica do [[Backlog-Canonico-ACIRV]] e os snapshots do board ACIRV + VCOM. Esta nota não transforma snapshot em estado operacional atual: registra o que já pode ser afirmado com segurança antes da reconciliação card a card.

## O que mudou na evidência

O backlog canônico nasceu como inventário histórico de ações extraídas de oito fontes explícitas de tarefas. Ele preserva **405 itens como `não_reconciliado`** e declara que a captura original não consultou o Trello. Em 23/09/2026, sete exports JSON do board `ACIRV + VCOM: SCRUM` passaram a existir em `000-Arquivos-originais/SCRUM da ACIRV + Vcom/`.

Isso cria uma transição importante no processo: antes havia memória histórica sem uma fonte operacional comparável; agora existe uma sequência de snapshots capaz de sustentar reconciliação, mas ainda não prova, por si só, o estado atual de cada item.

## Deduplicação no nível da fonte

Antes de interpretar cards, os sete arquivos foram comparados por blob SHA no `main`.

| Export | Blob SHA | Tratamento |
|---|---|---|
| `GDM8ZE3r - acirv-vcom-scrum.json` | `a6c72dbdb3b76f433f5e9847417332014638055b` | versão distinta |
| `GDM8ZE3r - acirv-vcom-scrum (1).json` | `1c2939610d054178e65354a23b9370ea8c875d8c` | versão distinta |
| `GDM8ZE3r - acirv-vcom-scrum (2).json` | `1c2939610d054178e65354a23b9370ea8c875d8c` | **duplicata byte a byte de `(1)`**; não reler como evidência nova |
| `GDM8ZE3r - acirv-vcom-scrum (3).json` | `d15c760461b97570f62dfa619802db9c851f3ac2` | versão distinta |
| `GDM8ZE3r - acirv-vcom-scrum (4).json` | `baa43f40f520a12069b784af7911dd99f0191af4` | versão distinta |
| `GDM8ZE3r - acirv-vcom-scrum (5).json` | `830dda5cc21ff36d1461f23b699f71640cfd81be` | versão distinta |
| `GDM8ZE3r - acirv-vcom-scrum (6).json` | `4997fef9b93dcd1fd751ac7817bdf09bbf384b89` | versão distinta |

Portanto, há **7 arquivos físicos, mas 6 blobs únicos**. A igualdade de SHA entre `(1)` e `(2)` é evidência suficiente de duplicação de conteúdo; os demais SHAs diferentes indicam versões distintas, não necessariamente mudanças semanticamente relevantes em todos os cards.

## Narrativa operacional sustentada

A sequência documentada até aqui é:

**memória histórica dispersa → backlog canônico não reconciliado → chegada de snapshots do sistema operacional → deduplicação das fontes → próxima etapa: reconciliação semântica card a card.**

O ganho dessa leitura é separar duas perguntas que antes podiam ser confundidas:

1. **A ação apareceu historicamente?** O backlog canônico responde a isso.
2. **Qual foi ou é seu estado no sistema de execução?** Os snapshots podem ajudar a responder, mas somente após identificação segura do card, interpretação da lista/estado e comparação temporal.

Essa distinção impede que checkbox histórico, presença em snapshot ou ausência em uma versão sejam promovidos automaticamente a “aberto”, “concluído” ou “cancelado”.

## Protocolo para a próxima etapa

A reconciliação deve trabalhar apenas sobre os **6 blobs únicos** e, para cada candidato, registrar:

- identidade ou equivalência provável entre item histórico e card;
- evidência usada para o vínculo;
- snapshots em que o card aparece;
- mudança de lista/estado quando documentalmente observável;
- grau de confiança do pareamento;
- divergências de título, descrição, responsável ou prazo;
- estado `não_reconciliado` quando a equivalência não for segura.

Não inferir conclusão a partir de desaparecimento entre snapshots. Não usar número de cards como produtividade. Não converter lista do Trello em semântica institucional sem validar o significado operacional da lista.

## Proveniência

- `08-Agenda-e-Execucao/Backlog-Canonico-ACIRV.md` — versão no `main` em 23/09/2026, blob `b3f5db9e29052719ae830b1f9cc4f2067d7d3787`.
- `000-Arquivos-originais/SCRUM da ACIRV + Vcom/GDM8ZE3r - acirv-vcom-scrum.json` — blob `a6c72dbdb3b76f433f5e9847417332014638055b`.
- `.../GDM8ZE3r - acirv-vcom-scrum (1).json` — blob `1c2939610d054178e65354a23b9370ea8c875d8c`.
- `.../GDM8ZE3r - acirv-vcom-scrum (2).json` — blob `1c2939610d054178e65354a23b9370ea8c875d8c`.
- `.../GDM8ZE3r - acirv-vcom-scrum (3).json` — blob `d15c760461b97570f62dfa619802db9c851f3ac2`.
- `.../GDM8ZE3r - acirv-vcom-scrum (4).json` — blob `baa43f40f520a12069b784af7911dd99f0191af4`.
- `.../GDM8ZE3r - acirv-vcom-scrum (5).json` — blob `830dda5cc21ff36d1461f23b699f71640cfd81be`.
- `.../GDM8ZE3r - acirv-vcom-scrum (6).json` — blob `4997fef9b93dcd1fd751ac7817bdf09bbf384b89`.

## Limites

Esta sessão realizou deduplicação no nível de arquivo/blob. Não executou parse integral dos JSONs nem reconciliação card a card. A existência de seis versões distintas não estabelece cronologia interna, causalidade, conclusão de tarefas ou estado atual sem leitura estruturada posterior.