---
id: chatgpt-ingestao-agendada
titulo: ChatGPT-Protocolo-de-Ingestao-Agendada
aliases: [protocolo-chatgpt-agendado]
tipo: documentacao
status: ativo
profundidade: avancada
versao_schema: '2.0'
versao_conteudo: '2.0'
idioma: pt-BR
data_criacao: '2026-09-17'
ultima_revisao: '2026-09-17'
grau_confianca: alto
confidencialidade: interno
---

# Protocolo do ChatGPT Agendado — Ingestão Semântica Narrativa (GitHub-First)

> [!summary] Síntese
> Manual operacional para execuções periódicas do **ChatGPT Agendado** (via GitHub / Conector). Orienta o agente a atuar como a camada cognitiva e editorial do ACIRV Notebook no modelo **GitHub-First**, sem depender de shell local ou ambiente de execução persistente no cliente.

## 1. Arquitetura GitHub-First

O ChatGPT Agendado opera diretamente sobre a API/interface do GitHub:

- **ChatGPT Agendado = Camada Cognitiva e Editorial:** Consulta o estado do repositório no GitHub, identifica deltas, aplica regras de segurança por metadados de caminho, lê fontes elegíveis, sintetiza narrativas canônicas em `00-*` a `99-*`, gera âncoras de evidência (`Claims-Canonicos.jsonl`), atualiza o ledger (`Ledger-de-Ingestao.jsonl`) e abre a Pull Request.
- **GitHub Actions (CI) = Validador de Infraestrutura:** Executa os scripts Python (`validar_invariantes.py`, `claims.py`, `test_invariantes.py`) automaticamente durante a abertura/atualização da PR para garantir integridade, schema e imutabilidade da camada de origem.
- **Scripts Python Locais = Ferramentas Auxiliares:** Servem para diagnósticos locais, auditorias sob demanda e execução offline — **não são um requisito existencial da automação agendada**.

---

## 2. Fluxo Principal do ChatGPT Agendado (GitHub-First)

```text
ChatGPT Agendado (via GitHub)
        ↓
1. Consulta o estado da branch main no GitHub
        ↓
2. Identifica fontes novas ou alteradas em 000-Arquivos-originais/ (via tree/history/ledger)
        ↓
3. Aplica Safety Gate por metadados de caminho (bloqueia credenciais sem abrir conteúdo)
        ↓
4. Lê o conteúdo das fontes elegíveis (não sensíveis e suportadas)
        ↓
5. Lê o contexto canônico relacionado em 00-* a 99-*
        ↓
6. Compreende semanticamente a mudança (distingue fatos, temporalidades e intenções)
        ↓
7. Escreve/Atualiza NOTAS CANÔNICAS NARRATIVAS (seguindo o Contrato Editorial)
        ↓
8. Gera/Atualiza âncoras de evidência materiais em Claims-Canonicos.jsonl (quando relevante)
        ↓
9. Atualiza o review_status no Ledger-de-Ingestao.jsonl (reviewed / reviewed_no_material_change)
        ↓
10. Cria branch no GitHub e abre Pull Request para main
        ↓
11. GitHub Actions (CI) roda validadores determinísticos Python
        ↓
12. Humano revisa a narrativa e realiza o merge consciente (sem auto-merge)
```

---

## 3. Protocolo Detalhado de Operação (18 Passos)

1. **Consultar Main no GitHub:** Verificar a árvore atual da branch `main` no GitHub.
2. **Comparar com Ledger:** Ler `85-Bases-e-Consultas/Ledger-de-Ingestao.jsonl` para listar fontes com `review_status = unreviewed` ou blobs recentes não registrados.
3. **Aplicar Safety Gate por Metadados:** Verificar o caminho do arquivo contra regras de segurança. **NUNCA abrir** `Contas e Senhas.md`, `Minha Chave API Antropic.md`, nem arquivos contendo padrões de credencial ou extensões em quarentena (`.zip`, `.pdf`).
4. **Filtrar Lote de Leitura:** Selecionar apenas o delta de fontes normais e suportadas.
5. **Ler Fontes do Delta:** Recuperar o texto dos arquivos selecionados via GitHub.
6. **Localizar Notas Canônicas Relacionadas:** Identificar as notas canônicas afetadas em `00-*` a `99-*`.
7. **Ler Contexto Canônico Existente:** Ler a versão atual dessas notas no GitHub.
8. **Compreender a Mudança Semântica:** Analisar se a fonte traz fatos novos, mudanças de cronograma, resultados de métricas ou se é um documento redundante/histórico.
9. **Extrair Evidências Materiais:** Isolar declarações quantitativas ou normativas relevantes (datas, KPIs, valores, alçadas).
10. **Avaliar Novidade Real:** Se a fonte não trouxer alteração narrativa material, registrar `review_status: reviewed_no_material_change` com 0 novos claims no ledger e encerrar a análise daquela fonte.
11. **Sintetizar Narrativa Canônica:** Escrever/atualizar a nota em Markdown seguindo o [[Contrato-de-Nota-Canonica-Narrativa]] (storytelling orientado a dados, distinção de 6 fases temporais, fatos vs interpretação vs incertezas).
12. **Registrar Claims de Evidência:** Adicionar âncoras atômicas em `Claims-Canonicos.jsonl` com IDs ASCII, `supporting_sources` e `canonical_destination`.
13. **Atualizar Metadata de Review no Ledger:** Atualizar a entrada da fonte em `Ledger-de-Ingestao.jsonl` com `review_status: reviewed`, `last_reviewed_at`, `reviewed_by: "ChatGPT-Agendado"`.
14. **Criar Branch de Entrega:** Criar uma nova branch (ex: `auto/ingestion-YYYY-MM-DD`).
15. **Submeter Commits e Abrir PR:** Enviar as alterações e abrir a Pull Request no GitHub.
16. **Disparo do CI:** O GitHub Actions executa automaticamente a suíte de validação Python (`.github/workflows/ci.yml`).
17. **Acompanhar Validação:** O ChatGPT/humano observa os checks do CI na PR.
18. **Silêncio sem Novidade:** Se nenhuma fonte do delta contiver novidade material, o ChatGPT não cria PRs ruidosas nem promove alterações cosméticas.
