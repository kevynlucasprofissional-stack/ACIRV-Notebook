# Reprogramação operacional das demandas de Samara — 09/10/2026

**Estado:** PLANO PREPARADO — PENDENTE DE RECONCILIAÇÃO DO TRELLO E VALIDAÇÃO DE CAPACIDADE COM SAMARA.
**Origem:** pedido de Samara para reordenar prioridades e corrigir prazos excessivamente curtos, inclusive colisões com CasaFértil.
**Escopo:** ACIRV Q4 2026; a carga total da designer inclui outros clientes e NÃO está visível nesta fonte.
**Natureza:** proposta de execução; NÃO altera o calendário editorial, a descrição canônica, os vencimentos reais do Trello, o estado de sincronização nem o status dos cards.

## 1. Situação editorial confirmada em 09/10

- 60 criativos estáticos, 0 Reels para Samara.
- 12 briefings do lote piloto já lançados/sincronizados no Trello conforme `execution_state_v2.json` (confirmado no estado do GitHub, não no Trello ao vivo).
- 48 briefings posteriores auditados: 32 `PRODUÇÃO_PRONTA`; 11 `PRODUÇÃO_PRONTA_COM_ASSET_PENDENTE`; 5 `BLOCKED_DATA_VALIDATION`.
- Os 43 (32+11) podem receber descrição canônica no card **somente após reconciliação da identidade do card**. Os 11 com asset pendente NÃO estão liberados para conclusão visual até entrega/validação do asset.
- Os 5 bloqueados (`011,023,033,036,042`) NÃO devem ser enviados como ordens prontas de produção.
- Histórico de 32 prontos: `010,048,013,049,015,016,050,018,019,051,021,052,022,024,053,025,026,054,028,029,055,031,056,034,035,057,037,058,039,059,060,043`.
- **Dia das Crianças = post 012**: NÃO pertence aos 32; está entre os 11 com asset pendente; 4 slides; publicação originalmente 12/10/2026, envio planejado para Samara em 07/10/2026, exige fotos reais/autorizadas do comércio de Rio Verde.

Fonte editorial: `../05-auditoria/REVISAO_BRIEFINGS_RESTANTE_Q4_v2.2.md`. Fonte de publicação/handoff: `../01-planejamento/v2/2026-10-1.md`, demais mensais e `../02-estado/execution_state_v2.json`.

## 2. Falha de semântica das datas — corrigir antes de novos vencimentos

Os briefings indicam `DATA DE ENTREGA PARA SAMARA` (data de **encaminhamento da demanda/briefing**). O procedimento antigo instruiu usar esse valor como vencimento nativo do Trello. Isso não estabelece o **prazo de conclusão da arte** e pode produzir percepção de atraso e sobrecarga.

A partir desta análise, distinguir SEMPRE:
1. **Data de envio do briefing a Samara** (handoff; histórico do plano).
2. **Data de conclusão da arte pela Samara** (novo vencimento nativo do Trello, somente depois de confirmar a capacidade real).
3. **Janela de revisão/aprovação** (não ocupar o vencimento da designer).
4. **Data de publicação** (calendário editorial; não alterar silenciosamente).

**Gate temporário:** NÃO utilizar a antiga `DATA DE ENTREGA PARA SAMARA` como novo vencimento nativo de um card. NÃO sobrescrever vencimentos já existentes sem inspecionar histórico, andamento e coordenação com Samara. Esta regra é preventiva; a definição final de nomenclatura e prazos exige alinhamento operacional.

## 3. Triagem imediata — sexta, 09/10

