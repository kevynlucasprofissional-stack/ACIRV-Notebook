---
id: chatgpt-ingestao-agendada
titulo: ChatGPT-Protocolo-de-Ingestao-Agendada
aliases: [protocolo-chatgpt-agendado]
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

# Protocolo do ChatGPT Agendado — Ingestão Semântica e Paridade

> [!summary] Síntese
> Manual operacional para execuções periódicas do **ChatGPT Agendado** (via GitHub / Agendados). Orienta o agente a atuar como a camada cognitiva e editorial do ACIRV Notebook.

## 1. Papel do ChatGPT Agendado

O ChatGPT Agendado é a **camada cognitiva e editorial principal** do repositório.

Seu trabalho é:
- Ler os deltas de fontes primárias novas ou modificadas em `000-Arquivos-originais/`;
- Compreender o contexto histórico e temporal dos documentos;
- Atualizar ou criar notas canônicas narrativas em `00-*` a `99-*` (seguindo o [[Contrato-de-Nota-Canonica-Narrativa]]);
- Gerar ou atualizar âncoras de evidência (`Claims-Canonicos.jsonl`) quando houver fatos materiais (KPIs, valores, datas, decisões);
- Atualizar o estado de revisão no ledger (`Ledger-de-Ingestao.jsonl`);
- Abrir um Pull Request auditável no GitHub (sem auto-merge).

---

## 2. Protocolo de Execução Passo a Passo (18 Passos)

1. **Obter Estado Atual:** Ler a branch `main` e o arquivo `85-Bases-e-Consultas/Ledger-de-Ingestao.jsonl`.
2. **Detectar Deltas:** Executar `python 98-Infraestrutura/ingestao/inventariar_fontes.py .` para identificar fontes com `review_status = unreviewed` ou novas versões de blobs.
3. **Aplicar Safety Gate:** Verificar a classificação do `safety_gate.py`. **NUNCA abrir** arquivos com `read_status = sensitive_do_not_read` (`Contas e Senhas.md`, `Minha Chave API Antropic.md`, credenciais ou ZIPs em quarentena).
4. **Filtrar Lote de Trabalho:** Selecionar o delta de fontes não sensíveis e suportadas.
5. **Ler Fontes do Delta:** Ler o conteúdo textual apenas das fontes elegíveis do lote.
6. **Localizar Notas Canônicas Relacionadas:** Identificar quais notas em `00-*` a `99-*` correspondem ao assunto.
7. **Ler Contexto Canônico Existente:** Ler a versão atual das notas canônicas afetadas para entender o histórico prévio.
8. **Compreender a Mudança Semântica:** Identificar o que a fonte traz de novo:
   - Nova decisão, cronograma ou resultado?
   - Confirmação de dado existente?
   - Dado histórico sem novidade material (`reviewed_no_material_change`)?
9. **Extrair Fatos e Evidências Materiais:** Isolar declarações quantitativas ou normativas relevantes (datas, KPIs, valores, alçadas).
10. **Avaliar Novidade Real:** Se a fonte for redundante ou sem efeito canônico, marcar `review_status: reviewed_no_material_change` com 0 novos claims e encerrar a análise daquela fonte.
11. **Atualizar/Criar Notas Narrativas:** Escrever/editar a nota canônica narrativa seguindo o [[Contrato-de-Nota-Canonica-Narrativa]].
12. **Registrar Claims de Evidência:** Adicionar/atualizar claims em `85-Bases-e-Consultas/Claims-Canonicos.jsonl` com IDs ASCII, `supporting_sources` e `canonical_destination`.
13. **Atualizar Review Status no Ledger:** Atualizar `Ledger-de-Ingestao.jsonl` registrando `review_status: reviewed` (ou `reviewed_no_material_change`), `last_reviewed_at`, `reviewed_by: "ChatGPT-Agendado"`.
14. **Validar Mecanicamente:** Executar os verificadores determinísticos:
    ```bash
    python 98-Infraestrutura/ingestao/claims.py .
    python 98-Infraestrutura/ingestao/validar_invariantes.py .
    python 98-Infraestrutura/ingestao/relatorio_cobertura.py .
    python -m pytest 98-Infraestrutura/ingestao/test_invariantes.py -v
    ```
15. **Criar Branch no Git:** Criar branch de entrega (ex: `auto/ingestion-2026-09-17`).
16. **Abrir Pull Request:** Criar PR para `main` detalhando: fontes revisadas, notas alteradas, claims gerados e resultados das validações.
17. **NÃO Fazer Merge:** Deixar o PR aberto para revisão e aprovação humana.
18. **Silêncio sem Novidade:** Se a varredura não encontrar nenhuma novidade material no delta, não gerar PRs ruidosos ou alterações cosméticas.

---

## 3. Regras Absolutas de Segurança e Preservação

- **Imutabilidade da Origem:** NUNCA editar, criar, mover, renomear ou deletar qualquer arquivo em `000-Arquivos-originais/`.
- **Proteção de Segredos:** NUNCA ler ou transcrever credenciais de arquivos classificados como sensíveis.
- **Não Invenção:** NUNCA inferir relações de causalidade não sustentadas por documentos ou validação humana explícita.
- **Autonomia Limitada:** Fazer proposta via PR; a decisão final de mesclagem é sempre do operador humano.
