# Verificação de completude — 2026-09

**✅ COMPLETO** — gerado em 2026-10-02T20:11:05+00:00 (UTC)

- Dias com stories no mês: **19**
- Esperado (day_shells `media_count`): **272**
- Inventário (reels_media): **272**
- Insights capturados: **273** (faltam 0)

| dia (do arquivo) | esperado | mídias | insights | |
|---|---|---|---|---|
| 2026-09-01 | 3 | 3 | 3 | ok |
| 2026-09-03 | 3 | 3 | 3 | ok |
| 2026-09-05 | 2 | 2 | 2 | ok |
| 2026-09-07 | 1 | 1 | 1 | ok |
| 2026-09-08 | 15 | 15 | 15 | ok |
| 2026-09-09 | 26 | 26 | 26 | ok |
| 2026-09-10 | 7 | 7 | 7 | ok |
| 2026-09-11 | 72 | 72 | 72 | ok |
| 2026-09-12 | 76 | 76 | 76 | ok |
| 2026-09-13 | 41 | 41 | 41 | ok |
| 2026-09-14 | 2 | 2 | 2 | ok |
| 2026-09-15 | 3 | 3 | 3 | ok |
| 2026-09-17 | 1 | 1 | 1 | ok |
| 2026-09-18 | 5 | 5 | 5 | ok |
| 2026-09-21 | 1 | 1 | 1 | ok |
| 2026-09-23 | 2 | 2 | 2 | ok |
| 2026-09-28 | 1 | 1 | 1 | ok |
| 2026-09-29 | 10 | 10 | 10 | ok |
| 2026-09-30 | 1 | 1 | 1 | ok |

## Checks

- `ESPERATIVA_POR_DIA` — ok: todo dia do mes com media_count == midias extraidas
- `SEM_BURACO` — ok: esperado 272, inventario tem 272
- `SEM_DUPLICATA` — ok: 272 entradas, 272 ids unicos
- `MIDIA_UTILIZAVEL` — ok: 0 sem pk/taken_at/url
- `INSIGHTS_EXATOS` — ok: faltam 0, sobram 0
- `INSIGHTS_COM_CONTEUDO` — ok: 0 registros sem metrica
- `MEDIA_ID_COERENTE` — ok: 0 divergencias
- `BORDA_DE_MES` — ok: buckets vizinhos: anterior=[] seguinte=['2026-10-01'] | midias fora do periodo capturadas de proposito: 1 | midias com data local fora do periodo: nenhuma
- `FORMATO_DAS_METRICAS` — ok: distribuicao: lista=121, umapi=152
- `METRICAS_DO_PERIODO` — ok: 272/272 ids do periodo com metrica real

## Procedência (sha256)

- `day_shells_2026-09.json` (3055 bytes) — `02b28dab43b364b9…`
- `midias_2026-09.json` (435785 bytes) — `f6da0204b37bdbea…`
- `insights_2026-09.json` (646660 bytes) — `a8a8efc64c655065…`

Gerado por `verificar_completude.py` (skill instagram-post-metrics-reporting).
Nenhum dado desta captura pode ir para a camada canônica sem este veredito.
