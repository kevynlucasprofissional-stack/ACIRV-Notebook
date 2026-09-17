---
id: hermes-ingestao-paridade
titulo: Hermes-Ingestao-e-Paridade
aliases: []
tipo: documentacao
status: ativo
profundidade: avancada
versao_schema: '1.0'
versao_conteudo: '1.0'
idioma: pt-BR
data_criacao: '2026-09-17'
ultima_revisao: '2026-09-17'
grau_confianca: alto
confidencialidade: interno
---

# Hermes — Documentação de Ingestão e Paridade

> [!summary] Síntese
> Documentação para o Hermes executar o pipeline de ingestão determinístico, reconciliação e paridade entre `000-Arquivos-originais/` e a camada canônica.

## Pipeline que o Hermes pode executar

```
scan (git ls-files → ledger delta)
  ↓
safety gate (classificar antes de abrir)
  ↓
ingest (ler apenas read_status=unread)
  ↓
extract claims (por fonte lida)
  ↓
reconcile (comparar com canônico existente)
  ↓
propose canonical changes (somente quando evidence suficiente)
  ↓
validate (rodar validar_invariantes.py)
  ↓
PR (abrir, NÃO fazer merge)
```

## Comandos disponíveis

```bash
# Inventariar fontes novas/modificadas (idempotente)
python 98-Infraestrutura/ingestao/inventariar_fontes.py <vault_root>

# Validar invariantes
python 98-Infraestrutura/ingestao/validar_invariantes.py <vault_root>

# Gerar relatório de cobertura
python 98-Infraestrutura/ingestao/relatorio_cobertura.py <vault_root>

# Validar claims
python 98-Infraestrutura/ingestao/claims.py 85-Bases-e-Consultas/Claims-Canonicos.jsonl

# Rodar testes
cd 98-Infraestrutura/ingestao
python -m pytest test_invariantes.py -v
```

## Regras absolutas para o Hermes

1. **NUNCA** criar, editar, mover ou excluir arquivos em `000-Arquivos-originais/`
2. **NUNCA** abrir arquivo com `read_status = sensitive_do_not_read`
3. **SEMPRE** rodar safety gate antes de abrir qualquer arquivo
4. **NUNCA** fazer merge automático de PR
5. **NUNCA** marcar contradiction como validated sem resolução explícita
6. **SEMPRE** registrar source_blob_sha em claims promovidos
7. **SEMPRE** testar idempotência antes de publicar

## Arquivos sensíveis confirmados (NUNCA ABRIR)

- `000-Arquivos-originais/Contas e Senhas.md`
- `000-Arquivos-originais/Minha Chave API Antropic.md`

## Ledger de ingestão

Local: `85-Bases-e-Consultas/Ledger-de-Ingestao.jsonl`

O Hermes deve:
- Ler o ledger para saber o que já foi processado
- Processar apenas entradas com `processing_status = unprocessed` e `read_status = unread`
- Atualizar `processing_status → processed` após processamento bem-sucedido
- Nunca reprocessar se `(source_path, blob_sha)` já foi processado com sucesso

## Claims canônicos

Local: `85-Bases-e-Consultas/Claims-Canonicos.jsonl`

- Cada claim deve ter `disposition` explícita
- Claims promovidos devem ter `source_blob_sha` + `canonical_destination`
- Contradições devem ter `validation_status = pending_validation` (nunca `validated`)
- Usar `claim_id` semântico: `entidade.propriedade.qualificador`

## Comportamento em caso de falha/restart

O ledger persiste o estado. Se o Hermes for interrompido e reiniciado:
- Fontes com `processing_status = unprocessed` serão reprocessadas
- Fontes com `processing_status = processed` serão puladas (idempotência)
- O `blob_sha` garante que reprocessar a mesma versão é seguro

## Relatório de cobertura

O Hermes deve gerar e incluir o relatório de cobertura em cada PR para informar:
- quantas fontes foram processadas
- quantos claims foram gerados
- cobertura por domínio
- pendências humanas restantes

## O que NÃO é responsabilidade do Hermes

- Resolver conflitos institucionais (registrar como `contradiction`)
- Decidir entre fontes divergentes sem evidência clara (registrar como `pending_validation`)
- Validar decisões que dependem de humano
- Fazer merge de PRs

## Integração com o vault

O Hermes opera nas camadas:
- **Leitura:** `000-Arquivos-originais/` (somente não sensíveis)
- **Escrita/atualização:** `85-Bases-e-Consultas/`, `07-Reunioes-e-Decisoes/`, `03-*`, `04-*`, `05-*`, `06-*`
- **Nunca:** `.obsidian/`, `000-Arquivos-originais/`
