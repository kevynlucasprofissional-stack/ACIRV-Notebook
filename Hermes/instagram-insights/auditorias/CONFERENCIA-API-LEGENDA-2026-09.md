# Conferencia da API interna contra a base canonica -- setembro/2026

Fonte da legenda: `GET /api/v1/media/<media_id>/info/` (header `x-ig-app-id`).
Captura: `Hermes/instagram-insights/captura/setembro-2026/_legendas_2026-09.json`.

## Casamento de conjunto (nunca por contagem)

- media_id na base canonica: 116
- media_id na captura: 116
- diferenca simetrica: 0 (vazio = mesmo conjunto)
- legendas nao vazias: 116 de 116
- divergencia de shortcode: 1 (`DdFXhdwp0L9` -> `DdFXhdwp0L9-io7p3GXQboCHTN3BgsY_AtwXW00`)
  A API as vezes devolve `<shortcode>-<sufixo>`; comparar por prefixo, nunca por igualdade.

## A API nao serve como fonte de metrica

O mesmo endpoint devolve `like_count` e `comment_count`. Contra a base:

- comentarios divergentes: 5 de 116 (deltas [1, 2, 6, 64])
- curtidas divergentes: 55 de 116
  - 48 sao contador vivo (deltas [-16, -15, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 6, 6, 8, 18, 1441])
  - 7 sao STUB: `like_count` = 3 num post de colaboracao com dezenas de curtidas

| media_id | curtidas na base | like_count da API | vinculo |
|---|---|---|---|
| 3978232126096138250 | 43 | 3 | colaboracao |
| 3978653935338255598 | 32 | 3 | colaboracao |
| 3981808087832690996 | 25 | 3 | colaboracao |
| 3982372324279313586 | 37 | 3 | colaboracao |
| 3985554726251273573 | 44 | 3 | colaboracao |
| 3986846222019327017 | 37 | 3 | colaboracao |
| 3997875435034841827 | 68 | 3 | colaboracao |

**Regra:** a API interna e fonte da LEGENDA, nunca das metricas. Metrica continua
vindo do painel de insights, que e o que `publicacoes_feed.py` audita.
