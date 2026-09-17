# Roadmap — ACIRV Notebook

> Estado de referência da análise: `main` em `e5e3356aa800bd84339c3f1fcaca90c64a6bf7fb` antes da criação deste roadmap.
> Atualizado em: 2026-09-17.

## Objetivo

Transformar o ACIRV Notebook em uma base de conhecimento institucional cuja relação entre fonte humana, versão Git, claim, evidência, validação, destino canônico e automação seja verificável de ponta a ponta.

A arquitetura de três camadas permanece invariável:

1. `000-Arquivos-originais/` — fonte humana primária, somente leitura para IA/automação;
2. `00-*` a `99-*` — conhecimento estruturado e canônico;
3. `Hermes/` — execução, checkpoints e estado operacional, nunca fonte única de verdade institucional.

---

## Estado atual

### Concluído / base já existente

- [x] Governança de três camadas formalizada.
- [x] Política de fontes, evidência e preservação da camada original.
- [x] Safety gate baseado em metadados/caminho antes da leitura.
- [x] Dois caminhos confirmados com credenciais bloqueados explicitamente pelo safety gate.
- [x] Inventário Git baseado em `source_path + blob_sha`.
- [x] `Ledger-de-Ingestao.jsonl` criado com 394 blobs Git inventariados.
- [x] `Claims-Canonicos.jsonl` criado.
- [x] Schema inicial de claims, dispositions, evidence classes e validation status.
- [x] Relatório reproduzível de cobertura criado.
- [x] Suite inicial com 28 testes unitários/invariantes criada.
- [x] Documentação `Hermes/Ingestao-e-Paridade.md` criada.
- [x] Reconciliação inicial de SudoExpo, KPIs de agosto, reuniões, serviços e tom de voz.
- [x] Proveniência por blob SHA introduzida em parte do canônico.

### Estado de cobertura registrado

O relatório atual registra:

- 394 blobs no ledger;
- 389 fontes processáveis;
- 0 fontes marcadas como processadas;
- 12 claims canônicos;
- paridade ainda incompleta.

Esse estado demonstra que a infraestrutura existe, mas o ciclo completo de processamento ainda não foi fechado.

---

# P0 — Segurança e governança do repositório

## P0.1 — Confirmar deliberadamente a visibilidade do repositório

- [ ] Confirmar se o repositório deve continuar público.
- [ ] Se o conteúdo institucional/interno não deve ser público, tornar o repositório privado por ação humana nas configurações do GitHub.
- [ ] Auditar dados pessoais e informações internas já publicadas antes de ampliar a ingestão.

**Critério de aceite:** decisão explícita e documentada sobre o modelo de acesso do repositório.

## P0.2 — Proteger `main`

- [ ] Parar de implementar ingestão/reconciliação diretamente em `main`.
- [ ] Criar workflow CI somente leitura (`permissions: contents: read`) para testes e invariantes.
- [ ] Exigir PR para alterações da pipeline e do canônico.
- [ ] Habilitar proteção de branch/required checks por configuração humana do GitHub, se desejado.

**Critério de aceite:** mudanças futuras da ingestão passam por branch + PR + checks antes de entrar em `main`.

## P0.3 — Tornar a imutabilidade da camada original verificável em runtime

Problema atual: `validar_invariantes.py` compara `main..HEAD`; quando executado no próprio `main`, esse diff é necessariamente vazio. Mudanças não commitadas na camada original são apenas avisadas.

- [ ] Implementar snapshot de estado da camada original antes e depois da execução da pipeline, sem abrir conteúdo sensível.
- [ ] Detectar qualquer alteração adicional causada pela automação durante a execução.
- [ ] Separar alterações humanas pré-existentes de alterações produzidas pela pipeline.
- [ ] Manter uma verificação CI adicional para impedir commits que toquem `000-Arquivos-originais/` em PRs de automação.

**Critério de aceite:** a automação consegue provar que não alterou a camada original durante uma execução.

---

# P1 — Hardening da infraestrutura de ingestão

## P1.1 — Corrigir a idempotência real do inventário

Problema atual: uma entrada existente com o mesmo `(source_path, blob_sha)` só é pulada se `processing_status` não for `unprocessed/error`. Assim, fontes ainda não processadas podem ser reconstruídas e contabilizadas novamente como `new_entries` em execuções sucessivas, atualizando `inventoried_at` e gerando ruído no ledger mesmo sem delta Git.

- [ ] Distinguir claramente `já inventariado` de `já processado`.
- [ ] Mesmo blob já inventariado nunca deve voltar a ser classificado como `new_entries`.
- [ ] Preservar `inventoried_at` da primeira observação.
- [ ] Criar estado/contador separado para `existing_unprocessed`.
- [ ] Não reescrever linhas do ledger sem mudança material.
- [ ] Tratar `sensitive_do_not_read` e `unsupported` como estados contabilizados, não como entradas eternamente “novas”.

