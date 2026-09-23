# EXECUTAR COM HERMES — Social Media ACIRV Q4 2026

## Missão
Sincronizar no Trello os briefings **já fechados editorialmente no GitHub**, com rastreabilidade, retomada segura e sem duplicação.

## Regra de responsabilidade

A autoria editorial **não pertence ao Hermes**.

Copy, texto exato slide a slide, direção visual, legenda, assets e restrições são definidos nos arquivos canônicos de:

`01-planejamento/v2/`

Quando um post possui `Status editorial: PRODUÇÃO_PRONTA` ou `PRODUÇÃO_PRONTA_COM_ASSET_PENDENTE`, o Hermes deve apenas:
1. localizar o card correto;
2. localizar o bloco `DESCRIÇÃO CANÔNICA PARA O TRELLO`;
3. copiar o bloco integralmente;
4. colar na descrição do card sem reescrever;
5. salvar;
6. verificar persistência;
7. atualizar o estado.

Se não existir briefing fechado, usar `BLOCKED_EDITORIAL_BRIEFING`. **Não criar a copy por conta própria.**

## Fontes canônicas obrigatórias

Plano editorial e briefings:
`01-planejamento/v2/README.md`

Padrão de briefing:
`01-planejamento/v2/PADRAO_BRIEFING_PRODUCAO.md`

Estado operacional:
`02-estado/execution_state_v2.json`

Padrão Trello:
`03-integracoes/PADRAO_DESCRICAO_CARTOES_TRELLO.md`

Mapa do lote piloto:
`03-integracoes/LOTE_PILOTO_TRELLO_SYNC.md`

Design System canônico (autoridade semântica visual):
`../../01-Estrategia-e-Marca/Design-System-ACIRV.md`

Moodboard operacional do Hermes:
`04-moodboard/MOODBOARD.md` — projeção `ACIRV-MOOD-v1`, obrigatoriamente alinhada ao canônico

## Escopo imutável
- Samara recebe somente peças estáticas.
- Reels/vídeos ficam fora do escopo.
- IDs 001–044 permanecem preservados.
- IDs 045–060 têm exatamente 2 slides: capa + CTA.
- Um post = um card canônico.

## Lote piloto liberado

Os 12 briefings de 16/09 a 05/10 já foram fechados editorialmente nos arquivos:
- `01-planejamento/v2/2026-09.md`
- `01-planejamento/v2/2026-10-1.md`

O Hermes **não deve melhorá-los**. Deve sincronizá-los com os cards já existentes.

Não avançar para posts posteriores a 05/10 enquanto eles estiverem apenas como pauta editorial.

## Trello
Destino obrigatório:
- Board `622e83218d717e4a16d7856c` — Calendário Editorial.
- List `69370019555b10bb6ad19e30` — ORDEM DE SERVIÇO - SAMARA.

Antes da primeira mutação da sessão:
1. validar board/list pelos IDs;
2. confirmar cada card pelo ID/URL registrado;
3. não recriar card já existente.

## Atualização da descrição

Para cada card do lote piloto:
1. abrir o arquivo mensal correto;
2. localizar o `post_id`;
3. confirmar que o status editorial está liberado;
4. copiar **somente o conteúdo dentro do bloco** `DESCRIÇÃO CANÔNICA PARA O TRELLO`;
5. abrir o card canônico indicado em `LOTE_PILOTO_TRELLO_SYNC.md`;
6. substituir a descrição atual;
7. clicar explicitamente em `Salvar` / `description-save-button`;
8. reabrir/verificar que o conteúdo persistiu;
9. registrar `trello_description_synced=true` no estado.

É proibido durante essa etapa:
- resumir;
- reescrever;
- corrigir estilo por conta própria;
- trocar CTA;
- remover texto por achar longo;
- mudar direção visual;
- alterar número de slides.

## Datas

A descrição já contém publicação e entrega.

Vencimento nativo planejado = data de entrega para Samara.

O campo personalizado `Data de publicação` não é o vencimento nativo.

Se o vencimento não puder ser atualizado com segurança, registrar a pendência; não usar outro campo por aproximação.

## Duplicidade conhecida

Existe um duplicado arquivado do post `ACIRV-SM-2026-005`.

Não reabrir nem reutilizar esse duplicado. Usar somente o card canônico registrado no mapa do lote.

## Persistência

Após cada mutação externa bem-sucedida:
- card ID/URL;
- descrição sincronizada;
- vencimento nativo ou pendência;
- erro/bloqueio;
- timestamp.

Salvar imediatamente no estado. Não esperar o fim do lote.

## Referência visual

A criação editorial das referências não deve preceder o briefing. Como o lote piloto já está fechado, essa etapa pode ser executada separadamente depois.

Nesta sincronização, a prioridade é deixar os 12 cards com a **descrição canônica correta**.

Quando chegar a etapa de referência visual, o Hermes lê `04-moodboard/MOODBOARD.md`; se existir qualquer ambiguidade de identidade, tokens, contraste, backgrounds ou legibilidade, prevalece `../../01-Estrategia-e-Marca/Design-System-ACIRV.md`.

## Limite desta execução

Parar em 05/10/2026.

Não criar nem editar briefings posteriores enquanto eles não estiverem marcados como `PRODUÇÃO_PRONTA` no GitHub.