| ID | Publicação original | Situação | Ação |
|---|---|---|---|
| 010 | 07/10 | Briefing pronto, data de publicação passada | Verificar se já foi publicado, produzido ou cancelado; não gerar produção duplicada |
| 048 | 08/10 | Briefing pronto, data de publicação passada | Mesmo procedimento do 010 |
| 011 | 09/10 | Bloqueado por falta de história/depoimento autorizado | Não passar para a designer; revisar ou substituir a pauta editorial |
| 012 — Dia das Crianças | 12/10 | 4 slides; assets locais pendentes; entrega original 07/10 vencida | Prioridade de decisão, NÃO exigência automática de entrega emergencial; confirmar fotos autorizadas e disponibilidade de Samara hoje. Sem ambas, não forçar promessa de entrega/publicação em 12/10; cancelar ou replanejar a pauta mediante decisão editorial |
| 013 | 14/10 | Pronto; entrega original 08/10 vencida | Primeiro candidato de produção de outubro, se ainda não produzido |
| 015 — Dia da Inovação | 19/10 | Pronto; entrega original 09/10 | Proteger a data comemorativa; negociar slot real antes de gerar urgência |
| 020 — Dia do Comerciário | 30/10 | Asset pendente | Solicitar fotos de equipes/comércio com antecedência, sem liberar finalização prematuramente |

**Atenção:** 12/10/2026 é segunda-feira, com feriado nacional no Brasil. A janela de produção antes do Dia das Crianças já está excepcionalmente reduzida. Não pressupor trabalho em fim de semana ou feriado.

## 4. Outubro — prioridades e datas de conclusão CANDIDATAS, não confirmadas

Objetivo: remover colisões internas de entrega ACIRV, preservar folgas para CasaFértil/outros clientes e evitar sobreposição de grandes carrosséis. **Estas datas são propostas condicionais; não alteram o Trello.** Elas partem da premissa de que o card está de fato pendente de produção, de que Samara aceita o slot e de que existe margem de revisão antes da publicação.

| Post | Tema abreviado | Slides | Publicação no plano | Handoff antigo | Conclusão da arte sugerida* | Nota |
|---|---|---:|---|---|---|---|
| 013 | Certificado Digital PF/PJ | 4 | 14/10 | 08/10 | 13/10 | Urgente; janela de aprovação muito curta |
| 049 | Benefícios do associado | 2 | 15/10 | 13/10 | 14/10 | Leve, mas compete com outros clientes |
| 015 | Dia da Inovação | 5 | 19/10 | 09/10 | 16/10 | Data temática prioritária |
| 016 | Pauta coletiva ACIRV | 6 | 21/10 | 16/10 | 19/10 | Reavaliar publicação se outra demanda prioritária ocupar o dia |
| 050 | 3 situações para procurar a ACIRV | 2 | 22/10 | 20/10 | 20/10 | Peça leve |
| 018 | Networking | 7 | 26/10 | 21/10 | 22/10 | Complexidade alta; reservar bloco exclusivo |
| 019 | 5 benefícios da ACIRV | 6 | 28/10 | 21/10 | 23/10 | Separado de 018; reservar bloco exclusivo |
| 051 | Qual espaço combina com você? | 2 | 29/10 | 27/10 | 27/10 | Peça leve |

\* Data candidata à conclusão, sujeita a aprovação da Samara, dependências e compatibilidade com CasaFértil. **Nenhuma data acima é compromisso confirmado**. Se os slots não couberem, mover publicações de conteúdo evergreen (013, 049, 016, 050, 018, 019, 051) mediante decisão editorial, em vez de exigir horas extras, encurtar a aprovação ou impor vencimentos impossíveis.

### Outros cards de outubro NÃO incluídos nas oito conclusões candidatas
- `014` (16/10) — 5 slides, fotos autorizadas de associados/selo pendentes: somente agendar após asset.
- `017` (23/10) — 6 slides, fotos dos espaços pendentes: somente agendar após asset.
- `020` (30/10) — 1 slide, fotos de equipes/comércio pendentes; pode ser priorizado quando asset existir.
- `012` — prioridade de decisão excepcional de 09/10, não um novo prazo compulsório.
- `010`, `048` — checar execução/publicação antes de qualquer nova data.
- `011` — bloqueado por validação de dados.

## 5. Registro dos outros 22 IDs prontos, sem antecipar cobrança

**Novembro — 12:** `021 (03/11), 052 (04/11), 022 (05/11), 024 (11/11), 053 (12/11), 025 (13/11), 026 (16/11), 054 (18/11), 028 (23/11), 029 (25/11), 055 (26/11), 031 (30/11)`.