**Critério de aceite:** duas execuções consecutivas sem mudança Git produzem zero delta semântico e zero diff no ledger/relatório, exceto timestamp de execução quando explicitamente desejado.

## P1.2 — Fechar o ciclo `fonte → claims → ledger`

Problema atual: existem claims e alterações canônicas originadas de fontes cujo ledger continua com `processing_status=unprocessed`.

- [ ] Implementar transição transacional de processamento.
- [ ] Registrar `processing_status`, `last_processed`, `processor_version`, quantidade de claims e resultado da reconciliação.
- [ ] Considerar estados como `in_progress`, `partially_processed`, `processed`, `error` se realmente necessários.
- [ ] Uma fonte só pode ser `processed` quando todos os seus claims materiais tiverem disposition explícita.
- [ ] O validador deve detectar claims ligados a fonte ainda marcada como não processada e vice-versa.

**Critério de aceite:** nenhuma fonte com claims materiais concluídos permanece silenciosamente `unprocessed`.

## P1.3 — Corrigir métricas de cobertura

Problemas atuais:

- `source_accounting_coverage` é calculada como `total_fontes / total_fontes`, portanto retorna 100% por construção;
- `0_secrets_lidos` é reportado como `True` por configuração, sem evidência de execução;
- fontes local-only ignoradas pelo Git não entram no denominador do inventário Git.

- [ ] Comparar ledger com a árvore Git atual para medir cobertura de inventário de verdade.
- [ ] Separar `git_tracked_source_coverage` de `known_local_only_source_accounting`.
- [ ] Criar registro metadata-only dos caminhos locais deliberadamente excluídos, sem ler seus conteúdos.
- [ ] Trocar `0_secrets_lidos` por métrica verificável, como `known_sensitive_paths_blocked`, salvo se existir audit log capaz de provar tentativas de leitura.
- [ ] Diferenciar cobertura de inventário, processamento, claim disposition, proveniência e validação.

**Critério de aceite:** nenhuma métrica pode ficar em 100% por tautologia ou por valor hardcoded.

## P1.4 — Parsing estrito de JSONL

Problema atual: linhas inválidas do ledger podem ser ignoradas silenciosamente; claims inválidos podem ser omitidos no carregamento e não necessariamente fazer o validador falhar.

- [ ] Validadores devem falhar em JSON inválido.
- [ ] Relatórios não podem omitir silenciosamente linhas corrompidas.
- [ ] Incluir número da linha e arquivo no erro.
- [ ] Validar enums, SHA, path root, tipos e timestamps relevantes.

**Critério de aceite:** corrupção de qualquer linha do ledger/claims causa FAIL explícito.

## P1.5 — Integridade referencial dos claims

- [ ] Garantir unicidade de `claim_id`.
- [ ] Validar que `source_path + source_blob_sha` existe no ledger ou em registro histórico válido.
- [ ] Validar que `canonical_destination` existe.
- [ ] Validar `supersedes`, `contradicts` e `duplicates` contra claims reais.
- [ ] Não permitir referência órfã como `supersedes` apontando para claim inexistente.
- [ ] Padronizar IDs para ASCII estável (`orcamento`, não `orçamento`).
- [ ] Definir política de migração/alias para IDs já criados.

**Critério de aceite:** zero referências órfãs e zero IDs ambíguos/duplicados.

## P1.6 — Tornar anchors de destino verificáveis

Problema atual: valores como `cronograma`, `conecta`, `orcamento` e `metricas` não necessariamente correspondem aos headings reais das notas Markdown.

- [ ] Preferir block IDs explícitos ou headings normalizados verificáveis.
- [ ] Validar `destination_anchor` quando presente.
- [ ] Não exigir anchor quando a granularidade de arquivo for suficiente.

**Critério de aceite:** todo anchor registrado resolve para um ponto real do destino.

## P1.7 — Separar proveniência documental de validação humana

Problema atual: alguns claims foram alterados com base em validação humana, mas continuam usando como `source_path` um documento que não necessariamente sustenta sozinho o estado final validado.

- [ ] Adicionar mecanismo de `supporting_sources` / `validation_source` / `validation_record` ou equivalente mínimo.
- [ ] Registrar validações humanas no `Registro-de-Decisoes` ou artefato canônico equivalente.
- [ ] Claim documental deve continuar apontando para a fonte documental.
- [ ] Estado validado por humano deve apontar também para o registro dessa validação.

