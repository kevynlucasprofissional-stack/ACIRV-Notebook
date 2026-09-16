# Planejamento 4º Trimestre de 2026 — ACIRV Social Media

Período operacional: **16/09/2026 a 31/12/2026**.

## Plano atual

Fonte vigente:

`01-planejamento/v2/README.md`

Escopo:
- **60 publicações estáticas** para a designer Samara;
- **0 Reels/vídeos** no escopo da designer;
- IDs `001–044` preservados;
- IDs `045–060` = 16 peças leves de **2 slides exatos: capa + CTA**;
- aprofundamento das peças extras na legenda.

## Separação de responsabilidades

### Planejamento / autoria editorial

Os arquivos de `01-planejamento/v2/` são responsáveis por:
- texto exato da arte;
- copy slide a slide;
- hierarquia textual;
- direção visual por slide;
- CTA;
- assets/referências;
- restrições;
- legenda final;
- pendências editoriais.

### Hermes / execução

Para pautas marcadas como `PRODUÇÃO_PRONTA`, o Hermes **não escreve o briefing**. Ele apenas sincroniza o bloco `DESCRIÇÃO CANÔNICA PARA O TRELLO` com o card canônico já reconciliado.

Se não houver briefing fechado, o Hermes usa `BLOCKED_EDITORIAL_BRIEFING` em vez de improvisar copy.

## Lote piloto

Os 12 briefings de 16/09 a 05/10 já estão fechados editorialmente nos arquivos:

- `01-planejamento/v2/2026-09.md`
- `01-planejamento/v2/2026-10-1.md`

Os 12 cards canônicos já existentes e seus IDs/URLs estão mapeados em:

`03-integracoes/LOTE_PILOTO_TRELLO_SYNC.md`

Existe uma duplicidade arquivada conhecida do post 005; o mapa indica qual card é o canônico.

## Fontes de verdade

- **Plano e briefings:** `01-planejamento/v2/README.md` + arquivos mensais.
- **Padrão editorial:** `01-planejamento/v2/PADRAO_BRIEFING_PRODUCAO.md`.
- **Estratégia:** `01-planejamento/v2/PLANEJAMENTO_ESTRATEGICO.md` e `05_DECISOES_ESTRATEGICAS.md`.
- **Execução:** `02-estado/execution_state_v2.json`.
- **Destino Trello:** `03-integracoes/trello_destination.json`.
- **Padrão Trello:** `03-integracoes/PADRAO_DESCRICAO_CARTOES_TRELLO.md`.
- **Mapa do lote piloto:** `03-integracoes/LOTE_PILOTO_TRELLO_SYNC.md`.
- **Reconciliação histórica:** `03-integracoes/RECONCILIACAO_TRELLO_INICIAL.md`.
- **Moodboard:** `04-moodboard/MOODBOARD.md` — `ACIRV-MOOD-v1`, status `READY`.
- **Auditoria:** `05-auditoria/`.

## Ordem de leitura do Hermes

1. `00_README.md`
2. `00_EXECUTAR_COM_HERMES.md`
3. `01_RUNBOOK_HERMES.md`
4. `01-planejamento/v2/README.md`
5. `01-planejamento/v2/PADRAO_BRIEFING_PRODUCAO.md`
6. arquivos mensais aplicáveis em `01-planejamento/v2/`
7. `03-integracoes/LOTE_PILOTO_TRELLO_SYNC.md`
8. `02-estado/execution_state_v2.json`
9. `03-integracoes/trello_destination.json`
10. `03-integracoes/PADRAO_DESCRICAO_CARTOES_TRELLO.md`
11. `04-moodboard/MOODBOARD.md`.

## Invariantes

- Samara recebe somente peças estáticas.
- Reels serão planejados separadamente.
- Um post = um card canônico.
- Todo slide liberado deve ter texto exato e direção visual específica.
- A designer não precisa escrever ou completar a copy.
- O Hermes não reescreve briefings fechados.
- IDs 045–060 permanecem com exatamente 2 slides.
- Dados voláteis não são inventados.
- Toda referência visual usa `ACIRV-MOOD-v1`.
- O Hermes persiste estado imediatamente após cada mutação externa.
- Não avançar para posts posteriores a 05/10 enquanto eles não tiverem briefing canônico fechado.