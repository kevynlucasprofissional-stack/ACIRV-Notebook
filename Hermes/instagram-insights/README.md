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

Regra: captura crua e script de agente **nunca** ficam em `000-Arquivos-originais/` (AGENTS.md). O que vai para a camada 2 é a base consolidada, não o raw.

## Estrutura

```text
Hermes/instagram-insights/
  README.md                     (este arquivo)
  captura/
    setembro-2026/              raws + pipeline de setembro
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
5. Unificar → gerar `85-Bases-e-Consultas/Instagram-Publicacoes-<AAAA-MM>.csv` com o **mesmo cabeçalho de 34 colunas** de `Instagram-Publicacoes-2026-09.csv`.
6. Registrar a base em `85-Bases-e-Consultas/LEIA-ME-Instagram-Insights.md` e no índice de fontes.

## Estado atual

- **Setembro/2026 fechado: 116/116 posts** do grid (60 próprios + 56 em colaboração), 25 dias com publicação, 01/09 a 30/09.
- Setembro foi o mês em que a coleta ficou completa pela primeira vez: as duas runs (01–14 e 15–30) foram unificadas e o post faltante foi recapturado.

## Limitações conhecidas

- `media_id 3982692900246340349` (reel em colaboração com `keniasleite`, 09/09): o painel de insights da ACIRV devolve `--` para visualizações, visualizadores e interações. A base registra a ausência em `metricas_ausentes` e deixa o número bruto da API pública em `notas` (não é o mesmo metro do painel). Não é falha de coleta: o painel não expõe os dados para este post.
- Métricas de "Atividade do perfil" e "Novos seguidores" não aparecem no rodapé da maioria dos posts; são marcadas como ausentes em vez de zeradas.
- O painel às vezes renderiza com placeholders no primeiro carregamento; a coleta só grava depois que o texto passa do limiar de tamanho e traz os rótulos-chave.
