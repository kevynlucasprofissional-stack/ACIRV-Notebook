# Instagram Insights — operação de coleta e base canônica

Camada 3 do vault (agentes e automações). Este é o **ponto único de referência** para a coleta de métricas do Instagram institucional `@acirvoficial`.

## Onde cada coisa mora

| O que | Onde | Camada |
|---|---|---|
| Export manual (XLSX) feito por humano | `000-Arquivos-originais/Dados para mega-relatório pós Sudoexpo/Redes sociais/` | 1 — fonte original (somente leitura para IA) |
| **Base canônica** (1 linha por publicação) | `85-Bases-e-Consultas/Instagram-Publicacoes-<AAAA-MM>.csv` | 2 — canônica |
| Dicionário da base + regras | `85-Bases-e-Consultas/LEIA-ME-Instagram-Insights.md` | 2 — canônica |
| Notas de métrica e diagnóstico | `05-Metricas-e-Decisao/` | 2 — canônica |
| Índice da fonte bruta / rastreabilidade | `97-Fontes-Brutas/01-Indices/Fonte - Instagram Insights.md` | 2 — canônica |
| **Captura crua + scripts** (este diretório) | `Hermes/instagram-insights/` | 3 — agentes |
| **Foto do painel da conta** (camada 2 da captura) | `Hermes/instagram-insights/captura/<mês>-<ano>/_painel_conta_<AAAA-MM-DD>_<timeframe>.json` | 3 — agentes |

Regra: captura crua e script de agente **nunca** ficam em `000-Arquivos-originais/` (AGENTS.md). O que vai para a camada 2 é a base consolidada, não o raw.

## As duas camadas de captura — sempre as duas

O Instagram expõe **duas medições diferentes** e nenhuma substitui a outra. Toda coleta passa a registrar as duas.

| | Camada 1 — post a post | Camada 2 — painel da conta |
|---|---|---|
| URL | `/insights/media/<media_id>/` | `/accounts/insights/?timeframe=30` |
| Unidade | a publicação (`media_id`) | a conta, na janela |
| Escopo | feed + reels do grid | Posts, Reels, **Stories**, Vídeos, split Instagram/Facebook |
| Contagem | visualizações **acumuladas** pelo post até a coleta | visualizações **ocorridas** na janela, em todo conteúdo |
| Resultado | base canônica por post | foto de totais, % e listas de destaque |

Lista ranqueada de conteúdo (mesmo painel, já filtrada):
`/accounts/insights/content/?media_type=all&metric=views&sort_by=highest&timeframe=30&view_type=card` — e o mesmo com `metric=interactions` e `media_type=posts|reels|stories|videos`.

**Nunca somar as duas nem "corrigir" uma pela outra.** Leitura verificada em 02/10/2026, `timeframe=30`: painel **1.315.639** visualizações contra **497.290** somadas dos 116 posts de setembro (2,6x). As causas, em ordem de peso:

1. **Janela** — a página é uma janela móvel de 30 dias terminando hoje (03/09 a 02/10); a base é o período calendário (01–30/09).
2. **Escopo** — o painel inclui Stories (31,2% do total, ~410 mil), Vídeos e Facebook (1.783); a base só tem feed e reels do grid.
3. **Unidade de contagem** — o painel conta visualização *por data em que ocorreu*, inclusive em conteúdo de meses anteriores; a base conta o acumulado do post até o instante da coleta.
4. **Unicidade** — `Visualizadores` e `Contas com engajamento` são únicos *por conteúdo*; somar por post duplica a mesma pessoa.

Onde as duas conversam: **interações** (painel 17.779 × base 18.414, −3,5%), porque 92% delas vêm de feed+reels; e as **magnitudes por conteúdo** da lista ranqueada (14,2 mil ≈ 14.153; 13,7 mil ≈ 13.052). Visualizações nunca fecham.

## Estrutura

```text
Hermes/instagram-insights/
  README.md                     (este arquivo)
  captura/
    setembro-2026/              raws + pipeline de setembro (+ _painel_conta_*.json)
    agosto-2026/                raws + pipeline de agosto
```

Cada `captura/<mes>-<ano>/` mantém os scripts e os JSONL brutos juntos, porque os scripts leem os artefatos do próprio diretório.

