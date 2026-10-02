# Conferencia da API interna contra a base canonica -- agosto/2026

Fonte da legenda: `GET /api/v1/media/<media_id>/info/` (header `x-ig-app-id`).
Captura: `Hermes/instagram-insights/captura/agosto-2026-legendas/_legendas_2026-08.json`.

## Casamento de conjunto (nunca por contagem)

- media_id na base canonica: 62
- media_id na captura: 62
- diferenca simetrica: 0 (vazio = mesmo conjunto)
- legendas nao vazias: 61 de 62
- sem legenda por natureza do post: 3963798502036418973 (`DcCPbyLGzGd`, carrossel -- o bruto do painel
  tambem esta vazio, ou seja, as duas fontes concordam que nao ha legenda)
- divergencia de shortcode: 0 (nenhuma)

## Duas fontes independentes para a mesma legenda

47 dos 62 posts ja tinham `legenda` nos brutos do painel (`captura/agosto-2026/*.json`).
Comparando o texto com a captura nova da API, ignorando espaco em branco:

- comparaveis: 47
- identicas: 44
- divergentes: 3

As 14 diferencas restantes eram so espaco em branco (a API devolve o texto cru, com espaco antes
de quebra de linha; o painel entrega o texto ja renderizado pelo navegador). Depois de normalizar
espaco, sobram **3 divergencias de conteudo**, todas para a API:

| shortcode | o que o painel entregou | o que a API entrega | leitura |
|---|---|---|---|
| `DcmHJv_G-0A` | `#Representatividade.` | `#Representatividade .` | espaco antes da pontuacao no texto cru |
| `DcUJGqJG3tO` | `@sicoob...oficial,` | `@sicoob...oficial ,` | mesmo caso: borda de entidade no DOM |
| `Dcl1hMpDirN` | `agradecemos ao Julio de Oliveira pelo conhecimento` | `agradecemos ao Julio de Oliveira por pelo conhecimento` | **o raspador do painel perdeu a palavra `por`** |

A terceira e a que importa: o painel monta a legenda juntando varios nos de texto do DOM, e a
juntanca pode engolir um pedaco no meio da frase. A API devolve a legenda como um campo unico,
sem concatenacao -- **por isso a API e a fonte da legenda, nao o painel.** As outras duas sao a
mesma regra vista de outro angulo: texto cru de um lado, texto renderizado do outro.

Limpeza aplicada na base: `rstrip` por linha + `strip` (mesmo nivel de limpeza da base de setembro).

## Raws fora da base de agosto

Shortcodes que existem em `captura/agosto-2026/` mas nao na base: `Dbd6DYGA0y3`, `DbdvooJOi2n`, `DbdvwQLu4_o`, `DbdwBOBOVJt`

Sao publicacoes de 31/07 que o split mandou para `auditorias/julho-2026-31-do-export-master.csv`,
nao linhas faltando em agosto.

**Regra:** a API interna e fonte da LEGENDA, nunca das metricas (em post de colaboracao ela devolve
`like_count` = 3 como stub). Metrica continua vindo do painel de insights, que e o que
`publicacoes_feed.py` audita.