**Critério de aceite:** é possível distinguir “a fonte disse X” de “o humano validou Y a partir de X + contexto”.

## P1.8 — Atomicidade de claims

Revisar claims que hoje agrupam múltiplas propriedades, por exemplo:

- métricas de agosto em um único claim;
- orçamento da SudoExpo agregando vários movimentos financeiros;
- áreas + gratuidade + canal de consultorias no mesmo claim.

- [ ] Dividir apenas quando propriedades possuírem ciclos de validade ou validação independentes.
- [ ] Permitir valor estruturado somente quando representar uma unidade semântica real.

**Critério de aceite:** cada claim pode ser validado, substituído ou contradito sem obrigar alteração de fatos independentes.

## P1.9 — Semântica de `promoted` × `pending_validation`

- [ ] Definir quando `promoted + pending_validation` é permitido.
- [ ] Se permitido, exigir que o destino canônico marque a informação como provisória/pendente.
- [ ] Para fatos documentais que não exigem validação humana, usar status coerente (`not_required` ou equivalente), em vez de deixar tudo pendente.
- [ ] Criar invariante contra fato pendente apresentado como verdade definitiva.

**Critério de aceite:** status de validação tem consequência real na apresentação canônica.

---

# P2 — Qualidade dos testes e CI

## P2.1 — Transformar testes unitários tautológicos em testes de integração

A suite atual é uma boa base, mas vários testes apenas reimplementam a lógica esperada dentro do próprio teste.

- [ ] Criar repositório Git temporário nos testes.
- [ ] Executar `inventariar_fontes.py` de verdade.
- [ ] Rodar duas vezes e provar idempotência real.
- [ ] Alterar um blob e provar versionamento.
- [ ] Remover/renomear fonte e verificar comportamento.
- [ ] Injetar JSONL corrompido e exigir falha.
- [ ] Criar referência de claim órfã e exigir falha.
- [ ] Simular tentativa de escrita na camada original e exigir falha.
- [ ] Testar geração do relatório contra árvore Git real do fixture.

## P2.2 — GitHub Actions mínimo e seguro

- [ ] Criar workflow apenas de leitura.
- [ ] `permissions: contents: read`.
- [ ] Sem secrets, sem `contents: write`, sem execução dinâmica/base64.
- [ ] Rodar testes, validador e checks de schema.
- [ ] Falhar se PR de automação modificar `000-Arquivos-originais/`.

**Critério de aceite:** um commit quebrando invariantes não pode passar CI.

---

# P3 — Consistência da camada canônica

## P3.1 — Corrigir inconsistências já encontradas

- [ ] Atualizar frontmatter (`ultima_revisao`, versão quando apropriado) nas notas modificadas em 17/09 e ainda marcadas como revisão antiga.
- [ ] Corrigir a seção `Claims registrados` de `SudoExpo-2026.md`, que ainda descreve `sudoexpo.2026.situacao_financeira.alerta` como `pending_validation` após a validação ter sido promovida.
- [ ] Garantir que `Validacoes-Humanas-Necessarias.md`, claims e notas canônicas concordem sobre o mesmo estado.
- [ ] Atualizar `Lacunas-de-Cobertura.md` à medida que lacunas forem realmente fechadas; não apagar lacunas ainda abertas.

## P3.2 — Revisar claims atuais antes de ampliar o corpus

- [ ] Revalidar os 12 claims atuais contra suas fontes e decisões humanas.
- [ ] Corrigir atomicidade, IDs, anchors, relations e validation status.
- [ ] Marcar no ledger as fontes já realmente processadas nesta primeira reconciliação.

**Critério de aceite:** o lote inicial serve como exemplar correto para o processamento histórico futuro.

---

# P4 — Pipeline operacional real

## P4.1 — Criar um orquestrador de ingestão/reconciliação

A rotina atual possui inventário, validação e relatório, mas não existe um estágio determinístico único que feche o processamento das fontes.

- [ ] Implementar um comando/orquestrador que trabalhe apenas sobre o delta.
- [ ] Registrar início/fim/resultado sem armazenar conteúdo sensível em logs.
- [ ] Atualizar ledger apenas após reconciliação concluída.
- [ ] Suportar retomada após interrupção.
- [ ] Evitar estado parcialmente escrito usando escrita atômica/temporária quando necessário.

Possível fluxo:

`scan → safety → select delta → Hermes/humano extrai claims → reconcile → validate → commit state → report`

O estágio de interpretação semântica pode continuar sendo executado pelo Hermes/IA; o estado ao redor dele deve ser determinístico.

## P4.2 — Overrides de classificação

Hoje domínio/tipo/autoridade são inferidos principalmente por nome e várias fontes recebem `nota_operacional_humana` por padrão.