## Pipeline (setembro-2026)

1. `_sweep_build.py` — varre o grid de `@acirvoficial` e gera `_grid_inventario2.json` + `_worklist2.json`.
2. captura por post — para cada `media_id`, abre `https://www.instagram.com/insights/media/<media_id>/` e grava o texto do painel em `_raw*.jsonl` (um arquivo por lote).
3. `_consolidar2.py` — junta os raws em `_cap2_consolidado.json` e reporta faltantes/suspeitos.
4. `_unificar_setembro.py` — **passo final**: junta a run 01–14/09 (`_set_linhas.json`) e a run 15–30/09 (`_set2_linhas.json`), acrescenta a captura tardia, valida contra o inventário e grava:
   - `_setembro_2026_116.jsonl` — 116 registros normalizados;
   - `85-Bases-e-Consultas/Instagram-Publicacoes-2026-09.csv` — base canônica.
5. captura do painel da conta — abre `/accounts/insights/?timeframe=...` e a lista ranqueada, e grava `_painel_conta_<AAAA-MM-DD>_<timeframe>.json` com `coletado_em`, janela estimada, totais, % por tipo e a lista de destaque (valores **como renderizados**: `"99 mil"`, `"--"`).

Rodar de dentro de `captura/setembro-2026/`:

```bash
python _unificar_setembro.py
```

O script localiza a raiz do vault sozinho (sobe a árvore até achar `85-Bases-e-Consultas/`), então funciona em qualquer lugar do repositório.

## Como acrescentar um mês novo

1. Criar `captura/<mes>-<ano>/`.
2. Varredura do grid → inventário do mês.
3. Captura post a post → raws.
4. Consolidar → conferir *faltando: 0*.
5. **Capturar o painel da conta** (camada 2) → `_painel_conta_<AAAA-MM-DD>_<timeframe>.json`, com data/hora da leitura e a janela. A página do painel costuma renderizar vazia no primeiro carregamento: reler depois de ~3 s até a lista aparecer.
6. Unificar → gerar `85-Bases-e-Consultas/Instagram-Publicacoes-<AAAA-MM>.csv` com o **mesmo cabeçalho de 34 colunas** de `Instagram-Publicacoes-2026-09.csv`.
7. Registrar a base em `85-Bases-e-Consultas/LEIA-ME-Instagram-Insights.md` e no índice de fontes, informando também o total do painel da janela correspondente e a data da leitura.

## Estado atual

- **Setembro/2026 fechado: 116/116 posts** do grid (60 próprios + 56 em colaboração), 25 dias com publicação, 01/09 a 30/09. Verificado por igualdade de conjunto entre inventário do grid, base canônica e capturas normalizadas (`_conferencia_final.py`).
- Setembro foi o mês em que a coleta ficou completa pela primeira vez: as duas runs (01–14 e 15–30) foram unificadas e o post faltante foi recapturado.
- Atenção ao **envelhecimento**: a run 01–14/09 foi coletada em **14/09** e a run 15–30/09 em **02/10**. Um período capturado em duas idades não é uma fotografia única — o campo `coletado_em` de cada registro existe para isso.

## Limitações conhecidas

- `media_id 3982692900246340349` (reel em colaboração com `keniasleite`, 09/09): o painel de insights da ACIRV devolve `--` para visualizações, visualizadores e interações. A base registra a ausência em `metricas_ausentes` e deixa o número bruto da API pública em `notas` (não é o mesmo metro do painel). Não é falha de coleta: o painel não expõe os dados para este post.
- Métricas de "Atividade do perfil" e "Novos seguidores" não aparecem no rodapé da maioria dos posts; são marcadas como ausentes em vez de zeradas. `atividade_do_perfil` falta em **todas** as 56 colaborações e em nenhum post próprio — é regra do painel para colaboração, não lacuna de captura.
- O painel às vezes renderiza com placeholders no primeiro carregamento; a coleta só grava depois que o texto passa do limiar de tamanho e traz os rótulos-chave.
- O painel da conta **abrevia** os números (`99 mil`, `5,1 mil`) e mostra `--` quando não expõe o valor; serve como retrato da conta, nunca como fonte de valor exato por post.