**Dezembro — 10:** `056 (03/12), 034 (07/12), 035 (09/12), 057 (10/12), 037 (14/12), 058 (17/12), 039 (18/12), 059 (22/12), 060 (29/12), 043 (30/12)`.

**Proteger janelas sazonais**: Black Friday `025,028,055` (e `030` com foto pendente); dezembro `040,041` com fotos pendentes e `042` com dados da retrospectiva bloqueados. Nenhum item futuro deve ganhar vencimento apertado apenas por ter briefing já pronto.

## 6. Política de capacidade, ordem e liberação

- Priorizar por **data comercial inadiável, criticidade, prontidão de dados/assets, dependências e esforço em slides**. Proximidade da publicação é indicador, não justificativa para atropelar a carga total da designer.
- Ter uma **fila única de execução de Samara entre ACIRV, CasaFértil e demais clientes**, com carga estimada e prazo negociado. O GitHub ACIRV **não possui dados suficientes sobre CasaFértil**.
- **Nunca despachar automaticamente os 32 de uma vez para a lista de trabalho ativo**. Manter backlog planejado separado da fila ativa; somente ativar o volume que cabe na capacidade confirmada.
- Meta operacional proposta até calibração: **no máximo duas demandas ACIRV simultaneamente em produção**; não marcar para um mesmo dia de conclusão dois carrosséis extensos. Não presumir expediente no fim de semana/feriado.
- Durante o alinhamento semanal com Samara, reservar primeiro compromissos reais já assumidos com CasaFértil e outros clientes; encaixar as demandas ACIRV nos slots restantes. Um slot só é confirmado após esse confronto.
- Para cada card registrar ou validar: `post_id`, título, URL, situação real, complexidade (slides e esforço), status de asset, data de handoff, **novo prazo de arte acordado**, data de aprovação e publicação.
- Ao atualizar um card, preservar identidade, histórico, anexos e **todo o conteúdo do bloco canônico**. O padrão de descrição Trello proíbe inserir metadados de prioridade dentro da descrição; usar etiquetas/ordem ou estado externo.
- Reconciliar publicações já ocorridas antes de replanejar: card aberto não comprova conteúdo não publicado.
- `BLOCKED_DATA_VALIDATION` não entra na fila de produção. `PRODUÇÃO_PRONTA_COM_ASSET_PENDENTE` pode receber briefing no card, mas não prazo incondicional de arte.
- Recalcular janelas semanalmente, com pelo menos um período de revisão antes da publicação; datas de publicação móveis precisam de decisão editorial registrada e atualização coordenada do plano.

## 7. Acesso e execução pendente

No momento da elaboração, a conexão Trello consultada lista somente quatro quadros acessíveis e **não retorna** `Calendário Editorial` (`622e83218d717e4a16d7856c`), nem os cards canônicos do lote piloto; busca por CasaFértil não trouxe cards acessíveis. Assim, não foi possível auditar carga por cliente, criar/ajustar vencimentos, organizar fisicamente a fila nem verificar status de execução ao vivo.

**Próximas ações obrigatórias**:
1. Obter acesso efetivo ao `Calendário Editorial` e à fila compartilhada de Samara/CasaFértil.
2. Conciliar cards com o plano e distinguir publicados, em produção, aprovados, pendentes, arquivados.
3. Conferir com Samara disponibilidade por dia, esforço dos carrosséis e compromissos CasaFértil.
4. Acordar novos prazos de conclusão e adequar publicações quando inviáveis.
5. Atualizar vencimentos reais no Trello; NÃO reutilizar handoff como due; validar pós-gravação.
6. Persistir IDs, URL, prazo acordado e resultado em estado operacional sem alterar retroativamente informações factuais.
7. Informar a Samara da nova ordem e manter a disciplina de liberação semanal.

**Não executar em modo automático sem gate humano de capacidade.** Os briefings 001–060 seguem como fonte editorial canônica; este plano governa apenas a triagem de carga e prazos propostos.