- [ ] Introduzir `unknown/unclassified` quando a autoridade não puder ser determinada por metadados.
- [ ] Criar overrides explícitos para fontes importantes.
- [ ] Evitar que um PDF institucional, relatório estruturado ou conversa receba autoridade incorreta só pelo default.
- [ ] Corrigir heurísticas conflitantes (`saas`, CAM, tecnologia etc.).

---

# P5 — Reconciliação histórica do corpus

Somente iniciar em escala após P1–P4 estarem estáveis.

## Onda 1 — piloto controlado

- [ ] Processar 10–20 fontes representativas de domínios diferentes.
- [ ] Incluir pelo menos: estratégia, reunião, métricas, SudoExpo, serviços, imprensa e campanha.
- [ ] Medir claims por fonte, taxa de `not_material`, conflitos e validações pendentes.
- [ ] Rodar idempotência após o lote.

## Onda 2 — lacunas prioritárias

- [ ] Serviços e benefícios.
- [ ] SudoExpo e pós-evento.
- [ ] Reuniões/decisões julho–setembro.
- [ ] KPIs e histórico operacional.
- [ ] Imprensa.
- [ ] CAM com política jurídica/confidencial apropriada.
- [ ] Stakeholders separando fato de interpretação.

## Onda 3 — domínios já bons / proveniência retroativa

- [ ] Campanha de Pertencimento.
- [ ] Conecta ACIRV.
- [ ] Estratégia e marca.
- [ ] Processos críticos.

## Onda 4 — corpus remanescente

- [ ] Processar progressivamente todos os blobs textuais materiais ainda não classificados.
- [ ] Registrar `duplicate`, `superseded`, `historical_only/not_material`, `pending_validation`, `contradiction` e `promoted` conforme aplicável.

**Critério de aceite:** nenhum blob processável permanece sem estado explícito.

---

# P6 — Formatos não Markdown

- [ ] Adicionar pipeline seguro para PDFs não sensíveis quando necessário.
- [ ] Preservar ZIPs em quarentena técnica; nunca extrair automaticamente conteúdo suspeito de `.env`, chaves ou credenciais.
- [ ] Definir política para planilhas/documentos futuros caso apareçam no corpus.
- [ ] Registrar `unsupported` somente quando realmente não houver parser seguro disponível.

---

# P7 — Hermes e automação diária

- [ ] Atualizar `Hermes/Ingestao-e-Paridade.md` após o hardening.
- [ ] Garantir que a rotina diária use o ledger como checkpoint real.
- [ ] Processar somente delta material.
- [ ] Não notificar quando nada mudou.
- [ ] Abrir branch/PR para promoções canônicas; nunca alterar `main` diretamente por padrão.
- [ ] Nunca fazer merge automático.
- [ ] Emitir resumo de: fontes novas/modificadas, claims, conflitos, validações e cobertura.

Comandos mínimos já definidos:

```bash
python 98-Infraestrutura/ingestao/inventariar_fontes.py .
python 98-Infraestrutura/ingestao/validar_invariantes.py .
python 98-Infraestrutura/ingestao/relatorio_cobertura.py .
```

Esses comandos devem permanecer idempotentes e auditáveis.

---

# P8 — Critério final de paridade

Só declarar paridade quando todos os critérios abaixo forem verificáveis, não presumidos:

- [ ] 100% das fontes Git atuais contabilizadas contra a árvore Git real.
- [ ] Fontes local-only conhecidas contabilizadas por metadata sem leitura de segredo.
- [ ] 100% das fontes processáveis com estado terminal explícito.
- [ ] 100% dos claims materiais com disposition.
- [ ] 100% dos claims promovidos com proveniência válida e destino existente.
- [ ] Zero relações entre claims órfãs.
- [ ] Zero divergências silenciosas de validação.
- [ ] Zero fatos `pending_validation` apresentados como canônicos definitivos sem marcação.
- [ ] Safety gate bloqueando todos os caminhos conhecidos/suspeitos antes da leitura.
- [ ] Pipeline provando que não modifica `000-Arquivos-originais/`.
- [ ] Segunda execução sem delta gera zero mudança semântica.
- [ ] Relatório de cobertura reproduz o estado real do repositório.

---

# Próximo passo recomendado

**Não iniciar ainda o processamento em massa dos 389 blobs processáveis.**

A próxima etapa é um ciclo de **hardening da infraestrutura + correção do lote inicial**, cobrindo principalmente P0–P4. Depois disso, executar um piloto controlado e só então escalar a reconciliação histórica.

Este `roadmap.md` deve ser atualizado ao fim de cada PR relevante, marcando itens concluídos e registrando novas lacunas descobertas.