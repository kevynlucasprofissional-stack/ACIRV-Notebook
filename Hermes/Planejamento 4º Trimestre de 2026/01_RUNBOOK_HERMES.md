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
4. para o lote piloto, o card está identificado no mapa; para os posts posteriores, o card existente foi reconciliado no Trello ao vivo e seu ID foi persistido no estado;
5. não está usando card duplicado ou arquivado.

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

## Datas — gate de capacidade a partir de 09/10/2026

A data `DATA DE ENTREGA PARA SAMARA` do briefing registra o **encaminhamento da demanda**, não comprova o prazo acordado para a **conclusão da arte**. O procedimento antigo equiparava esse valor ao vencimento nativo, o que gerou risco de prazos inadequados.

**Não gravar novos vencimentos nativos a partir do campo de handoff até haver validação explícita da carga real com Samara**. Distinguir:
1. envio do briefing;
2. vencimento acordado para a arte;
3. revisão/aprovação;
4. publicação.

O campo personalizado `Data de publicação` é diferente do vencimento nativo. Não alterar ou limpar vencimentos existentes cegamente: reconciliar histórico e andamento antes, inclusive demandas de outros clientes como CasaFértil. A sincronização de descrições canônicas pode continuar independentemente da alteração de prazos, quando o card correto estiver confirmado.

A ordem, colisões e datas candidatas estão documentadas em `03-integracoes/REPROGRAMACAO_PRIORIDADES_SAMARA_2026-10-09.md`. Aquelas datas **não são compromissos** e não devem ser aplicadas no Trello sem conferir capacidade da designer e demais clientes. Se não for possível gravar o prazo correto com segurança, registrar a pendência; não usar campo alternativo por aproximação.

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

## Escopo de sincronização vigente

O limite antigo de 05/10 foi removido após a canonização dos 48 briefings restantes.

O Hermes pode percorrer o calendário até 31/12/2026, respeitando o status editorial individual:
- `PRODUÇÃO_PRONTA` → pode sincronizar;
- `PRODUÇÃO_PRONTA_COM_ASSET_PENDENTE` → pode sincronizar a descrição; a produção visual continua dependente do asset;
- `BLOCKED_DATA_VALIDATION` → não sincronizar como ordem de produção e não completar copy.

Para posts posteriores ao lote piloto:
1. localizar o card existente no Trello ao vivo;
2. confirmar título/data/ID lógico antes de mutar;
3. persistir card ID e URL no estado;
4. se houver mais de um candidato, bloquear como duplicidade em vez de criar ou escolher por adivinhação;
5. não criar novo card quando já existir um card correspondente.