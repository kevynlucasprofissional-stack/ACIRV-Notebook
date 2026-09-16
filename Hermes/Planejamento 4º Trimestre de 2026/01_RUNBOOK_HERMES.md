# Runbook do Hermes — Social Media ACIRV Q4 2026

## Missão

Executar o planejamento de 16/09/2026 a 31/12/2026 com rastreabilidade, idempotência e baixa possibilidade de duplicação. O objetivo não é inventar um novo calendário, mas transformar o plano versionado em cartões, briefings, referências visuais e evidências auditáveis.

## Fontes de verdade

- `calendario/*.json`: plano editorial versionado.
- `03_EXECUTION_STATE.json`: progresso mutável.
- `02_TRELLO_CONFIG.json`: IDs externos confirmados.
- `04_RECONCILIACAO_TRELLO_INICIAL.md`: legado e riscos de duplicação.
- `moodboard/`: referências visuais, quando adicionadas.

O `post_id` é imutável. A `dedupe_key` é a chave editorial de deduplicação.

## Invariantes estratégicos

1. Direção: **Conectar para Crescer**.
2. Todo post tem um pilar principal entre Pertencimento, Resultados, Autoridade, Proximidade e Captação.
3. Não publicar números, condições comerciais, capacidades, datas, nomes ou promessas sem validação atual.
4. Prova social exige evidência e autorização quando aplicável.
5. Evento só entra com data confirmada; evento confirmado gera pacote pré/durante/pós.
6. Conteúdo de serviço deve explicar problema, utilidade ou benefício; evitar repetição de anúncio.
7. Não preencher automaticamente dias livres: folga é capacidade para aprovação, contingência e eventos reais.

## Estados

Fluxo principal:

`BRIEFING_CRIADO -> CARTAO_CRIADO -> REFERENCIA_VISUAL_CRIADA -> REVISAO_PENDENTE -> CONCLUIDA`

Estados auxiliares:

- `BLOCKED_TRELLO_ACCESS`
- `BLOCKED_DUPLICATE_CARD`
- `BLOCKED_MOODBOARD`
- `BLOCKED_DATA_VALIDATION`
- `CANCELADA`

## Inicialização e retomada

Ao iniciar ou retomar:

1. Ler este runbook.
2. Ler `02_TRELLO_CONFIG.json`.
3. Ler todos os arquivos mensais em `calendario/`.
4. Ler `03_EXECUTION_STATE.json`.
5. Reconciliar todos os `post_id`; nunca inferir progresso apenas pelo calendário.
6. Antes de qualquer escrita externa, validar o destino pelos IDs exatos.

Atualizar `03_EXECUTION_STATE.json` imediatamente após cada mutação externa bem-sucedida. Não esperar o fim de um lote.

## Reconciliação antes de criar card

Para cada `post_id`:

1. Pesquisar no Trello pelo `POST ID`.
2. Pesquisar pelo título e por conceitos/serviços próximos.
3. Consultar `04_RECONCILIACAO_TRELLO_INICIAL.md`.
4. Verificar evidência de publicação quando houver card histórico semelhante. Card aberto não prova que o post está pendente.
5. Classificar o candidato:
   - `NO_MATCH`
   - `REFERENCE_ONLY`
   - `REUSE_CARD`
   - `ALREADY_PUBLISHED`
   - `DUPLICATE_BLOCKED`
6. Só criar novo cartão quando a classificação permitir.

Se houver dois candidatos plausíveis e não for possível decidir com segurança, bloquear e registrar os IDs; não criar um terceiro.

## Criação do cartão

Destino obrigatório:

- Board `622e83218d717e4a16d7856c` — Calendário Editorial.
- List `69370019555b10bb6ad19e30` — ORDEM DE SERVIÇO - SAMARA.

Título:

`ACIRV — [title] — [DD/MM/AAAA]`

Data de vencimento = `delivery_date` do planejamento, pois o vencimento representa entrega para produção/aprovação.

Descrição mínima determinística:

```text
POST ID: [post_id]
Publicação: [publish_date] | Entrega: [delivery_date] | Prioridade: [priority]
Objetivo: [rationale]
Público: empresários, associados e potenciais associados da ACIRV; segmentar quando necessário.
Formato: [format]
Mensagem/conteúdo: transformar o racional e a pauta em texto de arte suficiente para a designer produzir sem adivinhar; usar os documentos-base quando o post exigir informação específica.
CTA: [cta]
Métrica principal: [metric]
Pilar: [pillar_primary] | Secundários: [pillars_secondary]
Serviço/benefício: [service]
Direção visual: [visual_direction]
Observação: não inventar informação volátil; validar antes da arte.
```

Um cartão = uma publicação. Nunca agrupar dois `post_id` em um mesmo card.

Depois de criar ou reutilizar um card, gravar imediatamente `trello_card_id`, `trello_card_url`, classificação da reconciliação e novo status no estado.

## Moodboard e referências visuais

Enquanto `moodboard.status != READY`, não marcar qualquer post como `REFERENCIA_VISUAL_CRIADA`.

Quando o usuário adicionar referências em `moodboard/`:

1. Registrar versão, ex. `ACIRV-MOOD-v1`.
2. Inventariar arquivos.
3. Extrair paleta, hierarquia, tipografia aparente, tratamento fotográfico, composição, densidade de texto e elementos recorrentes.
4. Tratar o moodboard como direção, não template rígido.

Para cada post com card reconciliado:

1. Abrir uma nova conversa no ChatGPT.
2. Anexar moodboard/referências aprovadas.
3. Enviar briefing + direção visual.
4. Pedir uma referência conceitual, não necessariamente arte final.
5. Salvar link/arquivo/evidência da referência.
6. Vincular inequivocamente ao card e atualizar o estado.

Prompt-base:

> Crie uma referência visual conceitual para uma publicação da ACIRV. Use as referências anexadas como direção de identidade, sem copiá-las literalmente. O objetivo é orientar a designer, não substituir a arte final. Respeite hierarquia, linguagem, cores e estilo fotográfico do moodboard, adaptando a composição ao conteúdo. Evite excesso de texto e não invente informações. Briefing: [briefing].

## Eventos e replanejamento

Se surgir evento/campanha nova:

1. Confirmar data, responsável e aprovador.
2. Criar pacote pré/durante/pós.
3. Abrir espaço deslocando primeiro P3/P2.
4. Nunca apagar ou deslocar P1 silenciosamente.
5. Registrar motivo, item afetado e nova data no Git e no estado.

## Auditoria por lote

Checar:

- `post_id` e `dedupe_key` únicos;
- 1 publicação = 1 card;
- board/list corretos;
- vencimento = entrega;
- briefing presente;
- dados voláteis validados;
- referência visual única quando aplicável;
- moodboard versionado;
- nenhum candidato duplicado ignorado;
- serviços presentes com recorrência adequada;
- campanhas anuais contempladas ou justificadas.

## Conclusão

Gerar um relatório final contendo:

- total por mês, pilar, formato, campanha e serviço;
- `post_id -> Trello URL -> referência visual`;
- posts sem card, briefing ou referência;
- duplicações e bloqueios;
- mudanças de data/conteúdo;
- itens cancelados e justificativas;
- lacunas de calendário;
- inconsistências corrigidas.

Só marcar o projeto como concluído quando todos os `post_id` ativos estiverem reconciliados ou explicitamente bloqueados/cancelados com motivo.
