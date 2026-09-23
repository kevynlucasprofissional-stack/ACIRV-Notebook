# Runbook do Hermes — Social Media ACIRV Q4 2026

## Missão
Sincronizar no Trello os briefings já aprovados no planejamento, com rastreabilidade, idempotência e baixa possibilidade de duplicação.

## Separação de responsabilidade

O Hermes **não escreve o briefing** quando o planejamento já possui um bloco `DESCRIÇÃO CANÔNICA PARA O TRELLO`.

A autoria editorial fica nos arquivos de `01-planejamento/v2/`.

Para itens fechados, o Hermes atua como executor:
- lê;
- localiza o card;
- transfere o texto integralmente;
- salva;
- verifica;
- registra estado.

Se o briefing ainda não estiver fechado, marcar `BLOCKED_EDITORIAL_BRIEFING` e não improvisar copy.

## Fontes operacionais

Plano e briefings:
`01-planejamento/v2/README.md`

Padrão editorial:
`01-planejamento/v2/PADRAO_BRIEFING_PRODUCAO.md`

Estado:
`02-estado/execution_state_v2.json`

Destino Trello:
`03-integracoes/trello_destination.json`

Padrão das descrições:
`03-integracoes/PADRAO_DESCRICAO_CARTOES_TRELLO.md`

Mapa do lote piloto:
`03-integracoes/LOTE_PILOTO_TRELLO_SYNC.md`

Design System canônico:
`../../01-Estrategia-e-Marca/Design-System-ACIRV.md`

Moodboard operacional:
`04-moodboard/MOODBOARD.md` — perfil `ACIRV-MOOD-v1`

## Invariantes
1. Samara recebe somente peças estáticas.
2. Reels/vídeos ficam fora do escopo.
3. IDs 001–044 permanecem imutáveis.
4. IDs 045–060 = 2 slides exatos, capa + CTA.
5. Um post = um card canônico.
6. Não publicar números, condições comerciais, capacidades, horários, nomes ou promessas sem validação atual.
7. O Trello recebe a copy já aprovada no GitHub; não uma versão reinterpretada pelo Hermes.
8. O Hermes não cria copy, títulos, CTAs ou direção visual para briefings fechados.

## Inicialização
1. Ler `00_README.md`.
2. Ler `00_EXECUTAR_COM_HERMES.md`.
3. Ler `01-planejamento/v2/README.md`.
4. Ler `01-planejamento/v2/PADRAO_BRIEFING_PRODUCAO.md`.
5. Ler os arquivos mensais aplicáveis.
6. Ler `03-integracoes/LOTE_PILOTO_TRELLO_SYNC.md`.
7. Ler `02-estado/execution_state_v2.json`.
8. Validar board/list pelos IDs exatos.
9. Confirmar estado externo dos cards antes de mutar.

## Estados
Fluxo do item já fechado editorialmente:

`PRODUÇÃO_PRONTA -> TRELLO_SYNC_PENDENTE -> TRELLO_SYNC_OK -> REFERENCIA_VISUAL_PENDENTE/REVISAO_PENDENTE`

Auxiliares:
- `BLOCKED_EDITORIAL_BRIEFING`
- `BLOCKED_TRELLO_ACCESS`
- `BLOCKED_DUPLICATE_CARD`
- `BLOCKED_DATA_VALIDATION`
- `BLOCKED_TRELLO_DESTINATION_DRIFT`
- `CANCELADA`

## Gate antes da sincronização

O Hermes não refaz o Quality Gate editorial. Apenas confirma:
1. o post está marcado como `PRODUÇÃO_PRONTA` ou `PRODUÇÃO_PRONTA_COM_ASSET_PENDENTE`;
2. existe `DESCRIÇÃO CANÔNICA PARA O TRELLO`;
3. o número de slides no bloco bate com o registro do post;
4. o card canônico está identificado no mapa de sincronização;
5. não está usando o duplicado arquivado.

Se qualquer item falhar, bloquear a sincronização daquele post e reportar.

## Atualização dos cards do lote piloto

Os 12 cards de 16/09 a 05/10 já existem no Trello.

Para cada um:
1. localizar o post no arquivo mensal;
2. copiar integralmente o conteúdo do bloco `DESCRIÇÃO CANÔNICA PARA O TRELLO`;
3. abrir o card canônico indicado em `LOTE_PILOTO_TRELLO_SYNC.md`;
4. entrar no editor da descrição;
5. substituir a descrição atual pelo bloco canônico;
6. clicar em `Salvar` / `description-save-button`;
7. reabrir/verificar persistência;
8. registrar sucesso imediatamente no estado.

Não criar card novo para o lote piloto.

## Procedimento via navegador

Para cards existentes:
- abrir o card correto;
- editar descrição;
- colar o bloco canônico;
- salvar;
- verificar.

Armadilhas conhecidas:
- `list-name-textarea` renomeia a lista;
- não usar o composer para substituir descrição;
- mutação direta por API encontrou bloqueio CSRF em sessão anterior; preferir UI autenticada enquanto persistir.

## Datas

Vencimento nativo desejado = `DATA DE ENTREGA PARA SAMARA` do briefing.

O campo personalizado `Data de publicação` é diferente do vencimento nativo.

Se não for possível gravar o due com segurança:
- não alterar outro campo por engano;
- registrar a pendência;
- seguir para a sincronização da descrição.

## Duplicidade conhecida

O post `ACIRV-SM-2026-005` possui um card duplicado arquivado.

Nunca usar o duplicado arquivado como card canônico. O mapa de sincronização contém os IDs corretos.

## Regra 045–060

O Hermes não interpreta nem expande a regra. Apenas preserva o briefing aprovado:
- Slide 1 = capa/gancho;
- Slide 2 = CTA;
- exatamente 2 slides.

## Moodboard / referências visuais

As referências visuais serão executadas em etapa separada, sempre com `ACIRV-MOOD-v1` e somente depois do briefing editorial fechado.

`ACIRV-MOOD-v1` é a projeção operacional do arquivo `../../01-Estrategia-e-Marca/Design-System-ACIRV.md`. O `MOODBOARD.md` pode especializar o fluxo de Social Media, mas não criar regras visuais concorrentes.

A sincronização dos briefings no Trello não depende de o Hermes reescrever ou recalcular direção visual: ela já está definida no bloco canônico.

## Persistência

Depois de cada mutação externa bem-sucedida, salvar imediatamente:
- card ID;
- URL;
- `trello_description_synced`;
- due nativo ou pendência;
- erro/bloqueio;
- timestamp.

Ao retomar:
1. ler estado;
2. verificar Trello ao vivo;
3. confirmar se a descrição já corresponde ao bloco canônico;
4. pular itens já sincronizados;
5. continuar do primeiro item incompleto.

## Limite do lote

Parar em 05/10/2026.

Posts posteriores permanecem bloqueados para execução até receberem briefing canônico no GitHub.